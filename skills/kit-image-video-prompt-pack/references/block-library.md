# Block library

Wording you can paste. Keep each block short, declarative and measurable. Replace every `<angle-bracket>` field. Never paraphrase an invariant block between the still and the animation.

---

## 1. `SCENE`

Name the room, the time, the materials and the scale. One sentence for the place, one for the surfaces, one for what is out of focus.

```
A working <room type> at <time of day>, <one architectural detail>, <one material detail>. The bench is <material and finish>; <one prop> sits at the <edge>. Background falls away at <distance>.
```

Example: *A working pottery studio at 7am, north-facing window with original steel glazing, lime-washed wall. The bench is pale oak with a worn front edge; a folded linen cloth sits at the right edge. Background falls away at 2.4 m.*

**Avoid:** "beautiful", "moody", "aesthetic", "perfect". They carry no instruction.

---

## 2. `HERO`

Product, dimensions, material, surface finish, construction details, label state. State what must not change.

```
A <product> measuring <height> × <width> × <depth>, <material>, <finish>, <one construction detail>, <one wear detail>. <Label clause>. Geometry is fixed; no redesign, no added parts, no proportion change.
```

Label clause, choose one:

- **Has a label:** `The label reads exactly "<text>"; label text is planar and vector-sharp, with no invented characters, no curvature and no perspective error.`
- **No label:** `No text, no logo, no label and no embossed wordmark anywhere on the product.`
- **Buyer's own artwork:** `The supplied artwork is reproduced exactly: same crop, same colours, same type. Do not redraw, extend or clean it.`

**Avoid:** naming a brand the buyer has not supplied. Describe the object, not its marketing.

---

## 3. `PLACEMENT`

Frame position, support, contact, distances, and the recomposition rule for the other aspect.

```
Base contact at <n>% frame height, <horizontal position>, front face <angle>. <n> cm of <surface> in front; <prop> at <distance> behind. Contact shadow: <soft/hard>, <direction>, <length>. In 9:16 the product sits at <n>% frame height, centred, with the same base contact point and the same front-face angle.
```

Example: *Base contact at 58% frame height, centred on the vertical third, front face parallel to the lens. Six centimetres of bench in front; linen cloth 40 cm behind. Contact shadow: soft, camera-right, 3 cm. In 9:16 the product sits at 52% frame height, centred, with the same base contact point and the same front-face angle.*

**Why the recomposition rule matters:** a 2:3 frame and a 9:16 frame cannot hold the same percentage of product. Decide the change in advance or the pair will disagree.

---

## 4. `OPTICS`

Two zones: fixed optics and variable frame.

```
Fixed: <focal length> <prime/zoom>, <distance> from the front face, <aperture>, shutter <angle> look, ISO look <value>, white balance <Kelvin>, <filtration or "no filtration">. Focus on the front face; depth of field <what is sharp>.
Frame, still: 2:3, <pixels>, product occupies <n>% of frame height, <headroom>, <negative space>.
Frame, motion: 9:16, <pixels>, product occupies <n>% of frame height, same base contact point.
```

Lens choices and what they do:

| Focal length | Distance | Character | Use for |
|---|---|---|---|
| 50 mm | 1.2-1.6 m | Natural, mild compression | A product in a room, with context |
| 85 mm | 0.8-1.1 m | Flattering compression, creamy falloff | Hero packshots, label-first |
| 100 mm macro | 0.35 to 0.5 m | Surface detail, shallow plane | Texture, droplets, stitching |
| 35 mm | 1.5-2.2 m | Wide context, slight edge stretch | Lifestyle, product small in a world |
| 24 mm | 2 to 3 m | Environmental, strong perspective | A product as part of a scene |

**Avoid:** "bokeh" as a standalone instruction. Say what is sharp and what falls away.

---

## 5. `LIGHT`

Key, fill, rim, practicals, flags, falloff, colour temperature. One direction per source.

```
Key: <source> from <direction>, <hard/soft>, <Kelvin>, flagged so the front face is <even/raking>. Fill: <source> from <direction> at <low level>. Rim: <source> from <direction>, <width>. Practicals: <source> at <distance>, <colour>. Falloff: <where it goes dark>.
```

**Avoid:** "cinematic lighting". It is a mood word, not a source.

---

## 6. `ATMOSPHERE`

Only what is physically present. Every atmospheric element must have a source and a place.

```
<Thin/thick> <haze/steam/dust>, source at <place>, density <low/medium>. <n> droplets on <surface>. <caustics/bloom> from <source>. No fog on the lens.
```

**Avoid:** stacking four atmospherics. Two is usually enough; the motion block will use them.

---

## 7. `MOTION`

Still:

```
Motion: none. A still photograph. No motion blur, no ghosting, no implied movement, no double edges.
```

Animation:

```
Hero motion: none. The product and its label remain perfectly still and razor-sharp for the whole clip.
Camera: <locked off / push-in n%>, no angle change, no pan, no orbit, no tilt, no handheld, no zoom, no rack focus off the front face.
Layer 1, <name>: <amplitude>, <window>, <direction>, <interaction rule>.
Layer 2 ...
Exposure and white balance locked for the whole clip. No auto-iris, no flicker, no colour drift.
```

Use the five-layer budget in `motion-map.md`.

---

## 8. `GUARDRAILS`

The shortest block that prevents the expensive failures.

```
Must not change: product geometry, proportions, label text, label placement, surface finish, base contact point, front-face angle, lit side, exposure, white balance.
Must not appear: extra products, hands, people, text, logos, watermarks, UI, frames, borders, duplicate shadows.
Physics: one gravity direction, one airflow direction, correct contact shadow, no floating parts, no fused or extra digits if a hand is present.
Do not redesign, restyle or "improve" the product.
```

Add the specific clauses from `failure-clauses.md` for the failures you have already seen with this product or this model.

---

## 9. `OUTPUT`

```
Still: 2:3, 2048 × 3072 or the model's native 2:3, sRGB, PNG, no border.
Motion: 9:16, 1080 × 1920 (draft) or 1440 × 2560 (final), <duration> s, <fps> fps, H.264 high bitrate, no audio unless supplied.
```

Render the draft at the lower size. Approve it. Then finish. Do not pay for a final resolution before the pair passes the checker and your eye.

---

## Short example (one product, two formats)

```
[SCENE]
A working pottery studio at 7am, north-facing window with original steel glazing, lime-washed wall. The bench is pale oak with a worn front edge; a folded linen cloth sits at the right edge. Background falls away at 2.4 m.

[HERO]
A 320 ml stoneware mug measuring 9.2 cm tall and 8.4 cm in diameter, matte oatmeal glaze with fine iron speckle, unglazed foot ring, straight D-handle on the right. No text, no logo, no label and no embossed wordmark anywhere on the product. Geometry is fixed; no redesign, no added parts, no proportion change.

[PLACEMENT]
Base contact at 58% frame height, centred on the vertical third, front face parallel to the lens. Six centimetres of bench in front; linen cloth 40 cm behind. Contact shadow: soft, camera-right, 3 cm. In 9:16 the product sits at 52% frame height, centred, with the same base contact point and the same front-face angle.

[OPTICS]
Fixed: 85 mm prime, 0.9 m from the front face, T2.0, shutter 180° look, ISO look 400, white balance 5200 K, Black Pro-Mist 1/8. Focus on the front face; the handle and the near bench edge are sharp, the wall falls away.
Frame, still: 2:3, 2048 × 3072, product occupies 34% of frame height, 8% headroom, negative space camera-right.
Frame, motion: 9:16, 1080 × 1920, product occupies 26% of frame height, same base contact point.

[LIGHT]
Key: north window from camera-left, soft, 5200 K, flagged so the front face is evenly lit with a gentle falloff to camera-right. Fill: white card from camera-right at low level. Rim: none. Practicals: a warm 2700 K bulb in the hallway behind, out of focus. Falloff: the back wall goes one stop darker.

[ATMOSPHERE]
Thin steam from the mug, source at the rim, density low. Nine dust motes in the window shaft. No fog on the lens.

[MOTION]
Motion: none. A still photograph. No motion blur, no ghosting, no implied movement, no double edges.

[GUARDRAILS]
Must not change: product geometry, proportions, glaze, handle, base contact point, front-face angle, lit side, exposure, white balance.
Must not appear: extra mugs, hands, people, text, logos, watermarks, UI, frames, borders, duplicate shadows.
Physics: one gravity direction, correct contact shadow, no floating parts.
Do not redesign, restyle or "improve" the product.

[OUTPUT]
Still: 2:3, 2048 × 3072, sRGB, PNG, no border.
```
