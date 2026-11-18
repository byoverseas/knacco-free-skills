---
name: kit-prompt-writing-system
description: "Build reusable prompts with clear facts, tasks and output examples, then identify missing or weak parts with local checks."
---

# Prompt Writing Guide

A prompt that works twice is built, not phrased. Four parts, each with one job: who is answering, what is true and what is missing, what must come back, and one passage of the output at the quality you want.

Status: **v1.0** | Category: **Frameworks** | Price: **Free**

Read [the product guide](GUIDE.md) before you write a prompt. Run the included tools from this product folder. Keep your prompts and outputs in your own workspace.

## What this framework does

1. Takes a job you would otherwise describe in one sentence.
2. Fills four parts: role, input, task, example.
3. Assembles them into one labelled prompt that a model can follow in order.
4. Checks the prompt against 14 rules and exits non-zero on a break.
5. Grades the prompt part by part, names the weakest part and the repair that buys the most.
6. Shows the test that matters: run it again with different facts and compare the shape.

## Route

- **Write a new prompt** → read `GUIDE.md`, then `python3 tools/rit.py --example > brief.json`, edit the four values, and run `python3 tools/rit.py brief.json --out prompt.txt`.
- **Find wording for one part** → `references/part-library.md`.
- **Fix a failure you can see in the output** → `references/failure-list.md`.
- **Improve a thin or average example** → `references/example-craft.md`.
- **Judge a prompt you already have** → `python3 tools/rit_grade.py prompt.txt`.

## Rules that are not negotiable

- The role names a discipline and a level of experience. It does not praise.
- The input states the situation, names at least one constraint, and says what is missing. Absent material is named, not invented.
- The task names a deliverable, its sections, its length, its register, and what the output must be usable for.
- The example is a passage of the output, not a description of it. The shape, the depth and the register, and nothing else.
- A prompt that cannot be rerun with different input is a question, not a prompt.
- The checker reads the prompt. It does not promise what the answer will be.

## Files

| File | Use |
|---|---|
| `GUIDE.md` | The full method: the four parts, the reuse test, the failure list, the voice route |
| `references/part-library.md` | Paste-ready blocks for all four parts, five variants each |
| `references/failure-list.md` | 24 named failures with symptom, cause and repair |
| `references/example-craft.md` | What a good example contains, and three ways a bad one poisons a prompt |
| `tools/rit.py` | Assembles a prompt from a JSON brief and checks it against 14 rules |
| `tools/rit_grade.py` | Grades a prompt out of 25 per part and names the weakest part |
