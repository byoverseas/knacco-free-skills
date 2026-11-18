# Product Photo & Video Prompts

Make one product look the same in a photograph and in a short video.

You write the shot down once. The pack turns that one description into two prompts, one for a still image and one for a short animation. Five parts of the description are copied into both, word for word, so the two cannot contradict each other. The product, its label, its material and its light stay the same. Only the frame shape and the movement change.

The photograph is not a still pulled from the video, and the video is not the photograph set in motion. Both are rendered fresh from the same written description. That is what keeps the pack, the label, the glaze, the stitching and the light identical while the format changes.

## The words this pack uses

Nothing below needs learning before you start. Come back when a word gets in the way.

| Word | What it means here |
| --- | --- |
| Brief | Your written description of the shot. A small file, not a paragraph in an email |
| Block | One part of that description, such as the light or the placement |
| Must not change | Copied into both prompts without a single word changed |
| Pair | The two prompts together: the photograph prompt and the video prompt |
| Motion layer | One thing that moves in the clip, such as steam |
| Motion map | A short table saying what moves, how far, and when |
| Camera budget | How much the camera is allowed to move, given as a percentage |
| Guardrails | The list of things that must not change or must not appear |
| Render | One image or video produced by an AI tool from a prompt |

Two things worth knowing before section 1. The pack writes text, not images: you paste the prompts into whatever image and video tool you already pay for. And the checker only compares the two prompts against each other. It cannot see how a particular tool will interpret them, so it catches a disagreement between your own instructions, not a bad render.

---

## 1. The problem this solves

A product campaign usually fails in one of four places.

1. **The pair disagrees.** The still says warm oak and the video says pale marble. The bottle is 24 cm tall in one and 31 cm in the other. The label is crisp in the still and mush in the video.
2. **The hero moves.** The model reads "cinematic product film" and invents a slow rotation. The label leaves the lens, the geometry warps, and the shot is unusable.
3. **The motion is unbounded.** Steam, dust, light, a curtain, a droplet and a camera push all happen at once. Nothing reads. The eye has no resting place.
4. **The money is spent before the look is approved.** The still was never checked, so the expensive video inherits the defect at 10× the cost.

The fix is procedural, not a better adjective. Write the scene once. Split it into blocks that must not change and blocks that must. Lock the hero. Give motion a budget with an owner for every layer. Check the pair before you pay for anything.

---

## 2. The nine blocks

Write the blocks in this order. The order is the contract: a reader (or a model) can find any instruction without hunting through prose.

| # | Block | What it fixes | Changes between still and motion? |
|---|---|---|---|
| 1 | `SCENE` | Place, time, materials, weather, scale of the room | No |
| 2 | `HERO` | The product, its surfaces, label integrity, exact geometry | No |
| 3 | `PLACEMENT` | Position in frame, support surface, contact shadow, distances | No |
| 4 | `OPTICS` | Lens, distance, aperture, shutter, ISO look, WB, filter, framing | **Yes, frame and aspect only** |
| 5 | `LIGHT` | Key, fill, rim, lights in the shot, flags, falloff | No |
| 6 | `ATMOSPHERE` | Haze, particles, droplets, light patterns on surfaces, bloom | No |
| 7 | `MOTION` | What moves, how far, when, camera budget | **Yes, still says none** |
| 8 | `GUARDRAILS` | What must not change, what must not appear, physics, exposure lock | No |
| 9 | `OUTPUT` | Aspect, pixels, duration, fps, codec | **Yes** |

Five blocks must not change: 1, 2, 3, 5 and 8. The pair builder copies them character for character. If you edit one, you edit it in the brief and rebuild both prompts. Never hand-edit one side of the pair.

### Why `OPTICS` is only partly variable

The lens, distance, aperture and the filter on the lens belong to the look and must not change. The frame and aspect do change: 2:3 for the still, 9:16 for the animation. So `OPTICS` is one block with two zones:

- **Fixed optics:** lens, distance, aperture, shutter, ISO look, white balance, filter.
- **Variable frame:** aspect, orientation, subject height in frame, headroom, empty space.

If the still is 2:3 and the animation is 9:16, the product cannot occupy the same percentage of the frame in both. Decide which one is the master. Usually the still is the master for catalogue and the animation is a safe reframe. State the reframing rule in `PLACEMENT`: for example, "in 9:16 the product sits at 52% frame height, centred, with the same base contact point and the same front-face angle."

---

## 3. The one-change rule

A pair holds when exactly one thing changes at a time:

- **Shape:** one frame change (2:3 → 9:16), one rule for how the product is reframed.
- **Time:** one motion plan (none → five layers), one camera budget.
- **Everything else:** identical.

This is why the method copies blocks instead of rewriting them. Paraphrase is where drift enters. "Warm oak counter" and "light wooden worktop" are the same idea and two different materials to a model.

Write the blocks that must not change as short, measurable lines:

```
SCENE: A working pottery studio at 7am, north-facing window, lime-washed wall, pale oak bench, one linen cloth at the right edge.
HERO: A 320 ml stoneware mug, 9.2 cm tall, 8.4 cm diameter, matte oatmeal glaze, unglazed foot ring, straight D-handle on the right, no text, no logo.
PLACEMENT: Base contact at 58% frame height, centred on the vertical third, front face parallel to the lens, 6 cm of bench visible in front, linen cloth 40 cm behind, soft contact shadow under the foot ring.
```

A model can hold those. It cannot hold "a nice mug in a lovely studio".

---

## 4. The motion budget

The hero is locked. Motion belongs to the world. Give every layer four values:

| Value | Meaning | Example |
|---|---|---|
| Layer | What physically moves | Steam from the mug |
| Amplitude | How far or how much something moves. The word the motion map prints | 3 to 6 cm of curl, opacity 8 to 14% |
| Window | When it happens inside the clip | 0.5-6.5 s, continuous |
| Interaction | What it must not touch | Must not cross the front face or the handle |

Rules:

- **Maximum five layers.** Four is better. One layer should be the slowest and quietest; it gives the eye a resting place.
- **Exactly one layer may be light.** A shadow shift, a caustic sweep or a specular pass. Not two.
- **No layer may cross the hero's front face** unless the brief says the product is meant to be obscured (for example, a steam-covered drink). Even then, the label stays readable.
- **Camera:** a push-in of 2% or less, or a locked-off frame. No pan, no orbit, no tilt, no handheld, no rack focus off the label.
- **Exposure and WB:** locked. No auto-iris, no flicker, no colour drift.
- **Physics:** one gravity direction, one airflow direction, consistent surface wetness, correct contact shadows.

A motion map is a small table, written before the prompt:

```
0.0-7.0 s  steam        amplitude 3 to 6 cm, opacity 8 to 14%, curls up and camera-left, never crosses the front face
0.0-7.0 s  dust         amplitude 1 to 2 px, 6 to 10 motes, slow drift camera-right
1.5-5.5 s  light        1 shadow edge moves 4 cm across the bench, no change to the product's lit side
2.0-2.8 s  droplet      one droplet forms at the base, slips 8 mm, stops
0.0-7.0 s  camera       push-in 2%, no angle change, focus on the front face
```

The animation prompt contains the map in words. The checker reads the camera line and the hero-lock line. The render plan uses the map to decide which layers are worth paying for.

---

## 5. Writing the still so it can become motion

The still is not a dead image. It is the first frame of a scene that already contains the motion sources.

- Put the motion source **in frame** but outside the hero's silhouette: a window, a candle, a steam source, a water surface, a curtain edge, a doorway with practical light.
- Describe the surface state that motion will change: dry bench, condensation ring, dust on the glass, water in a tray.
- Leave empty space where the motion can read. A frame filled edge to edge has nowhere for steam to curl.
- Do not bake motion into the still prompt ("swirling steam") if the still is meant to be a clean catalogue image. Use "a thin steam source at the rim, not yet visible as a plume" or accept a still with the plume.

The pair works when the still shows the world that *could* move, and the animation shows the same world *actually* moving.

---

## 6. Review before you pay

Run the checker first:

```sh
python3 tools/check_pair.py still.txt motion.txt
```

Then review the pair by eye, in this order:

1. **Read the five blocks that must not change aloud.** If any line differs by a word, rebuild.
2. **Find the hero.** Is its front face parallel to the lens in both? Is the base contact point the same? Is the height in frame consistent with the reframing rule?
3. **Find the label.** Is it planar, vector-sharp, and free of invented text? If the product has no label, does the prompt say so?
4. **Count the motion layers.** More than five? Cut one. Is any layer touching the front face? Move it.
5. **Check the camera line.** Any angle change is a fail, not a warning.
6. **Check the guardrails.** Exposure lock, WB lock, no redesign, one gravity, no extra objects, no hands unless planned.
7. **Only then render the still.** Approve the still. Then render the animation at the lowest acceptable resolution, check the first and last second, then finish.

The render plan template in `references/render-plan.md` puts a cost against each step so a failed pair is caught at the cheapest stage.

---

## 7. What this skill does not do

- It does not generate images or video. You use your own provider and pay that provider.
- It does not upload references or choose a model for you.
- It does not guarantee that a model follows the prompt. It makes the prompt checkable and the failure visible early.
- It does not invent a brand, logo or label. If the product has one, supply a reference image and describe it as fixed.
- It does not write a campaign strategy. It writes one scene as a still and a motion pair.

---

## Sources and reuse

Source references: a licensed collection of 25 paired still-and-motion product scenes and the method in Product Scene Briefs. Source prompts are not included or redistributed. See `README.md` for the product licence and reuse terms.
