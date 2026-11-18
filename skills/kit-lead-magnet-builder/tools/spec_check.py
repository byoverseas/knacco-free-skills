#!/usr/bin/env python3
"""Check a lead magnet build spec before a coding tool is asked to build it.

Usage:
    python3 spec_check.py build-spec.json
    python3 spec_check.py build-spec.json --json
    python3 spec_check.py --example > build-spec.json

The checker looks for eleven fields, then for the seven omissions that stall a
build: more than five inputs, no defined output, no gate after value, no call to
action path, no empty state, no mobile rule, no success measure.

Exit codes: 0 pass (warnings allowed), 2 one or more errors, or unreadable input.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

FIELDS = [
    ("niche", "who this is for, in one trade and one place"),
    ("paid_offer", "the thing the magnet bridges to"),
    ("pain", "the problem in the user's own words"),
    ("promise", "the sentence the tool can honour"),
    ("inputs", "the numbers the user supplies, five at most"),
    ("screens", "first screen, empty state, mobile rule"),
    ("logic", "the computation, step by step"),
    ("output", "the result the user receives"),
    ("gate", "where the email gate sits and what it holds back"),
    ("cta", "what happens after the result"),
    ("success_measure", "the metric, the target and the window"),
]

GATE_POSITIONS = ["after-partial"]
CTA_PLACES = ["result", "email", "result-and-email"]
PLACEHOLDERS = ["TODO", "TBD", "FIXME", "LOREM IPSUM", "XXX"]
CLAIM_WORDS = [
    "guarantee",
    "risk-free",
    "risk free",
    "proven to",
    "double your",
    "triple your",
    "will earn",
    "will make you",
    "instant results",
    "100%",
]

EXAMPLE = {
    "niche": "Independent physiotherapy clinics in the UK with two to six therapists and no dedicated practice manager.",
    "paid_offer": "A 90 minute clinic operations review at 450 pounds, which becomes a monthly retainer at 220 pounds a month.",
    "pain": "The owner knows some appointments are lost to no-shows and late cancellations, and cannot put a monthly figure on it, so the problem stays a feeling rather than a line in the accounts.",
    "promise": "The calculator multiplies the clinic's own appointment count, fee and missed appointments into a monthly and annual revenue figure, and shows the same arithmetic at a lower miss rate. It reports the arithmetic, not a forecast.",
    "inputs": [
        {"name": "Appointments booked per week", "type": "number", "why": "sets the volume the loss is counted against"},
        {"name": "Average appointment fee", "type": "number", "why": "turns missed appointments into money"},
        {"name": "No-shows in a typical week", "type": "number", "why": "the first of the two misses the clinic can already count"},
        {"name": "Late cancellations in a typical week", "type": "number", "why": "the second miss, which owners usually leave out of the count"},
    ],
    "screens": {
        "first": "One screen with the clinic name field at the top, four number fields in one column, a plain sentence saying what the calculator will do with them, and one button reading Show the monthly cost. No email field on this screen.",
        "empty_state": "Before any number is entered the result area holds one line: Nothing calculated yet. Enter the four numbers above. The button stays disabled until the four fields hold numbers.",
        "mobile": "One column at any width. The four fields stack, the result appears below the button rather than beside it, the monthly figure is set at 32px minimum, and the page is usable at 320px wide with no horizontal scroll.",
    },
    "logic": [
        "Weekly volume is appointments booked per week.",
        "Missed per week is no-shows plus late cancellations.",
        "Miss rate is missed per week divided by weekly volume, shown to one decimal place.",
        "Monthly cost is missed per week multiplied by the average fee, multiplied by 4.33.",
        "Annual cost is the monthly cost multiplied by 12.",
        "The lower-rate line repeats the same arithmetic at a miss rate one fifth lower than the user's own, and is labelled as arithmetic, not as a forecast.",
        "If missed per week is larger than weekly volume, the result is suppressed and the screen asks the user to check the four numbers.",
    ],
    "output": {
        "fields": [
            "monthly cost of missed appointments, in pounds, one decimal place",
            "annual cost of the same, in pounds, rounded to the nearest pound",
            "miss rate as a percentage, one decimal place",
            "missed appointments per week",
            "the same three money figures at a miss rate one fifth lower, labelled as arithmetic",
        ],
        "format": "A single results panel on the same page: the monthly figure set largest, the annual figure beneath it, the miss rate and the weekly count as two small lines, then the lower-rate block in a bordered box. Every figure carries its label and the unit. The panel can be copied as text.",
    },
    "gate": {
        "position": "after-partial",
        "shown_before": "The monthly figure, the miss rate and the missed appointments per week are shown with no email address given.",
        "held_back": "The annual figure and the lower-rate comparison are held until an email address is submitted.",
    },
    "cta": {
        "text": "If the annual figure is worth fixing, book the 90 minute review. Bring the four numbers and the review starts from them.",
        "destination": "The clinic's booking page for the operations review, with the monthly figure passed in the query string so the booking form shows the number the visitor arrived with.",
        "appears": "result-and-email",
    },
    "success_measure": {
        "metric": "Completed calculations as a share of page visits, and review bookings that name the calculator as the source.",
        "target": "A quarter of visits reach a result, and two review bookings a month name the calculator.",
        "window": "Measured over the first eight weeks after launch, reviewed at four weeks and at eight.",
    },
}


def text_of(value) -> str:
    """Flatten a string, list or dict of strings into one searchable block."""
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return " ".join(text_of(item) for item in value)
    if isinstance(value, dict):
        return " ".join(f"{k} {text_of(v)}" for k, v in value.items())
    if value is None:
        return ""
    return str(value)


def filled(value, minimum: int = 1) -> bool:
    if isinstance(value, str):
        return len(value.strip()) >= minimum
    if isinstance(value, (list, dict)):
        return len(value) > 0
    return False


def finding(rule: str, check: str, ok: bool, severity: str, evidence: str, fix: str) -> dict:
    return {
        "rule": rule,
        "check": check,
        "status": "ok" if ok else severity,
        "evidence": evidence,
        "fix": "" if ok else fix,
    }


def check(spec: dict) -> dict:
    findings: list[dict] = []

    # R01. The eleven fields, and the ones that carry prose must carry prose.
    missing = [name for name, _ in FIELDS if name not in spec]
    thin: list[str] = []
    for name in ["niche", "paid_offer", "pain", "promise"]:
        if name in spec and not (isinstance(spec[name], str) and len(spec[name].strip()) >= 20):
            thin.append(name)
    screens = spec.get("screens")
    if not isinstance(screens, dict) or not filled(screens.get("first"), 20):
        thin.append("screens.first")
    logic = spec.get("logic")
    logic_ok = (
        isinstance(logic, list) and len([s for s in logic if isinstance(s, str) and s.strip()]) >= 2
    ) or (isinstance(logic, str) and len(logic.strip()) >= 40)
    if not logic_ok:
        thin.append("logic")

    block = text_of(spec).upper()
    placeholders = [token for token in PLACEHOLDERS if token in block]

    if missing:
        evidence = "missing: " + ", ".join(missing)
    elif thin:
        evidence = "empty or too short to build from: " + ", ".join(thin)
    elif placeholders:
        evidence = "placeholder text left in: " + ", ".join(placeholders)
    else:
        evidence = "all eleven fields present and filled"
    findings.append(
        finding(
            "R01",
            "eleven fields present and filled",
            not missing and not thin and not placeholders,
            "error",
            evidence,
            "Fill every field in the list below. A field that holds a placeholder is treated as empty, because a coding tool will build the placeholder.",
        )
    )

    # R02. The input cap.
    inputs = spec.get("inputs")
    input_list = inputs if isinstance(inputs, list) else []
    shaped = [
        item
        for item in input_list
        if isinstance(item, dict) and filled(item.get("name"), 2) and filled(item.get("why"), 5)
    ]
    count = len(input_list)
    if count == 0:
        evidence = "no inputs listed"
    elif count > 5:
        evidence = f"{count} inputs listed, cap is 5"
    elif len(shaped) != count:
        evidence = f"{count - len(shaped)} input(s) with no name or no reason"
    else:
        evidence = f"{count} input(s), each with a name and a reason"
    findings.append(
        finding(
            "R02",
            "inputs capped at five",
            count > 0 and count <= 5 and len(shaped) == count,
            "error",
            evidence,
            "Cut to five inputs or fewer. Drop the field that only improves precision, prefill the one you can look up, and split the rest into a second step that runs after the first result.",
        )
    )

    # R03. A defined output.
    output = spec.get("output")
    fields_out = output.get("fields") if isinstance(output, dict) else None
    good_fields = (
        [f for f in fields_out if isinstance(f, str) and f.strip()]
        if isinstance(fields_out, list)
        else []
    )
    has_format = isinstance(output, dict) and filled(output.get("format"), 10)
    if not isinstance(output, dict):
        evidence = "output is not defined"
    elif not good_fields:
        evidence = "output has no named fields"
    elif not has_format:
        evidence = "output has no format"
    else:
        evidence = f"{len(good_fields)} output field(s) and a format"
    findings.append(
        finding(
            "R03",
            "output defined",
            bool(good_fields) and has_format,
            "error",
            evidence,
            "Name every field the result shows, with its unit and its rounding, then say how the result is laid out and what it can be copied as.",
        )
    )

    # R04. The gate sits after partial value.
    gate = spec.get("gate")
    position = gate.get("position") if isinstance(gate, dict) else None
    if not isinstance(gate, dict):
        evidence = "no gate defined"
    elif position not in GATE_POSITIONS:
        evidence = f"gate position is {position!r}, allowed: {' or '.join(GATE_POSITIONS)}"
    elif not filled(gate.get("shown_before"), 10):
        evidence = "gate does not say what is shown before the email is asked for"
    elif not filled(gate.get("held_back"), 10):
        evidence = "gate does not say what is held back"
    else:
        evidence = "partial result first, full result after the email"
    findings.append(
        finding(
            "R04",
            "gate after value",
            isinstance(gate, dict)
            and position in GATE_POSITIONS
            and filled(gate.get("shown_before"), 10)
            and filled(gate.get("held_back"), 10),
            "error",
            evidence,
            "Set gate.position to after-partial, name the part of the result shown before the email, and name the part held back. A gate at the door asks for an address before the visitor has seen anything work.",
        )
    )

    # R05. A call to action path.
    cta = spec.get("cta")
    if not isinstance(cta, dict):
        evidence = "no call to action defined"
    elif not filled(cta.get("text"), 10):
        evidence = "call to action has no text"
    elif not filled(cta.get("destination"), 5):
        evidence = "call to action has no destination"
    elif cta.get("appears") not in CTA_PLACES:
        evidence = f"cta.appears is {cta.get('appears')!r}, allowed: {', '.join(CTA_PLACES)}"
    else:
        evidence = f"call to action at {cta.get('appears')}, pointing at a named destination"
    findings.append(
        finding(
            "R05",
            "call to action path",
            isinstance(cta, dict)
            and filled(cta.get("text"), 10)
            and filled(cta.get("destination"), 5)
            and cta.get("appears") in CTA_PLACES,
            "error",
            evidence,
            "Write the sentence the user reads, the place it sends them, and whether it appears with the result or after the email. A result with no next step is a PDF with extra steps.",
        )
    )

    # R06. Empty state.
    empty_state = screens.get("empty_state") if isinstance(screens, dict) else None
    findings.append(
        finding(
            "R06",
            "empty state defined",
            filled(empty_state, 20),
            "error",
            "empty state defined" if filled(empty_state, 20) else "no empty state before any input",
            "Write what the result area holds before the first number is typed, and what the button does while fields are empty.",
        )
    )

    # R07. Mobile rule.
    mobile = screens.get("mobile") if isinstance(screens, dict) else None
    findings.append(
        finding(
            "R07",
            "mobile rule defined",
            filled(mobile, 20),
            "error",
            "mobile rule defined" if filled(mobile, 20) else "no mobile rule",
            "State the layout at narrow width, the minimum size of the main figure, and the width the tool is tested at.",
        )
    )

    # R08. Success measure.
    measure = spec.get("success_measure")
    parts = ["metric", "target", "window"] if isinstance(measure, dict) else []
    gaps = [p for p in parts if not filled(measure.get(p), 3)]
    if not isinstance(measure, dict):
        evidence = "no success measure defined"
    elif gaps:
        evidence = "success measure missing " + ", ".join(gaps)
    else:
        evidence = f"metric, target and window defined: {measure.get('metric')[:60]}"
    findings.append(
        finding(
            "R08",
            "success measure defined",
            isinstance(measure, dict) and not gaps,
            "error",
            evidence,
            "Name the metric, the number you are aiming at, and the window you will measure it over. Without this the build has no way to fail.",
        )
    )

    # W01. Claim language in the promise. A warning, not an error: the sentence
    # may be quoting a claim the owner has decided to drop.
    promise_text = spec.get("promise") if isinstance(spec.get("promise"), str) else ""
    found_claims = [word for word in CLAIM_WORDS if word in promise_text.lower()]
    findings.append(
        finding(
            "W01",
            "promise carries no claim language",
            not found_claims,
            "warning",
            "claim words in promise: " + ", ".join(found_claims) if found_claims else "no claim language in the promise",
            "Rewrite the promise as what the tool computes. A guarantee is not computable, and an uncomputable promise turns the result into an argument with the buyer.",
        )
    )

    errors = [f for f in findings if f["status"] == "error"]
    warnings = [f for f in findings if f["status"] == "warning"]
    score = max(0, 100 - 10 * len(errors) - 3 * len(warnings))
    return {"ok": not errors, "score": score, "errors": len(errors), "warnings": len(warnings), "findings": findings}


def shorten(text: str, limit: int = 74) -> str:
    text = " ".join(text.split())
    return text if len(text) <= limit else text[: limit - 3].rstrip() + "..."


def render_table(findings: list[dict]) -> str:
    head = ["rule", "check", "status", "evidence"]
    rows = [[f["rule"], f["check"], f["status"], shorten(f["evidence"])] for f in findings]
    widths = [len(h) for h in head]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(cell))

    def fmt(cells: list[str]) -> str:
        return "  ".join(cell.ljust(widths[i]) for i, cell in enumerate(cells)).rstrip()

    lines = [fmt(head), "-" * (sum(widths) + 2 * (len(widths) - 1))]
    lines.extend(fmt(row) for row in rows)
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check a lead magnet build spec for the eleven fields and the seven build-stopping omissions.",
        epilog=(
            "Exit 2 means at least one error. Warnings reduce the score but do not fail the spec. "
            "Run with --example to print a spec that passes."
        ),
    )
    parser.add_argument("spec", nargs="?", type=Path, help="build spec JSON file")
    parser.add_argument("--json", action="store_true", help="print machine-readable JSON only")
    parser.add_argument("--example", action="store_true", help="print a passing build spec and exit")
    args = parser.parse_args()

    if args.example:
        print(json.dumps(EXAMPLE, indent=2, ensure_ascii=False))
        return 0

    if args.spec is None:
        parser.error("a build spec file is required unless --example is used")

    try:
        spec = json.loads(args.spec.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"{args.spec}: file not found", file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print(f"{args.spec}: not valid JSON ({exc.msg}, line {exc.lineno}, column {exc.colno})", file=sys.stderr)
        return 2
    except OSError as exc:
        print(f"{args.spec}: could not be read ({exc.strerror})", file=sys.stderr)
        return 2

    if not isinstance(spec, dict):
        print(f"{args.spec}: a build spec must be a JSON object", file=sys.stderr)
        return 2

    result = check(spec)

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0 if result["ok"] else 2

    verdict = "PASS" if result["ok"] else "FAIL"
    print(
        f"{verdict}  score {result['score']}/100  "
        f"errors {result['errors']}  warnings {result['warnings']}\n"
    )
    print(render_table(result["findings"]))

    fixes = [f for f in result["findings"] if f["status"] != "ok"]
    if fixes:
        print()
        print("What to fix:")
        for item in fixes:
            label = "error" if item["status"] == "error" else "warning"
            print(f"  {item['rule']}  {label}: {item['fix']}")

    return 0 if result["ok"] else 2


if __name__ == "__main__":
    sys.exit(main())
