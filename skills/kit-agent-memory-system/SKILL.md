---
name: kit-agent-memory-system
description: "Organize workspace, project and campaign decisions in readable memory files, then check for stale information, conflicting records and missing details."
---

# AI Project Memory

Three levels of memory, one boundary between them, and a folder on disk that survives a change of provider. The folder is five sections of plain Markdown per project. The auditor checks it.

Status: **v1.0** | Category: **Frameworks** | Price: **Free**

Read [the product guide](GUIDE.md) before you write a card. Run the included tools from this product folder. Keep your cards in your own workspace, not in this package.

## What this skill does

1. Separates memory into three levels: who you are, one project in progress, and a record on disk.
2. Sets the boundary that stops the levels contradicting each other: one home per fact.
3. Gives a project one card with five fields, the third of which is the reason the folder is worth keeping.
4. Sets up the folder tree with `tools/memory_init.py`, one card per project, an index beside them.
5. Audits the tree with `tools/memory_audit.py`, which finds a stale section, a contradiction across levels, a decision with no reason, a name leaked from a project, a section past a readable size, and a heading with nothing under it.

## Route

- **Set up a memory from nothing** → read `GUIDE.md`, then run `python3 tools/memory_init.py --workspace "<name>" --out ./memory`.
- **Add a project** → `python3 tools/memory_init.py --project "<name>" --out ./memory --workspace ./memory`.
- **Add a time-boxed piece of work** → the same command with `--campaign`.
- **Decide where a fact belongs** → `references/level-boundaries.md`, with a row for each kind of fact that turns up in working memory and the row it is usually misfiled into.
- **Write or repair one card** → `references/memory-md-shape.md`, field by field, with a good and a useless entry for each.
- **Check a tree before you rely on it** → `python3 tools/memory_audit.py ./memory`.
- **Understand a finding** → `references/audit-rules.md`, one section per rule with a worked failure.

## Rules that are not negotiable

- One fact, one home. A fact that lives in two levels will disagree with itself, and the copy inside the session wins.
- Level one carries no project state. It is read in every session, including sessions about other work.
- Level two does not restate level one. Two copies drift, and the project copy is the one the model reads.
- Level three records the summary and the reasons. It is not a transcript and not a file dump.
- A decision is written with its reason, in the same line. A decision without a reason is a changelog entry, and the audit fails it.
- Every section carries the date it was last confirmed. A section with no date cannot be checked.
- A proper noun that belongs to one project does not appear on the workspace card.
- One section stays under 40 lines. If it does not fit, the section is holding history that belongs in the decisions list, or two subjects that belong on two cards.
- The card is evidence you can check, not a promise that the model read it.

## Files

| File | Use |
|---|---|
| `GUIDE.md` | The full method: three levels, the boundary, the card, update and prune rules, four failure modes, portability, migration |
| `references/memory-md-shape.md` | The standard card, field by field, with a good and a useless entry for each |
| `references/level-boundaries.md` | Every kind of fact, which level owns it, and why |
| `references/audit-rules.md` | The rules `memory_audit.py` enforces, with a worked failure for each |
| `tools/memory_init.py` | Sets up a workspace, a project card or a campaign card |
| `tools/memory_audit.py` | Audits a tree and names every finding with a file and a line |
