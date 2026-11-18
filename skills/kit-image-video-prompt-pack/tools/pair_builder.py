#!/usr/bin/env python3
"""Build a matched still/animation prompt pair from one JSON brief.

Usage:
    python3 pair_builder.py brief.json --out ./out
    python3 pair_builder.py --example > brief.json

The five blocks that must not change (SCENE, HERO, PLACEMENT, LIGHT, GUARDRAILS)
are rendered once and copied into both prompts, so the pair cannot paraphrase
itself apart.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

BLOCKS = ["SCENE", "HERO", "PLACEMENT", "OPTICS", "LIGHT", "ATMOSPHERE", "MOTION", "GUARDRAILS", "OUTPUT"]
INVARIANTS = ["SCENE", "HERO", "PLACEMENT", "LIGHT", "GUARDRAILS"]

EXAMPLE = {
    "name": "stoneware-mug",
    "product": "320 ml stoneware mug",
    "dimensions": {"height_cm": 9.2, "width_cm": 8.4, "depth_cm": 8.4},
    "material": "matte oatmeal-glazed stoneware with fine iron speckle",
    "detail": "unglazed foot ring and a straight D-handle on the right",
    "label": "none",
    "scene": "A working pottery studio at 7am, north-facing window with original steel glazing and a lime-washed wall. The bench is pale oak with a worn front edge; a folded linen cloth sits at the right edge. Background falls away at 2.4 m.",
    "surface": "pale oak bench",
    "placement": {
        "height_pct": 58,
        "horizontal": "centred on the vertical third",
        "angle": "parallel to the lens",
        "front_cm": 6,
        "behind": "linen cloth",
        "behind_cm": 40,
        "shadow": "soft, camera-right, 3 cm",
        "motion_height_pct": 52,
    },
    "lens": "85 mm prime",
    "distance_m": 0.9,
    "aperture": "T2.0",
    "shutter": "180 deg",
    "iso": "400",
    "wb": "5200",
    "filtration": "Black Pro-Mist 1/8",
    "sharp": "the handle and the near bench edge",
    "falloff": "the back wall",
    "light": "Key: north window from camera-left, soft, 5200 K, flagged so the front face is evenly lit with a gentle falloff to camera-right. Fill: white card from camera-right at low level. Rim: none. Practicals: a warm 2700 K bulb in the hallway behind, out of focus. Falloff: the back wall goes one stop darker.",
    "atmosphere": "Thin steam from the mug, source at the rim, density low. Nine dust motes in the window shaft. No fog on the lens.",
    "motion_layers": [
        {"name": "steam", "amplitude": "3-6 cm", "window": "0.0-7.0 s", "direction": "up and camera-left", "rule": "must not cross the front face or the handle"},
        {"name": "dust", "amplitude": "1-2 px", "window": "0.0-7.0 s", "direction": "slow drift camera-right", "rule": "six to ten motes; none lands on the product"},
        {"name": "shadow edge", "amplitude": "4 cm", "window": "1.5-5.5 s", "direction": "across the bench, camera-right", "rule": "the product's lit side does not change"},
        {"name": "droplet", "amplitude": "8 mm", "window": "2.0-2.8 s", "direction": "down the base, once", "rule": "must not touch the foot ring"},
    ],
    "camera": {"type": "push-in", "percent": 2},
    "duration_s": 7,
    "fps": 24,
    "still_aspect": "2:3",
    "motion_aspect": "9:16",
    "still_px": "2048x3072",
    "motion_px": "1080x1920",
    "extra_guardrails": [],
}


def sentence(text: str) -> str:
    text = " ".join(str(text).split())
    return text if text.endswith((".", "!", "?")) else text + "."


def require(brief: dict, key: str) -> object:
    if key not in brief or brief[key] in (None, "", [], {}):
        raise SystemExit(f"brief is missing required field: {key}")
    return brief[key]


def label_clause(label: str) -> str:
    label = (label or "").strip()
    if label.lower() in ("", "none", "no", "unlabelled", "unlabeled"):
        return "No text, no logo, no label and no embossed wordmark anywhere on the product."
    return (
        f'The label reads exactly "{label}"; label text is planar and vector-sharp, '
        "with no invented characters, no curvature and no perspective error."
    )


def capitalise(text: str) -> str:
    text = text.strip()
    return text[:1].upper() + text[1:] if text else text


def hero_block(b: dict) -> str:
    dims = b.get("dimensions") or {}
    size = ""
    if dims:
        parts = [f'{dims[k]} cm {axis}' for k, axis in (("height_cm", "tall"), ("width_cm", "wide"), ("depth_cm", "deep")) if dims.get(k)]
        if parts:
            size = " measuring " + ", ".join(parts)
    material = sentence(b.get("material", "the stated material"))
    material = material[:1].lower() + material[1:] if material else material
    detail = capitalise(sentence(b.get("detail", "the stated construction"))) if b.get("detail") else ""
    text = (
        f"A {require(b, 'product')}{size}, {material}"
        + (f" {detail}" if detail else "")
        + f" {label_clause(b.get('label', 'none'))} "
        "Geometry is fixed; no redesign, no added parts, no proportion change."
    )
    return "[HERO]\n" + " ".join(text.split())


def scene_block(b: dict) -> str:
    return "[SCENE]\n" + sentence(require(b, "scene"))


def placement_block(b: dict) -> str:
    p = b.get("placement") or {}
    front = p.get("front_cm", 6)
    behind = p.get("behind", "the background")
    behind_cm = p.get("behind_cm", 40)
    text = (
        f"Base contact at {p.get('height_pct', 58)}% frame height from the top, {p.get('horizontal', 'centred')}, "
        f"front face {p.get('angle', 'parallel to the lens')}. "
        f"{front} cm of {b.get('surface', 'the surface')} in front; {behind} at {behind_cm} cm behind. "
        f"Contact shadow: {p.get('shadow', 'soft, camera-right, 3 cm')}. "
        f"In {b.get('motion_aspect', '9:16')} the base contact moves to {p.get('motion_height_pct', 52)}% frame height, "
        "keeping the same horizontal position, the same front-face angle and the same relative distances."
    )
    return "[PLACEMENT]\n" + " ".join(text.split())


def optics_fixed(b: dict) -> str:
    sharp = b.get("sharp", "the front face")
    falloff = b.get("falloff", "the background")
    verb = "are" if (" and " in str(sharp) or "," in str(sharp)) else "is"
    return (
        f"Fixed: {b.get('lens', '85 mm prime')}, {b.get('distance_m', 0.9)} m from the front face, "
        f"{b.get('aperture', 'T2.0')}, shutter {b.get('shutter', '180 deg')} look, "
        f"ISO look {b.get('iso', '400')}, white balance {b.get('wb', '5200')} K, "
        f"{b.get('filtration', 'no filtration')}. Focus on the front face; "
        f"{sharp} {verb} sharp, {falloff} falls away."
    )


def optics_still(b: dict) -> str:
    return (
        "[OPTICS]\n"
        + optics_fixed(b)
        + f" Frame: {b.get('still_aspect', '2:3')}, {b.get('still_px', '2048x3072')}, "
        f"product occupies {b.get('placement', {}).get('height_pct', 58)}% of frame height, "
        "8% headroom, negative space on the open side."
    )


def optics_motion(b: dict) -> str:
    return (
        "[OPTICS]\n"
        + optics_fixed(b)
        + f" Frame: {b.get('motion_aspect', '9:16')}, {b.get('motion_px', '1080x1920')}, "
        f"product occupies {b.get('placement', {}).get('motion_height_pct', 52)}% of frame height, "
        "same base contact point and same front-face angle."
    )


def light_block(b: dict) -> str:
    return "[LIGHT]\n" + sentence(require(b, "light"))


def atmosphere_block(b: dict) -> str:
    return "[ATMOSPHERE]\n" + sentence(require(b, "atmosphere"))


def still_motion_block(b: dict) -> str:
    return "[MOTION]\nMotion: none. A still photograph. No motion blur, no ghosting, no implied movement, no double edges."


def camera_line(camera: dict) -> str:
    kind = (camera or {}).get("type", "locked").lower()
    if kind in ("locked", "locked-off", "static"):
        return "Camera: locked off, no angle change, no pan, no orbit, no tilt, no handheld, no zoom, no rack focus off the front face."
    percent = float(camera.get("percent", 2))
    if percent > 2:
        raise SystemExit("camera push-in must be 2% or less; the product would change size")
    return (
        f"Camera: push-in {percent:g}%, no angle change, no pan, no orbit, no tilt, no handheld, no zoom, "
        "no rack focus off the front face."
    )


def motion_block(b: dict, layers: list[dict]) -> str:
    if len(layers) > 5:
        raise SystemExit(f"motion layer limit is 5; brief has {len(layers)}")
    lines = [
        "[MOTION]",
        "Hero motion: none. The product and its label remain perfectly still and razor-sharp for the whole clip.",
        camera_line(b.get("camera") or {}),
    ]
    for i, layer in enumerate(layers, 1):
        lines.append(
            f"Layer {i} - {layer.get('name', 'motion')}: amplitude {layer.get('amplitude', 'small')}, "
            f"window {layer.get('window', '0.0 s to end')}, direction {layer.get('direction', 'as described')}, "
            f"{sentence(layer.get('rule', 'must not touch the product'))}"
        )
    lines.append("Exposure and white balance are locked for the whole clip. No auto-iris, no flicker, no colour drift.")
    return "\n".join(lines)


def guardrails_block(b: dict) -> str:
    base = (
        "Must not change: product geometry, proportions, surface finish, label text and placement, "
        "base contact point, front-face angle, lit side, exposure, white balance.\n"
        "Must not appear: extra products, hands, people, text, logos, watermarks, UI, frames, borders, duplicate shadows.\n"
        "Physics: one gravity direction, one airflow direction, correct contact shadow, no floating parts, "
        "no fused or extra digits if a hand is present.\n"
        'Do not redesign, restyle or "improve" the product.'
    )
    extra = [sentence(x) for x in b.get("extra_guardrails", []) if str(x).strip()]
    return "[GUARDRAILS]\n" + base + (("\n" + "\n".join(extra)) if extra else "")


def output_still(b: dict) -> str:
    return (
        "[OUTPUT]\n"
        f"Still: {b.get('still_aspect', '2:3')}, {b.get('still_px', '2048x3072')}, sRGB, PNG, no border."
    )


def output_motion(b: dict) -> str:
    duration = int(b.get("duration_s", 7))
    if not 3 <= duration <= 10:
        raise SystemExit("duration must be between 3 and 10 seconds")
    fps = int(b.get("fps", 24))
    if fps not in (24, 25, 30):
        raise SystemExit("fps must be 24, 25 or 30")
    return (
        "[OUTPUT]\n"
        f"Motion: {b.get('motion_aspect', '9:16')}, {b.get('motion_px', '1080x1920')}, "
        f"{duration} s, {fps} fps, H.264 high bitrate, no audio unless supplied."
    )


def build(b: dict) -> tuple[str, str, list[dict]]:
    layers = b.get("motion_layers") or []
    if not layers:
        raise SystemExit("brief needs at least one motion layer for the animation")
    for key in ("product", "scene", "light", "atmosphere"):
        require(b, key)
    invariant = {
        "SCENE": scene_block(b),
        "HERO": hero_block(b),
        "PLACEMENT": placement_block(b),
        "LIGHT": light_block(b),
        "GUARDRAILS": guardrails_block(b),
    }
    still = "\n\n".join(
        [
            invariant["SCENE"],
            invariant["HERO"],
            invariant["PLACEMENT"],
            optics_still(b),
            invariant["LIGHT"],
            atmosphere_block(b),
            still_motion_block(b),
            invariant["GUARDRAILS"],
            output_still(b),
        ]
    )
    motion = "\n\n".join(
        [
            invariant["SCENE"],
            invariant["HERO"],
            invariant["PLACEMENT"],
            optics_motion(b),
            invariant["LIGHT"],
            atmosphere_block(b),
            motion_block(b, layers),
            invariant["GUARDRAILS"],
            output_motion(b),
        ]
    )
    return still, motion, layers


def motion_map_markdown(b: dict, layers: list[dict]) -> str:
    rows = [
        "| Window | Layer | Amplitude | Direction | Prohibition |",
        "|---|---|---|---|---|",
    ]
    for layer in layers:
        rows.append(
            f"| {layer.get('window', '0.0 s to end')} | {layer.get('name', 'motion')} | "
            f"{layer.get('amplitude', 'small')} | {layer.get('direction', 'as described')} | "
            f"{layer.get('rule', 'must not touch the product')} |"
        )
    camera = b.get("camera") or {}
    kind = camera.get("type", "locked")
    cam = "locked off" if kind in ("locked", "locked-off", "static") else f"push-in {camera.get('percent', 2):g}%"
    return (
        f"# Motion map: {b.get('name', b.get('product', 'scene'))}\n\n"
        f"Duration {b.get('duration_s', 7)} s at {b.get('fps', 24)} fps. Hero motion: none. "
        f"Camera: {cam}.\n\n" + "\n".join(rows) + "\n\n"
        "## Review\n\n"
        f"- Layers: {len(layers)} of 5.\n"
        "- Light layers: count the light-family rows; keep at most one.\n"
        "- No layer crosses the front face or the label.\n"
        "- Camera move is 2% or less.\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a hero-locked still and motion prompt pair.")
    parser.add_argument("brief", nargs="?", help="path to a JSON brief")
    parser.add_argument("--out", default="./pair", help="output folder (default: ./pair)")
    parser.add_argument("--example", action="store_true", help="print an example brief and exit")
    args = parser.parse_args()

    if args.example:
        print(json.dumps(EXAMPLE, indent=2, ensure_ascii=False))
        return 0
    if not args.brief:
        parser.error("a brief path is required (or use --example)")

    brief = json.loads(Path(args.brief).read_text())
    still, motion, layers = build(brief)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "still.txt").write_text(still + "\n")
    (out / "motion.txt").write_text(motion + "\n")
    (out / "motion-map.md").write_text(motion_map_markdown(brief, layers))
    (out / "brief.resolved.json").write_text(json.dumps(brief, indent=2, ensure_ascii=False) + "\n")
    print(
        json.dumps(
            {
                "out": str(out),
                "files": ["still.txt", "motion.txt", "motion-map.md", "brief.resolved.json"],
                "layers": len(layers),
                "next": f"python3 tools/check_pair.py {out / 'still.txt'} {out / 'motion.txt'}",
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
