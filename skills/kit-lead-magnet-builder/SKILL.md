---
name: kit-lead-magnet-builder
description: "Rank free-offer ideas for your audience and paid offer, then prepare a build specification with clear inputs, outputs and success measures."
---

# Lead Magnet Planner

Five stages: define the niche and the offer, generate fifteen ideas across seven shapes, score them, choose one, write the build spec. Four stages are thinking. The fifth is a document a coding tool can execute without inventing anything.

Status: **v1.0** | Category: **Workflows** | Price: **Free**

Read [the product guide](GUIDE.md) before writing a spec. Run the included tools from this product folder. Keep your idea files, specs and build in your own workspace.

## What this skill does

1. Turns a trade and a paid offer into a bridge sentence that names the figure the offer starts from.
2. Generates fifteen lead magnet ideas across seven recognised shapes: calculator, assessment, swipe file, template pack, checklist, short course, data lookup.
3. Scores every idea on six criteria with fixed weights, and ranks them deterministically with `tools/score_ideas.py`.
4. Applies the three questions and the five input cap to the top five, then records the choice and the reason.
5. Writes the eleven field build spec and checks it with `tools/spec_check.py` before any build starts.

## Route

- **Start a new run** → read `GUIDE.md` stage 1, write `niche.md` with the niche line, the offer line and the bridge.
- **Generate ideas** → `GUIDE.md` stage 2 and `references/shape-library.md`, then write fifteen entries in an ideas file.
- **Score them** → `python3 tools/score_ideas.py ideas.json --explain`. Add `--top 3` for a shorter table or `--json` for machine output.
- **Choose one** → `GUIDE.md` stage 4. Answer the three questions for the top five and record the decision.
- **Write the spec** → `references/build-spec-shape.md`, then `python3 tools/spec_check.py build-spec.json`.
- **Disagree with a ranking** → read the per-criterion contribution, rescore the criterion you dispute, rerun, and write the argument down.
- **Understand a score** → `references/scoring-model.md` has the anchors for every point on every scale.
- **Check a claim or a gate** → `references/ethics-and-limits.md`.

## Rules that are not negotiable

- The paid offer is named, with a price, before the first idea is written. A magnet with no far bank is a quiz.
- Fifteen ideas across all seven shapes, written before any of them is scored.
- The six weights are fixed at 25, 20, 15, 15, 10 and 15. A change to a weight is an edit to the script with the reason written beside it, and it invalidates older rankings.
- Any idea needing more than five inputs is cut, whatever it scores.
- The gate comes after partial value. The first screen never asks for an email address.
- No guarantee, no diagnosis, and no projection presented as a forecast. The tool reports arithmetic over the user's own numbers.
- A margin under five points is an argument, not a decision, and the argument is written down with the criterion it rests on.
- Nothing is built until the spec passes `tools/spec_check.py`.

## Files

| File | Use |
|---|---|
| `GUIDE.md` | The five stages, the weights, the input cap, the gate rule, the review order |
| `references/scoring-model.md` | The six criteria in detail, the anchors for 1 to 5, and a fully scored idea |
| `references/build-spec-shape.md` | The eleven fields, with a bad answer and a filled example for each |
| `references/shape-library.md` | The seven shapes with cost, timing, best use and failure mode |
| `references/ethics-and-limits.md` | Claims allowed and refused, consent at the gate, data not to collect |
| `tools/score_ideas.py` | Ranks ideas on fixed weights, explains every contribution, exits 2 on bad input |
| `tools/spec_check.py` | Checks the eleven fields and seven build-stopping omissions, score out of 100 |
