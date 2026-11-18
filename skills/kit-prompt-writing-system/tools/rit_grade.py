#!/usr/bin/env python3
"""Grade a prompt against the four-part framework and name the weakest part.

Reads a JSON brief (keys: role, input, task, example) or a plain-text prompt
with ROLE / INPUT / TASK / EXAMPLE headings, or with those labels followed by a
colon at the start of a line.

Commands:
    python3 rit_grade.py brief.json
    python3 rit_grade.py prompt.txt
    python3 rit_grade.py brief.json --json

Exit codes: 0 for any readable prompt, 1 when the file cannot be read or parsed.
The grade is a reading aid, not a verdict on the model's answer.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

PART_ORDER = ("role", "input", "task", "example")
PART_TITLE = {"role": "Role", "input": "Input", "task": "Task", "example": "Example"}

NUMBER_WORDS = (
    "one two three four five six seven eight nine ten eleven twelve thirteen "
    "fourteen fifteen sixteen seventeen eighteen nineteen twenty"
).split()

DISCIPLINES = """
accountant actuary analyst architect archivist auditor biologist buyer chemist
clinician coach consultant copywriter curator designer developer dietitian
economist editor electrician engineer facilitator historian illustrator
journalist lawyer lecturer librarian marketer merchandiser nurse operator
pharmacist photographer physiotherapist planner plumber producer programmer
recruiter researcher reviewer scientist scriptwriter sociologist statistician
strategist surveyor teacher technician trainer translator tutor underwriter
veterinarian writer
""".split()

LEVEL_WORDS = [
    "junior", "senior", "principal", "lead", "head of", "director", "chief",
    "staff", "mid-level", "midweight", "entry-level", "entry level", "veteran",
    "seasoned", "experienced", "apprentice", "graduate", "fellow",
]

YEARS_RE = re.compile(
    rf"\b(?:\d{{1,2}}|{'|'.join(NUMBER_WORDS)})\s*\+?\s*(?:years?|yrs?)\b"
)
DECADE_RE = re.compile(r"\bdecades?\b")

BARE_ADJECTIVES = [
    "world-class", "world class", "brilliant", "genius", "elite", "top-tier",
    "top tier", "best-in-class", "best in class", "amazing", "awesome",
    "incredible", "passionate", "talented", "visionary", "dynamic", "guru",
    "ninja", "rockstar", "wizard", "superstar", "expert", "cutting-edge",
    "unparalleled", "renowned", "highly skilled", "exceptional", "premier",
]

ACTORS = (
    "we ", "we'", "our ", "i ", "my ", "the client", "the team", "the company",
    "the business", "the customer", "the studio", "the charity", "the school",
    "the practice", "the firm", "the organisation", "the organization",
)
STATE_MARKERS = (
    "now", "currently", "at present", "at the moment", "right now", "this year",
    "last month", "last year", "last quarter", "this quarter", "so far",
    "today", "recently", "this month", "this week",
)

CONSTRAINT_MARKERS = (
    "must", "has to", "have to", "cannot", "can't", "can not", "should not",
    "shouldn't", "no more than", "no fewer than", "no longer than", "at most",
    "at least", "within", "maximum", "max ", "minimum", "min ", "budget",
    "deadline", "not allowed", "limited to", "cap ", "do not", "don't",
    "only ", "no bullet", "one page", "single page", "word limit",
)

MISSING_MARKERS = (
    "we have no", "we do not have", "we don't have", "we have not", "we haven't",
    "no data", "no figures", "no numbers", "no revenue", "not available",
    "unavailable", "missing", "unknown", "we cannot supply", "we can't supply",
    "not supplied", "ask us for", "ask me for", "if they matter", "we lack",
    "we did not collect", "never collected", "nothing on", "no records",
    "no history",
)
MATERIAL_MARKERS = (
    "notes", "data", "transcript", "attached", "below", "we have", "we collected",
    "interview", "spreadsheet", "csv", "report", "figures", "quotes",
    "recordings", "survey", "tickets", "emails", "log", "minutes", "sample",
)

DELIVERABLES = """
memo profile brief report plan proposal email letter summary page document
spreadsheet table list guide script checklist one-pager deck presentation spec
specification note outline draft analysis policy contract invoice agenda minutes schedule
playbook template assessment review statement pitch article post thread
questionnaire form pack handbook runbook
""".split()

LENGTH_PATTERNS = (
    r"\b\d+\s*(?:to|and|[--])\s*\d+\s*words\b",
    r"\b\d+\s*words\b",
    r"\b(?:one|two|three|four|five|six|seven|eight|nine|ten)\s+"
    r"(?:page|pages|paragraph|paragraphs|section|sections|slide|slides|"
    r"bullet|bullets|line|lines|sentence|sentences)\b",
    r"\b\d+\s*(?:page|pages|paragraph|paragraphs|section|sections|slide|slides|"
    r"bullet|bullets|line|lines|character|characters|sentence|sentences)\b",
    r"\b(?:one|1)[- ]page\b",
    r"\bmax(?:imum)?\b",
    r"\bat most\b",
    r"\bno more than\b",
    r"\bunder \d+\b",
    r"\bbetween \d+ and \d+\b",
    r"\bword limit\b",
)

REGISTER_MARKERS = (
    "plain english", "plain business english", "plain language", "formal",
    "informal", "conversational", "third person", "first person",
    "second person", "active voice", "passive voice", "no jargon",
    "no marketing", "no adjectives", "british spelling", "american spelling",
    "tone", "register", "technical", "non-technical", "everyday language",
    "short sentences", "no slang", "neutral", "direct", "no hype",
)

PURPOSE_MARKERS = (
    "usable", "use it", "used by", "will be used", "for use", "so that",
    "so the", "read by", "handed to", "to brief", "briefing", "will read",
    "the reader", "audience", "purpose", "before a", "before the", "to open a",
    "to support", "to decide", "so a", "so we",
)

META_PHRASES = (
    "an example of", "example of the", "a description of", "description of",
    "should look like", "would look like", "should read like", "imagine a",
    "an illustration of", "sample of the", "something like this describes",
    "this is what a", "a good example", "the sort of thing",
)
INSTRUCTION_MARKERS = (
    "you should", "you must", "you will", "you need to", "the model",
    "the assistant", "make sure the", "be sure to",
)

REPAIRS = {
    "discipline": (
        "Name the discipline with a role noun, for example 'a pricing analyst' "
        "or 'a building surveyor'."
    ),
    "level": (
        "Add a level: years of practice ('eleven years') or a rank ('senior', "
        "'principal', 'head of')."
    ),
    "adjective": (
        "Replace the praise adjective with the discipline and the level it "
        "stands in for."
    ),
    "situation": (
        "State the situation: who is asking, and what is true right now, in one "
        "or two sentences with a named actor."
    ),
    "constraint": (
        "Name a hard edge as a directive: must, has to, cannot, no more than, "
        "within."
    ),
    "gap": (
        "Say what you do not have and what to do about it: 'we have no churn "
        "data, ask rather than estimate'."
    ),
    "deliverable": (
        "Name the deliverable with a noun: 'a one-page profile', 'a 200-word "
        "email', 'a two-column table'."
    ),
    "length": (
        "State a length or a bound: a word count, a page count, or a ceiling "
        "such as 'no more than 450 words'."
    ),
    "register": (
        "State the register: person, formality, diction and spelling, for "
        "example 'plain business English, third person, British spelling'."
    ),
    "purpose": (
        "Say what the deliverable must be usable for, and by whom: 'usable as a "
        "briefing sheet before a first call'."
    ),
    "present": (
        "Write one example of the output at the depth you want. One passage is "
        "enough; it is the part most prompts leave out."
    ),
    "quality": (
        "Replace the description of the output with a real passage of it, at the "
        "length and in the register you want."
    ),
    "consistency": (
        "Make the example show the sections and the format the task asks for, "
        "and keep it inside the length the task sets."
    ),
}

CRITERIA = {
    "role": [
        {"key": "discipline", "points": 10, "label": "names a discipline",
         "fail": "it names no discipline"},
        {"key": "level", "points": 9, "label": "names a level",
         "fail": "it names no level"},
        {"key": "adjective", "points": 6, "label": "no praise adjective",
         "fail": "it leans on a praise adjective"},
    ],
    "input": [
        {"key": "situation", "points": 9, "label": "states the situation",
         "fail": "it does not state the situation"},
        {"key": "constraint", "points": 8, "label": "names a constraint",
         "fail": "it names no constraint"},
        {"key": "gap", "points": 8, "label": "names the gap or supplies material",
         "fail": "it neither supplies material nor names what is missing"},
    ],
    "task": [
        {"key": "deliverable", "points": 8, "label": "names a deliverable",
         "fail": "it names no deliverable"},
        {"key": "length", "points": 6, "label": "sets a length or bound",
         "fail": "it sets no length or bound"},
        {"key": "register", "points": 5, "label": "sets a register",
         "fail": "it sets no register"},
        {"key": "purpose", "points": 6, "label": "says what it is usable for",
         "fail": "it does not say what the output is usable for"},
    ],
    "example": [
        {"key": "present", "points": 10, "label": "is present",
         "fail": "there is no example"},
        {"key": "quality", "points": 8, "label": "is an example, not a description",
         "fail": "it describes the output instead of showing it"},
        {"key": "consistency", "points": 7, "label": "agrees with the task",
         "fail": "it disagrees with the task"},
    ],
}


# ------------------------------------------------------------------- helpers


def word_count(text: str) -> int:
    return len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'\-]*", text))


def has_any(text: str, markers) -> bool:
    low = text.lower()
    return any(marker in low for marker in markers)


def first_marker(text: str, markers) -> str:
    low = text.lower()
    for marker in markers:
        if marker in low:
            return marker.strip()
    return ""


def clean(text) -> str:
    if text is None:
        return ""
    if isinstance(text, (list, tuple)):
        text = "\n".join(str(item) for item in text)
    text = str(text).replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.rstrip() for line in text.split("\n")]
    out: list[str] = []
    blanks = 0
    for line in lines:
        if not line.strip():
            blanks += 1
            if blanks > 1:
                continue
        else:
            blanks = 0
        out.append(line)
    while out and not out[0].strip():
        out.pop(0)
    while out and not out[-1].strip():
        out.pop()
    body = "\n".join(out)
    return "" if body.strip().lower() in {"(not supplied)", "(missing)", "n/a"} else body


def heading_of(line: str):
    raw = line.strip()
    if not raw:
        return None
    hashed = raw.startswith("#")
    core = raw.lstrip("#").strip().strip("*_ ").strip()
    match = re.match(r"^(role|input|task|example)\b\s*([:\--])?\s*(.*)$", core, re.I)
    if not match:
        return None
    name, separator, rest = match.group(1), match.group(2), match.group(3)
    word = core[: len(name)]
    if rest.strip() and not separator and not hashed and not word.isupper():
        return None
    return name.lower(), rest.strip()


def parse_text(raw: str):
    """Return (blocks, labelled). With no labels, the whole text is the task."""
    blocks: dict[str, list[str]] = {name: [] for name in PART_ORDER}
    current = None
    found = False
    for line in raw.splitlines():
        heading = heading_of(line)
        if heading:
            current = heading[0]
            found = True
            if heading[1]:
                blocks[current].append(heading[1])
            continue
        if current:
            blocks[current].append(line)
    if not found:
        return {"role": "", "input": "", "task": clean(raw), "example": ""}, False
    return {name: clean("\n".join(lines)) for name, lines in blocks.items()}, True


def parse_json(raw: str) -> dict:
    data = json.loads(raw)
    if not isinstance(data, dict):
        raise ValueError("the JSON root must be an object")
    blocks = {
        "role": clean(data.get("role")),
        "input": clean(data.get("input")),
        "task": clean(data.get("task")),
        "example": clean(data.get("example")),
    }
    constraints = clean(data.get("constraints"))
    if constraints:
        blocks["input"] = f"{blocks['input']}\n{constraints}".strip()
    output_format = clean(data.get("output_format"))
    if output_format:
        blocks["task"] = f"{blocks['task']}\n{output_format}".strip()
    return blocks


# ------------------------------------------------------------------ grading


def max_length(task: str) -> int:
    low_task = task.lower()
    match = re.search(r"(\d+)\s*(?:to|and|[--])\s*(\d+)\s*words", low_task)
    if match:
        return int(match.group(2))
    match = re.search(
        r"(?:under|fewer than|less than|max(?:imum)?(?: of)?|at most|"
        r"no more than|no longer than)\s*(\d+)\s*words",
        low_task,
    )
    if match:
        return int(match.group(1))
    return 0


def grade(blocks: dict) -> dict:
    role = blocks.get("role", "")
    inp = blocks.get("input", "")
    task = blocks.get("task", "")
    example = blocks.get("example", "")

    checks = {
        "discipline": bool(
            next((d for d in DISCIPLINES if re.search(rf"\b{d}s?\b", role.lower())), "")
        ),
        "level": bool(
            YEARS_RE.search(role)
            or DECADE_RE.search(role)
            or first_marker(role, LEVEL_WORDS)
        ),
        "adjective": word_count(role) >= 4
        and not first_marker(role, BARE_ADJECTIVES),
        "situation": (
            word_count(inp) >= 25
            and has_any(inp, ACTORS)
            and has_any(inp, STATE_MARKERS)
        ),
        "constraint": bool(first_marker(inp, CONSTRAINT_MARKERS)),
        "gap": has_any(inp, MISSING_MARKERS)
        or (word_count(inp) >= 40 and has_any(inp, MATERIAL_MARKERS)),
        "deliverable": bool(
            next((d for d in DELIVERABLES if re.search(rf"\b{d}s?\b", task.lower())), "")
        ),
        "length": any(re.search(p, task.lower()) for p in LENGTH_PATTERNS),
        "register": bool(first_marker(task, REGISTER_MARKERS)),
        "purpose": bool(first_marker(task, PURPOSE_MARKERS)),
        "present": word_count(example) > 0,
        "quality": False,
        "consistency": False,
    }

    if checks["present"]:
        meta = first_marker(example, META_PHRASES)
        instruction = first_marker(example, INSTRUCTION_MARKERS)
        checks["quality"] = not (
            meta or instruction or word_count(example) < 40
        )
        bound = max_length(task)
        too_long = bool(bound) and word_count(example) > bound
        heads = [
            line.strip().lstrip("#").strip()
            for line in example.splitlines()
            if line.strip()
            and len(line.strip().split()) <= 8
            and not re.search(r"[.:;!?]$", line.strip())
            and line.strip()[0].isupper()
        ]
        task_low = task.lower()
        mismatch = False
        for head in heads:
            key = re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", "", head.lower())).strip()
            if not key or key in task_low:
                continue
            head_tokens = set(key.split())
            task_tokens = set(re.findall(r"[a-z0-9]+", task_low))
            if len(head_tokens & task_tokens) / max(1, len(head_tokens)) < 0.6:
                mismatch = True
                break
        checks["consistency"] = not (too_long or mismatch)

    parts = []
    for name in PART_ORDER:
        earned = 0
        of = 0
        failures = []
        detail = []
        for criterion in CRITERIA[name]:
            ok = checks[criterion["key"]]
            of += criterion["points"]
            if ok:
                earned += criterion["points"]
            else:
                failures.append(criterion)
            detail.append(
                f"{criterion['label']} {criterion['points'] if ok else 0}"
                f"/{criterion['points']}"
            )
        parts.append(
            {
                "part": name,
                "title": PART_TITLE[name],
                "earned": earned,
                "of": of,
                "failures": failures,
                "detail": detail,
            }
        )

    total = sum(part["earned"] for part in parts)
    weakest = min(parts, key=lambda part: (part["earned"], PART_ORDER.index(part["part"])))

    candidates = []
    for part in parts:
        for criterion in part["failures"]:
            candidates.append((criterion["points"], part, criterion))
    candidates.sort(key=lambda item: (-item[0], PART_ORDER.index(item[1]["part"])))

    highest = ""
    second = ""
    if candidates:
        top = candidates[0]
        highest = (
            f"{top[0]} points, {top[1]['title']}. {REPAIRS[top[2]['key']]}"
        )
        rest = [c for c in candidates[1:] if c[1]["part"] != top[1]["part"]]
        if not rest:
            rest = candidates[1:]
        if rest:
            nxt = rest[0]
            second = (
                f"{nxt[0]} points, {nxt[1]['title']}. {REPAIRS[nxt[2]['key']]}"
            )

    if total == 100:
        reason = "all four parts carry their full weight."
    elif weakest["earned"] == 0:
        reason = "it scores nothing: " + "; ".join(
            c["fail"] for c in weakest["failures"]
        ) + "."
    elif len(weakest["failures"]) == len(CRITERIA[weakest["part"]]):
        reason = "it scores nothing: " + "; ".join(
            c["fail"] for c in weakest["failures"]
        ) + "."
    else:
        reason = "it scores " + f"{weakest['earned']}/25 because " + "; ".join(
            c["fail"] for c in weakest["failures"]
        ) + "."

    return {
        "total": total,
        "parts": parts,
        "weakest": weakest["part"],
        "weakest_title": weakest["title"],
        "weakest_score": weakest["earned"],
        "reason": reason,
        "highest": highest,
        "second": second,
        "words": {name: word_count(blocks.get(name, "")) for name in PART_ORDER},
    }


def report_text(result: dict, source: str) -> str:
    lines = ["Prompt Writing System: grade", "", f"File: {source}"]
    if not result.get("labelled", True):
        lines.append(
            "No part labels found: the whole file is graded as the task, and the "
            "other three parts score nothing."
        )
    lines.append(f"Total: {result['total']}/100")
    lines.append("")
    for part in result["parts"]:
        lines.append(
            f"  {part['title']:<8} {part['earned']:>2}/25   "
            + ", ".join(part["detail"])
        )
    lines.append("")
    if result["total"] == 100:
        lines.append("Weakest part: none. All four parts score 25.")
        lines.append("Reason: the prompt carries all four parts at full weight.")
        lines.append("")
        lines.append("Highest-value repair: none. Run it again with different input and compare.")
        lines.append("Second repair: none.")
    else:
        lines.append(
            f"Weakest part: {result['weakest_title']} "
            f"({result['weakest_score']}/25)."
        )
        lines.append(f"Reason: {result['reason']}")
        lines.append("")
        lines.append(f"Highest-value repair: {result['highest']}")
        lines.append(
            f"Second repair: {result['second']}" if result["second"]
            else "Second repair: none left. This is the one that matters."
        )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Grade a prompt against role, input, task and example. Each part "
            "scores out of 25. Names the weakest part, the highest-value repair "
            "and the second."
        ),
        epilog=(
            "Accepts a JSON brief (role, input, task, example) or a plain-text "
            "prompt with ROLE / INPUT / TASK / EXAMPLE headings. "
            "Exit 0 for any readable prompt, 1 when the file cannot be read."
        ),
    )
    parser.add_argument("prompt", type=Path, help="JSON brief or plain-text prompt")
    parser.add_argument("--json", action="store_true", help="print the grade as JSON")
    args = parser.parse_args()

    try:
        raw = args.prompt.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"error: cannot read {args.prompt}: {exc}", file=sys.stderr)
        return 1

    stripped = raw.lstrip()
    labelled = True
    try:
        if args.prompt.suffix.lower() == ".json" or stripped.startswith("{"):
            blocks = parse_json(raw)
        else:
            blocks, labelled = parse_text(raw)
    except (json.JSONDecodeError, ValueError) as exc:
        print(f"error: {args.prompt} could not be parsed: {exc}", file=sys.stderr)
        return 1

    result = grade(blocks)
    result["source"] = str(args.prompt)
    result["labelled"] = labelled
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        sys.stdout.write(report_text(result, str(args.prompt)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
