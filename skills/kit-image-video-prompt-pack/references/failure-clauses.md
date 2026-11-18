# Failure clauses

Find the failure you see. Add the clause to `GUARDRAILS`. Change one thing at a time, then re-check.

## The rule of one defect

A prompt with five new clauses is a new prompt, not a repair. You will not know which clause fixed the defect, and the next product inherits all five. Name one defect, add one clause, render once, compare. If the defect persists, replace the clause; do not stack a second one.

---

## 1. The product changes

| What you see | Cause | Clause to add |
|---|---|---|
| Product grows, shrinks or changes proportion between shots | No fixed dimensions; model invents scale | `Product dimensions are fixed at <h> × <w> × <d>. The product occupies <n>% of frame height in every shot. No proportion change.` |
| Product rotates or turns to reveal another side | "Show the product" read as a turnaround | `The product does not rotate. The front face stays parallel to the lens for the whole clip. No reveal, no turn, no float.` |
| Shape drifts between still and video | Invariant blocks paraphrased | Copy the `SCENE`, `HERO`, `PLACEMENT`, `LIGHT` and `GUARDRAILS` blocks byte for byte. |
| Extra parts appear (a second handle, a lid, a strap) | Model completing a familiar object | `Exactly one <part>; no added parts, no invented hardware, no lid unless stated.` |
| Product floats above the surface | Contact shadow not described | `Base contact at <n>% frame height with a <soft> contact shadow <direction>, <length>. The product rests on the surface; it does not float.` |

## 2. The label and typography

| What you see | Cause | Clause to add |
|---|---|---|
| Letters melt, curve or duplicate | No planar instruction | `Label text is planar and vector-sharp, parallel to the lens, with no curvature, no perspective error and no duplicated letters.` |
| Invented words appear | Model fills an unreadable label | `No invented text. If a character is not legible in the reference, leave it out rather than inventing it.` |
| Label changes between still and video | Label described differently in each prompt | Repeat the exact label clause in both prompts, including punctuation. |
| Label drifts around the bottle | No fixed label placement | `Label is centred on the front face, <n> mm from the base and <n> mm from each side. Placement does not change.` |
| Logo is redrawn | Brand supplied only as a word | Supply the artwork as an image reference; add `Reproduce the supplied artwork exactly; do not redraw, extend or clean it.` |

## 3. Motion and camera

| What you see | Cause | Clause to add |
|---|---|---|
| Hero moves | "Cinematic" implies movement | `Hero motion: none. The product and label remain perfectly still and razor-sharp for the whole clip.` |
| Camera orbits or pans | Open-ended "camera move" | `Camera: locked off or push-in ≤2%. No pan, orbit, tilt, truck, handheld, zoom, crane or roll. No angle change.` |
| Everything moves at once | No layer budget | `Maximum four motion layers: <list>. All other elements are static.` |
| Motion crosses the label | No interaction rule | `<Layer> must not cross the front face or the label at any point.` |
| Focus drifts off the label | Shallow depth of field plus movement | `Focus is locked to the front face for the whole clip. No rack focus.` |
| Motion loops visibly | Window equals clip length with no easing | `<Layer> eases in at 0.4 s and settles by <end-0.4> s; no visible loop point.` |

## 4. Light and exposure

| What you see | Cause | Clause to add |
|---|---|---|
| Brightness pulses | Auto-exposure implied | `Exposure is locked for the whole clip. No auto-iris, no flicker, no brightness ramp.` |
| Colour shifts warm/cool | Auto white balance implied | `White balance is locked at <Kelvin> for the whole clip. No colour drift.` |
| Lit side changes mid-clip | Two light layers | `One light layer only: <describe>. The product's lit side does not change.` |
| Shadow doubles | Two key directions | `One key light from <direction>. One contact shadow. No duplicate shadows.` |
| Highlights clip on glass | No highlight control | `Specular highlights stay below clipping; glass edges remain visible, not blown out.` |

## 5. Material and surface

| What you see | Cause | Clause to add |
|---|---|---|
| Plastic-looking metal or ceramic | No micro-surface instruction | `Micro surface imperfections: fine roughness variation, subtle tool marks, controlled speculars. Not glossy plastic.` |
| Fabric looks like paper | No drape or weight | `Fabric has visible weight and drape, natural folds, no paper-like stiffness.` |
| Liquid looks like gel | No meniscus or refraction | `Liquid has a visible meniscus, correct refraction and a still surface unless motion is described.` |
| Wood grain repeats | Tiled texture | `Wood grain is continuous and non-repeating across the visible surface.` |
| Condensation is uniform | No droplet distribution | `Condensation is uneven: <n> droplets of mixed size, clustered near the base, none on the label.` |

## 6. Hands, people and reflections

| What you see | Cause | Clause to add |
|---|---|---|
| Extra or fused fingers | Hand in frame with no clause | `If a hand is present: five fingers, correct joints, natural contact with the product, no fused or extra digits.` |
| A person appears where none was planned | "Lifestyle" implies a model | `No people, no hands, no body parts in frame.` |
| Reflection shows a camera or crew | Mirror or glass surface | `Reflections show only the described room and the product; no camera, crew, lights or phone.` |
| Reflection duplicates the product | Two reflective planes | `One reflection only, physically correct; no duplicated product in the reflection.` |

## 7. Set and background

| What you see | Cause | Clause to add |
|---|---|---|
| Background clutter | No negative-space instruction | `Background is <surface> with <one prop> at <distance>. No additional objects.` |
| Set changes between still and video | Background described in prose, not blocks | Keep `SCENE` identical and copy it. |
| Horizon or table edge cuts the product | No placement rule | `No horizon line, table edge or frame border crosses the product silhouette.` |
| Scale reads wrong | No reference object | `A <known object> at <distance> establishes scale; the product is <n> cm tall.` |

## 8. The repair report

Write one line per round. Keep it with the prompts.

```
Round 1, defect: label letters curve at the right edge. Clause added: label text planar and vector-sharp, no curvature. Result: fixed.
Round 2, defect: steam crosses the front face at 4 s. Clause added: steam must not cross the front face. Result: fixed.
Round 3, defect: base shadow too long. Clause added: contact shadow 3 cm, camera-right. Result: fixed.
```

Three rounds is normal. If a defect survives three rounds, change the model or the reference, not the wording.
