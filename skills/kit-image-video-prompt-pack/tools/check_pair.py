#!/usr/bin/env python3
"""Check a still/animation prompt pair.

Usage:
    python3 check_pair.py still.txt motion.txt
    python3 check_pair.py still.txt motion.txt --json

Exit codes: 0 pass (warnings allowed), 2 one or more errors.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

BLOCKS = ["SCENE", "HERO", "PLACEMENT", "OPTICS", "LIGHT", "ATMOSPHERE", "MOTION", "GUARDRAILS", "OUTPUT"]
INVARIANTS = ["SCENE", "HERO", "PLACEMENT", "LIGHT", "GUARDRAILS"]
CAMERA_BANS = ["orbit", "pan", "tilt", "handheld", "whip", "zoom", "rotate", "spin", "crane", "dolly", "truck", "roll", "swish"]
NEGATIONS = ("no ", "not ", "never", "without", "locked off", "zero ", "none")


def prohibited_only(clause: str) -> bool:
    """True when a clause names a move only in order to forbid it."""
    low = clause.lower().strip()
    return any(low.startswith(n) or f" {n}" in low for n in NEGATIONS)


def parse(text: str) -> dict[str, str]:
    blocks: dict[str, str] = {}
    current = None
    buf: list[str] = []
    for line in text.splitlines():
        match = re.fullmatch(r"\[([A-Z][A-Z ]*)\]\s*", line.strip())
        if match:
            if current:
                blocks[current] = "\n".join(buf).strip()
            current = match.group(1)
            buf = []
        elif current:
            buf.append(line)
    if current:
        blocks[current] = "\n".join(buf).strip()
    return blocks


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def add(findings, rule, ok, severity, evidence, fix, message):
    findings.append(
        {
            "rule": rule,
            "status": "ok" if ok else severity,
            "message": message,
            "evidence": evidence[:220] if evidence else "",
            "fix": "" if ok else fix,
        }
    )


def run(still_path: Path, motion_path: Path) -> dict:
    still = parse(still_path.read_text())
    motion = parse(motion_path.read_text())
    findings: list[dict] = []

    missing_s = [b for b in BLOCKS if b not in still]
    missing_m = [b for b in BLOCKS if b not in motion]
    add(
        findings, "R01", not missing_s and not missing_m, "error",
        f"still missing {missing_s}; motion missing {missing_m}",
        "Add the missing blocks in the nine-block order.", "Both prompts carry all nine blocks.",
    )

    for block in INVARIANTS:
        a = norm(still.get(block, ""))
        b = norm(motion.get(block, ""))
        same = bool(a) and a == b
        first_diff = ""
        if a and b and not same:
            aw, bw = a.split(), b.split()
            for i, (x, y) in enumerate(zip(aw, bw)):
                if x != y:
                    first_diff = f"word {i + 1}: '{x}' vs '{y}'"
                    break
            else:
                first_diff = f"length differs: {len(aw)} vs {len(bw)} words"
        add(
            findings, f"R02-{block}", same, "error", first_diff,
            f"Copy the {block} block byte for byte from the still into the motion prompt (or rebuild both from one brief).",
            f"{block} is identical in both prompts.",
        )

    still_motion = still.get("MOTION", "").lower()
    add(
        findings, "R03", "motion: none" in still_motion, "error", still.get("MOTION", ""),
        "Add: Motion: none. A still photograph. No motion blur, no ghosting, no implied movement.",
        "The still switches motion off.",
    )

    motion_block = motion.get("MOTION", "")
    low = motion_block.lower()
    add(
        findings, "R04", "hero motion: none" in low, "error", motion_block,
        "Add: Hero motion: none. The product and its label remain perfectly still and razor-sharp for the whole clip.",
        "The animation locks the hero.",
    )

    camera = next((ln for ln in motion_block.splitlines() if ln.lower().startswith("camera:")), "")
    cam_low = camera.lower()
    percent = re.search(r"push-in\s*([0-9]+(?:\.[0-9]+)?)\s*%", cam_low)
    if "locked off" in cam_low:
        budget_ok = True
        budget_note = "camera is locked off"
    elif percent:
        budget_ok = float(percent.group(1)) <= 2.0
        budget_note = f"push-in {percent.group(1)}%"
    else:
        budget_ok = False
        budget_note = "no camera line with a locked frame or a push-in percentage"
    add(
        findings, "R05", bool(camera) and budget_ok, "error", camera or budget_note,
        "Use a locked-off camera or a push-in of 2% or less. Name the move and the percentage.",
        "The camera budget is within 2%.",
    )

    clauses = [c for c in re.split(r"[,;.]", cam_low) if c.strip()]
    used = sorted(
        {
            w
            for clause in clauses
            if not prohibited_only(clause)
            for w in CAMERA_BANS
            if re.search(rf"\b{w}\b", clause)
        }
    )
    add(
        findings, "R06", not used, "error", ", ".join(used),
        "Remove the banned move(s) from the camera line. A move named without a negation reads as an instruction.",
        "No banned camera move is requested.",
    )

    hero = still.get("HERO", "")
    has_label = "label reads" in hero.lower() or "label" in hero.lower() and "no label" not in hero.lower()
    if has_label:
        integrity = "planar" in hero.lower() and "vector-sharp" in hero.lower()
    else:
        integrity = "no text" in hero.lower() or "no label" in hero.lower()
    add(
        findings, "R07", integrity, "error", hero,
        "State either the exact label text plus 'planar and vector-sharp', or 'no text, no logo, no label'.",
        "The label state is explicit and protected.",
    )

    guard = motion.get("GUARDRAILS", "").lower()
    add(
        findings, "R08", "exposure" in guard and ("white balance" in guard or "wb" in guard), "error", motion.get("GUARDRAILS", ""),
        "Add exposure and white balance to the Must not change list, and the lock sentence to MOTION.",
        "Exposure and white balance are locked.",
    )

    aspect_ok = "2:3" in still.get("OUTPUT", "") and "9:16" in motion.get("OUTPUT", "")
    add(
        findings, "R09", aspect_ok, "error", f"still: {still.get('OUTPUT', '')[:80]} | motion: {motion.get('OUTPUT', '')[:80]}",
        "Set the still output to 2:3 and the motion output to 9:16 (or update the listing if you intend another frame).",
        "The two outputs carry the intended aspects.",
    )

    duration = re.search(r"(\d+)\s*s\b", motion.get("OUTPUT", ""))
    fps = re.search(r"(\d+)\s*fps", motion.get("OUTPUT", ""))
    duration_ok = bool(duration) and 3 <= int(duration.group(1)) <= 10
    fps_ok = bool(fps) and int(fps.group(1)) in (24, 25, 30)
    add(
        findings, "R10", duration_ok and fps_ok, "error", motion.get("OUTPUT", ""),
        "Use a duration of 3-10 s and 24, 25 or 30 fps.",
        "Duration and frame rate are in range.",
    )

    layers = re.findall(r"^Layer\s+\d+\s*-", motion_block, flags=re.MULTILINE)
    add(
        findings, "R11", 1 <= len(layers) <= 5, "error", f"{len(layers)} layer(s)",
        "Keep one to five motion layers. Four is the working target.",
        f"{len(layers)} motion layer(s) declared.",
    )

    redesign = "do not redesign" in guard
    must_not = "must not appear" in guard
    add(
        findings, "R12", redesign and must_not, "warning", motion.get("GUARDRAILS", ""),
        "Add 'Do not redesign, restyle or improve the product' and a Must not appear list.",
        "The negative guardrails are present.",
    )

    still_optics = norm(still.get("OPTICS", ""))
    motion_optics = norm(motion.get("OPTICS", ""))
    fixed_s = still_optics.split("Frame:")[0]
    fixed_m = motion_optics.split("Frame:")[0]
    add(
        findings, "R13", bool(fixed_s) and fixed_s == fixed_m, "error",
        "fixed optics differ" if fixed_s != fixed_m else "",
        "Copy the Fixed: sentence exactly; only the Frame: sentence may change.",
        "Fixed optics match between the pair.",
    )

    errors = [f for f in findings if f["status"] == "error"]
    warnings = [f for f in findings if f["status"] == "warning"]
    score = max(0, 100 - 10 * len(errors) - 3 * len(warnings))
    return {
        "ok": not errors,
        "score": score,
        "errors": len(errors),
        "warnings": len(warnings),
        "findings": findings,
        "still": str(still_path),
        "motion": str(motion_path),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Check a still/motion prompt pair.")
    parser.add_argument("still", type=Path)
    parser.add_argument("motion", type=Path)
    parser.add_argument("--json", action="store_true", help="print JSON only")
    args = parser.parse_args()

    report = run(args.still, args.motion)
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        verdict = "PASS" if report["ok"] else "FAIL"
        print(f"{verdict}  score {report['score']}/100  errors {report['errors']}  warnings {report['warnings']}\n")
        for f in report["findings"]:
            mark = {"ok": "ok  ", "error": "ERR ", "warning": "WARN"}[f["status"]]
            print(f"[{mark}] {f['rule']:<12} {f['message']}")
            if f["evidence"]:
                print(f"         evidence: {f['evidence']}")
            if f["fix"]:
                print(f"         fix: {f['fix']}")
    return 0 if report["ok"] else 2


if __name__ == "__main__":
    sys.exit(main())
