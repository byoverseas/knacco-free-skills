# Brand Guide Builder

Turn existing brand assets into reusable rules, separate recorded facts from inferred choices, and check proposed documents against the brand specification.

Installation is described in the [repository README](../../README.md#installation).

## First use

Give your agent a folder of brand assets (stylesheets, theme files, logo files, imagery) and ask for an audit. It writes `brand-spec.json`, lists every inferred value, and names the owner questions the folder raises.

The tools also run from a terminal, inside this folder:

```sh
python3 tools/brand_audit.py "<your brand folder>" --out brand-spec.json
python3 tools/brand_check.py brand-spec.json output-description.json
```

## Contents

| Path | Use |
| --- | --- |
| `SKILL.md` | The instructions your agent loads |
| `GUIDE.md` | The full method |
| `references/` | Reference notes: the audit fields, the twelve owner questions and the rule blocks for your own skill |
| `tools/` | `brand_audit.py` and `brand_check.py` |
| `agents/openai.yaml` | Display details for Codex |

## Requirements

Python 3.9 or newer for the two included tools (standard library only). No brand service, account or cloud storage is involved.

## Licence and reuse

MIT licence. Free to use, change and share, including in paid client work. Keep the
copyright and licence notice with any copy you pass on.

What you make with it stays yours. Nothing here claims any right over your output, your
data or your brand. Every prompt, clause and template in this product was written for it,
so there is no third-party prompt text to clear before you use it.

The full terms are in the [licence](../../LICENSE).

## Product page

[Brand Guide Builder on Knacco](https://knacco.com/en/products/kit-brand-guide-builder?utm_source=github&utm_medium=repository&utm_campaign=free-skills)
