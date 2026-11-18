#!/usr/bin/env python3
"""Rank lead magnet ideas with a fixed weighted model.

Usage:
    python3 score_ideas.py ideas.json
    python3 score_ideas.py ideas.json --top 3 --explain
    python3 score_ideas.py ideas.json --json
    python3 score_ideas.py --example > ideas.json

Every idea carries six scores from 1 to 5. The weights are fixed in this file
and are never passed on the command line, so a ranking written in March can be
compared with a ranking written in September without renegotiating the model.

Exit codes: 0 ranked, 2 invalid input.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Fixed weights, and the reason each one holds its share of 100. The reasons are
# printed by --explain so a reader can argue with the model instead of guessing
# where the numbers came from.
WEIGHTS = [
    (
        "closeness",
        25,
        "Closeness to the paid offer. The magnet exists to sell one thing. If the "
        "result does not point at that thing, the build is a hobby with an email list.",
    ),
    (
        "speed",
        20,
        "Speed to value. A lead magnet is used in a distracted minute. The less the "
        "user has to do before something useful appears, the more of them finish.",
    ),
    (
        "breadth",
        15,
        "Breadth of appeal. A result that only lands for a narrow slice of the "
        "audience caps the list you can build from it.",
    ),
    (
        "build_cost",
        15,
        "Build cost, scored 5 for cheapest. Cost is weighted below closeness and "
        "speed on purpose: a cheap idea that sells nothing is still a loss.",
    ),
    (
        "durability",
        10,
        "Durability. How long the magnet stays true before a rule, a price or a "
        "platform changes and the result becomes wrong. Low weight because most "
        "magnets are replaced before they decay.",
    ),
    (
        "differentiation",
        15,
        "Differentiation. How hard the result is for a competitor to copy in an "
        "afternoon. Equal to breadth and build cost because a copied magnet still "
        "works, it just costs more to keep in front of people.",
    ),
]

CRITERIA = [key for key, _, _ in WEIGHTS]
LABELS = {
    "closeness": "closeness to offer",
    "speed": "speed to value",
    "breadth": "breadth of appeal",
    "build_cost": "build cost",
    "durability": "durability",
    "differentiation": "differentiation",
}
NOTE = {
    "closeness": "does the result point at the paid offer",
    "speed": "how little the user does before value appears",
    "breadth": "how much of the audience wants this result",
    "build_cost": "5 is cheapest to build",
    "durability": "how long before a rule or a price changes it",
    "differentiation": "how hard to copy in an afternoon",
}

# The tie-break order is fixed and printed, so two runs over the same file can
# never disagree and two people can never disagree about why a tie was broken.
TIE_ORDER = ["closeness", "speed", "differentiation", "build_cost", "breadth", "durability"]
TIE_TEXT = (
    "Ties break on the criteria in this order: closeness, speed, differentiation, "
    "build cost, breadth, durability, then the idea id alphabetically. The order is "
    "fixed so a tie is never settled by file order or by chance."
)

EXAMPLE = [
    {
        "id": "noshow-cost-calculator",
        "name": "No-show cost calculator",
        "shape": "calculator",
        "scores": {
            "closeness": 5,
            "speed": 5,
            "breadth": 4,
            "build_cost": 4,
            "durability": 4,
            "differentiation": 3,
        },
        "reason": "Two numbers in, a monthly loss figure out, and the figure is the first slide of the paid review.",
    },
    {
        "id": "reminder-message-swipe",
        "name": "Reminder message swipe file",
        "shape": "swipe file",
        "scores": {
            "closeness": 4,
            "speed": 5,
            "breadth": 4,
            "build_cost": 5,
            "durability": 3,
            "differentiation": 2,
        },
        "reason": "Fast to build and easy to use, but nothing in it is computed, so it proves no skill.",
    },
    {
        "id": "clinic-operations-score",
        "name": "Clinic operations score",
        "shape": "assessment",
        "scores": {
            "closeness": 5,
            "speed": 4,
            "breadth": 3,
            "build_cost": 3,
            "durability": 4,
            "differentiation": 3,
        },
        "reason": "Twelve questions produce a score and a weakest area, which is a natural opening for the review.",
    },
]


def load(path: Path) -> tuple[list[dict], list[str]]:
    """Read and validate the idea file. Returns (ideas, errors)."""
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return [], [f"{path}: file not found"]
    except json.JSONDecodeError as exc:
        return [], [f"{path}: not valid JSON ({exc.msg}, line {exc.lineno}, column {exc.colno})"]
    except OSError as exc:
        return [], [f"{path}: could not be read ({exc.strerror})"]

    if isinstance(raw, dict):
        if "ideas" not in raw:
            return [], [f"{path}: expected a list of ideas, or an object with an 'ideas' list"]
        raw = raw["ideas"]
    if not isinstance(raw, list):
        return [], [f"{path}: expected a list of ideas"]
    if not raw:
        return [], [f"{path}: the ideas list is empty"]

    errors: list[str] = []
    ideas: list[dict] = []
    seen: dict[str, int] = {}

    for index, item in enumerate(raw, start=1):
        if not isinstance(item, dict):
            errors.append(f"idea {index}: not an object")
            continue

        idea_id = item.get("id")
        if not isinstance(idea_id, str) or not idea_id.strip():
            errors.append(f"idea {index}: missing a non-empty 'id'")
            idea_id = f"idea-{index}"
        else:
            idea_id = idea_id.strip()
        if idea_id in seen:
            errors.append(f"idea {index} ({idea_id}): duplicate id, already used by idea {seen[idea_id]}")
        else:
            seen[idea_id] = index

        scores = item.get("scores")
        if not isinstance(scores, dict):
            errors.append(f"idea {index} ({idea_id}): missing a 'scores' object with the six criteria")
            continue

        unknown = [k for k in scores if k not in CRITERIA]
        if unknown:
            errors.append(
                f"idea {index} ({idea_id}): unknown criteria {', '.join(sorted(unknown))}; "
                f"allowed: {', '.join(CRITERIA)}"
            )

        clean: dict[str, int] = {}
        missing = [c for c in CRITERIA if c not in scores]
        if missing:
            errors.append(f"idea {index} ({idea_id}): scores missing {', '.join(missing)}")

        for criterion in CRITERIA:
            if criterion not in scores:
                continue
            value = scores[criterion]
            if isinstance(value, bool) or not isinstance(value, int):
                errors.append(
                    f"idea {index} ({idea_id}): {criterion} score {value!r} is not a whole number"
                )
            elif not 1 <= value <= 5:
                errors.append(
                    f"idea {index} ({idea_id}): {criterion} score {value} is outside 1 to 5"
                )
            else:
                clean[criterion] = value

        if len(clean) != len(CRITERIA):
            continue

        name = item.get("name")
        name = name.strip() if isinstance(name, str) and name.strip() else idea_id
        shape = item.get("shape")
        shape = shape.strip() if isinstance(shape, str) and shape.strip() else "-"
        reason = item.get("reason")
        reason = " ".join(reason.split()) if isinstance(reason, str) else ""

        ideas.append(
            {
                "id": idea_id,
                "name": name,
                "shape": shape,
                "scores": clean,
                "reason": reason,
            }
        )

    return ideas, errors


def rank(ideas: list[dict]) -> list[dict]:
    """Weighted total in tenths of a point, so ordering is exact integer maths."""
    rows = []
    for idea in ideas:
        # contribution in tenths = 2 * weight * score, because weight * score / 5
        # is the same number of points out of 100.
        contribution = {k: 2 * w * idea["scores"][k] for k, w, _ in WEIGHTS}
        tenths = sum(contribution.values())
        rows.append({**idea, "contribution": contribution, "tenths": tenths})

    rows.sort(
        key=lambda row: (-row["tenths"],)
        + tuple(-row["scores"][k] for k in TIE_ORDER)
        + (row["id"],)
    )
    for position, row in enumerate(rows, start=1):
        row["rank"] = position
    return rows


def as_points(tenths: int) -> float:
    return tenths / 10.0


def render_table(rows: list[dict]) -> str:
    head = ["rank", "idea", "shape", "close", "speed", "breadth", "build", "durable", "diff", "total"]
    body = []
    for row in rows:
        body.append(
            [
                str(row["rank"]),
                row["id"],
                row["shape"],
                str(row["scores"]["closeness"]),
                str(row["scores"]["speed"]),
                str(row["scores"]["breadth"]),
                str(row["scores"]["build_cost"]),
                str(row["scores"]["durability"]),
                str(row["scores"]["differentiation"]),
                f"{as_points(row['tenths']):.1f}",
            ]
        )

    widths = [len(h) for h in head]
    for line in body:
        for i, cell in enumerate(line):
            widths[i] = max(widths[i], len(cell))

    def fmt(cells: list[str]) -> str:
        out = []
        for i, cell in enumerate(cells):
            out.append(cell.ljust(widths[i]) if i in (1, 2) else cell.rjust(widths[i]))
        return "  ".join(out).rstrip()

    lines = [fmt(head), "-" * (sum(widths) + 2 * (len(widths) - 1))]
    lines.extend(fmt(line) for line in body)
    return "\n".join(lines)


def render_weights() -> str:
    lines = ["Weights, fixed in the script (out of 100):", ""]
    for key, weight, reason in WEIGHTS:
        lines.append(f"  {LABELS[key]:<20} {weight:>3}   {reason}")
    lines.append("")
    lines.append(f"  {'total':<20} {sum(w for _, w, _ in WEIGHTS):>3}")
    lines.append("")
    lines.append("Scores run 1 to 5 and 5 is always the better outcome, including build cost.")
    lines.append(TIE_TEXT)
    return "\n".join(lines)


def render_explain(rows: list[dict]) -> str:
    blocks = []
    for row in rows:
        head = (
            f"[{row['rank']}] {row['id']}  ({row['shape']})  "
            f"total {as_points(row['tenths']):.1f}/100"
        )
        lines = [head]
        for key, weight, _ in WEIGHTS:
            score = row["scores"][key]
            points = as_points(row["contribution"][key])
            lines.append(
                f"    {LABELS[key]:<20} {score} x {weight:<3} -> {points:>5.1f}   {NOTE[key]}"
            )
        if row["reason"]:
            lines.append(f"    reason given: {row['reason']}")
        blocks.append("\n".join(lines))
    return "\n\n".join(blocks)


def report(rows: list[dict], shown: int, total: int) -> dict:
    return {
        "weights": [
            {"criterion": key, "label": LABELS[key], "weight": weight, "reason": reason}
            for key, weight, reason in WEIGHTS
        ],
        "tie_break": TIE_TEXT,
        "count": total,
        "shown": shown,
        "ideas": [
            {
                "rank": row["rank"],
                "id": row["id"],
                "name": row["name"],
                "shape": row["shape"],
                "scores": row["scores"],
                "contribution": {k: as_points(v) for k, v in row["contribution"].items()},
                "total": as_points(row["tenths"]),
                "reason": row["reason"],
            }
            for row in rows
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Rank lead magnet ideas with a fixed weighted model.",
        epilog=(
            "Weights are fixed at 25/20/15/15/10/15 and cannot be changed from the "
            "command line. " + TIE_TEXT
        ),
    )
    parser.add_argument("ideas", nargs="?", type=Path, help="JSON file holding the ideas")
    parser.add_argument("--top", type=int, default=5, metavar="N", help="show the top N ideas (default 5)")
    parser.add_argument("--explain", action="store_true", help="print the weights and every contribution")
    parser.add_argument("--json", action="store_true", help="print machine-readable JSON only")
    parser.add_argument("--example", action="store_true", help="print a small valid idea file and exit")
    args = parser.parse_args()

    if args.example:
        print(json.dumps(EXAMPLE, indent=2, ensure_ascii=False))
        return 0

    if args.ideas is None:
        parser.error("an ideas file is required unless --example is used")
    if args.top < 1:
        print("error: --top must be 1 or more", file=sys.stderr)
        return 2

    ideas, errors = load(args.ideas)
    if errors:
        print(f"{args.ideas}: {len(errors)} problem(s)", file=sys.stderr)
        for error in errors:
            print(f"  {error}", file=sys.stderr)
        print("Nothing was ranked.", file=sys.stderr)
        return 2

    rows = rank(ideas)
    shown = min(args.top, len(rows))
    shortlist = rows[:shown]

    if args.json:
        print(json.dumps(report(shortlist, shown, len(rows)), indent=2, ensure_ascii=False))
        return 0

    print(render_table(shortlist))
    print()
    print(f"Shown {shown} of {len(rows)} ideas. Weights are fixed; see --explain for the reason behind each one.")

    if args.explain:
        print()
        print(render_weights())
        print()
        print("Contribution per criterion, in points out of 100:")
        print()
        print(render_explain(shortlist))

    return 0


if __name__ == "__main__":
    sys.exit(main())
