# AI Project Memory

Organize workspace, project and campaign decisions in readable memory files, then check for stale information, conflicting records and missing details.

Installation is described in the [repository README](../../README.md#installation).

## First use

Choose a memory folder outside the installed skill, create the first cards with the commands below, and fill them in any editor. Point your agent at the project card at the start of a session and have it write the card back at the end.

The tools also run from a terminal, inside this folder:

```sh
python3 tools/memory_init.py --workspace "<your name or studio>" --out "<memory folder>"
python3 tools/memory_init.py --project "<first project>" --out "<memory folder>" --workspace "<memory folder>"
python3 tools/memory_audit.py "<memory folder>"
```

## Contents

| Path | Use |
| --- | --- |
| `SKILL.md` | The instructions your agent loads |
| `GUIDE.md` | The full method |
| `references/` | Reference notes: the card shape, the boundaries between the three levels and the audit rules |
| `tools/` | `memory_init.py` and `memory_audit.py` |
| `agents/openai.yaml` | Display details for Codex |

## Requirements

Python 3.9 or newer for the two included tools (standard library only). Nothing leaves your machine.

## Licence and reuse

MIT licence. Free to use, change and share, including in paid client work. Keep the
copyright and licence notice with any copy you pass on.

What you make with it stays yours. Nothing here claims any right over your output, your
data or your brand. Every prompt, clause and template in this product was written for it,
so there is no third-party prompt text to clear before you use it.

The full terms are in the [licence](../../LICENSE).

## Product page

[AI Project Memory on Knacco](https://knacco.com/en/products/kit-agent-memory-system?utm_source=github&utm_medium=repository&utm_campaign=free-skills)
