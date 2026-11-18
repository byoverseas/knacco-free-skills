# Prompt Writing Guide

Build reusable prompts with clear facts, tasks and output examples, then identify missing or weak parts with local checks.

Installation is described in the [repository README](../../README.md#installation).

## First use

Describe the job, the material you have and the thing you do not have. Your agent fills the four parts, assembles the prompt and runs the checker before it answers.

The tools also run from a terminal, inside this folder:

```sh
python3 tools/rit.py --example > brief.json
python3 tools/rit.py brief.json --out prompt.txt
python3 tools/rit_grade.py brief.json
```

## Contents

| Path | Use |
| --- | --- |
| `SKILL.md` | The instructions your agent loads |
| `GUIDE.md` | The full method |
| `references/` | Reference notes: paste-ready blocks for each part, 24 named failures and notes on writing an example |
| `tools/` | `rit.py` and `rit_grade.py` |
| `agents/openai.yaml` | Display details for Codex |

## Requirements

Python 3.9 or newer for the two included tools (standard library only). No account and no API key.

## Licence and reuse

Free to use, including in paid client work. You may install it, use it, change it for your
own purposes, and ship whatever you make with it. You may not resell this product itself,
or redistribute it as your own.

What you make with it stays yours. Nothing here claims any right over your output, your
data or your brand. Every prompt, clause and template in this product was written for it,
so there is no third-party prompt text to clear before you use it.

The full terms are in the [licence](../../LICENSE).

## Product page

[Prompt Writing Guide on Knacco](https://knacco.com/en/products/kit-prompt-writing-system?utm_source=github&utm_medium=repository&utm_campaign=free-skills)
