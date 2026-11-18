#!/usr/bin/env python3
"""Read a folder of brand assets and write brand-spec.json.

Standard library only. Python 3.9 or newer. No image library is used: image
dimensions come from PNG, JPEG and SVG headers read with struct and bytes.

    python3 brand_audit.py <folder> --out brand-spec.json
    python3 brand_audit.py <folder> --out brand-spec.json --json

Every value in the spec carries three keys:

    value     the value
    source    "read" when a declaration states it, "inferred" when the tool
              worked it out
    evidence  "file:line" or "file"

Exit codes: 0 on success, 2 when the folder cannot be read or written.
"""

import argparse
import json
import os
import re
import struct
import sys
import zlib
from pathlib import Path
from typing import Dict, List, Optional, Tuple

SCHEMA_VERSION = "1.0"
TOOL_VERSION = "1.0"

CSS_EXT = {".css", ".scss", ".sass", ".less", ".html", ".htm"}
SVG_EXT = {".svg"}
JSON_EXT = {".json"}
JS_EXT = {".js", ".cjs", ".mjs", ".ts", ".jsx", ".tsx"}
TEXT_EXT = {".md", ".markdown", ".txt"}
FONT_EXT = {".woff2", ".woff", ".ttf", ".otf", ".eot"}
IMAGE_EXT = {".png", ".jpg", ".jpeg", ".svg", ".gif", ".webp", ".avif"}

SKIP_DIRS = {
    "node_modules", ".git", ".svn", ".hg", "dist", "build", "out", ".cache",
    "__pycache__", ".next", ".nuxt", "vendor", "coverage",
}

MAX_TEXT_BYTES = 512 * 1024
MAX_SAMPLE_PIXELS = 2_000_000

# The spec is written into the folder it describes, so it is never read back as
# an asset. Without this, a second run would audit the first run's output.
EXCLUDED_NAMES = {"brand-spec.json"}

HEX_RE = re.compile(r"#([0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{3,4})\b")
RGB_RE = re.compile(
    r"rgba?\(\s*(\d{1,3})\s*[,\s]\s*(\d{1,3})\s*[,\s]\s*(\d{1,3})", re.IGNORECASE
)
TOKEN_RE = re.compile(r"(--[A-Za-z0-9_-]+)\s*:")
FONT_FAMILY_RE = re.compile(r"font-family\s*:\s*([^;{}]+)", re.IGNORECASE)
FONT_SIZE_RE = re.compile(
    r"font-size\s*:\s*([0-9]*\.?[0-9]+)\s*(px|rem|em|pt)", re.IGNORECASE
)
FONT_WEIGHT_RE = re.compile(
    r"font-weight\s*:\s*([0-9]{3}|normal|bold|bolder|lighter)", re.IGNORECASE
)
SIZE_TOKEN_RE = re.compile(r"^\s*([0-9]*\.?[0-9]+)\s*(px|rem|em|pt)\s*;?\s*$", re.IGNORECASE)
TYPE_TOKEN_RE = re.compile(r"(font|type|face|family|display|body|heading)", re.IGNORECASE)
GRADIENT_RE = re.compile(r"(linear|radial|conic)-gradient", re.IGNORECASE)
TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)
BRAND_LINE_RE = re.compile(
    r"^\s*(?:[-*]\s*)?(?:\*\*)?(brand|brand name|company|studio)(?:\*\*)?\s*[:\-]\s*(.+)$",
    re.IGNORECASE | re.MULTILINE,
)
TAGLINE_LINE_RE = re.compile(
    r"^\s*(?:[-*]\s*)?(?:\*\*)?(tagline|strapline)(?:\*\*)?\s*[:\-]\s*(.+)$",
    re.IGNORECASE | re.MULTILINE,
)
JS_COLOUR_RE = re.compile(
    r"['\"]?([A-Za-z0-9_'-]+)['\"]?\s*:\s*['\"]?"
    r"(#[0-9a-fA-F]{3,8}|rgba?\([^)]*\))['\"]?"
)
JS_FONT_BLOCK_RE = re.compile(r"fontFamily\s*:\s*\{([^}]*)\}", re.DOTALL)
JS_FONT_ENTRY_RE = re.compile(r"['\"]?([A-Za-z0-9_-]+)['\"]?\s*:\s*\[([^\]]*)\]")

ROLE_WORDS = {
    "ground": {"ground", "background", "bg", "paper", "canvas", "base", "page"},
    "ink": {"ink", "text", "body-text", "bodytext", "fg", "foreground", "copy"},
    "accent": {"accent", "highlight", "brand-accent", "spot", "signal"},
    "surface": {"surface", "card", "panel", "layer", "raised"},
}

GENERIC_FAMILIES = {
    "serif", "sans-serif", "monospace", "cursive", "fantasy", "system-ui",
    "ui-serif", "ui-sans-serif", "ui-monospace", "inherit", "initial",
}

# The questions the audit method requires. The tool raises the subset that its
# own gaps make unavoidable; the full set is in references/owner-questions.md.
QUESTIONS = [
    ("QA01", "What is the registered brand name, spelled exactly as it must appear?",
     "The brand name could not be read from a declaration, so a folder name was used."),
    ("QA02", "Which colour is ground, which is ink, and which is accent?",
     "At least one colour role was assigned by measurement, not by a named token."),
    ("QA03", "Which typeface is the brand face, and is the file licensed for this use?",
     "No font family is declared anywhere in the folder."),
    ("QA04", "Is one accent enough, and how many times may it appear on a page?",
     "The accent was chosen by saturation, so its role and its budget are guesses."),
    ("QA05", "What clear space and minimum size does the logo require?",
     "No guideline states clear space, so a rule of thumb was derived from the artwork."),
    ("QA06", "Which logo variants exist, and which one goes on a dark ground?",
     "Fewer than two logo variants were found."),
    ("QA07", "What may appear in a photograph, and what must never appear in one?",
     "No imagery was found, so no imagery rule could be read."),
    ("QA08", "What are the exact type sizes and weights, and the smallest permitted size?",
     "Fewer than three type sizes were declared, so no scale could be read."),
    ("QA09", "What does the brand sound like, and what does it never say?",
     "No guideline or brand book was found."),
    ("QA10", "Who owns the logo and the typefaces, and what may be reproduced?",
     "Ownership is never stated in an asset folder."),
    ("QA11", "Who approves a new template, and which folder holds the master assets?",
     "An asset folder is not a source of truth on its own."),
    ("QA12", "What contrast pair carries body text, and may the accent carry text at all?",
     "No pair of read colours reached 4.5:1, so a safe body pair was not established."),
]
QUESTION_TEXT = {q[0]: q[1] for q in QUESTIONS}
QUESTION_WHY = {q[0]: q[2] for q in QUESTIONS}


# ---------------------------------------------------------------- primitives


def rel_posix(path: Path, root: Path) -> str:
    """A stable relative path with forward slashes."""
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def val(value, source: str, evidence: str, **extra) -> dict:
    """One spec value. Every value carries the same three keys."""
    out = {"value": value, "source": source, "evidence": evidence}
    out.update(extra)
    return out


def expand_hex(raw: str) -> Optional[str]:
    """Normalise a hex colour to #rrggbb. Alpha is dropped."""
    h = raw.lstrip("#")
    if len(h) in (3, 4):
        h = "".join(ch * 2 for ch in h[:3])
    elif len(h) in (6, 8):
        h = h[:6]
    else:
        return None
    if not re.fullmatch(r"[0-9a-fA-F]{6}", h):
        return None
    return "#" + h.lower()


def rgb_to_hex(r: int, g: int, b: int) -> Optional[str]:
    if not all(0 <= c <= 255 for c in (r, g, b)):
        return None
    return "#{:02x}{:02x}{:02x}".format(r, g, b)


def hex_to_rgb(value: str) -> Tuple[int, int, int]:
    h = value.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def luminance(value: str) -> float:
    r, g, b = hex_to_rgb(value)
    channels = []
    for c in (r, g, b):
        s = c / 255.0
        channels.append(s / 12.92 if s <= 0.04045 else ((s + 0.055) / 1.055) ** 2.4)
    return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2]


def contrast(a: str, b: str) -> float:
    la, lb = luminance(a), luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return round((hi + 0.05) / (lo + 0.05), 2)


def saturation(value: str) -> float:
    r, g, b = (c / 255.0 for c in hex_to_rgb(value))
    hi, lo = max(r, g, b), min(r, g, b)
    if hi == 0:
        return 0.0
    return (hi - lo) / hi


def read_text(path: Path) -> Optional[str]:
    try:
        if path.stat().st_size > MAX_TEXT_BYTES:
            return None
        return path.read_bytes().decode("utf-8", errors="replace")
    except OSError:
        return None


def strip_block_comments(lines: List[str]) -> List[str]:
    """Remove /* ... */ spans while keeping line numbers intact."""
    out = []
    inside = False
    for line in lines:
        buf = []
        i = 0
        while i < len(line):
            if inside:
                end = line.find("*/", i)
                if end == -1:
                    i = len(line)
                else:
                    inside = False
                    i = end + 2
                continue
            start = line.find("/*", i)
            if start == -1:
                buf.append(line[i:])
                i = len(line)
            else:
                buf.append(line[i:start])
                inside = True
                i = start + 2
        out.append("".join(buf))
    return out


def token_role(token: Optional[str]) -> Optional[str]:
    """Map a declared token name to a palette role, if the name states one."""
    if not token:
        return None
    last = re.split(r"[.:\s/_-]+", token.strip().lower())[-1]
    last = last.replace("_", "-")
    for role, words in ROLE_WORDS.items():
        if last in words:
            return role
    return None


def clean_family(raw: str) -> Optional[str]:
    name = raw.strip().strip('"\'').strip()
    if not name:
        return None
    if name.lower() in GENERIC_FAMILIES:
        return None
    if re.fullmatch(r"[0-9.\s]+", name):
        return None
    if re.fullmatch(r"[0-9.]+\s*(px|rem|em|pt|%)", name, re.IGNORECASE):
        return None
    if not re.search(r"[A-Za-z]{2,}", name):
        return None
    if name.lower().startswith(("var(", "url(", "calc(", "env(")):
        return None
    if len(name) > 60:
        return None
    return name


def split_families(raw: str) -> List[str]:
    parts = [p for p in re.split(r",(?![^(]*\))", raw)]
    out = []
    for part in parts:
        name = clean_family(part)
        if name:
            out.append(name)
    return out


def size_to_px(number: str, unit: str) -> Tuple[float, bool]:
    """Return (px, converted). A converted size is not a read px value."""
    n = float(number)
    unit = unit.lower()
    if unit == "px":
        return round(n, 2), False
    if unit in ("rem", "em"):
        return round(n * 16.0, 2), True
    if unit == "pt":
        return round(n * 4.0 / 3.0, 2), True
    return round(n, 2), True


# ---------------------------------------------------------------- collection


class Collector:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.colours: List[dict] = []
        self.families: List[dict] = []
        self.sizes: List[dict] = []
        self.weights: List[dict] = []
        self.font_files: List[dict] = []
        self.images: List[dict] = []
        self.logos: List[dict] = []
        self.notices: List[dict] = []
        self.name_candidates: List[dict] = []
        self.tagline_candidates: List[dict] = []
        self.has_gradient = False
        self.files: List[str] = []
        self.by_extension: Dict[str, int] = {}
        self.unreadable: List[str] = []

    def add_colour(self, hex_value: Optional[str], evidence: str,
                   token: Optional[str] = None, context: str = "") -> None:
        if not hex_value:
            return
        self.colours.append(
            {"hex": hex_value, "evidence": evidence, "token": token, "context": context}
        )

    def add_families(self, raw: str, evidence: str, token: Optional[str]) -> None:
        names = split_families(raw)
        for index, name in enumerate(names):
            self.families.append(
                {"family": name, "evidence": evidence, "token": token, "rank": index}
            )


# ------------------------------------------------------------------ scanners


def scan_css(collector: Collector, rel: str, text: str) -> None:
    lines = strip_block_comments(text.splitlines())
    token: Optional[str] = None
    for number, raw_line in enumerate(lines, start=1):
        line = raw_line
        match = TOKEN_RE.search(line)
        if match:
            token = match.group(1)
            declared = line[match.end():].strip().rstrip(";").strip()
            if (
                TYPE_TOKEN_RE.search(token)
                and declared
                and not HEX_RE.search(declared)
                and not SIZE_TOKEN_RE.match(declared)
                and re.search(r"[A-Za-z]{2,}", declared)
            ):
                collector.add_families(declared, evidence, token)
            size_match = SIZE_TOKEN_RE.match(declared)
            if size_match and re.search(r"size|text|type|scale", token, re.IGNORECASE):
                px, converted = size_to_px(size_match.group(1), size_match.group(2))
                collector.sizes.append(
                    {
                        "px": px,
                        "raw": "{}{}".format(size_match.group(1), size_match.group(2)),
                        "converted": converted,
                        "evidence": evidence,
                    }
                )
        elif "}" in line:
            token = None
        if GRADIENT_RE.search(line):
            collector.has_gradient = True
        evidence = "{}:{}".format(rel, number)
        for match in HEX_RE.finditer(line):
            collector.add_colour(expand_hex(match.group(0)), evidence, token, "css")
        for match in RGB_RE.finditer(line):
            collector.add_colour(
                rgb_to_hex(int(match.group(1)), int(match.group(2)), int(match.group(3))),
                evidence,
                token,
                "css",
            )
        for match in FONT_FAMILY_RE.finditer(line):
            collector.add_families(match.group(1), evidence, token)
        for match in FONT_SIZE_RE.finditer(line):
            px, converted = size_to_px(match.group(1), match.group(2))
            collector.sizes.append(
                {
                    "px": px,
                    "raw": "{}{}".format(match.group(1), match.group(2)),
                    "converted": converted,
                    "evidence": evidence,
                }
            )
        for match in FONT_WEIGHT_RE.finditer(line):
            raw = match.group(1).lower()
            weight = {"normal": 400, "bold": 700, "bolder": 700, "lighter": 300}.get(
                raw, None
            )
            if weight is None:
                weight = int(raw)
            collector.weights.append({"weight": weight, "evidence": evidence})


SVG_ATTR_RE = re.compile(
    r"\b(fill|stroke|stop-color|color|flood-color)\s*=\s*[\"']([^\"']+)[\"']",
    re.IGNORECASE,
)
SVG_STYLE_RE = re.compile(
    r"\b(fill|stroke|stop-color|color)\s*:\s*(#[0-9a-fA-F]{3,8}|rgba?\([^)]*\))",
    re.IGNORECASE,
)


def scan_svg(collector: Collector, rel: str, text: str, allow_name: bool = False) -> None:
    for number, line in enumerate(text.splitlines(), start=1):
        evidence = "{}:{}".format(rel, number)
        for match in SVG_ATTR_RE.finditer(line):
            value = match.group(2)
            if value.lower() in ("none", "currentcolor", "inherit", "transparent"):
                continue
            collector.add_colour(expand_hex(value), evidence, None, "svg")
        for match in SVG_STYLE_RE.finditer(line):
            value = match.group(2)
            if value.startswith("#"):
                collector.add_colour(expand_hex(value), evidence, None, "svg")
            else:
                hex_value = None
                rgb_match = RGB_RE.search(value)
                if rgb_match:
                    hex_value = rgb_to_hex(
                        int(rgb_match.group(1)),
                        int(rgb_match.group(2)),
                        int(rgb_match.group(3)),
                    )
                collector.add_colour(hex_value, evidence, None, "svg")
    title = TITLE_RE.search(text)
    if allow_name and title:
        name = " ".join(title.group(1).split())
        if name:
            collector.name_candidates.append(
                {"name": name, "evidence": "{} (title)".format(rel), "rank": 2}
            )


COLOUR_KEY_RE = re.compile(
    r"(colou?r|colour|bg|background|ink|accent|surface|ground|text|fg|foreground|"
    r"border|neutral|brand)",
    re.IGNORECASE,
)
FONT_KEY_RE = re.compile(r"font|typeface|type-family", re.IGNORECASE)


def walk_json(collector: Collector, rel: str, node, path: str) -> None:
    if isinstance(node, dict):
        for key in node:
            walk_json(collector, rel, node[key], "{}.{}".format(path, key) if path else key)
        return
    if isinstance(node, list):
        for index, item in enumerate(node):
            walk_json(collector, rel, item, "{}[{}]".format(path, index))
        return
    if isinstance(node, str):
        evidence = "{} ({})".format(rel, path)
        if HEX_RE.fullmatch(node.strip()):
            collector.add_colour(expand_hex(node.strip()), evidence, path, "json")
            return
        rgb_match = RGB_RE.fullmatch(node.strip())
        if rgb_match:
            collector.add_colour(
                rgb_to_hex(
                    int(rgb_match.group(1)),
                    int(rgb_match.group(2)),
                    int(rgb_match.group(3)),
                ),
                evidence,
                path,
                "json",
            )
            return
        leaf = re.split(r"[.\[]", path)[-1].rstrip("]")
        if COLOUR_KEY_RE.search(leaf) and HEX_RE.search(node):
            collector.add_colour(expand_hex(HEX_RE.search(node).group(0)), evidence, path, "json")
        elif FONT_KEY_RE.search(path) and re.search(r"[A-Za-z]", node):
            collector.add_families(node, evidence, path)


def scan_json(collector: Collector, rel: str, text: str) -> None:
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        collector.notices.append(
            val("{model} could not be parsed".format(model=rel), "read", rel)
        )
        return
    walk_json(collector, rel, data, "")
    if isinstance(data, dict):
        for key in ("name", "brand", "brandName", "brand_name"):
            candidate = data.get(key)
            if isinstance(candidate, str) and candidate.strip():
                collector.name_candidates.append(
                    {"name": candidate.strip(), "evidence": "{} ({})".format(rel, key), "rank": 1}
                )
                break
        for key in ("tagline", "strapline", "slogan"):
            candidate = data.get(key)
            if isinstance(candidate, str) and candidate.strip():
                collector.tagline_candidates.append(
                    {"name": candidate.strip(), "evidence": "{} ({})".format(rel, key)}
                )
                break


def scan_js(collector: Collector, rel: str, text: str) -> None:
    lowered = rel.lower()
    if "tailwind" not in lowered and "theme" not in lowered and "token" not in lowered:
        return
    for number, line in enumerate(text.splitlines(), start=1):
        evidence = "{}:{}".format(rel, number)
        for match in JS_COLOUR_RE.finditer(line):
            key, raw = match.group(1), match.group(2)
            if raw.startswith("#"):
                collector.add_colour(expand_hex(raw), evidence, key, "js")
            else:
                rgb_match = RGB_RE.search(raw)
                if rgb_match:
                    collector.add_colour(
                        rgb_to_hex(
                            int(rgb_match.group(1)),
                            int(rgb_match.group(2)),
                            int(rgb_match.group(3)),
                        ),
                        evidence,
                        key,
                        "js",
                    )
    for block in JS_FONT_BLOCK_RE.finditer(text):
        body = block.group(1)
        base_line = text[: block.start()].count("\n") + 1
        for entry in JS_FONT_ENTRY_RE.finditer(body):
            key, raw_list = entry.group(1), entry.group(2)
            first = re.match(r"\s*['\"]([^'\"]+)['\"]", raw_list)
            if first:
                collector.families.append(
                    {
                        "family": first.group(1),
                        "evidence": "{}:{}".format(rel, base_line),
                        "token": key,
                        "rank": 0,
                    }
                )


def scan_text(collector: Collector, rel: str, text: str) -> None:
    for match in BRAND_LINE_RE.finditer(text):
        name = re.sub(r"\s+", " ", match.group(2)).strip().strip("*_` ")
        if name:
            line = text[: match.start()].count("\n") + 1
            collector.name_candidates.append(
                {"name": name, "evidence": "{}:{}".format(rel, line), "rank": 0}
            )
    for match in TAGLINE_LINE_RE.finditer(text):
        tagline = re.sub(r"\s+", " ", match.group(2)).strip().strip("*_` ")
        if tagline:
            line = text[: match.start()].count("\n") + 1
            collector.tagline_candidates.append(
                {"name": tagline, "evidence": "{}:{}".format(rel, line)}
            )


# ------------------------------------------------------------ image headers


def png_size(data: bytes) -> Tuple[Optional[int], Optional[int]]:
    if data[:8] != b"\x89PNG\r\n\x1a\n" or len(data) < 24:
        return None, None
    if data[12:16] != b"IHDR":
        return None, None
    width, height = struct.unpack(">II", data[16:24])
    return width, height


JPEG_SOF = {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}


def jpeg_size(data: bytes) -> Tuple[Optional[int], Optional[int]]:
    if data[:2] != b"\xff\xd8":
        return None, None
    pos = 2
    limit = len(data)
    while pos + 3 < limit:
        if data[pos] != 0xFF:
            pos += 1
            continue
        marker = data[pos + 1]
        if marker in (0x00, 0x01, 0xFF) or 0xD0 <= marker <= 0xD9:
            pos += 2
            continue
        if pos + 4 > limit:
            return None, None
        length = struct.unpack(">H", data[pos + 2:pos + 4])[0]
        if length < 2:
            return None, None
        if marker in JPEG_SOF and pos + 9 <= limit:
            height, width = struct.unpack(">HH", data[pos + 5:pos + 9])
            return width, height
        pos += 2 + length
    return None, None


SVG_OPEN_RE = re.compile(r"<svg\b[^>]*>", re.IGNORECASE | re.DOTALL)
SVG_DIM_RE = re.compile(r"\b(width|height)\s*=\s*[\"']([0-9.]+)\s*(px)?[\"']", re.IGNORECASE)
SVG_VIEWBOX_RE = re.compile(
    r"\bviewBox\s*=\s*[\"']([-0-9.\s,]+)[\"']", re.IGNORECASE
)


def svg_size(text: str) -> Tuple[Optional[int], Optional[int], str]:
    open_tag = SVG_OPEN_RE.search(text)
    tag = open_tag.group(0) if open_tag else text[:600]
    dims = {
        match.group(1).lower(): float(match.group(2))
        for match in SVG_DIM_RE.finditer(tag)
    }
    viewbox = SVG_VIEWBOX_RE.search(tag)
    if viewbox:
        numbers = [n for n in re.split(r"[\s,]+", viewbox.group(1).strip()) if n]
        if len(numbers) == 4:
            vb_w = float(numbers[2])
            vb_h = float(numbers[3])
            if "width" not in dims or "height" not in dims:
                return int(round(vb_w)), int(round(vb_h)), "viewBox"
    if "width" in dims and "height" in dims:
        return int(round(dims["width"])), int(round(dims["height"])), "width/height"
    return None, None, "no size"


def png_sample_colours(path: Path) -> Tuple[List[dict], str]:
    """Sample a PNG's own pixels. Returns (clusters, note)."""
    try:
        data = path.read_bytes()
    except OSError:
        return [], "unreadable"
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        return [], "not a PNG"
    pos = 8
    idat = bytearray()
    width = height = None
    depth = colour_type = interlace = None
    while pos + 8 <= len(data):

        length = struct.unpack(">I", data[pos:pos + 4])[0]
        chunk_type = data[pos + 4:pos + 8]
        chunk = data[pos + 8:pos + 8 + length]
        if chunk_type == b"IHDR" and len(chunk) >= 13:
            width, height, depth, colour_type, _, _, interlace = struct.unpack(
                ">IIBBBBB", chunk[:13]
            )
        elif chunk_type == b"IDAT":
            idat.extend(chunk)
        elif chunk_type == b"IEND":
            break
        pos += 12 + length
    if width is None or height is None:
        return [], "no header"
    if depth != 8 or interlace != 0 or colour_type not in (0, 2, 4, 6):
        return [], "unsupported PNG variant"
    if width * height > MAX_SAMPLE_PIXELS:
        return [], "image too large to sample without a decoder"
    channels = {0: 1, 2: 3, 4: 2, 6: 4}[colour_type]
    try:
        raw = zlib.decompress(bytes(idat))
    except zlib.error:
        return [], "compressed data unreadable"
    stride = width * channels
    previous = bytearray(stride)
    counts: Dict[Tuple[int, int, int], int] = {}
    total = 0
    offset = 0
    step_pixels = 7
    for _row in range(height):
        if offset >= len(raw):
            break
        filter_type = raw[offset]
        offset += 1
        line = bytearray(raw[offset:offset + stride])
        if len(line) < stride:
            break
        offset += stride
        if filter_type == 1:
            for i in range(channels, stride):
                line[i] = (line[i] + line[i - channels]) & 0xFF
        elif filter_type == 2:
            for i in range(stride):
                line[i] = (line[i] + previous[i]) & 0xFF
        elif filter_type == 3:
            for i in range(stride):
                left = line[i - channels] if i >= channels else 0
                line[i] = (line[i] + ((left + previous[i]) >> 1)) & 0xFF
        elif filter_type == 4:
            for i in range(stride):
                left = line[i - channels] if i >= channels else 0
                up = previous[i]
                up_left = previous[i - channels] if i >= channels else 0
                p = left + up - up_left
                pa, pb, pc = abs(p - left), abs(p - up), abs(p - up_left)
                if pa <= pb and pa <= pc:
                    predictor = left
                elif pb <= pc:
                    predictor = up
                else:
                    predictor = up_left
                line[i] = (line[i] + predictor) & 0xFF
        previous = line
        for px in range(0, width, step_pixels):
            base = px * channels
            if colour_type in (0, 4):
                r = g = b = line[base]
            else:
                r, g, b = line[base], line[base + 1], line[base + 2]
            key = (r >> 3, g >> 3, b >> 3)
            counts[key] = counts.get(key, 0) + 1
            total += 1
    if not total:
        return [], "no pixels read"
    ranked = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    clusters = []
    for (r, g, b), count in ranked[:3]:
        hex_value = rgb_to_hex((r << 3) | 4, (g << 3) | 4, (b << 3) | 4)
        clusters.append({"hex": hex_value, "share": round(count / total, 3)})
    return clusters, "sampled every 7th pixel"


def inventory_image(collector: Collector, path: Path, rel: str) -> None:
    ext = path.suffix.lower()
    try:
        size_bytes = path.stat().st_size
    except OSError:
        collector.unreadable.append(rel)
        return
    width = height = None
    method = ""
    sample_note = ""
    clusters: List[dict] = []
    try:
        if ext == ".png":
            width, height = png_size(path.read_bytes()[:64])
            method = "PNG IHDR"
            clusters, sample_note = png_sample_colours(path)
        elif ext in (".jpg", ".jpeg"):
            width, height = jpeg_size(path.read_bytes())
            method = "JPEG SOF"
        elif ext == ".svg":
            text = read_text(path) or ""
            width, height, method = svg_size(text)
        else:
            method = "unsupported format"
    except OSError:
        collector.unreadable.append(rel)
        return

    record = {
        "path": rel,
        "bytes": size_bytes,
        "format": ext.lstrip("."),
    }
    if width and height:
        record["value"] = "{}x{}".format(width, height)
        record["source"] = "read"
        record["evidence"] = "{} ({} header)".format(rel, method)
        record["width"] = width
        record["height"] = height
        record["aspect"] = round(width / height, 2)
        record["orientation"] = (
            "square" if width == height else ("landscape" if width > height else "portrait")
        )
    else:
        record["value"] = "unknown"
        record["source"] = "inferred"
        record["evidence"] = "{} ({}: no dimensions found)".format(rel, method)
        record["width"] = None
        record["height"] = None
    collector.images.append(record)

    if clusters:
        collector.notices.append(
            val(
                "{}: sampled colours {}".format(
                    rel, ", ".join(c["hex"] for c in clusters)
                ),
                "inferred",
                "{} ({})".format(rel, sample_note),
                sample_hexes=[c["hex"] for c in clusters],
            )
        )
        collector.sampled = getattr(collector, "sampled", [])
        for cluster in clusters:
            collector.sampled.append(
                val(
                    cluster["hex"],
                    "inferred",
                    "{} ({}, share {})".format(rel, sample_note, cluster["share"]),
                    share=cluster["share"],
                )
            )


LOGO_HINTS = ("logo", "mark", "wordmark", "lockup", "brandmark", "monogram", "symbol")
VARIANT_HINTS = [
    ("primary", "primary"),
    ("wordmark", "wordmark"),
    ("monogram", "monogram"),
    ("symbol", "symbol"),
    ("icon", "icon"),
    ("mark", "mark"),
    ("stacked", "stacked"),
    ("horizontal", "horizontal"),
    ("reverse", "reverse"),
    ("inverted", "reverse"),
    ("negative", "reverse"),
    ("mono", "mono"),
    ("light", "light"),
    ("dark", "dark"),
]


def looks_like_logo(rel: str) -> bool:
    lowered = rel.lower()
    stem = Path(rel).stem.lower()
    if not any(hint in stem for hint in LOGO_HINTS):
        return False
    return not stem.startswith(("og-", "favicon-"))


def variant_from_name(rel: str) -> Tuple[str, str]:
    stem = Path(rel).stem.lower()
    for hint, variant in VARIANT_HINTS:
        if hint in stem:
            return variant, "filename"
    return "unspecified", "no variant word in the filename"


# ----------------------------------------------------------------- analysis


def rank_colours(collector: Collector) -> List[dict]:
    grouped: Dict[str, dict] = {}
    for item in collector.colours:
        entry = grouped.setdefault(
            item["hex"], {"hex": item["hex"], "uses": 0, "files": set(),
                          "first": item["evidence"], "tokens": []}
        )
        entry["uses"] += 1
        entry["files"].add(item["evidence"].split(":")[0].split(" ")[0])
        if item["token"]:
            entry["tokens"].append(item["token"])
    ranked = sorted(grouped.values(), key=lambda e: (-e["uses"], e["hex"]))
    return ranked


def assign_roles(ranked: List[dict]) -> Dict[str, dict]:
    roles: Dict[str, dict] = {}
    used: set = set()

    def from_token(role: str) -> Optional[dict]:
        for entry in ranked:
            for token in entry["tokens"]:
                if token_role(token) == role:
                    return entry
        return None

    ground = from_token("ground")
    if ground is None:
        for entry in ranked:
            if luminance(entry["hex"]) >= 0.80:
                ground = entry
                break
    ink = from_token("ink")
    if ink is None:
        for entry in ranked:
            if luminance(entry["hex"]) <= 0.30:
                ink = entry
                break
    accent = from_token("accent")
    if accent is None:
        for entry in ranked:
            if saturation(entry["hex"]) >= 0.30 and 0.15 <= luminance(entry["hex"]) <= 0.80:
                accent = entry
                break
    surface = from_token("surface")
    if surface is None:
        for entry in ranked:
            if entry is ground or entry in (ink, accent):
                continue
            if 0.55 <= luminance(entry["hex"]) < 0.95 and entry is not ground:
                surface = entry
                break

    def emit(role: str, entry: Optional[dict], fallback_note: str) -> None:
        if entry is None:
            roles[role] = val(None, "inferred", fallback_note, uses=0)
            return
        used.add(entry["hex"])
        token = None
        for candidate in entry["tokens"]:
            if token_role(candidate) == role:
                token = candidate
                break
        if token:
            roles[role] = val(
                entry["hex"], "read",
                "{} (token {})".format(entry["first"], token),
                uses=entry["uses"],
            )
        else:
            roles[role] = val(
                entry["hex"], "inferred",
                "{} (chosen by frequency and luminance, most used {} times)".format(
                    entry["first"], entry["uses"]
                ),
                uses=entry["uses"],
            )

    emit("ground", ground, "no light colour qualified as a ground")
    emit("ink", ink, "no dark colour qualified as ink")
    emit("accent", accent, "no saturated colour qualified as an accent")
    if surface is not None and surface not in (ground, ink, accent):
        emit("surface", surface, "")
    else:
        if ground is not None:
            roles["surface"] = val(
                ground["hex"], "inferred",
                "{} (no separate surface colour found, ground doubles as surface)".format(
                    ground["first"]
                ),
                uses=ground["uses"],
            )
        else:
            roles["surface"] = val(None, "inferred", "no surface colour candidate")
    return roles


def build_pairings(ranked: List[dict], roles: Dict[str, dict]) -> List[dict]:
    pairings = []
    lights = [e for e in ranked if luminance(e["hex"]) >= 0.60][:6]
    darks = [e for e in ranked if luminance(e["hex"]) <= 0.40][:6]
    seen = set()
    for dark in darks:
        for light in lights:
            key = (dark["hex"], light["hex"])
            if key in seen:
                continue
            seen.add(key)
            ratio = contrast(dark["hex"], light["hex"])
            if ratio < 3.0:
                continue
            use = "body" if ratio >= 4.5 else "large text only"
            sources = []
            for role in ("ink", "ground", "surface", "accent"):
                entry = roles.get(role)
                if entry and entry["value"] in (dark["hex"], light["hex"]):
                    sources.append("{} {}".format(role, entry["source"]))
            inferred = any("inferred" in item for item in sources)
            pairings.append(
                val(
                    "{} on {}".format(dark["hex"], light["hex"]),
                    "inferred" if inferred else "read",
                    "{} and {} (contrast computed by WCAG relative luminance)".format(
                        dark["first"], light["first"]
                    ),
                    ratio=ratio,
                    use=use,
                )
            )
    pairings.sort(key=lambda p: (-p["ratio"], p["value"]))
    return pairings


def build_type(collector: Collector) -> dict:
    family_groups: Dict[str, dict] = {}
    for item in collector.families:
        entry = family_groups.setdefault(
            item["family"].lower(),
            {"family": item["family"], "uses": 0, "first": item["evidence"],
             "tokens": [], "min_rank": item["rank"]},
        )
        entry["uses"] += 1
        entry["min_rank"] = min(entry["min_rank"], item["rank"])
        if item["token"]:
            entry["tokens"].append(item["token"])
    ordered = sorted(
        family_groups.values(),
        key=lambda e: (e["min_rank"], -e["uses"], e["family"].lower()),
    )
    families = [
        val(
            entry["family"],
            "read",
            entry["first"],
            uses=entry["uses"],
            role="brand face" if entry["min_rank"] == 0 else "fallback",
        )
        for entry in ordered
    ]

    size_groups: Dict[float, dict] = {}
    for item in collector.sizes:
        entry = size_groups.setdefault(
            item["px"], {"px": item["px"], "uses": 0, "first": item["evidence"],
                         "raw": item["raw"], "converted": item["converted"]}
        )
        entry["uses"] += 1
        if item["converted"]:
            entry["converted"] = True
    scale = []
    for entry in sorted(size_groups.values(), key=lambda e: (e["px"], e["raw"])):
        px = entry["px"]
        shown = "{}px".format(int(px) if float(px).is_integer() else px)
        if entry["converted"]:
            scale.append(
                val(
                    shown, "inferred",
                    "{} ({} converted at a 16px root)".format(entry["first"], entry["raw"]),
                    uses=entry["uses"],
                )
            )
        else:
            scale.append(val(shown, "read", entry["first"], uses=entry["uses"]))

    weight_groups: Dict[int, dict] = {}
    for item in collector.weights:
        entry = weight_groups.setdefault(
            item["weight"], {"weight": item["weight"], "uses": 0, "first": item["evidence"]}
        )
        entry["uses"] += 1
    weights = [
        val(entry["weight"], "read", entry["first"], uses=entry["uses"])
        for entry in sorted(weight_groups.values(), key=lambda e: e["weight"])
    ]

    return {"families": families, "scale": scale, "weights": weights,
            "font_files": collector.font_files}


def build_logo(collector: Collector) -> dict:
    variants = []
    for record in collector.logos:
        variant, basis = variant_from_name(record["path"])
        source = "read" if basis == "filename" else "inferred"
        variants.append(
            val(
                record["path"],
                record["source"],
                record["evidence"],
                variant=variant,
                variant_source=source,
                variant_basis=basis,
                width=record.get("width"),
                height=record.get("height"),
                aspect=record.get("aspect"),
            )
        )
    tallest = None
    for record in collector.logos:
        height = record.get("height")
        if height and (tallest is None or height > tallest[0]):
            tallest = (height, record["path"])
    if tallest:
        clear = int(round(tallest[0] * 0.5))
        clear_space = val(
            "{}px".format(clear),
            "inferred",
            "{} (half the tallest logo height, {}px; no guideline states a rule)".format(
                tallest[1], tallest[0]
            ),
            minimum_px=clear,
        )
    else:
        clear_space = val(
            "unknown", "inferred", "no logo with a readable height was found"
        )
    return {
        "variants": variants,
        "variant_count": val(len(variants), "read", "counted from the logo files found"),
        "clear_space": clear_space,
        "clear_space_rule": val(
            "Hold clear space on all four sides equal to half the logo height. Nothing enters it.",
            "inferred",
            "derived rule, not a declared one",
        ),
    }


def build_imagery(collector: Collector) -> dict:
    files = [record for record in collector.images]
    landscape = sum(1 for f in files if f.get("orientation") == "landscape")
    portrait = sum(1 for f in files if f.get("orientation") == "portrait")
    square = sum(1 for f in files if f.get("orientation") == "square")
    rules = []
    if files:
        if landscape and not portrait:
            rules.append(
                val(
                    "Use landscape imagery. Every readable image in the folder is landscape.",
                    "inferred",
                    "{} of {} images are landscape".format(landscape, len(files)),
                )
            )
        if portrait and not landscape:
            rules.append(
                val(
                    "Use portrait imagery. Every readable image in the folder is portrait.",
                    "inferred",
                    "{} of {} images are portrait".format(portrait, len(files)),
                )
            )
        if square:
            rules.append(
                val(
                    "Square crops are available.",
                    "inferred",
                    "{} of {} images are square".format(square, len(files)),
                )
            )
        rules.append(
            val(
                "Never stretch an image. Scale it and crop it, keeping the aspect ratio.",
                "inferred",
                "derived from the readable dimensions of {} files".format(len(files)),
            )
        )
        rules.append(
            val(
                "Photographic colour was sampled, not declared. Treat it as a guide, not a rule.",
                "inferred",
                "sampled from PNG pixels only; JPEG content is not decoded by this tool",
            )
        )
    else:
        rules.append(
            val(
                "No imagery rule could be read: the folder holds no image files.",
                "inferred",
                "no image files found",
            )
        )
    return {
        "files": files,
        "count": val(len(files), "read", "counted from files with an image extension"),
        "sampled_colours": getattr(collector, "sampled", []),
        "rules": rules,
    }


def build_anti_patterns(ranked, roles, collector, logo_block, imagery_block) -> List[dict]:
    patterns = []
    patterns.append(
        val(
            "Do not introduce a colour outside the ranked palette.",
            "inferred",
            "the palette has {} declared colours".format(len(ranked)),
        )
    )
    accent_values = [e["hex"] for e in ranked if saturation(e["hex"]) >= 0.30]
    if len(accent_values) <= 1:
        patterns.append(
            val(
                "Do not add a second accent colour.",
                "inferred",
                "{} saturated colour found in the whole folder".format(len(accent_values)),
            )
        )
    if not collector.has_gradient:
        patterns.append(
            val(
                "Do not add gradients. None appear in the assets.",
                "inferred",
                "no gradient function in any stylesheet or SVG",
            )
        )
    accent = roles.get("accent", {}).get("value")
    ground = roles.get("ground", {}).get("value")
    if accent and ground and contrast(accent, ground) < 4.5:
        patterns.append(
            val(
                "Do not set body text in the accent colour: {} on {} is {:.2f}:1.".format(
                    accent, ground, contrast(accent, ground)
                ),
                "inferred",
                "contrast computed between the accent and the ground",
            )
        )
    if imagery_block["count"]["value"] and not any(
        f.get("orientation") == "portrait" for f in imagery_block["files"]
    ):
        patterns.append(
            val(
                "Do not use portrait crops of the imagery.",
                "inferred",
                "no portrait image is present to crop",
            )
        )
    if logo_block["variant_count"]["value"]:
        if not any(v.get("variant") in ("reverse", "mono") for v in logo_block["variants"]):
            patterns.append(
                val(
                    "Do not place the logo on a dark ground: no reverse or mono variant exists.",
                    "inferred",
                    "only {} logo file(s), none of them a reverse or mono variant".format(
                        logo_block["variant_count"]["value"]
                    ),
                )
            )
    return patterns


def build_questions(collector, ranked, roles, type_block, logo_block, imagery_block, pairings):
    raised = []
    reported = set()

    def raise_question(qid: str, reason: str, evidence: str) -> None:
        if qid in reported:
            return
        reported.add(qid)
        raised.append(
            val(
                "{}: {}".format(qid, QUESTION_TEXT[qid]),
                "inferred",
                evidence,
                id=qid,
                reason=reason,
            )
        )

    name_entry = None
    if collector.name_candidates:
        name_entry = sorted(collector.name_candidates, key=lambda c: c["rank"])[0]
    if name_entry is None:
        raise_question(
            "QA01",
            "The brand name is not declared in any file, so a folder name was used.",
            "no Brand: line, JSON name key or SVG title found",
        )

    inferred_roles = [role for role in ("ground", "ink", "accent", "surface")
                      if roles[role]["source"] == "inferred"]
    if inferred_roles:
        raise_question(
            "QA02",
            "These roles were assigned by measurement, not by a named token: {}.".format(
                ", ".join(inferred_roles)
            ),
            "; ".join(roles[role]["evidence"] for role in inferred_roles[:2]),
        )

    if not type_block["families"]:
        raise_question(
            "QA03",
            "No font family is declared anywhere in the folder.",
            "no font-family declaration found",
        )

    if roles["accent"]["source"] == "inferred":
        raise_question(
            "QA04",
            "The accent was chosen by saturation and luminance, and no file states an accent budget.",
            roles["accent"]["evidence"],
        )

    raise_question(
        "QA05",
        "Clear space was derived from the artwork because no guideline states a rule.",
        logo_block["clear_space"]["evidence"],
    )

    if logo_block["variant_count"]["value"] < 2:
        count = logo_block["variant_count"]["value"]
        raise_question(
            "QA06",
            "Only {} logo file was found, so no variant set could be read.".format(count)
            if count == 1
            else "No logo file was found, so no variant set could be read.",
            "one logo file in the folder" if count == 1 else "no logo file in the folder",
        )

    if not imagery_block["count"]["value"]:
        raise_question(
            "QA07",
            "The folder holds no imagery, so no imagery rule could be read.",
            "no files with an image extension",
        )

    if len(type_block["scale"]) < 3:
        count = len(type_block["scale"])
        if count == 0:
            reason = "No type size was declared anywhere, so no scale could be read."
        elif count == 1:
            reason = "Only one type size was declared, so no scale could be read."
        else:
            reason = "Only two type sizes were declared, so no scale could be read."
        raise_question(
            "QA08",
            reason,
            "fewer than three font-size declarations",
        )

    if not any(p["ratio"] >= 4.5 for p in pairings):
        raise_question(
            "QA12",
            "No pair of read colours reached 4.5:1, so a safe body pair was not established.",
            "highest computed contrast in the folder is {:.2f}:1".format(
                max([p["ratio"] for p in pairings]) if pairings else 0.0
            ),
        )

    order = [q[0] for q in QUESTIONS]
    raised.sort(key=lambda q: order.index(q["id"]))
    return raised


def collect_inferred(spec: dict) -> List[str]:
    """Every dotted path whose value is marked inferred."""
    paths: List[str] = []

    def walk(node, path: str) -> None:
        if isinstance(node, dict):
            if "source" in node and "value" in node:
                if node["source"] == "inferred" and not path.startswith("questions_raised"):
                    paths.append(path)
                return
            for key in node:
                walk(node[key], "{}.{}".format(path, key) if path else key)
        elif isinstance(node, list):
            for index, item in enumerate(node):
                walk(item, "{}[{}]".format(path, index))

    walk(spec, "")
    return paths


# --------------------------------------------------------------------- build


def walk_files(root: Path, exclude: Optional[set] = None) -> List[Path]:
    excluded = exclude or set()
    found: List[Path] = []
    for current, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS and not d.startswith("."))
        for name in sorted(filenames):
            if name.startswith(".") or name in EXCLUDED_NAMES:
                continue
            candidate = Path(current) / name
            if candidate.resolve() in excluded:
                continue
            found.append(candidate)
    return sorted(found, key=lambda p: rel_posix(p, root))


def audit(root: Path, exclude: Optional[set] = None) -> dict:
    root = root.resolve()
    collector = Collector(root)
    collector.sampled = []
    files = walk_files(root, exclude)

    for path in files:
        rel = rel_posix(path, root)
        ext = path.suffix.lower()
        collector.files.append(rel)
        collector.by_extension[ext] = collector.by_extension.get(ext, 0) + 1

        if ext in FONT_EXT:
            stem = path.stem
            weight_hint = "regular"
            for word, weight in (
                ("thin", "100"), ("extralight", "200"), ("light", "300"),
                ("regular", "400"), ("book", "400"), ("medium", "500"),
                ("semibold", "600"), ("bold", "700"), ("black", "900"),
            ):
                if word in stem.lower():
                    weight_hint = weight
                    break
            family_guess = re.split(r"[-_]", stem)[0]
            collector.font_files.append(
                {
                    "value": rel,
                    "source": "read",
                    "evidence": rel,
                    "format": ext.lstrip("."),
                    "family_guess": val(
                        family_guess, "inferred",
                        "{} (family read from the filename, not from the font table)".format(rel),
                    ),
                    "weight_guess": val(
                        weight_hint, "inferred",
                        "{} (weight read from the filename)".format(rel),
                    ),
                }
            )
            continue

        if ext in IMAGE_EXT:
            inventory_image(collector, path, rel)
            if ext == ".svg":
                svg_text = read_text(path)
                if svg_text is not None:
                    scan_svg(
                        collector, rel, svg_text, allow_name=looks_like_logo(rel)
                    )
            continue

        text = read_text(path)
        if text is None:
            collector.unreadable.append(rel)
            continue
        if ext in CSS_EXT:
            scan_css(collector, rel, text)
        elif ext in JSON_EXT:
            scan_json(collector, rel, text)
        elif ext in JS_EXT:
            scan_js(collector, rel, text)
        elif ext in TEXT_EXT:
            scan_text(collector, rel, text)

    collector.logos = [
        record for record in collector.images if looks_like_logo(record["path"])
    ]
    collector.images = [
        record for record in collector.images if not looks_like_logo(record["path"])
    ]

    ranked = rank_colours(collector)
    roles = assign_roles(ranked)
    type_block = build_type(collector)
    logo_block = build_logo(collector)
    imagery_block = build_imagery(collector)
    pairings = build_pairings(ranked, roles)
    anti_patterns = build_anti_patterns(
        ranked, roles, collector, logo_block, imagery_block
    )
    questions = build_questions(
        collector, ranked, roles, type_block, logo_block, imagery_block, pairings
    )

    if collector.name_candidates:
        best_name = sorted(collector.name_candidates, key=lambda c: c["rank"])[0]
        brand_name = val(best_name["name"], "read", best_name["evidence"])
    else:
        guess = root.name.replace("-", " ").replace("_", " ").title()
        brand_name = val(
            guess, "inferred",
            "{} (folder name; no Brand: line, JSON name key or SVG title found)".format(root.name),
        )
    if collector.tagline_candidates:
        tagline = val(
            collector.tagline_candidates[0]["name"], "read",
            collector.tagline_candidates[0]["evidence"],
        )
    else:
        tagline = val(None, "inferred", "no tagline declared in any file")

    ranked_colours = []
    for entry in ranked:
        first_token = entry["tokens"][0] if entry["tokens"] else None
        ranked_colours.append(
            val(
                entry["hex"], "read", entry["first"],
                uses=entry["uses"],
                files=sorted(entry["files"]),
                token=first_token,
            )
        )

    spec = {
        "schema_version": SCHEMA_VERSION,
        "tool": "brand_audit.py",
        "tool_version": TOOL_VERSION,
        "folder": root.name,
        "audit": {
            "files_scanned": val(len(collector.files), "read", "counted from the folder walk"),
            "by_extension": val(
                {k: collector.by_extension[k] for k in sorted(collector.by_extension)},
                "read",
                "counted from the folder walk",
            ),
            "unreadable": val(
                collector.unreadable, "read", "files the walk could not decode as text"
            ),
            "notices": sorted(collector.notices, key=lambda n: str(n["value"])),
        },
        "brand": {"name": brand_name, "tagline": tagline},
        "colours": {
            "ranked": ranked_colours,
            "roles": roles,
            "tolerance": val(
                6, "inferred",
                "a channel tolerance of 6 of 255, chosen so a render with rounding still passes",
            ),
        },
        "type": {
            "families": type_block["families"],
            "scale": type_block["scale"],
            "weights": type_block["weights"],
            "font_files": type_block["font_files"],
        },
        "logo": logo_block,
        "imagery": {
            "files": imagery_block["files"],
            "count": imagery_block["count"],
            "sampled_colours": imagery_block["sampled_colours"],
            "rules": imagery_block["rules"],
        },
        "pairings": pairings,
        "anti_patterns": anti_patterns,
        "questions_raised": questions,
        "all_questions": [q[0] for q in QUESTIONS],
        "unconfirmed": [],
    }
    spec["unconfirmed"] = collect_inferred(spec)
    return spec


def summarise(spec: dict) -> str:
    roles = spec["colours"]["roles"]
    lines = [
        "brand_audit.py: {}".format(spec["folder"]),
        "files scanned: {}".format(spec["audit"]["files_scanned"]["value"]),
        "colours ranked: {}".format(len(spec["colours"]["ranked"])),
        "roles:",
    ]
    for role in ("ground", "ink", "accent", "surface"):
        entry = roles[role]
        lines.append(
            "  {:<8} {:<10} {}".format(
                role, str(entry["value"]), entry["source"]
            )
        )
    lines.append(
        "type families: {}".format(
            ", ".join(str(f["value"]) for f in spec["type"]["families"]) or "none"
        )
    )
    lines.append(
        "type sizes: {}".format(len(spec["type"]["scale"]))
    )
    lines.append("logo variants: {}".format(spec["logo"]["variant_count"]["value"]))
    lines.append("imagery files: {}".format(spec["imagery"]["count"]["value"]))
    lines.append("safe pairings: {}".format(len(spec["pairings"])))
    lines.append("anti-patterns: {}".format(len(spec["anti_patterns"])))
    lines.append("questions raised: {}".format(len(spec["questions_raised"])))
    for question in spec["questions_raised"]:
        lines.append("  " + str(question["value"]))
    lines.append("unconfirmed inferred values: {}".format(len(spec["unconfirmed"])))
    return "\n".join(lines)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Read a folder of brand assets and write brand-spec.json. "
            "Standard library only; no image library is used."
        ),
        epilog=(
            "Example: python3 brand_audit.py examples/example-1-clean-assets "
            "--out brand-spec.json --json"
        ),
    )
    parser.add_argument("folder", type=Path, help="folder of brand assets to audit")
    parser.add_argument(
        "--out", type=Path, default=Path("brand-spec.json"),
        help="path for the written spec (default: brand-spec.json)",
    )
    parser.add_argument(
        "--json", action="store_true",
        help="print the whole spec to stdout as well as writing it",
    )
    args = parser.parse_args(argv)

    if not args.folder.is_dir():
        print("error: {} is not a folder".format(args.folder), file=sys.stderr)
        return 2

    spec = audit(args.folder, exclude={args.out.resolve()})
    try:
        args.out.write_text(
            json.dumps(spec, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
    except OSError as error:
        print("error: cannot write {}: {}".format(args.out, error), file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(spec, indent=2, ensure_ascii=False))
    else:
        print(summarise(spec))
        print("\nwritten: {}".format(args.out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
