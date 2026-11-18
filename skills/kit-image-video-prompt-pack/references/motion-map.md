# Motion map

A motion map is the plan the animation prompt describes and the editor checks. It is written before the prompt, not after the render.

## The budget

| Limit | Value | Why |
|---|---|---|
| Motion layers | 5 maximum, 4 preferred | The eye can follow four things; five is the ceiling |
| Light layers | 1 | Two light changes read as a mistake |
| Camera moves | 1, and only a push-in of 2% or less | Any angle change re-renders the product |
| Hero motion | 0 | The product is the fixed point |
| Focus racks | 0 | A rack off the label is a lost frame |
| Duration | 5 to 10 s | Long enough for a loop, short enough to keep detail |
| Frame rate | 24, 25 or 30 fps | 24 for film feel, 30 for phone-native |

## Layer types

Every layer is one of six physical families. Name the family, then the specific event.

| Family | Examples | Typical amplitude | Typical window |
|---|---|---|---|
| Air | Steam, smoke, breath, curtain movement | 3 to 8 cm of travel, opacity 8 to 14% | Continuous, 0-end |
| Particle | Dust, pollen, flour, sand, ash | 1 to 3 px, 4 to 12 particles | Continuous |
| Water | Droplet forming, condensation slip, ripple, spray | 2 to 10 mm | One event, 1 to 3 s |
| Light | Shadow edge, caustic sweep, specular pass, practical flicker | 2 to 6 cm or 5 to 10% intensity | One event, 2 to 4 s |
| Surface | Fabric settling, paper edge lifting, smoke leaving a surface | 2 to 5 mm | One event |
| Camera | Push-in, locked-off | ≤2% scale | Whole clip |

## Writing a layer

```
Layer 3, condensation slip: one droplet forms at the base of the bottle at 2.0 s, grows to 4 mm, slips 8 mm down the glass and stops by 2.8 s. It must not cross the label or change the label's sharpness.
```

A layer is complete when it has **a start, an end, an amplitude, a direction, and a prohibition**.

## The interaction rule

Each layer gets one sentence about what it must not touch. This is the part most prompts omit, and it is the part that protects the hero.

- Steam must not cross the front face.
- Dust must not land on the product.
- Shadow must not change the product's lit side.
- Droplet must not cross the label.
- Fabric must not touch the base.
- Camera must not change the front-face angle.

## Four ready-made maps

### A. Quiet studio (ceramics, leather, wood, stationery)

```
0.0-7.0  steam      3 to 6 cm curl, opacity 8 to 12%, camera-left, never crosses the front face
0.0-7.0  dust       6 to 10 motes, 1 to 2 px, slow drift camera-right
1.5-5.5  light      one shadow edge moves 4 cm across the bench; lit side unchanged
2.0-2.8  droplet    one 4 mm droplet forms and slips 8 mm at the base
0.0-7.0  camera     push-in 2%, no angle change
```

### B. Night glass (fragrance, jewellery, watches, electronics)

```
0.0-6.0  particles  pollen or dust, 8 to 14 motes, 1 to 2 px, mixed depths
0.5-5.5  light      one caustic sweep across the plinth, 5 to 8% intensity
1.8-3.0  water      one condensation slip, 3 to 5 mm, stops above the label
3.0-5.0  bloom      specular bloom breathes 5%, no exposure change
0.0-6.0  camera     locked off
```

### C. Morning kitchen (food, drink, appliances, packaging)

```
0.0-8.0  steam      4 to 8 cm, opacity 10 to 16%, rises and bends camera-right
0.0-8.0  light      window shaft holds; one dust mote crosses it at 3.2 s
2.0-4.0  surface    linen edge lifts 2 mm and settles
4.0-4.8  water      one droplet on the glass, 6 mm slip
0.0-8.0  camera     push-in 1.5%
```

### D. Outdoor weather (sport, outdoor gear, vehicles)

```
0.0-7.0  rain       6 to 10 beads on the surface, one runs 2 cm and stops
0.0-7.0  air        mist moves 5 to 10 cm camera-left
1.0-6.0  light      cloud edge changes 6% intensity once
3.0-3.6  water      one splash at the base, 4 cm, returns to still
0.0-7.0  camera     locked off
```

## Checking a motion map

1. Count the layers. Over five: merge two or cut the least meaningful.
2. Count the light layers. Over one: cut.
3. Does any layer cross the front face or the label? Move it.
4. Is the camera move a push-in of 2% or less? If not, cut it.
5. Is there a quiet layer? If every layer is fast, add one slow layer or remove one.
6. Does every layer have a physical source in frame? If not, add the source to `ATMOSPHERE` or remove the layer.
7. Does the map fit the duration? A 1.2 s window inside a 6 s clip is fine; a 9 s window inside a 6 s clip is not.

## What a bad map looks like

```
Steam swirls, dust floats, light flickers, camera orbits slowly, product rotates to show the label, water splashes.
```

This has six failures: five layers plus a camera move, a light flicker with no source, an orbit, product rotation, a splash with no impact, and no timing. It will produce a video where nothing is readable and the label is gone by second two.
