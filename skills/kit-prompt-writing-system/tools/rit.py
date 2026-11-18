#!/usr/bin/env python3
"""Assemble and check a four-part prompt: role, input, task, example.

Commands:
    python3 rit.py brief.json                     assemble to stdout, check to stderr
    python3 rit.py brief.json --out prompt.txt    write the prompt, report to stdout
    python3 rit.py brief.json --check-only        report only
    python3 rit.py brief.json --json              report as JSON
    python3 rit.py --example > brief.json         a complete brief that passes every rule

Exit codes: 0 clean, 2 one or more rule breaks, 1 input unreadable.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

PARTS = ("role", "input", "task", "example")

# Rule weights. Each part is worth what it changes in the output; presence of
# an example carries the most of any single rule, because it is the part most
# often left out and the part that sets the quality of the answer.
WEIGHTS = {
    "R01": 8, "R02": 7, "R03": 5,          # role, 20
    "R04": 8, "R05": 7, "R06": 5,          # input, 20
    "R07": 7, "R08": 6, "R09": 5, "R10": 7,  # task, 25
    "R11": 18, "R12": 7, "R13": 5,         # example, 30
    "R14": 5,                              # hygiene, 5
}
PART_OF = {
    "R01": "role", "R02": "role", "R03": "role",
    "R04": "input", "R05": "input", "R06": "input",
    "R07": "task", "R08": "task", "R09": "task", "R10": "task",
    "R11": "example", "R12": "example", "R13": "example",
    "R14": "hygiene",
}
PART_ORDER = ("role", "input", "task", "example", "hygiene")

NUMBER_WORDS = (
    "one two three four five six seven eight nine ten eleven twelve thirteen "
    "fourteen fifteen sixteen seventeen eighteen nineteen twenty"
).split()

# Role vocabulary. Add your own discipline to this list if the checks do not
# know it; the rule is that the role names a discipline, not that it uses one of
# these words.
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
    r"\b\d+\s*(?:to|and|[-\u2013])\s*\d+\s*words\b",
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

PLACEHOLDER_PATTERNS = (
    r"<[A-Za-z][^<>\n]{0,80}>",
    r"\[(?:INSERT|YOUR|TODO|TBD|ADD|FILL|PLACEHOLDER)[^\]\n]*\]",
    r"\{\{[^}\n]{0,80}\}\}",
    r"\bTODO\b",
    r"\bTBD\b",
    r"\bFIXME\b",
    r"\bXXX+\b",
    r"\bINSERT\b",
    r"\bLorem ipsum\b",
)


# ---------------------------------------------------------------- text helpers


def clean(text) -> str:
    """Normalise a value to plain text: list items on their own lines."""
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
    return "\n".join(out)


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


def low(text: str) -> str:
    return text.lower()


def clip(text: str, limit: int = 160) -> str:
    flat = re.sub(r"\s+", " ", text).strip()
    return flat if len(flat) <= limit else flat[: limit - 1] + "…"


# ------------------------------------------------------------------ assembly


def sections_of(data: dict) -> dict:
    """Return the four parts, with the optional keys folded into their part."""
    inp = clean(data.get("input"))
    constraints = clean(data.get("constraints"))
    if constraints:
        block = f"Constraints:\n{constraints}"
        inp = f"{inp}\n\n{block}" if inp else block
    task = clean(data.get("task"))
    output_format = clean(data.get("output_format"))
    if output_format:
        block = f"Output format:\n{output_format}"
        task = f"{task}\n\n{block}" if task else block
    return {
        "role": clean(data.get("role")),
        "input": inp,
        "task": task,
        "example": clean(data.get("example")),
    }


def assemble(data: dict) -> str:
    """Return the prompt as it should be pasted into a model."""
    parts = sections_of(data)
    blocks: list[str] = []
    for name in PARTS:
        body = parts[name]
        blocks.append(name.upper())
        blocks.append(body if body else "(not supplied)")
        blocks.append("")
    return "\n".join(blocks).rstrip() + "\n"


# --------------------------------------------------------------------- check


def add(findings, rule, ok, evidence, fix, message, skipped=False):
    status = "skipped" if skipped else ("ok" if ok else "error")
    findings.append(
        {
            "rule": rule,
            "part": PART_OF[rule],
            "weight": WEIGHTS[rule],
            "status": status,
            "message": message,
            "evidence": "" if status == "ok" else clip(evidence),
            "fix": fix if status == "error" else "",
        }
    )


def heading_lines(text: str) -> list[str]:
    """Short, unpunctuated, capitalised lines: the example's own headings."""
    heads: list[str] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("#"):
            title = line.lstrip("#").strip()
            if title:
                heads.append(title)
            continue
        if line[0] in "-*+>":
            continue
        if re.search(r"[.:;!?]$", line):
            continue
        if len(line.split()) > 8:
            continue
        if line[0].isupper():
            heads.append(line)
    return heads


def max_length(task: str) -> int:
    """The largest word count the task allows, or 0 when it sets none."""
    low_task = task.lower()
    match = re.search(r"(\d+)\s*(?:to|and|[-\u2013])\s*(\d+)\s*words", low_task)
    if match:
        return int(match.group(2))
    match = re.search(
        r"(?:under|fewer than|less than|max(?:imum)?(?: of)?|at most|"
        r"no more than|no longer than)\s*(\d+)\s*words",
        low_task,
    )
    if match:
        return int(match.group(1))
    match = re.search(r"(\d+)\s*words\b", low_task)
    if match and re.search(r"\bexactly\b", low_task):
        return int(match.group(1))
    return 0


def check(data: dict) -> dict:
    parts = sections_of(data)
    role, inp, task, example = (parts[p] for p in PARTS)
    joined = "\n".join([role, inp, task, example])
    findings: list[dict] = []

    # --- role -------------------------------------------------------------
    discipline = next(
        (d for d in DISCIPLINES if re.search(rf"\b{d}s?\b", low(role))), ""
    )
    add(
        findings, "R01", bool(discipline), role,
        "Name the discipline with a role noun, for example 'a pricing analyst' "
        "or 'a building surveyor'. A field of interest is not a discipline.",
        "The role names a discipline.", 
    )

    level_word = first_marker(role, LEVEL_WORDS)
    level_ok = bool(YEARS_RE.search(role) or DECADE_RE.search(role) or level_word)
    add(
        findings, "R02", level_ok, role,
        "Add a level: years of practice ('eleven years') or a rank "
        "('senior', 'principal', 'head of'). A discipline with no level reads "
        "as a generic answer.",
        "The role names a level or an amount of experience.",
    )

    adjective = first_marker(role, BARE_ADJECTIVES)
    if adjective:
        adjective_fix = (
            f"Replace '{adjective}' with the discipline and the level it stands "
            "in for. Words that praise do not specify."
        )
    else:
        adjective_fix = "Write the role first: a discipline and a level of experience."
    add(
        findings, "R03", word_count(role) >= 4 and not adjective, role or "no role text",
        adjective_fix,
        "The role praises nothing instead of specifying something.",
    )

    # --- input ------------------------------------------------------------
    situation_ok = (
        word_count(inp) >= 25
        and has_any(inp, ACTORS)
        and has_any(inp, STATE_MARKERS)
    )
    add(
        findings, "R04", situation_ok, inp,
        "State the situation: who is asking, and what is true right now. "
        "One or two sentences with a named actor and a present state.",
        "The input states the situation.",
    )

    constraint = first_marker(inp, CONSTRAINT_MARKERS)
    add(
        findings, "R05", bool(constraint), inp,
        "Name a hard edge as a directive: 'must', 'has to', 'cannot', "
        "'no more than', 'within'. A constraint the model cannot read is not "
        "a constraint.",
        "The input names at least one constraint.",
    )

    says_missing = has_any(inp, MISSING_MARKERS)
    has_material = word_count(inp) >= 40 and has_any(inp, MATERIAL_MARKERS)
    add(
        findings, "R06", says_missing or has_material, inp,
        "Say what you do not have, in the input: 'we have no churn data, ask "
        "for it rather than estimating'. A gap that is named is a gap the "
        "model will respect.",
        "The input says what is missing when nothing is supplied.",
    )

    # --- task -------------------------------------------------------------
    deliverable = next(
        (d for d in DELIVERABLES if re.search(rf"\b{d}s?\b", low(task))), ""
    )
    add(
        findings, "R07", bool(deliverable), task,
        "Name the deliverable with a noun: 'a one-page profile', 'a two-column "
        "table', 'a 200-word email'. A verb alone leaves the shape open.",
        "The task names a deliverable.",
    )

    length_ok = any(re.search(p, low(task)) for p in LENGTH_PATTERNS)
    add(
        findings, "R08", length_ok, task,
        "State a length or a bound: a word count, a page count, a section "
        "count, or a ceiling ('no more than 450 words').",
        "The task states a length or a bound.",
    )

    register = first_marker(task, REGISTER_MARKERS)
    add(
        findings, "R09", bool(register), task,
        "State the register: person, formality, diction and spelling. For "
        "example 'plain business English, third person, British spelling'.",
        "The task states a register.",
    )

    purpose = first_marker(task, PURPOSE_MARKERS)
    add(
        findings, "R10", bool(purpose), task,
        "Say what the deliverable must be usable for: 'usable as a briefing "
        "sheet before a first call'. Use decides the level of detail.",
        "The task states what the output must be usable for.",
    )

    # --- example ----------------------------------------------------------
    example_present = word_count(example) > 0
    add(
        findings, "R11", example_present, "no example key, or an empty example",
        "Write one example of the output at the depth you want. The shape, the "
        "depth and the register, and nothing else.",
        "An example is present.",
    )

    if not example_present:
        add(
            findings, "R12", False, "no example to inspect", "",
            "The example is an example of the output, not a description of it.",
            skipped=True,
        )
        add(
            findings, "R13", False, "no example to inspect", "",
            "The example agrees with the task.", skipped=True,
        )
    else:
        meta = first_marker(example, META_PHRASES)
        instruction = first_marker(example, INSTRUCTION_MARKERS)
        thin = word_count(example) < 40
        problem = ""
        if meta:
            problem = f"the example describes an output: '{meta}'"
        elif instruction:
            problem = f"the example instructs the model: '{instruction}'"
        elif thin:
            problem = f"the example is {word_count(example)} words, too thin to show depth"
        add(
            findings, "R12", not problem, problem or example,
            "Replace the description with one real passage of the deliverable, "
            "at the length and in the register you want. Do not explain it.",
            "The example is an example of the output, not a description of it.",
        )

        heads = heading_lines(example)
        task_low = re.sub(r"\s+", " ", low(task))
        mismatched = []
        for head in heads:
            key = re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", "", low(head))).strip()
            if not key:
                continue
            if key in task_low:
                continue
            head_tokens = set(key.split())
            task_tokens = set(re.findall(r"[a-z0-9]+", task_low))
            overlap = len(head_tokens & task_tokens) / max(1, len(head_tokens))
            if overlap < 0.6:
                mismatched.append(head)
        banned_bullets = re.search(r"\bno bullet|\bprose only|\bno lists?\b", low(task))
        has_bullets = any(
            line.strip().startswith(("- ", "* ", "1."))
            for line in example.splitlines()
        )
        no_headings = re.search(r"\bno headings?\b", low(task))
        contradiction = ""
        if mismatched:
            contradiction = f"the example shows a section the task never asks for: '{mismatched[0]}'"
        elif banned_bullets and has_bullets:
            contradiction = "the task bans bullet lists and the example uses them"
        elif no_headings and heads:
            contradiction = "the task bans headings and the example uses them"
        else:
            bound = max_length(task)
            if bound and word_count(example) > bound:
                contradiction = (
                    f"the example is {word_count(example)} words against a task "
                    f"ceiling of {bound}"
                )
        add(
            findings, "R13", not contradiction, contradiction or example,
            "Make the example demonstrate the sections and the format the task "
            "asks for, and stay inside the length the task sets.",
            "The example agrees with the task.",
        )

    # --- hygiene ----------------------------------------------------------
    placeholder = ""
    for pattern in PLACEHOLDER_PATTERNS:
        match = re.search(pattern, joined)
        if match:
            placeholder = match.group(0)
            break
    add(
        findings, "R14", not placeholder, placeholder,
        f"Fill or delete '{placeholder}'. A prompt that still carries a "
        "placeholder asks the model to guess.",
        "No unresolved placeholder is left in the text.",
    )

    errors = [f for f in findings if f["status"] == "error"]
    skipped = [f for f in findings if f["status"] == "skipped"]
    parts_score: dict[str, dict] = {}
    for name in PART_ORDER:
        of = sum(WEIGHTS[r] for r in WEIGHTS if PART_OF[r] == name)
        earned = sum(
            f["weight"]
            for f in findings
            if f["part"] == name and f["status"] == "ok"
        )
        parts_score[name] = {"earned": earned, "of": of}
    total = sum(p["earned"] for p in parts_score.values())

    return {
        "ok": not errors,
        "score": total,
        "errors": len(errors),
        "skipped": len(skipped),
        "parts": parts_score,
        "findings": findings,
        "words": {name: word_count(parts[name]) for name in PARTS},
    }


# --------------------------------------------------------------------- output


def report_text(report: dict) -> str:
    verdict = "PASS" if report["ok"] else "FAIL"
    lines = [
        f"{verdict}  score {report['score']}/100  errors {report['errors']}  "
        f"skipped {report['skipped']}",
        "      " + "  ".join(
            f"{name} {report['parts'][name]['earned']}/{report['parts'][name]['of']}"
            for name in PART_ORDER
        ),
        "",
    ]
    marks = {"ok": "ok  ", "error": "ERR ", "skipped": "SKIP"}
    for finding in report["findings"]:
        lines.append(
            f"[{marks[finding['status']]}] {finding['rule']:<4} "
            f"{finding['message']}"
        )
        if finding["evidence"]:
            lines.append(f"         evidence: {finding['evidence']}")
        if finding["fix"]:
            lines.append(f"         fix: {finding['fix']}")
    return "\n".join(lines) + "\n"


EXAMPLE_BRIEF = {
    "role": (
        "You are a service design analyst with nine years of experience "
        "observing how small teams handle customer complaints. You work from "
        "notes and recordings, and you separate what a customer did from what "
        "they said."
    ),
    "input": (
        "We run a six-person repair workshop in Sheffield. Right now complaints "
        "arrive by phone, email and the counter, and nobody can say how many "
        "are open at the end of a week.\n\n"
        "We have the last two months of complaint emails and the counter book. "
        "Both are incomplete: the counter book stops in the second week of last "
        "month.\n\n"
        "We have no timing data. We do not know how long a repair takes from "
        "arrival to collection. Ask for it if it matters. Do not estimate it."
    ),
    "constraints": (
        "The note must not name a customer or an order number.\n"
        "It has to stay inside 200 words.\n"
        "Write in British English."
    ),
    "task": (
        "Write a complaint review of 150 to 200 words, titled \"Where complaints "
        "come from\".\n"
        "Use three sections: where they arrive, what they are about, and the one "
        "change we should make first.\n"
        "Register: plain business English, third person, no adjectives that "
        "praise or alarm.\n"
        "It must be usable as the first page of a Monday team meeting, so a "
        "technician can read it in a minute."
    ),
    "output_format": "Three short paragraphs, one per section. No bullets, no table.",
    "example": (
        "Where they arrive\n"
        "Two thirds of the complaints in the sample came in by phone, and most "
        "of those arrived on the two days after a collection date. Email "
        "complaints were fewer and longer, and they tended to arrive a week "
        "after the repair rather than a day.\n\n"
        "What they are about\n"
        "The largest group is a missed collection date. The second is a repair "
        "that failed within a fortnight. Price appears once in the whole sample, "
        "and only alongside a missed date.\n\n"
        "The one change to make first\n"
        "Phone the customer on the morning of a collection date, before the "
        "workshop opens. It is one call per job, it needs no new system, and it "
        "targets the group that generates most of the calls."
    ),
}


def load(path: Path) -> tuple[dict, str]:
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        return {}, f"cannot read {path}: {exc}"
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        return {}, f"{path} is not valid JSON: {exc}"
    if not isinstance(data, dict):
        return {}, f"{path} must hold a JSON object, not {type(data).__name__}"
    return data, ""


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Assemble a four-part prompt from a JSON brief and check it. "
            "Keys: role, input, task, example, and optional constraints and "
            "output_format."
        ),
        epilog=(
            "Rules R01-R14 are listed in references/failure-list.md. They read "
            "word lists defined at the top of this file. "
            "Exit 0 clean, 2 rule breaks, 1 unreadable input."
        ),
    )
    parser.add_argument("brief", nargs="?", type=Path, help="JSON brief to read")
    parser.add_argument("--out", type=Path, help="write the assembled prompt here")
    parser.add_argument("--check-only", "--lint-only", dest="check_only",
                        action="store_true", help="print the report, no prompt")
    parser.add_argument("--json", action="store_true", help="print the report as JSON")
    parser.add_argument(
        "--example", action="store_true",
        help="print a complete brief that passes all 14 rules",
    )
    args = parser.parse_args()

    if args.example:
        print(json.dumps(EXAMPLE_BRIEF, indent=2))
        return 0
    if not args.brief:
        parser.error("a brief is required unless --example is used")

    data, problem = load(args.brief)
    if problem:
        print(f"error: {problem}", file=sys.stderr)
        return 1

    report = check(data)

    if args.json:
        print(json.dumps(report, indent=2))
        return 0 if report["ok"] else 2

    prompt = assemble(data)
    if args.out:
        try:
            args.out.write_text(prompt, encoding="utf-8")
        except OSError as exc:
            print(f"error: cannot write {args.out}: {exc}", file=sys.stderr)
            return 1
        print(f"wrote {args.out} ({word_count(prompt)} words)")
        sys.stdout.write(report_text(report))
    elif args.check_only:
        sys.stdout.write(report_text(report))
    else:
        sys.stdout.write(prompt)
        sys.stderr.write(report_text(report))

    return 0 if report["ok"] else 2


if __name__ == "__main__":
    sys.exit(main())
