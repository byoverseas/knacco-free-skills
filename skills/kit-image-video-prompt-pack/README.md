# Product Photo & Video Prompts

Write matching image and motion prompts from one product brief, then check the product details before generating the media.

Installation is described in the [repository README](../../README.md#installation).

## First use

Give your agent a product, a place, a surface, a light story and the motion you want. It fills a brief, builds both prompts and runs the checker.

The tools also run from a terminal, inside this folder:

```sh
python3 tools/pair_builder.py --example > brief.json
python3 tools/pair_builder.py brief.json --out ./pair
python3 tools/check_pair.py pair/still.txt pair/motion.txt
```

## Contents

| Path | Use |
| --- | --- |
| `SKILL.md` | The instructions your agent loads |
| `GUIDE.md` | The full method |
| `references/` | Reference notes: wording for the nine blocks, the motion map, failure clauses and the render plan |
| `tools/` | `pair_builder.py`, `check_pair.py` and an example brief |
| `agents/openai.yaml` | Display details for Codex |

## Requirements

Python 3.9 or newer for the two included tools (standard library only). No account is needed to write or check a pair. Rendering needs your own image or video account.

## Licence and reuse

MIT licence. Free to use, change and share, including in paid client work. Keep the
copyright and licence notice with any copy you pass on.

What you make with it stays yours. Nothing here claims any right over your output, your
data or your brand. Every prompt, clause and template in this product was written for it,
so there is no third-party prompt text to clear before you use it.

The full terms are in the [licence](../../LICENSE).

## Product page

[Product Photo & Video Prompts on Knacco](https://knacco.com/en/products/kit-image-video-prompt-pack?utm_source=github&utm_medium=repository&utm_campaign=free-skills)
