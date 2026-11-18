---
name: kit-brand-guide-builder
description: "Turn existing brand assets into reusable rules, separate recorded facts from inferred choices, and check proposed documents against the brand specification."
---

# Brand Guide Builder

A folder of brand assets is not a brand skill. A brand skill is a written set of rules an agent applies without being asked, and it can only be built from an audit of what the brand actually does.

Status: **v1.0** | Category: **Skills** | Price: **Free**

Read [the product guide](GUIDE.md) before you run an audit. Run the included tools from this product folder. Keep your brand files in your own workspace.

## What this skill does

1. Takes a folder of brand assets: stylesheets, theme files, logo files, imagery, notes.
2. Runs `tools/brand_audit.py` over the folder and writes `brand-spec.json` with a ranked palette, named colour roles, the type hierarchy, logo variants and clear space, imagery rules, safe contrast pairings and anti-patterns.
3. Marks every value it could not read from a declaration as `"source": "inferred"` and lists its path in `unconfirmed`.
4. Puts the twelve owner questions to the brand owner and records the answers against those paths.
5. Hands you the rule blocks in `references/skill-rules.md` to paste into the skill you build, and checks each output with `tools/brand_check.py` before it ships.

## Route

- **Audit a folder** → `python3 tools/brand_audit.py <folder> --out brand-spec.json --json`, then read `GUIDE.md` section 4 before you trust a single value.
- **Ask the owner** → `references/owner-questions.md`. All twelve, even when the audit raises only one.
- **Build the skill** → `references/skill-rules.md`. Paste the blocks into the skill, fill the confirmed values, keep the refusal rules.
- **Check one output** → `python3 tools/brand_check.py brand-spec.json output-description.json`. Twelve rules, a score, exit 2 on a fail.
- **Check prose** → point the checker at a text file. It checks the palette, the type sizes and the brand name, and skips the rules prose cannot carry.

## Rules that are not negotiable

- **The audit comes before the skill.** A skill written from a folder without an audit is a set of guesses with brand vocabulary.
- **Every inferred value is confirmed by the owner.** A rule built on an unconfirmed inference is worse than no rule.
- **The spec is the only source of colour, type and logo.** The built skill does not carry its own copy of the palette.
- **The skill applies the brand.** It does not redesign it, improve it or modernise it.
- **No logo is ever redrawn, restretched or rebuilt from a description.** The file is used as it is, or the output ships without one.
- **The checker runs before delivery.** A brand break found by the owner is a different problem from one found by the checker.

## Files

| File | Use |
|---|---|
| `GUIDE.md` | The full method: collect, audit, build, and why the order cannot be reversed |
| `references/audit-fields.md` | Every field in the brand spec: type, how it is derived, read or inferred |
| `references/skill-rules.md` | Paste-ready rule blocks for the skill you build |
| `references/owner-questions.md` | The twelve questions, with what goes wrong when one is skipped |
| `tools/brand_audit.py` | Walks a folder and writes `brand-spec.json` |
| `tools/brand_check.py` | Twelve rules against one proposed output, scored out of 100 |
