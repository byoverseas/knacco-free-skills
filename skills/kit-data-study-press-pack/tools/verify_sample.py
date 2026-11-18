#!/usr/bin/env python3
"""Draw a fixed sample from a coded sheet and report how often the coder was wrong.

Usage:
    python3 verify_sample.py sample --sheet sheet.csv --size 20 --out sample.csv
    python3 verify_sample.py sample --sheet sheet.csv --size 20 --out sample.csv --offset 3 --label "Study label"
    python3 verify_sample.py record --sample sample.csv --row 3 --agree --note "rule applies"
    python3 verify_sample.py record --sample sample.csv --row 7 --disagree --note "names no method"
    python3 verify_sample.py report --sample sample.csv

The sampling rule is fixed, and it is part of the file:

    1. Take every row that carries a counting decision. Excluded rows are out of frame.
    2. Sort those rows by a stable key: the source id, then the raw text, then the date,
       then the sheet row number. Sorting on the record's own content means the sample
       does not depend on the order the rows were collected in.
    3. Stride N = round(population / sample size), with halves rounded up. N is at least 1.
    4. Start at the offset (default 0) and take every Nth row until the sample is full.

The stride, the offset, the population and the drawn count are written into the sample
file's header lines. A sample cannot be re-drawn inside the same file. Drawing again
writes a new file, which is a new check and has to be reported as one.

Lines starting with # are kept and ignored, so a sample can carry its own label.
Use --label to add one when the sample is drawn.

Exit codes: 0 the command completed, 2 the command could not proceed honestly.
"""
from __future__ import annotations

import argparse
import csv
import io
import sys
from pathlib import Path

FIELDS = ["sample", "sheet_row", "id", "raw", "date", "category", "verdict", "note"]
VERDICTS = ("agree", "disagree")
RULE_BANDS = [
    (0.0, 20, "holds: publish the finding with the sample size and the bound stated"),
    (0.0, 0, "holds, but the sample is small: state the bound and do not round it away"),
    (5.0, 0, "usable after the disagreed rows are recoded and the sheet is re-tallied"),
    (10.0, 0, "requalify: narrow the claim or count again before publishing"),
]


def stop(message: str) -> "None":
    print(f"error: {message}")
    sys.exit(2)


def read_csv_with_comments(path: Path) -> tuple:
    if not path.exists():
        stop(f"no file at {path}")
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    comments = [line.rstrip("\r\n") for line in lines if line.startswith("#")]
    data = "".join(line for line in lines if not line.startswith("#"))
    reader = csv.DictReader(io.StringIO(data))
    if reader.fieldnames is None:
        stop(f"{path} has no header row")
    rows = []
    for record in reader:
        item = {key: (record.get(key) or "").strip() for key in reader.fieldnames}
        if not any(item.values()):
            continue
        rows.append(item)
    return comments, rows


def write_csv_with_comments(path: Path, comments: list, rows: list) -> None:
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=FIELDS, lineterminator="\n")
    writer.writeheader()
    for row in rows:
        writer.writerow({field: row.get(field, "") for field in FIELDS})
    path.write_text("".join(c + "\n" for c in comments) + buffer.getvalue(), encoding="utf-8")


def read_sheet(path: Path) -> tuple:
    comments, rows = read_csv_with_comments(path)
    return comments, rows


def parse_header(comments: list) -> dict:
    """Read 'key=value' pairs from a header line starting '# sample:'."""
    for comment in comments:
        body = comment.lstrip("# ").strip()
        if not body.lower().startswith("sample rule") and not body.lower().startswith("sample:"):
            continue
        pairs = {}
        for token in body.split():
            if "=" in token:
                key, value = token.split("=", 1)
                pairs[key.strip().lower()] = value.strip()
        return pairs
    return {}


def cmd_sample(args: argparse.Namespace) -> int:
    sheet = Path(args.sheet)
    _, rows = read_sheet(sheet)
    frame_all = [r for r in rows if r.get("category")]
    blocked = [r["row"] for r in rows if r.get("category") in ("", "ambiguous")]
    if blocked:
        print(f"error: the sheet still holds {len(blocked)} rows with no counting decision")
        print("rows: " + ", ".join(blocked))
        print("A sample drawn across undecided rows checks the coder against nothing.")
        print("Finish the coding, then draw the sample.")
        return 2
    frame = [r for r in frame_all if r["category"] != "excluded"]
    frame.sort(key=lambda r: (r.get("id", ""), r.get("raw", ""), r.get("date", ""), int(r["row"])))
    total = len(frame)
    if total == 0:
        stop("no coded rows; there is nothing to sample")
    size = args.size
    if size < 1:
        stop("--size must be at least 1")
    if size > total:
        print(f"note: a sample of {size} was asked for from a population of {total}; the sample is the population")
        size = total
    stride = max(1, int(total / size + 0.5))
    offset = args.offset
    if offset < 0 or offset >= total:
        stop(f"--offset must be between 0 and {total - 1}")
    picked = list(range(offset, total, stride))[:size]
    if not picked:
        stop("the stride selected no rows; check --size and --offset")

    out = Path(args.out)
    sample_rows = []
    for number, index in enumerate(picked, start=1):
        source = frame[index]
        sample_rows.append(
            {
                "sample": str(number),
                "sheet_row": source["row"],
                "id": source.get("id", ""),
                "raw": source.get("raw", ""),
                "date": source.get("date", ""),
                "category": source["category"],
                "verdict": "",
                "note": "",
            }
        )
    header = [label if label.startswith("#") else "# " + label for label in (args.label or [])]
    header.append("# Check this sample against the raw rows. Record every row, agree or disagree.")
    header.append(
        f"# sample rule: stride={stride} offset={offset} requested={args.size} drawn={len(sample_rows)} "
        f"population={total} sorted_by=id,raw,date,row"
    )
    write_csv_with_comments(out, header, sample_rows)
    print(f"sample: {out}")
    print(f"population: {total} coded rows")
    print(f"stride: {stride} (round({total} / {size})), offset {offset}")
    print(f"drawn: {len(sample_rows)} rows, from sheet rows " + ", ".join(r["sheet_row"] for r in sample_rows))
    print("")
    print("The rule is in the file's header. This sample is now fixed.")
    print("Check each raw row against its category, then record it:")
    print(f'python3 verify_sample.py record --sample {out} --row 1 --agree --note "why"')
    return 0


def cmd_record(args: argparse.Namespace) -> int:
    path = Path(args.sample)
    comments, rows = read_csv_with_comments(path)
    if len(rows) == 0:
        stop(f"{path} holds no rows")
    if bool(args.agree) == bool(args.disagree):
        stop("pass exactly one of --agree or --disagree")
    target = None
    for row in rows:
        if row.get("sample") == str(args.row):
            target = row
            break
    if target is None:
        stop(f"no sample row {args.row} in {path}; the sample has {len(rows)} rows (column 'sample')")
    target["verdict"] = "agree" if args.agree else "disagree"
    target["note"] = (args.note or "").strip()
    write_csv_with_comments(path, comments, rows)
    decided = sum(1 for r in rows if r.get("verdict") in VERDICTS)
    print(f"sample {target['sample']} (sheet row {target['sheet_row']}): {target['verdict']}")
    print(f"recorded {decided} of {len(rows)}")
    return 0


def cmd_report(args: argparse.Namespace) -> int:
    path = Path(args.sample)
    comments, rows = read_csv_with_comments(path)
    header = parse_header(comments)
    if not rows:
        stop(f"{path} holds no rows")
    missing = [r.get("sample", "?") for r in rows if r.get("verdict") not in VERDICTS]
    if missing:
        print("REFUSED: the sample is not finished.")
        print(f"sample: {path}")
        print(f"rows recorded: {len(rows) - len(missing)} of {len(rows)}")
        print("missing: " + ", ".join(missing))
        print("")
        print("A disagreement rate over a half-checked sample says nothing about the rest of it.")
        return 2

    total = len(rows)
    disagreements = [r for r in rows if r["verdict"] == "disagree"]
    k = len(disagreements)
    rate = k / total * 100

    print(f"sample: {path}")
    print(
        "rule: stride={stride} offset={offset} requested={requested} drawn={drawn} population={population}".format(
            stride=header.get("stride", "?"),
            offset=header.get("offset", "?"),
            requested=header.get("requested", "?"),
            drawn=header.get("drawn", str(total)),
            population=header.get("population", "?"),
        )
    )
    print(f"checked: {total} rows, all recorded")
    print(f"disagreements: {k} of {total}")
    print(f"disagreement rate: {rate:.1f}% ({k} of {total})")
    if k == 0:
        bound = 3 / total * 100
        print(f"95% upper bound, rule of three: {bound:.1f}% (3 / {total})")
        print("note: the rule of three is the upper bound that applies when a sample shows no disagreements.")
    else:
        print("95% upper bound, rule of three: not applicable, the sample is not zero-disagreement")
        print(f"note: {k} disagreement(s) in {total} checked rows is a point estimate over {total} rows, not a bound.")

    if k == 0:
        band = RULE_BANDS[0][2] if total >= 20 else RULE_BANDS[1][2]
    elif rate <= 5.0:
        band = RULE_BANDS[2][2]
    elif rate <= 10.0:
        band = RULE_BANDS[3][2]
    else:
        band = "unusable: do not publish this finding"
    print(f"verdict band: {band}")
    if disagreements:
        print("")
        print("disagreed rows")
        for row in disagreements:
            print(f"  sample {row['sample']:<3} sheet row {row['sheet_row']:<4} {row.get('note', '')}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Draw a fixed sample from a coded sheet and report the disagreement rate.",
        epilog="Exit 2 when the sample is incomplete or the command cannot proceed honestly.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_sample = sub.add_parser("sample", help="draw the sample by the fixed stride rule")
    p_sample.add_argument("--sheet", required=True)
    p_sample.add_argument("--size", type=int, required=True, help="how many rows to check")
    p_sample.add_argument("--out", required=True, help="path of the sample CSV to write")
    p_sample.add_argument("--offset", type=int, default=0, help="0-based start position in the sorted frame (default 0)")
    p_sample.add_argument("--label", action="append", help="a comment line to keep at the top of the sample; repeatable")
    p_sample.set_defaults(func=cmd_sample)

    p_record = sub.add_parser("record", help="record one checked row")
    p_record.add_argument("--sample", required=True)
    p_record.add_argument("--row", type=int, required=True, help="the sample number, first column of sample.csv")
    p_record.add_argument("--agree", action="store_true")
    p_record.add_argument("--disagree", action="store_true")
    p_record.add_argument("--note", default="", help="what you saw when you re-read the raw row")
    p_record.set_defaults(func=cmd_record)

    p_report = sub.add_parser("report", help="print the disagreement rate and its bound")
    p_report.add_argument("--sample", required=True)
    p_report.set_defaults(func=cmd_report)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
