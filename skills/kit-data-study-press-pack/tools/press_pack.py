#!/usr/bin/env python3
"""Check a findings document and a press pack for the things that make a study unusable.

Usage:
    python3 press_pack.py FINDINGS.md PRESS-PACK.md
    python3 press_pack.py FINDINGS.md PRESS-PACK.md --json

Seven error rules:
    E01  the headline finding carries no number
    E02  no method note with a date
    E03  no sample size
    E04  no limitations section
    E05  a percentage with no denominator in the same line or paragraph
    E06  a claim of causation drawn from a count
    E07  a quote attributed to a person with no role

Four warning rules:
    W01  the pack carries no citation line
    W02  the pack carries no contact
    W03  neither document points at the raw data
    W04  the pack lists fewer than two charts

Score: 100 minus 10 per error and 3 per warning, floored at 0.
Exit codes: 0 pass (warnings allowed), 2 one or more errors.

The checker reads Markdown. It is a floor, not a substitute for an editor.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

MONTHS = "January|February|March|April|May|June|July|August|September|October|November|December"
DATE = re.compile(r"\b(?:\d{4}-\d{2}-\d{2}|\d{1,2}\s+(?:" + MONTHS + r")\s+\d{4}|(?:" + MONTHS + r")\s+\d{4})\b")
PCT = re.compile(r"\d+(?:[.,]\d+)?\s*(?:%|per cent\b|percent\b)")
DENOM = [
    re.compile(r"\bof\s+(?:the\s+)?\d[\d,]*"),
    re.compile(r"\bn\s*=\s*\d"),
    re.compile(r"\bout of\s+\d"),
    re.compile(r"\bdenominator\b", re.I),
    re.compile(
        r"\b\d[\d,]*\s+(?:[A-Za-z-]+\s+){0,2}(?:rows|listings|records|entries|items|responses|makers|posts|profiles)\b",
        re.I,
    ),
]
SAMPLE_SIZE = [
    re.compile(r"\bn\s*=\s*\d+"),
    re.compile(r"\b\d{2,}\s+(?:rows|listings|records|entries|items|responses|makers|posts|profiles)\b", re.I),
]
CAUSAL = re.compile(
    r"\b(?:proves?|proved|causes?|caused|causing|leads?\s+to|led\s+to|drives?|driven\s+by|"
    r"results?\s+in|because\b|explains?\s+why)\b",
    re.I,
)
NEGATION = re.compile(r"\b(?:not|no|never|cannot|can't|without|none|neither|nor)\b", re.I)
QUOTE = re.compile(r"[\"\u201c]([^\"\u201d]{12,})[\"\u201d]\s*(?:[\u2014\u2013-]{1,2}\s*)?([A-Z][^\n]*)")
ROLES = (
    "founder", "director", "researcher", "analyst", "author", "editor", "manager", "lead",
    "head of", "spokesperson", "spokesman", "spokeswoman", "partner", "owner", "curator",
    "statistician", "professor", "chief", "coordinator", "maker", "chair", "trustee",
)


def add(findings: list, rule: str, ok: bool, severity: str, message: str, evidence: str = "", fix: str = "") -> None:
    findings.append(
        {
            "rule": rule,
            "status": "ok" if ok else severity,
            "message": message,
            "evidence": re.sub(r"\s+", " ", evidence).strip()[:220],
            "fix": "" if ok else fix,
        }
    )


def sections(text: str) -> list:
    """Split Markdown into (heading, body) pairs. The preamble keeps an empty heading."""
    out = []
    heading, body = "", []
    for line in text.splitlines():
        match = re.match(r"^(#{1,6})\s+(.*)$", line)
        if match:
            out.append((heading, "\n".join(body)))
            heading, body = match.group(2).strip(), []
        else:
            body.append(line)
    out.append((heading, "\n".join(body)))
    return out


def headline(text: str) -> str:
    for line in text.splitlines():
        match = re.match(r"^#\s+(.+)$", line)
        if match:
            return match.group(1).strip()
    return ""


def units(text: str) -> list:
    """Blocks a reader takes in one glance: a paragraph, a bullet, a table row."""
    out = []
    for chunk in re.split(r"\n\s*\n", text):
        chunk = chunk.strip()
        if not chunk:
            continue
        current = []
        for line in chunk.splitlines():
            if not line.strip():
                continue
            if re.match(r"\s*(?:[-*+]|\d+\.|\|)", line) or line.strip().startswith(">"):
                if current:
                    out.append("\n".join(current))
                    current = []
                out.append(line.strip())
            else:
                current.append(line.strip())
        if current:
            out.append("\n".join(current))
    return out


def sentences(block: str) -> list:
    return [s for s in re.split(r"(?<=[.!?])\s+", block) if s.strip()]


def has_denominator(block: str) -> bool:
    return any(pattern.search(block) for pattern in DENOM)


def run(findings_path: Path, pack_path: Path) -> dict:
    if not findings_path.exists():
        print(f"error: no findings document at {findings_path}")
        sys.exit(2)
    if not pack_path.exists():
        print(f"error: no press pack at {pack_path}")
        sys.exit(2)
    findings_text = findings_path.read_text(encoding="utf-8")
    pack_text = pack_path.read_text(encoding="utf-8")
    findings: list = []

    findings_headline = headline(findings_text)
    pack_headline = headline(pack_text)
    missing_headline = [name for name, value in (("findings", findings_headline), ("pack", pack_headline)) if not value]
    numbered = [value for value in (findings_headline, pack_headline) if value and re.search(r"\d", value)]
    add(
        findings,
        "E01",
        len(numbered) == 2 and not missing_headline,
        "error",
        "The headline finding carries a number.",
        "; ".join(f"{k}: {v or '(no heading)'}" for k, v in (("findings", findings_headline), ("pack", pack_headline))),
        "Write the headline as the count: how many of how many, or the percentage with its denominator. "
        "A headline with a judgement and no number is an opinion.",
    )

    dated_method = False
    method_evidence = ""
    for heading, body in sections(findings_text):
        blob = heading + "\n" + body
        if re.search(r"\bmethod\b|how the count was made|counting rule", blob, re.I) and DATE.search(blob):
            dated_method = True
            method_evidence = heading or body[:160]
            break
    add(
        findings,
        "E02",
        dated_method,
        "error",
        "The method note carries a date.",
        method_evidence or "no section mentions a method and a date",
        "Add a method section that says when the data was retrieved and read. An undated method note cannot be checked by anyone.",
    )

    sample_hit = ""
    for pattern in SAMPLE_SIZE:
        match = pattern.search(findings_text)
        if match:
            sample_hit = match.group(0)
            break
    add(
        findings,
        "E03",
        bool(sample_hit),
        "error",
        "The sample size is stated.",
        sample_hit or "no 'n = ...' and no '... rows/listings' phrasing in the findings",
        "State the denominator in the findings: n = 118, or '118 listings'. A rate with no base cannot be read.",
    )

    limitation_headings = [h for h, _ in sections(findings_text) if re.search(r"limitation|what this study cannot|what this does not show", h, re.I)]
    limitation_block = re.search(r"(?im)^\s*(?:#{1,6}\s*|\*\*)?\s*limitations?\b", findings_text)
    add(
        findings,
        "E04",
        bool(limitation_headings) or bool(limitation_block),
        "error",
        "The findings carry a limitations section.",
        ", ".join(limitation_headings) or (limitation_block.group(0).strip() if limitation_block else "no heading or block mentions limitations"),
        "Add a limitations section to the findings document itself, not to the pack. Name what the count cannot show.",
    )

    offenders = []
    for label, text in (("findings", findings_text), ("pack", pack_text)):
        for unit in units(text):
            if PCT.search(unit) and not has_denominator(unit):
                offenders.append(f"{label}: {unit}")
    add(
        findings,
        "E05",
        not offenders,
        "error",
        "Every percentage carries its own denominator.",
        " | ".join(offenders[:3]) + (f" (+{len(offenders) - 3} more)" if len(offenders) > 3 else "") if offenders else "every percentage sits beside its base",
        "Write the base next to the rate: '45 of 118 (38.1%)'. A journalist quotes the line, not the document, so the line has to hold on its own.",
    )

    causal_hits = []
    for label, text in (("findings", findings_text), ("pack", pack_text)):
        for unit in units(text):
            if not re.search(r"\d", unit):
                continue
            for sentence in sentences(unit):
                if CAUSAL.search(sentence) and not NEGATION.search(sentence):
                    causal_hits.append(f"{label}: {sentence.strip()}")
    add(
        findings,
        "E06",
        not causal_hits,
        "error",
        "No cause is claimed from a count.",
        " | ".join(causal_hits[:2]) + (f" (+{len(causal_hits) - 2} more)" if len(causal_hits) > 2 else "") if causal_hits else "no causal claim in a sentence that carries a number",
        "Say what was counted and what it does not settle. 'X is more common than Y' is a finding. 'X causes Y' needs a design this method does not have.",
    )

    quote_hits = []
    for line in pack_text.splitlines():
        for match in QUOTE.finditer(line):
            quote, attribution = match.group(1).strip(), match.group(2).strip()
            if not any(role in attribution.lower() for role in ROLES):
                quote_hits.append(attribution[:90])
    add(
        findings,
        "E07",
        not quote_hits,
        "error",
        "Every quote names the speaker's role.",
        " | ".join(quote_hits) if quote_hits else "quotes, if any, carry a role",
        "Attribute as name, role, organisation: 'Mara Ellison, study author, Riverside Makers Directory'. "
        "A name with no role is a name a journalist cannot use.",
    )

    citation_ok = bool(re.search(r"cite this study|cite as|citation line|citation:", pack_text, re.I))
    add(findings, "W01", citation_ok, "warning", "The pack carries a citation line.",
        "" if citation_ok else "no 'Cite this study:' line in the pack",
        "Add a line a journalist can paste: author, year, title, page address.")

    contact_ok = bool(re.search(r"contact", pack_text, re.I)) and bool(re.search(r"\S+@\S+\.\S+|@[A-Za-z0-9_.]{3,}", pack_text))
    add(findings, "W02", contact_ok, "warning", "The pack carries a contact.",
        "" if contact_ok else "no contact name with an address in the pack",
        "Add a named contact with an email or handle. A pack with no contact is a document, not a pitch.")

    data_ok = bool(re.search(r"raw data|\.csv\b|data/\S+|github\.com|zenodo|osf\.io", findings_text + pack_text, re.I))
    add(findings, "W03", data_ok, "warning", "The raw data is pointed at.",
        "" if data_ok else "neither document names the raw data or a place to get it",
        "Name the file or the address a reader can download the rows and the coding sheet from.")

    charts = len(re.findall(r"\bchart\s*\d|\bfigure\s*\d", pack_text, re.I))
    add(findings, "W04", charts >= 2, "warning", "The pack lists at least two charts.",
        f"charts named: {charts}",
        "Name the charts and what each one shows. A pack with no chart asks the journalist to make one.")

    errors = [f for f in findings if f["status"] == "error"]
    warnings = [f for f in findings if f["status"] == "warning"]
    score = max(0, 100 - 10 * len(errors) - 3 * len(warnings))
    return {
        "ok": not errors,
        "score": score,
        "errors": len(errors),
        "warnings": len(warnings),
        "findings_title": findings_headline,
        "pack_title": pack_headline,
        "findings": findings,
        "paths": {"findings": str(findings_path), "pack": str(pack_path)},
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check a findings document and a press pack before either is published.",
        epilog="Exit codes: 0 pass (warnings allowed), 2 one or more errors.",
    )
    parser.add_argument("findings", type=Path)
    parser.add_argument("pack", type=Path)
    parser.add_argument("--json", action="store_true", help="print JSON only")
    args = parser.parse_args()

    report = run(args.findings, args.pack)
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        verdict = "PASS" if report["ok"] else "FAIL"
        print(f"{verdict}  score {report['score']}/100  errors {report['errors']}  warnings {report['warnings']}\n")
        print(f"findings: {report['findings_title'] or '(no heading)'}")
        print(f"pack: {report['pack_title'] or '(no heading)'}\n")
        for item in report["findings"]:
            mark = {"ok": "ok  ", "error": "ERR ", "warning": "WARN"}[item["status"]]
            print(f"[{mark}] {item['rule']:<4} {item['message']}")
            if item["evidence"]:
                print(f"         evidence: {item['evidence']}")
            if item["fix"]:
                print(f"         fix: {item['fix']}")
    return 0 if report["ok"] else 2


if __name__ == "__main__":
    sys.exit(main())
