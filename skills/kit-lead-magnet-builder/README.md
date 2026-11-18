# Lead Magnet Planner

Rank free-offer ideas for your audience and paid offer, then prepare a build specification with clear inputs, outputs and success measures.

Installation is described in the [repository README](../../README.md#installation).

## First use

Give your agent a trade, a size, a country and the paid offer with its price. It writes the bridge sentence, generates fifteen ideas, scores them and reports the top five.

The tools also run from a terminal, inside this folder:

```sh
python3 tools/score_ideas.py --example > ideas.json
python3 tools/score_ideas.py ideas.json --explain
python3 tools/spec_check.py --example > build-spec.json
python3 tools/spec_check.py build-spec.json
```

## Contents

| Path | Use |
| --- | --- |
| `SKILL.md` | The instructions your agent loads |
| `GUIDE.md` | The full method |
| `references/` | Reference notes: the scoring model, the seven shapes, the build specification and the limits on claims and consent |
| `tools/` | `score_ideas.py` and `spec_check.py` |
| `agents/openai.yaml` | Display details for Codex |

## Requirements

Python 3.9 or newer for the two included tools (standard library only). It produces a ranked idea list and a build specification, not a finished app.

## Licence and reuse

Free to use, including in paid client work. You may install it, use it, change it for your
own purposes, and ship whatever you make with it. You may not resell this product itself,
or redistribute it as your own.

What you make with it stays yours. Nothing here claims any right over your output, your
data or your brand. Every prompt, clause and template in this product was written for it,
so there is no third-party prompt text to clear before you use it.

The full terms are in the [licence](../../LICENSE).

## Product page

[Lead Magnet Planner on Knacco](https://knacco.com/en/products/kit-lead-magnet-builder?utm_source=github&utm_medium=repository&utm_campaign=free-skills)
