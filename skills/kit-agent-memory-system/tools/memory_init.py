#!/usr/bin/env python3
"""Scaffold a three-level memory tree.

Three modes. The flag that decides the mode also decides what --workspace means.

  Workspace mode: --workspace takes the NAME of the new workspace.
      python3 memory_init.py --workspace "Fieldnote Studio" --out ./memory

  Project mode: --project takes the NAME of the project, and --workspace takes
  the FOLDER of an existing workspace, because the index lives there.
      python3 memory_init.py --project "Autumn catalogue" \
          --out ./memory --workspace ./memory

  Campaign mode: a time-boxed piece of work with an end date.
      python3 memory_init.py --campaign "November sample drop" \
          --out ./memory --workspace ./memory

Every card is written with all five sections, a short instruction comment in
each, and a fill marker where the owner has to supply content. Nothing is
written with a guessed fact.

The tool never reads the clock. Pass --confirmed YYYY-MM-DD to date every
section on creation, or leave it out and fill the dates as you confirm them.
Same arguments, same bytes out.

Exit codes: 0 written, 1 refused (target exists without --force), 2 usage.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

DATE_HELP = "YYYY-MM-DD"
MODES = ("workspace", "project", "campaign")

WORKSPACE_SECTIONS = [
    (
        "Purpose",
        "Two sentences at most. What this workspace is for, and who it serves.",
        "one line on what this workspace is for",
    ),
    (
        "Current state",
        "Facts that are true today, one bullet each, written as 'key: value'. "
        "No history and no reasoning. When a fact changes, change the value.",
        "key: value",
    ),
    (
        "Decisions and why",
        "One bullet per decision: the date, what was decided, then the reason. "
        "A decision with no reason is a changelog line, and the audit will flag it.",
        "YYYY-MM-DD what was decided, because ...",
    ),
    (
        "What's next",
        "The next three moves, in order. Nothing left over from a session older than the last one.",
        "next move",
    ),
    (
        "Key links",
        "Where the work actually lives: folders, files, URLs, thread names. "
        "A link that no longer opens is worse than no link.",
        "link and what it is",
    ),
]

PROJECT_SECTIONS = [
    (
        "Purpose",
        "What this project is for and what finished looks like. Two sentences.",
        "one line on what this project is for",
    ),
    (
        "Current state",
        "Facts that are true today for this project, written as 'key: value'. "
        "Workspace facts stay out. They are already true everywhere.",
        "key: value",
    ),
    (
        "Decisions and why",
        "One bullet per decision: the date, what was decided, then the reason. "
        "This section is the reason the folder is worth keeping in month six.",
        "YYYY-MM-DD what was decided, because ...",
    ),
    (
        "What's next",
        "The next three moves, in order, as at the end of the last session.",
        "next move",
    ),
    (
        "Key links",
        "Where this project's work lives: folders, files, URLs, thread names.",
        "link and what it is",
    ),
]

CAMPAIGN_SECTIONS = PROJECT_SECTIONS + [
    (
        "Wind-down",
        "What has to be true before this folder is archived: decisions carried up "
        "to the workspace, links stored, the section that closes it.",
        "what has to happen before this is archived",
    ),
]

INDEX_HEAD = """# memory index

Checked at the end of a session, not trusted. A row that names a folder with no
`memory.md` is a broken row. A card with no row is a card nobody will read.

The workspace card is not listed. It is the file at the root of this folder.
Rows are added by `memory_init.py --project` and `--campaign`, or by hand.

| Scope | Name | Card | Confirmed | One line |
|---|---|---|---|---|
"""


def slugify(name: str) -> str:
    """Lowercase, hyphen-separated, ASCII-safe enough for a folder name."""
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return slug or "untitled"


def card_header(name: str, level: str, confirmed: str | None) -> str:
    if level == "workspace":
        lines = [
            f"# memory: {name}",
            "",
            "Level: workspace",
            "Scope: every project in this folder. A fact that is true of one project only does not belong here.",
            "Owner: <!-- fill: who owns this card -->",
        ]
    elif level == "project":
        lines = [
            f"# memory: {name}",
            "",
            "Level: project",
            "Scope: this project only. Level one facts stay out. They are already true everywhere.",
            "Owns: <!-- fill: proper nouns that belong to this project, comma separated -->",
        ]
    else:
        lines = [
            f"# memory: {name}",
            "",
            "Level: campaign",
            "Scope: one piece of work with an end date. It is archived, not kept alive.",
            "Runs until: <!-- fill: YYYY-MM-DD -->",
            "Owns: <!-- fill: proper nouns that belong to this campaign, comma separated -->",
        ]
    lines += [
        "",
        "<!-- Read this card at the start of a session. Write it at the end of one.",
        "     Five sections, always present, in this order. Plain Markdown on purpose. -->",
        "",
    ]
    return "\n".join(lines)


def section_block(title: str, instruction: str, example: str, confirmed: str | None) -> str:
    stamp = f"Confirmed: {confirmed}" if confirmed else "Confirmed: <!-- fill: YYYY-MM-DD -->"
    return "\n".join(
        [
            f"## {title}",
            "",
            f"<!-- {instruction} -->",
            "",
            stamp,
            "",
            f"- <!-- fill: {example} -->",
            "",
        ]
    )


def build_card(name: str, level: str, confirmed: str | None) -> str:
    sections = {"workspace": WORKSPACE_SECTIONS, "project": PROJECT_SECTIONS, "campaign": CAMPAIGN_SECTIONS}[level]
    body = [card_header(name, level, confirmed)]
    body += [section_block(title, instruction, example, confirmed) for title, instruction, example in sections]
    return "\n".join(body).rstrip("\n") + "\n"


def write(path: Path, text: str, force: bool) -> bool:
    if path.exists() and not force:
        print(f"refused: {path} already exists. Add --force to overwrite it.", file=sys.stderr)
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    print(f"wrote {path}")
    return True


def append_index(index: Path, row: str) -> None:
    if not index.exists():
        print(f"note: no index at {index}. Nothing to append. Create the workspace first.")
        return
    text = index.read_text(encoding="utf-8")
    lines = text.rstrip("\n").split("\n")
    last_row = max((i for i, line in enumerate(lines) if line.startswith("|")), default=len(lines) - 1)
    lines.insert(last_row + 1, row)
    with index.open("w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    print(f"indexed in {index}")


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="memory_init.py",
        description="Scaffold a three-level memory tree: one workspace card, one card per project, one per campaign.",
        epilog=(
            "Examples:\n"
            '  python3 memory_init.py --workspace "Fieldnote Studio" --out ./memory\n'
            '  python3 memory_init.py --project "Autumn catalogue" --out ./memory --workspace ./memory\n'
            '  python3 memory_init.py --campaign "November sample drop" --out ./memory --workspace ./memory\n'
            "\n"
            "In workspace mode, --workspace is the new workspace name.\n"
            "In project and campaign mode, --workspace is the folder that holds the index."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--project", metavar="NAME", help="create one project card under projects/")
    mode.add_argument("--campaign", metavar="NAME", help="create one campaign card under campaigns/")
    parser.add_argument(
        "--workspace",
        metavar="NAME_OR_DIR",
        required=True,
        help="the new workspace name in workspace mode, or the workspace folder in project and campaign mode",
    )
    parser.add_argument("--out", metavar="DIR", required=True, help="folder to write into")
    parser.add_argument(
        "--confirmed",
        metavar=DATE_HELP,
        default=None,
        help="date every section on creation; omit it and the dates are fill markers",
    )
    parser.add_argument("--force", action="store_true", help="overwrite an existing card")
    args = parser.parse_args()

    if args.confirmed and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", args.confirmed):
        parser.error(f"--confirmed must look like {DATE_HELP}, not {args.confirmed!r}")

    out = Path(args.out).expanduser()

    if args.project or args.campaign:
        workspace = Path(args.workspace).expanduser()
        if not (workspace / "memory.md").exists():
            print(
                f"refused: no workspace card at {workspace / 'memory.md'}. "
                "Create the workspace first, or point --workspace at the right folder.",
                file=sys.stderr,
            )
            return 1
        level = "project" if args.project else "campaign"
        name = args.project or args.campaign
        folder = "projects" if level == "project" else "campaigns"
        path = out / folder / slugify(name) / "memory.md"
        if not write(path, build_card(name, level, args.confirmed), args.force):
            return 1
        try:
            rel = path.resolve().relative_to(workspace.resolve()).as_posix()
        except ValueError:
            rel = str(path)
        stamp = args.confirmed or "<!-- fill: YYYY-MM-DD -->"
        append_index(workspace / "index.md", f"| {level} | {name} | `{rel}` | {stamp} | <!-- fill: one line --> |")
        return 0

    name = args.workspace
    root = out
    if not write(root / "memory.md", build_card(name, "workspace", args.confirmed), args.force):
        return 1
    if not write(root / "index.md", INDEX_HEAD, args.force):
        return 1
    for folder in ("projects", "campaigns"):
        (root / folder).mkdir(parents=True, exist_ok=True)
    print(f"created {root / 'projects'} and {root / 'campaigns'}")
    print("next: fill the workspace card, then add a project with --project.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
