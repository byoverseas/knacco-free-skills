#!/usr/bin/env python3
"""Check a proposed output against a brand-spec.json written by brand_audit.py.

Standard library only. Python 3.9 or newer.

    python3 brand_check.py <brand-spec.json> <output-description.json>
    python3 brand_check.py <brand-spec.json> <notes.txt>

Twelve rules, R01 to R12. A structured description is checked against all
twelve. A plain text file is checked on the rules that text can carry, and the
rest are reported as skipped, which costs no points.

Exit codes: 0 when every rule passes, 2 when any rule fails or the files cannot
be read.
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

HEX_RE = re.compile(r"#[0-9a-fA-F]{3,8}\b")
PX_RE = re.compile(r"([0-9]+(?:\.[0-9]+)?)\s*px", re.IGNORECASE)
GENERIC_FAMILIES = {
    "serif", "sans-serif", "monospace", "cursive", "fantasy", "system-ui",
    "ui-serif", "ui-sans-serif", "ui-monospace", "inherit", "initial",
}

RULES = [
    ("R01", "Palette contains only colours from the spec"),
    ("R02", "Ink colour carries body text"),
    ("R03", "Accent is used at most twice"),
    ("R04", "Only spec fonts are used"),
    ("R05", "Logo appears exactly once"),
    ("R06", "Logo clear space is respected"),
    ("R07", "No invented logo"),
    ("R08", "Imagery rule is respected"),
    ("R09", "Type sizes stay inside the scale"),
    ("R10", "Contrast pair comes from the safe pairings list"),
    ("R11", "No unconfirmed inferred value is used"),
    ("R12", "The output names the brand correctly"),
]
RULE_TITLES = dict(RULES)


# ------------------------------------------------------------------ helpers


def norm_hex(value: str) -> Optional[str]:
    h = value.strip().lstrip("#")
    if len(h) in (3, 4):
        h = "".join(ch * 2 for ch in h[:3])
    elif len(h) in (6, 8):
        h = h[:6]
    else:
        return None
    if not re.fullmatch(r"[0-9a-fA-F]{6}", h):
        return None
    return "#" + h.lower()


def rgb(value: str) -> Tuple[int, int, int]:
    h = value.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def channel_distance(a: str, b: str) -> int:
    ra, ga, ba = rgb(a)
    rb, gb, bb = rgb(b)
    return max(abs(ra - rb), abs(ga - gb), abs(ba - bb))


def luminance(value: str) -> float:
    out = []
    for c in rgb(value):
        s = c / 255.0
        out.append(s / 12.92 if s <= 0.04045 else ((s + 0.055) / 1.055) ** 2.4)
    return 0.2126 * out[0] + 0.7152 * out[1] + 0.0722 * out[2]


def contrast(a: str, b: str) -> float:
    la, lb = luminance(a), luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return round((hi + 0.05) / (lo + 0.05), 2)


def times(count: int, noun: str) -> str:
    """'2 times', '1 time'."""
    return "{} {}{}".format(count, noun, "" if count == 1 else "s")


def spec_value(entry, default=None):
    """Read .value from a spec value object, or the object itself."""
    if isinstance(entry, dict):
        return entry.get("value", default)
    return default if entry is None else entry


def hexes_in(value) -> List[str]:
    found = []
    if isinstance(value, str):
        for match in HEX_RE.finditer(value):
            normalised = norm_hex(match.group(0))
            if normalised:
                found.append(normalised)
    elif isinstance(value, list):
        for item in value:
            found.extend(hexes_in(item))
    return found


class Report:
    def __init__(self) -> None:
        self.rows: List[dict] = []

    def add(self, rule: str, status: str, detail: str,
            fix: str = "", evidence: str = "") -> None:
        self.rows.append(
            {
                "rule": rule,
                "title": RULE_TITLES[rule],
                "status": status,
                "detail": detail,
                "fix": fix,
                "evidence": evidence,
            }
        )

    def count(self, status: str) -> int:
        return sum(1 for row in self.rows if row["status"] == status)

    def score(self) -> int:
        return max(0, 100 - 10 * self.count("error") - 3 * self.count("warning"))

    def ok(self) -> bool:
        return self.count("error") == 0

    def as_dict(self) -> dict:
        return {
            "ok": self.ok(),
            "score": self.score(),
            "errors": self.count("error"),
            "warnings": self.count("warning"),
            "skipped": self.count("skip"),
            "rows": self.rows,
        }


# ---------------------------------------------------------------- the rules


def rule_palette(report: Report, spec: dict, description: dict, text: str) -> None:
    tolerance = int(spec_value(spec.get("colours", {}).get("tolerance"), 6) or 6)
    palette = [c["value"] for c in spec["colours"]["ranked"]]
    used = list(description.get("colours_used") or [])
    for key in ("body_text_colour", "background_colour"):
        if description.get(key):
            used.append(description[key])
    pair = description.get("contrast_pair") or {}
    if isinstance(pair, dict):
        used.extend([v for v in pair.values() if isinstance(v, str)])
    used.extend(hexes_in(description.get("text")))
    if not used:
        report.add("R01", "skip", "No colours declared in the description.",
                   "Add colours_used so the palette can be checked.")
        return
    unknown = []
    for raw in used:
        value = norm_hex(str(raw))
        if value is None:
            unknown.append(str(raw))
            continue
        if not any(channel_distance(value, known) <= tolerance for known in palette):
            nearest = min(palette, key=lambda known: channel_distance(value, known)) if palette else "none"
            distance = channel_distance(value, nearest) if palette else 0
            unknown.append("{} (nearest spec colour {} at {} of 255)".format(value, nearest, distance))
    if unknown:
        report.add(
            "R01", "error",
            "{} outside the spec palette at a tolerance of {} of 255.".format(
                times(len(unknown), "colour"), tolerance
            ),
            "Replace each colour with the nearest spec colour, or add the colour to the spec "
            "with the owner's confirmation.",
            "; ".join(unknown),
        )
    else:
        report.add(
            "R01", "ok",
            "All {} colours are within {} of 255 of a spec colour.".format(len(used), tolerance),
        )


def rule_ink(report: Report, spec: dict, description: dict, text: str) -> None:
    tolerance = int(spec_value(spec.get("colours", {}).get("tolerance"), 6) or 6)
    ink = spec_value(spec["colours"]["roles"].get("ink"))
    body = description.get("body_text_colour")
    if not ink:
        report.add("R02", "warning", "The spec has no ink colour.",
                   "Confirm ink with the owner, then rebuild the spec.")
        return
    if not body:
        report.add("R02", "warning", "The description does not name a body text colour.",
                   "Declare body_text_colour.")
        return
    value = norm_hex(str(body))
    if value and channel_distance(value, ink) <= tolerance:
        report.add("R02", "ok", "Body text is set in ink {}.".format(ink))
    else:
        report.add(
            "R02", "error",
            "Body text is {}, and ink is {}.".format(body, ink),
            "Set body text in the ink colour. The muted or accent colour may carry captions, not body copy.",
        )


def rule_accent(report: Report, spec: dict, description: dict, text: str) -> None:
    accent = spec_value(spec["colours"]["roles"].get("accent"))
    budget = 2
    if not accent:
        report.add("R03", "warning", "The spec has no accent colour.",
                   "Confirm an accent with the owner before building the skill.")
        return
    uses = description.get("accent_uses")
    if isinstance(uses, list):
        normalised = [norm_hex(str(item)) or str(item) for item in uses]
        count = sum(1 for item in normalised if item == accent)
    elif isinstance(uses, int):
        count = uses
    elif uses is None:
        report.add("R03", "warning", "The description does not declare accent_uses.",
                   "Declare accent_uses as a number or as the list of colours used.")
        return
    else:
        report.add("R03", "warning", "accent_uses must be a number or a list.",
                   "Fix the field type.")
        return
    if count > budget:
        report.add(
            "R03", "error",
            "The accent {} is used {}; the budget is {}.".format(
                accent, times(count, "time"), budget
            ),
            "Remove {} of the accent. An accent that appears three times is a second brand colour.".format(
                times(count - budget, "use")
            ),
        )
    else:
        report.add(
            "R03", "ok",
            "Accent used {} of a budget of {}.".format(times(count, "time"), budget),
        )


def rule_fonts(report: Report, spec: dict, description: dict, text: str) -> None:
    faces = [
        str(f["value"]).lower()
        for f in spec["type"]["families"]
        if f.get("role") == "brand face"
    ]
    fallbacks = [
        str(f["value"]).lower()
        for f in spec["type"]["families"]
        if f.get("role") != "brand face"
    ]
    used = [str(f) for f in (description.get("fonts_used") or [])]
    if not used:
        report.add("R04", "warning", "The description does not declare fonts_used.",
                   "Declare every family the output sets type in.")
        return
    problems = []
    soft = []
    for family in used:
        key = family.strip().lower()
        if key in GENERIC_FAMILIES:
            continue
        if key in faces:
            continue
        if key in fallbacks:
            soft.append(family)
        else:
            problems.append(family)
    if problems:
        report.add(
            "R04", "error",
            "Font(s) outside the spec: {}.".format(", ".join(sorted(problems))),
            "Set type only in {}. A fourth typeface is not a brand face.".format(
                ", ".join(f["value"] for f in spec["type"]["families"] if f.get("role") == "brand face")
                or "the declared brand faces"
            ),
        )
    elif soft:
        report.add(
            "R04", "warning",
            "Fallback families used: {}.".format(", ".join(sorted(soft))),
            "Fallbacks are allowed only when the brand face is unavailable. Say so in the output notes.",
        )
    else:
        report.add("R04", "ok", "Every family is a declared brand face.")


def rule_logo_once(report: Report, spec: dict, description: dict, text: str) -> None:
    logo = description.get("logo") or {}
    instances = logo.get("instances")
    if instances is None:
        report.add("R05", "warning", "The description does not declare logo instances.",
                   "Declare logo.instances, or 0 when the output carries no logo.")
        return
    if instances == 1:
        report.add("R05", "ok", "One logo instance.")
    else:
        report.add(
            "R05", "error",
            "The logo appears {}.".format(times(instances, "time")),
            "Place the logo once. A second placement competes with the first and reads as decoration.",
        )


def rule_clear_space(report: Report, spec: dict, description: dict, text: str) -> None:
    logo = description.get("logo") or {}
    minimum = spec["logo"]["clear_space"].get("minimum_px")
    declared = logo.get("clear_space_px")
    if declared is None:
        report.add("R06", "warning", "The description does not declare clear space.",
                   "Declare logo.clear_space_px so the rule can be checked.")
        return
    if minimum is None:
        report.add("R06", "warning", "The spec has no clear space figure.",
                   "Confirm clear space with the owner.")
        return
    if float(declared) >= float(minimum):
        report.add("R06", "ok", "Clear space {}px meets the {}px minimum.".format(declared, minimum))
    else:
        report.add(
            "R06", "error",
            "Clear space is {}px against a {}px minimum.".format(declared, minimum),
            "Grow the space around the logo to at least {}px on all four sides.".format(minimum),
        )


def rule_invented_logo(report: Report, spec: dict, description: dict, text: str) -> None:
    logo = description.get("logo") or {}
    if logo.get("invented") is True:
        report.add(
            "R07", "error",
            "The description says the logo was drawn for this output.",
            "Use a logo variant from the spec. A brand skill never draws a logo.",
        )
        return
    source = logo.get("source_file")
    variants = [str(v["value"]) for v in spec["logo"]["variants"]]
    if not variants:
        report.add("R07", "warning", "The spec lists no logo variants.",
                   "Add the logo files to the asset folder and audit again.")
        return
    if not source:
        report.add(
            "R07", "warning", "No logo source file is declared.",
            "Declare logo.source_file so the variant can be matched to the spec.",
        )
        return
    matches = [
        variant for variant in variants
        if variant == source or variant.endswith("/" + source) or source.endswith(Path(variant).name)
    ]
    if matches:
        report.add("R07", "ok", "Logo source {} is a spec variant.".format(source))
    else:
        report.add(
            "R07", "error",
            "Logo source {} is not in the spec.".format(source),
            "Use one of: {}. If a new variant is needed, add the file and audit again.".format(
                ", ".join(variants)
            ),
        )


def rule_imagery(report: Report, spec: dict, description: dict, text: str) -> None:
    items = description.get("imagery")
    spec_files = spec["imagery"]["files"]
    orientations = {f.get("orientation") for f in spec_files if f.get("orientation")}
    if items is None:
        report.add("R08", "skip", "The description declares no imagery.",
                   "Declare imagery as a list, or an empty list when the output has none.")
        return
    if not isinstance(items, list):
        report.add("R08", "error", "imagery must be a list.", "Fix the field type.")
        return
    if not items:
        report.add("R08", "ok", "No imagery used, so no imagery rule applies.")
        return
    if not spec_files:
        report.add(
            "R08", "error",
            "The output uses {} image(s) but the spec holds no imagery.".format(len(items)),
            "Audit an asset folder that contains imagery, or remove the images from this output.",
        )
        return
    problems = []
    for item in items:
        if not isinstance(item, dict):
            problems.append("imagery entry is not an object")
            continue
        if item.get("stretched") is True:
            problems.append("{} is stretched".format(item.get("id", "an image")))
        aspect = item.get("aspect")
        allowed = {f.get("aspect") for f in spec_files if f.get("aspect")}
        if isinstance(aspect, (int, float)) and aspect > 0:
            orientation = (
                "square" if abs(aspect - 1.0) < 0.01 else ("landscape" if aspect > 1 else "portrait")
            )
            if orientations and orientation not in orientations:
                problems.append(
                    "{} is {} and the spec holds only {}".format(
                        item.get("id", "an image"), orientation, ", ".join(sorted(orientations))
                    )
                )
            if allowed and not any(abs(aspect - candidate) <= 0.1 for candidate in allowed):
                problems.append(
                    "{} has aspect {:.2f}, outside the sampled ratios".format(
                        item.get("id", "an image"), aspect
                    )
                )
    if problems:
        report.add(
            "R08", "error",
            "; ".join(problems) + ".",
            "Crop to a ratio the brand already uses, and never stretch an image.",
        )
    else:
        report.add("R08", "ok", "{}, no stretch, ratios inside the spec.".format(times(len(items), "image")))


def rule_type_scale(report: Report, spec: dict, description: dict, text: str) -> None:
    scale = []
    for entry in spec["type"]["scale"]:
        shown = str(entry["value"]).replace("px", "")
        try:
            scale.append(float(shown))
        except ValueError:
            continue
    sizes = description.get("type_sizes_px")
    if sizes is None:
        report.add("R09", "warning", "The description does not declare type sizes.",
                   "Declare type_sizes_px as a list of numbers.")
        return
    if not isinstance(sizes, list) or not sizes:
        report.add("R09", "skip", "No type sizes to check.")
        return
    if not scale:
        report.add(
            "R09", "warning",
            "The spec holds no type scale, so sizes cannot be checked.",
            "The audit found fewer than three declared sizes. Get the scale from the owner.",
        )
        return
    outside = []
    for size in sizes:
        try:
            number = float(size)
        except (TypeError, ValueError):
            outside.append(str(size))
            continue
        if not any(abs(number - allowed) <= 1 for allowed in scale):
            outside.append("{}px".format(int(number) if number.is_integer() else number))
    count_limit = len(scale)
    if outside:
        report.add(
            "R09", "error",
            "{} outside the scale: {}. The scale holds {}.".format(
                times(len(outside), "size"), ", ".join(outside), times(len(scale), "size")
            ),
            "Set every size to one of: {}. More sizes than the scale is a second type system.".format(
                ", ".join("{}px".format(int(s) if s.is_integer() else s) for s in sorted(scale))
            ),
        )
    elif len(set(float(s) for s in sizes)) > count_limit:
        report.add(
            "R09", "error",
            "{} distinct sizes against a scale of {}.".format(len(set(sizes)), count_limit),
            "Drop the extra sizes and reuse the scale.",
        )
    else:
        report.add("R09", "ok", "All {} sizes are inside the scale of {}.".format(len(sizes), len(scale)))


def rule_contrast(report: Report, spec: dict, description: dict, text: str) -> None:
    pair = description.get("contrast_pair")
    if not isinstance(pair, dict):
        report.add("R10", "warning", "The description does not declare a contrast pair.",
                   "Declare contrast_pair as {text, background}.")
        return
    text_hex = norm_hex(str(pair.get("text", "")))
    background_hex = norm_hex(str(pair.get("background", "")))
    if not text_hex or not background_hex:
        report.add("R10", "error", "The contrast pair is not two hex colours.",
                   "Declare the pair as two hex values.")
        return
    safe = []
    for entry in spec.get("pairings", []):
        raw = str(entry.get("value", ""))
        parts = [part.strip() for part in raw.split(" on ")]
        if len(parts) != 2:
            continue
        front, back = norm_hex(parts[0]), norm_hex(parts[1])
        if not front or not back:
            continue
        if float(entry.get("ratio", 0)) >= 4.5:
            safe.append((front, back, float(entry.get("ratio", 0))))
    match = [
        ratio for front, back, ratio in safe
        if {front, back} == {text_hex, background_hex}
    ]
    if match:
        report.add(
            "R10", "ok",
            "{} on {} is a safe pair at {:.2f}:1.".format(text_hex, background_hex, max(match)),
        )
        return
    best = ""
    if safe:
        front, back, ratio = max(safe, key=lambda item: item[2])
        best = " The safest pair in the spec is {} on {} at {:.2f}:1.".format(front, back, ratio)
    report.add(
        "R10", "error",
        "{} on {} is not in the safe pairings list.".format(text_hex, background_hex),
        "Use a pair the spec lists at 4.5:1 or better." + best,
    )


def rule_unconfirmed(report: Report, spec: dict, description: dict, text: str) -> None:
    unconfirmed = list(spec.get("unconfirmed") or [])
    if not unconfirmed:
        report.add("R11", "ok", "The spec holds no unconfirmed inferred values.")
        return
    declared = description.get("uses_inferred")
    hits = []
    if isinstance(declared, list):
        for path in declared:
            clean = str(path).strip()
            if clean in unconfirmed or any(
                clean == item or clean.startswith(item + ".") or item.startswith(clean + ".")
                for item in unconfirmed
            ):
                hits.append(clean)
    palette = [c["value"] for c in spec["colours"]["ranked"]]
    inferred_hexes: Dict[str, str] = {}
    for path in unconfirmed:
        node = resolve_path(spec, path)
        if node is None:
            continue
        for hex_value in hexes_in(node.get("value")):
            if hex_value not in palette:
                inferred_hexes[hex_value] = path
    used = hexes_in(description.get("colours_used"))
    for key in ("body_text_colour", "background_colour"):
        used.extend(hexes_in(description.get(key)))
    for value in used:
        if value in inferred_hexes:
            hits.append("{} from {}".format(value, inferred_hexes[value]))
    if hits:
        report.add(
            "R11", "error",
            "The output depends on {} unconfirmed inferred value(s).".format(len(set(hits))),
            "Confirm each value with the owner and audit again, or remove it from the output.",
            "; ".join(sorted(set(hits))),
        )
    else:
        report.add(
            "R11", "ok",
            "Nothing in the output depends on an unconfirmed value ({} remain in the spec).".format(
                len(unconfirmed)
            ),
        )


def rule_brand_name(report: Report, spec: dict, description: dict, text: str) -> None:
    expected = spec_value(spec.get("brand", {}).get("name"), "") or ""
    declared = description.get("brand_name_used")
    if not declared:
        if expected and expected.lower() in text.lower():
            report.add("R12", "ok", "The text names {}.".format(expected))
            return
        report.add("R12", "warning", "The description does not declare the brand name.",
                   "Declare brand_name_used.")
        return
    left = " ".join(str(declared).split())
    right = " ".join(str(expected).split())
    if left == right:
        report.add("R12", "ok", "The output names {} exactly.".format(right))
    elif left.lower() == right.lower():
        report.add(
            "R12", "warning",
            "The name matches in lower case but not in case: {} against {}.".format(left, right),
            "Use the exact spelling and case from the spec. A wordmark may be all caps; copy may not.",
        )
    else:
        report.add(
            "R12", "error",
            "The output names {} and the brand is {}.".format(left, right or "unset"),
            "Copy the name from the spec, character for character.",
        )


def resolve_path(spec: dict, path: str):
    """Resolve a dotted path such as colours.roles.ink or pairings[0]."""
    node = spec
    for part in re.split(r"\.", path):
        if not part:
            continue
        match = re.fullmatch(r"([A-Za-z0-9_]+)\[(\d+)\]", part)
        if match:
            key, index = match.group(1), int(match.group(2))
            if not isinstance(node, dict) or key not in node:
                return None
            node = node[key]
            if not isinstance(node, list) or index >= len(node):
                return None
            node = node[index]
            continue
        if not isinstance(node, dict) or part not in node:
            return None
        node = node[part]
    return node if isinstance(node, dict) else None


def run_structured(spec: dict, description: dict, raw_text: str) -> Report:
    report = Report()
    rule_palette(report, spec, description, raw_text)
    rule_ink(report, spec, description, raw_text)
    rule_accent(report, spec, description, raw_text)
    rule_fonts(report, spec, description, raw_text)
    rule_logo_once(report, spec, description, raw_text)
    rule_clear_space(report, spec, description, raw_text)
    rule_invented_logo(report, spec, description, raw_text)
    rule_imagery(report, spec, description, raw_text)
    rule_type_scale(report, spec, description, raw_text)
    rule_contrast(report, spec, description, raw_text)
    rule_unconfirmed(report, spec, description, raw_text)
    rule_brand_name(report, spec, description, raw_text)
    return report


def run_plain(spec: dict, raw_text: str) -> Report:
    """Check what prose can carry. Structural rules are skipped, not failed."""
    report = Report()
    description = {}
    colours = hexes_in(raw_text)
    if colours:
        description["colours_used"] = colours
    sizes = [float(match.group(1)) for match in PX_RE.finditer(raw_text)]
    if sizes:
        description["type_sizes_px"] = sizes
    report.add(
        "R02", "skip", "No body text colour can be read from prose.",
        "Use a description JSON to check ink.",
    )
    rule_palette(report, spec, description, raw_text)
    rule_type_scale(report, spec, description, raw_text)
    for rule in ("R03", "R04", "R05", "R06", "R07", "R08", "R10"):
        report.add(rule, "skip", "This rule needs a structured description.",
                   "Write an output-description JSON to check it.")
    rule_unconfirmed(report, spec, description, raw_text)
    rule_brand_name(report, spec, description, raw_text)
    order = [rule for rule, _ in RULES]
    report.rows.sort(key=lambda row: order.index(row["rule"]))
    return report


def print_report(report: Report, spec_path: Path, output_path: Path) -> None:
    verdict = "PASS" if report.ok() else "FAIL"
    print(
        "{}  score {}/100  errors {}  warnings {}  skipped {}".format(
            verdict, report.score(), report.count("error"),
            report.count("warning"), report.count("skip"),
        )
    )
    print("spec:   {}".format(spec_path))
    print("output: {}".format(output_path))
    print("")
    print("{:<4}  {:<7} {:<46} {}".format("rule", "status", "check", "detail"))
    print("{:<4}  {:<7} {:<46} {}".format("-" * 4, "-" * 7, "-" * 46, "-" * 40))
    for row in report.rows:
        status = {"ok": "ok", "error": "FAIL", "warning": "warn", "skip": "skip"}[row["status"]]
        print("{:<4}  {:<7} {:<46} {}".format(row["rule"], status, row["title"], row["detail"]))
        if row["evidence"]:
            print("      {:<7} {:<46} {}".format("", "", row["evidence"]))
    fixes = [row for row in report.rows if row["fix"] and row["status"] in ("error", "warning")]
    if fixes:
        print("\nfixes")
        for row in fixes:
            print("  {} {}: {}".format(row["rule"], row["title"], row["fix"]))
    errors = [row for row in report.rows if row["status"] == "error"]
    if errors:
        print("\n{} rule(s) failed. Do not ship this output.".format(len(errors)))


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Check a proposed output against a brand-spec.json. Twelve rules, "
            "a score out of 100, and exit 2 on any failed rule."
        ),
        epilog=(
            "Example: python3 brand_check.py brand-spec.json output-description.json"
        ),
    )
    parser.add_argument("spec", type=Path, help="brand-spec.json written by brand_audit.py")
    parser.add_argument("output", type=Path,
                        help="output description JSON, or a plain text file")
    parser.add_argument("--json", action="store_true", help="print the report as JSON")
    args = parser.parse_args(argv)

    try:
        spec = json.loads(args.spec.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        print("error: cannot read spec {}: {}".format(args.spec, error), file=sys.stderr)
        return 2
    try:
        raw = args.output.read_text(encoding="utf-8")
    except OSError as error:
        print("error: cannot read output {}: {}".format(args.output, error), file=sys.stderr)
        return 2

    try:
        description = json.loads(raw)
        structured = isinstance(description, dict)
    except json.JSONDecodeError:
        description = None
        structured = False

    if structured:
        report = run_structured(spec, description, raw)
    else:
        report = run_plain(spec, raw)

    if args.json:
        print(json.dumps(report.as_dict(), indent=2))
    else:
        print_report(report, args.spec, args.output)
    return 0 if report.ok() else 2


if __name__ == "__main__":
    sys.exit(main())
