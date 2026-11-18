---
name: kit-image-video-prompt-pack
description: "Write matching image and motion prompts from one product brief, then check the product details before generating the media."
---

# Product Photo & Video Prompts

One scene brief becomes two prompts that cannot disagree: a still and an animation. The product, its placement and its light are written once and copied into both. Only the frame and the motion change.

Status: **v1.0** | Category: **Skills** | Price: **Free**

Read [the product guide](GUIDE.md) before writing a pair. Run the included tools from this product folder. Keep your briefs, prompts and renders in your own workspace.

## What this skill does

1. Takes a product, a place, a surface, a light story and a motion idea.
2. Writes a nine-block scene brief once.
3. Emits a **2:3 still prompt** with motion switched off.
4. Emits a **9:16 animation prompt** that reuses the same five blocks word for word, unchanged and adds a motion map with a hard budget.
5. Checks the pair with `tools/check_pair.py` before anything paid runs.

## Route

- **Write a new pair** → read `GUIDE.md`, then copy `tools/brief.example.json`, edit it, run `python3 tools/pair_builder.py brief.json --out ./out`.
- **Check a pair you already have** → `python3 tools/check_pair.py still.txt motion.txt`.
- **Choose motion that will not move the product** → `references/motion-map.md`.
- **Fix a specific failure** (label mush, drift, flicker, plastic look, warped geometry) → `references/failure-clauses.md`.
- **Plan the render and its cost** → `references/render-plan.md`.

## Rules that are not negotiable

- The hero does not move. No rotation, no turn, no float, no reveal, no hand entering frame.
- The camera does not change angle. A push-in of 2% or less is the whole camera budget.
- The five blocks that must not change are copied, not rewritten, between the still and the animation.
- Label and typography are described as planar and vector-sharp, or the product is described as unlabelled.
- Exposure and white balance are locked in the animation.
- No brand name, logo or livery is invented. If the buyer's product carries one, it comes from their own reference image.

## Files

| File | Use |
|---|---|
| `GUIDE.md` | The full method: block order, the blocks that must not change, motion budget, review checklist |
| `references/block-library.md` | Wording for each of the nine blocks |
| `references/motion-map.md` | How to write timed motion layers that cannot touch the hero |
| `references/failure-clauses.md` | Failure → cause → exact clause to add |
| `references/render-plan.md` | Still-first render plan, approval gates and cost sheet |
| `tools/pair_builder.py` | Builds both prompts and the motion map from one JSON brief |
| `tools/check_pair.py` | Scores a pair and names every break |
