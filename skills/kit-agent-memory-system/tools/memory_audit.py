#!/usr/bin/env python3
"""Audit a memory tree for the failures that make a memory file useless.

Six checks, all of them on real Markdown structure rather than on the presence
of a phrase:

  S01  stale          a section confirmed longer ago than the horizon allows
  S02  undated        a section with content and no readable Confirmed date
  C01  contradiction  one subject stated two ways across levels
  D01  no reason      a decision line with no because/since clause
  L01  leak           a project-owned name appearing on the workspace card
  O01  oversize       a section past the readable line limit
  E01  empty          a heading with nothing under it
  X01  structure      a file named memory.md with no sections at all
  W01  missing        a card without one of the five canonical sections

Only S01-S02 count as part of the stale family. All of E, X, S, C, D, L, O are
errors. W01 is a warning and does not change the exit code.

Usage:
    python3 memory_audit.py ./memory
    python3 memory_audit.py ./memory --horizon 60 --as-of 2026-10-26
    python3 memory_audit.py ./memory --json

Exit codes: 0 no error-level finding, 2 one or more error-level findings.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

CANONICAL_SECTIONS = ["Purpose", "Current state", "Decisions and why", "What's next", "Key links"]
DEFAULT_HORIZON_DAYS = 90
DEFAULT_MAX_LINES = 40
DATE_HELP = "YYYY-MM-DD"

# A decision line passes when it carries one of these. The set is deliberately
# short: it names a cause, a consequence or a reason, and nothing else.
REASON_PATTERNS = [
    r"\bbecause\b",
    r"\bsince\b",
    r"\bso that\b",
    r"\bso we\b",
    r"\bso i\b",
    r"\botherwise\b",
    r"\bto avoid\b",
    r"\breason\b",
]

# Pairs that the same subject can be named with. A pair fires when one card
# uses the left name and a card at another level uses the right name. Edit this
# list for your own workspace: the two below are the pair that bites most often,
# a provider named by product and by company.
CONTRADICTION_PAIRS = [
    ("model provider", "Claude", "ChatGPT"),
    ("model provider", "Anthropic", "OpenAI"),
]

# Keys that are allowed to differ between two cards.
SKIP_KEYS = {"confirmed", "last confirmed", "updated", "reviewed", "row"}

# Values that mean "this key does not apply here". A card that says a key does
# not apply is not contradicting a card that names a value for a different scope.
NO_VALUES = {"none", "n/a", "na", "nil", "-", "tbd", "unknown", "not set", "no"}

LEVELS = ("workspace", "project", "campaign")
BULLET = re.compile(r"^[-*]\s+(.*)$")
HEADING = re.compile(r"^##\s+(.+?)\s*$")
HEADER_FIELD = re.compile(r"^([A-Za-z][A-Za-z \-]{1,30}):\s*(.*)$")
CONFIRMED = re.compile(r"^confirmed:\s*(.*)$", re.IGNORECASE)
KV = re.compile(r"^[-*]\s+(.+?):\s+(.+)$")


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip()).strip(" .;,").lower()


def strip_comments(text: str) -> list[str]:
    """Remove HTML comments, keeping one output line per input line."""
    out: list[str] = []
    inside = False
    for raw in text.splitlines():
        kept: list[str] = []
        i = 0
        while i < len(raw):
            if not inside and raw.startswith("<!--", i):
                inside = True
                i += 4
                continue
            if inside and raw.startswith("-->", i):
                inside = False
                i += 3
                continue
            if not inside:
                kept.append(raw[i])
            i += 1
        out.append("".join(kept))
    return out


@dataclass
class Section:
    name: str
    line: int
    content: list[tuple[int, str]] = field(default_factory=list)
    confirmed: date | None = None
    confirmed_line: int | None = None
    confirmed_raw: str = ""


@dataclass
class Card:
    path: Path
    rel: str
    level: str
    title: str
    header: dict[str, tuple[str, int]]
    sections: list[Section]
    lines: list[str]


@dataclass
class Finding:
    rule: str
    severity: str
    file: str
    line: int
    subject: str
    message: str


def infer_level(rel: Path) -> str:
    parts = [p.lower() for p in rel.parts]
    if "campaigns" in parts:
        return "campaign"
    if "projects" in parts:
        return "project"
    return "workspace"


def parse_card(path: Path, root: Path) -> Card:
    text = path.read_text(encoding="utf-8")
    clean = strip_comments(text)
    try:
        rel = path.relative_to(root)
    except ValueError:
        rel = Path(path.name)

    title = ""
    header: dict[str, tuple[str, int]] = {}
    sections: list[Section] = []
    current: Section | None = None

    for number, raw in enumerate(clean, start=1):
        line = raw.strip()
        if not title and line.startswith("# "):
            title = line[2:].strip()
            continue
        heading = HEADING.match(line)
        if heading:
            current = Section(name=heading.group(1).strip(), line=number)
            sections.append(current)
            continue
        if current is None:
            field_match = HEADER_FIELD.match(line)
            if field_match and not line.startswith("#"):
                header[field_match.group(1).strip().lower()] = (field_match.group(2).strip(), number)
            continue
        if not line or line in {"-", "*", "+"}:
            continue
        stamp = CONFIRMED.match(line)
        if stamp:
            if current.confirmed_raw:
                continue
            current.confirmed_raw = stamp.group(1).strip()
            current.confirmed_line = number
            try:
                current.confirmed = date.fromisoformat(current.confirmed_raw)
            except ValueError:
                current.confirmed = None
            continue
        current.content.append((number, line))

    level = header.get("level", ("", 0))[0].strip().lower()
    if level not in LEVELS:
        level = infer_level(rel)
    return Card(path=path, rel=rel, level=level, title=title, header=header, sections=sections, lines=clean)


def find_cards(root: Path) -> list[Card]:
    cards = []
    for path in sorted(root.rglob("memory.md")):
        if path.is_file():
            cards.append(parse_card(path, root))
    return cards


def has_reason(text: str) -> bool:
    low = text.lower()
    return any(re.search(pattern, low) for pattern in REASON_PATTERNS)


def kv_pairs(card: Card) -> dict[str, tuple[str, int, str]]:
    pairs: dict[str, tuple[str, int, str]] = {}
    for section in card.sections:
        if section.name.strip().lower() != "current state":
            continue
        for number, line in section.content:
            match = KV.match(line)
            if not match:
                continue
            key = match.group(1).strip().lower()
            if not key or key in SKIP_KEYS:
                continue
            pairs.setdefault(key, (norm(match.group(2)), number, f"{match.group(1).strip()}: {match.group(2).strip()}"))
    return pairs


def owned_names(card: Card) -> list[str]:
    raw = card.header.get("owns", ("", 0))[0]
    names = []
    for token in raw.split(","):
        token = token.strip().strip(".")
        if len(token) < 4:
            continue
        if card.title and (token.lower() in card.title.lower() or card.title.lower() in token.lower()):
            continue
        names.append(token)
    return names


def audit(root: Path, as_of: date, horizon: int, max_lines: int) -> tuple[list[Card], list[Finding]]:
    cards = find_cards(root)
    findings: list[Finding] = []

    for card in cards:
        if not card.sections:
            findings.append(
                Finding("X01", "error", card.rel.as_posix(), 1, "structure",
                        "no '##' sections found, so this file cannot be read as a memory card")
            )
            continue

        present = {section.name.strip().lower() for section in card.sections}
        for name in CANONICAL_SECTIONS:
            if name.lower() not in present:
                findings.append(
                    Finding("W01", "warning", card.rel.as_posix(), 1, name,
                            f"canonical section '{name}' is missing")
                )

        for section in card.sections:
            rel = card.rel.as_posix()
            if not section.content:
                findings.append(
                    Finding("E01", "error", rel, section.line, section.name,
                            f"'{section.name}' has a heading and no content")
                )
                continue
            if section.confirmed is None:
                shown = section.confirmed_raw or "no line"
                findings.append(
                    Finding("S02", "error", rel, section.confirmed_line or section.line, section.name,
                            f"'{section.name}' has content but no readable Confirmed date ({shown})")
                )
            else:
                age = (as_of - section.confirmed).days
                if age > horizon:
                    findings.append(
                        Finding("S01", "error", rel, section.confirmed_line or section.line, section.name,
                                f"'{section.name}' was last confirmed {section.confirmed.isoformat()}, "
                                f"{age} days ago, past the {horizon}-day horizon")
                    )
            if len(section.content) > max_lines:
                findings.append(
                    Finding("O01", "error", rel, section.line, section.name,
                            f"'{section.name}' holds {len(section.content)} content lines, "
                            f"over the {max_lines}-line limit")
                )

        for section in card.sections:
            if not section.name.strip().lower().startswith("decision"):
                continue
            for number, line in section.content:
                bullet = BULLET.match(line)
                body = bullet.group(1) if bullet else line
                if has_reason(body):
                    continue
                findings.append(
                    Finding("D01", "error", card.rel.as_posix(), number, "decision",
                            f"decision with no reason: '{body[:90]}'")
                )

    # Leak: a name owned by a project or campaign appearing on the workspace card.
    for card in cards:
        if card.level != "workspace":
            continue
        for owner in cards:
            if owner.level == "workspace":
                continue
            for token in owned_names(owner):
                hit = next(((n, line) for n, line in enumerate(card.lines, start=1) if token.lower() in line.lower()), None)
                if hit is None:
                    continue
                findings.append(
                    Finding("L01", "error", card.rel.as_posix(), hit[0], token,
                            f"'{token}' belongs to {owner.rel.parent.as_posix()}, so it does not belong at workspace level")
                )
                break

    # Contradictions are collected by subject, so one subject reported by two
    # checks is one finding with all of the evidence on it.
    contradictions: dict[str, dict] = {}

    def note_contradiction(subject: str, entries: list[tuple[str, int, str]], note: str = "",
                           add_entries: bool = True) -> None:
        bucket = contradictions.setdefault(subject.lower(), {"subject": subject, "entries": [], "notes": []})
        if add_entries:
            for entry in entries:
                if entry not in bucket["entries"]:
                    bucket["entries"].append(entry)
        if note and note not in bucket["notes"]:
            bucket["notes"].append(note)

    for workspace in cards:
        if workspace.level != "workspace":
            continue
        mine = kv_pairs(workspace)
        for other in cards:
            if other.level == "workspace":
                continue
            theirs = kv_pairs(other)
            for key in sorted(set(mine) & set(theirs)):
                if mine[key][0] == theirs[key][0]:
                    continue
                if mine[key][0].split(",")[0] in NO_VALUES or theirs[key][0].split(",")[0] in NO_VALUES:
                    continue
                note_contradiction(
                    key,
                    [
                        (workspace.rel.as_posix(), mine[key][1], mine[key][2]),
                        (other.rel.as_posix(), theirs[key][1], theirs[key][2]),
                    ],
                )

    for subject, left, right in CONTRADICTION_PAIRS:
        left_files = []
        right_files = []
        for card in cards:
            text = "\n".join(card.lines).lower()
            has_left = left.lower() in text
            has_right = right.lower() in text
            if has_left and not has_right:
                left_files.append(card)
            elif has_right and not has_left:
                right_files.append(card)
        for a in left_files:
            for b in right_files:
                if a.level == b.level:
                    continue
                line_a = next(n for n, line in enumerate(a.lines, start=1) if left.lower() in line.lower())
                line_b = next(n for n, line in enumerate(b.lines, start=1) if right.lower() in line.lower())
                note_contradiction(
                    subject,
                    [(a.rel.as_posix(), line_a, left), (b.rel.as_posix(), line_b, right)],
                    note=f"name pair '{left}' against '{right}'",
                    add_entries=subject.lower() not in contradictions,
                )

    for bucket in contradictions.values():
        entries = bucket["entries"]
        if len(entries) < 2 and not bucket["notes"]:
            continue
        parts = [f"{file}:{line} has '{text}'" for file, line, text in entries]
        message = f"'{bucket['subject']}' is stated differently across levels: " + "; ".join(parts)
        if bucket["notes"]:
            message += " (" + "; ".join(bucket["notes"]) + ")"
        findings.append(Finding("C01", "error", entries[0][0], entries[0][1], bucket["subject"], message))

    findings.sort(key=lambda f: (f.file, f.line, f.rule))
    return cards, findings


def render(cards: list[Card], findings: list[Finding], horizon: int, as_of: date) -> None:
    scope = ", ".join(
        f"{sum(1 for c in cards if c.level == level)} {level}" for level in LEVELS
    )
    print(f"memory audit: {len(cards)} cards ({scope}), horizon {horizon} days, as of {as_of.isoformat()}")
    print()
    if not findings:
        print("No findings.")
        return
    rows = [
        (f.file, str(f.line), f.rule, f.severity, f.message) for f in findings
    ]
    widths = [max(len(r[i]) for r in rows + [("FILE", "LINE", "RULE", "SEV", "FINDING")]) for i in range(4)]
    header = ("FILE", "LINE", "RULE", "SEV", "FINDING")
    print(f"{header[0]:<{widths[0]}}  {header[1]:>4}  {header[2]:<4}  {header[3]:<7}  {header[4]}")
    for row in rows:
        print(f"{row[0]:<{widths[0]}}  {row[1]:>4}  {row[2]:<4}  {row[3]:<7}  {row[4]}")


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="memory_audit.py",
        description=(
            "Audit a memory tree. Errors: E01 empty section, X01 not a memory card, "
            "S01 stale, S02 undated, C01 contradiction, D01 decision with no reason, "
            "L01 leak, O01 oversize. Warnings: W01 missing canonical section."
        ),
        epilog=(
            "The horizon is how many days a section may go unconfirmed. The limit is how "
            "many content lines one section may hold. Both are yours to set.\n\n"
            "Exit 2 means at least one error. Exit 0 means none, warnings allowed."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("root", metavar="ROOT", help="folder that holds the memory tree")
    parser.add_argument("--horizon", type=int, default=DEFAULT_HORIZON_DAYS, metavar="DAYS",
                        help=f"days a section may go unconfirmed (default {DEFAULT_HORIZON_DAYS})")
    parser.add_argument("--as-of", metavar=DATE_HELP, default=None,
                        help="treat this date as today, for a reproducible run")
    parser.add_argument("--max-lines", type=int, default=DEFAULT_MAX_LINES, metavar="N",
                        help=f"content lines one section may hold (default {DEFAULT_MAX_LINES})")
    parser.add_argument("--json", action="store_true", help="print the findings as JSON")
    args = parser.parse_args()

    root = Path(args.root).expanduser()
    if not root.is_dir():
        print(f"error: {root} is not a folder", file=sys.stderr)
        return 2
    try:
        as_of = date.fromisoformat(args.as_of) if args.as_of else date.today()
    except ValueError:
        print(f"error: --as-of must look like {DATE_HELP}", file=sys.stderr)
        return 2
    if args.horizon < 1 or args.max_lines < 1:
        print("error: --horizon and --max-lines take a positive whole number", file=sys.stderr)
        return 2

    cards, findings = audit(root, as_of, args.horizon, args.max_lines)
    errors = sum(1 for f in findings if f.severity == "error")
    warnings = len(findings) - errors

    if args.json:
        payload = {
            "root": str(root),
            "as_of": as_of.isoformat(),
            "horizon_days": args.horizon,
            "max_lines": args.max_lines,
            "cards": [
                {"file": c.rel.as_posix(), "level": c.level, "title": c.title,
                 "sections": [{"name": s.name, "line": s.line,
                               "confirmed": s.confirmed.isoformat() if s.confirmed else None,
                               "content_lines": len(s.content)} for s in c.sections]}
                for c in cards
            ],
            "findings": [
                {"rule": f.rule, "severity": f.severity, "file": f.file,
                 "line": f.line, "subject": f.subject, "message": f.message}
                for f in findings
            ],
            "counts": {"error": errors, "warning": warnings, "total": len(findings)},
            "exit_code": 2 if errors else 0,
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        render(cards, findings, args.horizon, as_of)
        print()
        print(f"{errors} error{'' if errors == 1 else 's'}, {warnings} warning{'' if warnings == 1 else 's'}")
        print("clean" if not errors else "not clean")

    return 2 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
