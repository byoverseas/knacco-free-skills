# Render plan

The pair is cheap to write and expensive to render. This plan puts the cheapest check before every paid step.

## Stage gates

| Gate | What you have | What you check | Cost |
|---|---|---|---|
| G0 | JSON brief | Required fields, one scene, one product, motion layers ≤ 4 | Free |
| G1 | Two prompt files | `check_pair.py` passes; five invariant blocks identical | Free |
| G2 | One still, low resolution | Product shape, label, placement, light, contact shadow | One image |
| G3 | One still, final resolution | Same, at full size, with the buyer's reference beside it | One image |
| G4 | One animation, draft resolution, first and last second | Hero lock, label, camera, layer count, exposure | One short video |
| G5 | Full animation | Whole clip, frame by frame at 1 fps, then real time | One final video |
| G6 | Delivery | File names, aspect, duration, colour, no watermark | Free |

Do not skip G2 to save one image. A defect at G2 costs one image; the same defect at G5 costs the whole video.

## The cost sheet

Fill this in before you start. Prices are the provider's, checked on the day; this template does not assert any price.

```
Provider: ____________________
Still model / size: __________  unit price: ______  number of attempts: ____  subtotal: ______
Video model / size: __________  price per second: ______  clip length: ____  subtotal: ______
Number of video attempts budgeted: ____  video subtotal: ______
Total budget: ______
Stop rule: if G3 fails three times, stop and change the reference or the model.
```

Example, using a hypothetical price of 0.20 per second for a 7-second clip: one final video is 1.40, and a three-attempt budget is 4.20. A single unnecessary final render costs more than the entire still stage. That is why the still is approved first.

## Prompt packaging per provider

The prompts are plain text. Keep them plain and adapt only the fields the provider owns.

| Provider field | Where it goes | Do not put it in the prompt |
|---|---|---|
| Aspect ratio | Provider UI or API field | A sentence asking for 2:3 if the field already sets it |
| Duration | Provider field | "7 seconds" repeated three times |
| Resolution | Provider field | Pixel dimensions if the model ignores them |
| Seed | Provider field, when available | A made-up seed number |
| Reference image | Provider upload | A description of the reference |
| Audio | Separate track | Sound instructions inside a silent video prompt |

If the provider has a negative-prompt field, move the `Must not appear` list there and leave a one-line summary in `GUARDRAILS`. Do not duplicate the whole list in both places; duplicated negatives can cancel each other.

## File names

```
<product>-<scene>-still-<aspect>-v<n>.png
<product>-<scene>-motion-<aspect>-<duration>s-v<n>.mp4
<product>-<scene>-brief-v<n>.json
<product>-<scene>-check-v<n>.json
```

Version every file. A pair without a version is a pair you cannot audit.

## Delivery checklist

- [ ] The still and the animation use the same five invariant blocks.
- [ ] The checker exits 0, or every remaining warning is written down and accepted.
- [ ] The product's front face is parallel to the lens in both.
- [ ] The label is legible at 100% and at thumbnail size.
- [ ] No invented text, logo or brand element.
- [ ] Motion layers ≤ 4; one light layer; camera ≤ 2% push-in.
- [ ] Exposure and white balance do not move.
- [ ] Duration and aspect match the listing.
- [ ] The buyer's reference is not embedded in the delivered prompt if it is confidential.
- [ ] The cost sheet is filled in, including failed attempts.

## What "approved" means

A still is approved when a person who knows the product says: that is the product, that is the label, that is the colour, and I would put it on the product page. An animation is approved when the same person watches it once at full size, once at thumbnail size, and once with the sound off, and the product never moves, never changes and never becomes unreadable.

If approval needs an explanation, it is not approved.
