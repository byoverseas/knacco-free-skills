# Data Research & Press Kit

Plan a focused data study, check a sample of the records, and prepare findings and press materials with a documented method.

Installation is described in the [repository README](../../README.md#installation).

## First use

Give your agent one question, the group it concerns, and the source you can reach. Ask it to run the six question tests and write the source paragraph before it collects anything.

The tools also run from a terminal, inside this folder:

```sh
python3 tools/study_sheet.py init --out sheet.csv --categories delivery,collection,both,neither --title "Your study title"
python3 tools/study_sheet.py tally --sheet sheet.csv
python3 tools/verify_sample.py sample --sheet sheet.csv --size 60 --out sample.csv
python3 tools/press_pack.py FINDINGS.md PRESS-PACK.md
```

## Contents

| Path | Use |
| --- | --- |
| `SKILL.md` | The instructions your agent loads |
| `GUIDE.md` | The full method |
| `references/` | Reference notes: the question tests, the source types, the verification protocol and the press pack shape |
| `tools/` | `study_sheet.py`, `verify_sample.py` and `press_pack.py` |
| `agents/openai.yaml` | Display details for Codex |

## Requirements

Python 3.9 or newer for the three included tools (standard library only). The tools never use the network; you collect the data yourself.

## Licence and reuse

MIT licence. Free to use, change and share, including in paid client work. Keep the
copyright and licence notice with any copy you pass on.

What you make with it stays yours. Nothing here claims any right over your output, your
data or your brand. Every prompt, clause and template in this product was written for it,
so there is no third-party prompt text to clear before you use it.

The full terms are in the [licence](../../LICENSE).

## Product page

[Data Research & Press Kit on Knacco](https://knacco.com/en/products/kit-data-study-press-pack?utm_source=github&utm_medium=repository&utm_campaign=free-skills)
