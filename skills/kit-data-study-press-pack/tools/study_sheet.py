#!/usr/bin/env python3
"""Keep a coding sheet as a CSV file, and refuse to total an unfinished count.

Usage:
    python3 study_sheet.py init --out sheet.csv --categories collection,delivery --title "Study title"
    python3 study_sheet.py add-row --sheet sheet.csv --raw "listing text" [--id RSV-001] [--date 2026-01-04]
    python3 study_sheet.py code --sheet sheet.csv --row 4 --category delivery --note "names a courier"
    python3 study_sheet.py review --sheet sheet.csv
    python3 study_sheet.py tally --sheet sheet.csv
    python3 study_sheet.py export --sheet sheet.csv --out rows.json

Reserved category values:
    ambiguous   codable in principle, not yet decided. Blocks the tally.
    excluded    out of the count. Needs a note, or the tally refuses.

The sheet is a CSV with the columns row,id,raw,date,category,note.
Lines starting with # are kept and ignored, so a sheet can carry its own label.
The title and the category list live in <sheet>.meta.json, written by init.

Exit codes: 0 the command completed, 2 the command could not proceed honestly.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import sys
from pathlib import Path

FIELDS = ["row", "id", "raw", "date", "category", "note"]
RESERVED = ["ambiguous", "excluded"]


def say(*parts: object) -> None:
    print(*parts)


def stop(message: str) -> "None":
    say(f"error: {message}")
    sys.exit(2)


def meta_path(sheet: Path) -> Path:
    return sheet.with_name(sheet.name + ".meta.json")


def read_meta(sheet: Path) -> dict:
    path = meta_path(sheet)
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            stop(f"{path} is not valid JSON")
    return {}


def write_meta(sheet: Path, meta: dict) -> None:
    meta_path(sheet).write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def read_sheet(sheet: Path) -> tuple:
    if not sheet.exists():
        stop(f"no sheet at {sheet}")
    text = sheet.read_text(encoding="utf-8").splitlines(keepends=True)
    comments = [line.rstrip("\r\n") for line in text if line.startswith("#")]
    data = "".join(line for line in text if not line.startswith("#"))
    reader = csv.DictReader(io.StringIO(data))
    if reader.fieldnames is None:
        stop(f"{sheet} has no header row")
    if "raw" not in reader.fieldnames:
        stop(f"{sheet} has no 'raw' column; expected {','.join(FIELDS)}")
    rows = []
    for line_no, record in enumerate(reader, start=2):
        item = {field: (record.get(field) or "").strip() for field in FIELDS}
        if not any(item.values()):
            continue
        if not item["row"]:
            item["row"] = str(len(rows) + 1)
        rows.append(item)
    rows.sort(key=lambda r: int(r["row"]) if r["row"].isdigit() else 0)
    return comments, rows


def write_sheet(sheet: Path, comments: list, rows: list) -> None:
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=FIELDS, lineterminator="\n")
    writer.writeheader()
    for row in rows:
        writer.writerow({field: row.get(field, "") for field in FIELDS})
    body = buffer.getvalue()
    prefix = "".join(comment + "\n" for comment in comments)
    sheet.write_text(prefix + body, encoding="utf-8")


def categories_of(sheet: Path, rows: list) -> list:
    meta = read_meta(sheet)
    listed = [c for c in meta.get("categories", []) if c]
    if listed:
        return listed
    seen = []
    for row in rows:
        value = row["category"]
        if value and value not in RESERVED and value not in seen:
            seen.append(value)
    say("note: no meta file found; categories inferred from the coded rows")
    return seen


def cmd_init(args: argparse.Namespace) -> int:
    sheet = Path(args.out)
    if sheet.exists() and not args.force:
        stop(f"{sheet} already exists; move it aside or pass --force")
    names = [name.strip() for name in args.categories.split(",") if name.strip()]
    if not names:
        stop("--categories needs at least one name, comma separated")
    clash = [name for name in names if name in RESERVED]
    if clash:
        stop(f"{', '.join(clash)} is a reserved category value; pick another name")
    if len(set(names)) != len(names):
        stop("--categories contains a duplicate name")
    sheet.parent.mkdir(parents=True, exist_ok=True)
    comments = [line for line in (args.note or []) if line]
    comments = ["# " + line.lstrip("# ") if not line.startswith("#") else line for line in comments]
    blank = []
    for index in range(args.rows):
        blank.append({"row": str(index + 1), "id": "", "raw": "", "date": "", "category": "", "note": ""})
    write_sheet(sheet, comments, blank)
    write_meta(sheet, {"title": args.title, "categories": names, "version": 1})
    say(f"sheet: {Path(args.out)}")
    say(f"title: {args.title}")
    say(f"categories: {', '.join(names)}")
    say(f"rows: {len(blank)}")
    if not blank:
        say("add rows with: add-row --sheet " + str(sheet) + ' --raw "..."')
    return 0


def cmd_add_row(args: argparse.Namespace) -> int:
    sheet = Path(args.sheet)
    comments, rows = read_sheet(sheet)
    raw = args.raw.strip()
    if not raw:
        stop("--raw is empty; a row with no text cannot be coded")
    next_row = 1 + max([int(r["row"]) for r in rows if r["row"].isdigit()] or [0])
    rows.append(
        {
            "row": str(next_row),
            "id": (args.id or "").strip(),
            "raw": raw,
            "date": (args.date or "").strip(),
            "category": "",
            "note": "",
        }
    )
    write_sheet(sheet, comments, rows)
    say(f"row {next_row} added; sheet now holds {len(rows)} rows")
    return 0


def cmd_code(args: argparse.Namespace) -> int:
    sheet = Path(args.sheet)
    comments, rows = read_sheet(sheet)
    valid = categories_of(sheet, rows) + RESERVED
    if args.category not in valid:
        say(f"error: '{args.category}' is not a category on this sheet")
        say(f"valid: {', '.join(valid)}")
        sys.exit(2)
    target = None
    for row in rows:
        if row["row"] == str(args.row):
            target = row
            break
    if target is None:
        stop(f"no row {args.row} in {sheet}; the sheet has {len(rows)} rows")
    note = (args.note or "").strip()
    if args.category == "excluded" and not note:
        stop("excluded needs --note saying why this row is out of the count")
    target["category"] = args.category
    if note:
        target["note"] = note
    write_sheet(sheet, comments, rows)
    say(f"row {target['row']}: {args.category}" + (f"  note: {target['note']}" if target["note"] else ""))
    return 0


def excerpt(text: str, width: int = 64) -> str:
    flat = " ".join(text.split())
    return flat if len(flat) <= width else flat[: width - 3] + "..."


def cmd_review(args: argparse.Namespace) -> int:
    sheet = Path(args.sheet)
    _, rows = read_sheet(sheet)
    meta = read_meta(sheet)
    uncoded = [r for r in rows if not r["category"]]
    ambiguous = [r for r in rows if r["category"] == "ambiguous"]
    excluded = [r for r in rows if r["category"] == "excluded"]
    coded = [r for r in rows if r["category"] and r["category"] not in ("ambiguous", "excluded")]
    say(f"title: {meta.get('title', '(no title)')}")
    say(f"sheet: {sheet}")
    say(
        f"rows: {len(rows)}  coded: {len(coded)}  uncoded: {len(uncoded)}  "
        f"ambiguous: {len(ambiguous)}  excluded: {len(excluded)}"
    )
    for label, group in (("uncoded", uncoded), ("ambiguous", ambiguous)):
        if not group:
            continue
        say("")
        say(label)
        for row in group:
            tag = f"{row['id']:<10}" if row["id"] else ""
            say(f"  row {row['row']:<4} {tag} {excerpt(row['raw'])}")
    if not uncoded and not ambiguous:
        say("")
        say("every row carries a decision")
    return 0


def cmd_tally(args: argparse.Namespace) -> int:
    sheet = Path(args.sheet)
    _, rows = read_sheet(sheet)
    meta = read_meta(sheet)
    categories = categories_of(sheet, rows)
    title = meta.get("title", "(no title)")

    uncoded = [r["row"] for r in rows if not r["category"]]
    ambiguous = [r["row"] for r in rows if r["category"] == "ambiguous"]
    unknown = sorted({r["category"] for r in rows if r["category"] and r["category"] not in categories + RESERVED})
    excluded = [r for r in rows if r["category"] == "excluded"]
    unstated = [r["row"] for r in excluded if not r["note"]]

    problems = []
    if uncoded:
        label = "row is" if len(uncoded) == 1 else "rows are"
        problems.append(f"{len(uncoded)} {label} uncoded")
    if ambiguous:
        label = "row is" if len(ambiguous) == 1 else "rows are"
        problems.append(f"{len(ambiguous)} {label} ambiguous")
    if unknown:
        problems.append(f"{len(unknown)} values are not categories on this sheet: {', '.join(unknown)}")
    if unstated:
        label = "row has" if len(unstated) == 1 else "rows have"
        problems.append(f"{len(unstated)} excluded {label} no recorded reason")

    if problems:
        say(f"title: {title}")
        say(f"sheet: {sheet}")
        say("")
        say("REFUSED: this sheet is not ready to tally.")
        say("reason: " + "; ".join(problems) + ".")
        if uncoded:
            say("uncoded rows: " + ", ".join(uncoded))
        if ambiguous:
            say("ambiguous rows: " + ", ".join(ambiguous))
        if unstated:
            say("excluded with no reason: " + ", ".join(unstated))
        say("")
        say("A percentage over an incomplete count is not a finding.")
        say("Code every row, or exclude it with a note that says why.")
        return 2

    coded = [r for r in rows if r["category"] in categories]
    denominator = len(coded)
    if denominator == 0:
        stop("no coded rows; there is nothing to count")

    counts = {name: sum(1 for r in coded if r["category"] == name) for name in categories}
    width = max([len(name) for name in categories] + [len("total")]) + 2

    say(f"title: {title}")
    say(f"sheet: {sheet}")
    say(f"rows in sheet: {len(rows)}")
    if excluded:
        note = "with a recorded reason" if len(excluded) == 1 else "each with a recorded reason"
        say(f"excluded: {len(excluded)} ({note})")
    else:
        say("excluded: 0")
    row_word = "row" if denominator == 1 else "rows"
    say(f"denominator: {denominator} coded {row_word}")
    say("")
    say("counts and percentages of the denominator:")
    total_pct = 0.0
    for name in categories:
        pct = counts[name] / denominator * 100
        total_pct += round(pct, 1)
        say("  " + name.ljust(width) + str(counts[name]).rjust(4) + f"  {pct:5.1f}%")
    say("  " + "total".ljust(width) + str(denominator).rjust(4) + f"  {total_pct:5.1f}%")
    if abs(total_pct - 100.0) > 0.05:
        say(f"note: percentages are rounded to one decimal and sum to {total_pct:.1f}%, not 100.0%")
    return 0


def cmd_export(args: argparse.Namespace) -> int:
    sheet = Path(args.sheet)
    _, rows = read_sheet(sheet)
    meta = read_meta(sheet)
    payload = {
        "title": meta.get("title", ""),
        "categories": meta.get("categories", categories_of(sheet, rows)),
        "row_count": len(rows),
        "rows": [
            {
                "row": int(r["row"]) if r["row"].isdigit() else r["row"],
                "id": r["id"],
                "raw": r["raw"],
                "date": r["date"],
                "category": r["category"],
                "note": r["note"],
            }
            for r in rows
        ],
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    say(f"wrote {out} ({len(rows)} rows)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Keep a coding sheet as CSV and refuse to total an unfinished count.",
        epilog="Reserved categories: " + ", ".join(RESERVED) + ". Exit 2 when the command cannot proceed honestly.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser("init", help="create a sheet with its categories")
    p_init.add_argument("--out", required=True, help="path of the sheet to create")
    p_init.add_argument("--categories", required=True, help="comma separated category names")
    p_init.add_argument("--title", required=True, help="study title, printed by every later command")
    p_init.add_argument("--rows", type=int, default=0, help="number of blank rows to write now (default 0)")
    p_init.add_argument("--note", action="append", help="a label line to keep at the top of the CSV; repeatable")
    p_init.add_argument("--force", action="store_true", help="overwrite an existing sheet")
    p_init.set_defaults(func=cmd_init)

    p_add = sub.add_parser("add-row", help="append one raw row")
    p_add.add_argument("--sheet", required=True)
    p_add.add_argument("--raw", required=True, help="the text being coded")
    p_add.add_argument("--id", default="", help="the source record id, if the source has one")
    p_add.add_argument("--date", default="", help="a date carried from the source record")
    p_add.set_defaults(func=cmd_add_row)

    p_code = sub.add_parser("code", help="record the decision for one row")
    p_code.add_argument("--sheet", required=True)
    p_code.add_argument("--row", type=int, required=True)
    p_code.add_argument("--category", required=True)
    p_code.add_argument("--note", default="", help="what in the text decided it")
    p_code.set_defaults(func=cmd_code)

    p_review = sub.add_parser("review", help="list uncoded and ambiguous rows")
    p_review.add_argument("--sheet", required=True)
    p_review.set_defaults(func=cmd_review)

    p_tally = sub.add_parser("tally", help="count the rows, if the count is finished")
    p_tally.add_argument("--sheet", required=True)
    p_tally.set_defaults(func=cmd_tally)

    p_export = sub.add_parser("export", help="write the coded sheet as JSON")
    p_export.add_argument("--sheet", required=True)
    p_export.add_argument("--out", required=True)
    p_export.set_defaults(func=cmd_export)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
