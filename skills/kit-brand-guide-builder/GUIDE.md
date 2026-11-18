# Brand Guide Builder

A method for turning a folder of brand files into a skill that applies the brand to every output without being asked.

The folder is evidence. The audit is the reading of that evidence. The skill is a set of rules derived from the reading, with every uncertain value confirmed by the person who owns the brand. Skip the middle step and you get a skill that sounds like a brand and is wrong in the places that matter: the wrong ink on the wrong ground, a logo with no room around it, an accent used five times on one page.

## The words this guide uses

Nothing below needs learning before you start. Come back when a word gets in the way.

| Word | What it means here |
| --- | --- |
| Skill | A set of written rules an AI assistant applies without being asked each time |
| Audit | A reading of your brand files, with a note of what each value came from |
| Brand guide | The written specification this tool produces, covering colour, type, logo and imagery |
| Read | A value stated plainly in one of your files, so it is not a guess |
| Inferred | A value the tool could not read, so it guessed and flagged it for you to confirm |
| Palette | The set of colours your brand uses, with their codes |
| Type scale | The sizes your headings and body text take, in a fixed set |

---

---

## 1. The problem this solves

Brand work fails in one of five places.

1. **Drift.** Each new document is a fresh interpretation. The palette widens by a shade per quarter. Nobody decides this; it accumulates.
2. **The guideline nobody opens.** A forty-page PDF states the rules in prose. An AI tool cannot apply prose. A person applies it from memory, and memory keeps the mood and loses the numbers.
3. **The prompt that invents.** You ask for an on-brand page and get a plausible page: the right feeling, a colour that is nearly right, a font that is close, and a logo that has been quietly redrawn.
4. **The one-off.** A single urgent deck is made by hand, correctly, and none of the decisions in it are written down. The next deck starts from zero.
5. **The confident guess.** Someone reads the folder in ten minutes and writes rules from it. The rules are specific, tidy and partly wrong, and they carry the authority of a document.

The fix is procedural. Collect the assets into one folder. Audit the folder and record where every value came from. Ask the owner about everything the audit could not read. Only then write the rules.

---

## 2. The three stages, and why the order cannot be reversed

| Stage | Input | Output | Gate before the next stage |
|---|---|---|---|
| 1. Collect | A brand owner, and whatever files exist | One folder, with every asset in it and nothing renamed | The owner confirms the folder is the current set |
| 2. Audit | The folder | `brand-spec.json`, with `read` and `inferred` on every value | Every inferred value is confirmed or removed |
| 3. Build | A confirmed spec | A skill: choosing the output type, palette, type, logo, imagery, refusals, checks | Ten outputs reviewed in order |

The order is not a preference. Each reversal has a specific cost.

- **Build before audit.** You write rules first, then run the audit to check them. The audit stops being a reading and becomes a confirmation of what you already believed. Everything the folder contradicts gets explained away.
- **Audit before collect.** The audit only knows what is in the folder. A missing logo variant, a font that lives on a designer's laptop, a colour used only in print: none of it can be read. You get a tidy spec with holes, and the holes are invisible because an empty field looks the same as a field that was never needed.
- **Build without confirmation.** Every inferred value becomes a rule with no owner behind it. When the rule is wrong, nobody can say who decided, and the fix is an argument rather than a correction.

A useful test before stage three: read each rule aloud and ask "where did this come from?" If the answer is a file and a line, the rule is ready. If the answer is "it looked like that", it is not.

---

## 3. Stage one: collect

Ask for seven things. Most owners will have four.

| Ask for | Why the audit needs it | If it is missing |
|---|---|---|
| The stylesheet or theme file for the site or product | Colours and type in declarations, with names attached | Roles have to be guessed from frequency |
| Every logo file, in every variant | Variants and their true dimensions | One file, and no reverse or mono variant |
| Font files, or the licence that names the family | The family name, and proof it may be embedded | A family name with no file, and a fallback in practice |
| Imagery: ten to twenty real images | Aspect ratios, orientation, treatment | No imagery rule can be read |
| Any guideline document | Stated rules, including clear space and accent budget | Every rule is derived, and every derived rule needs confirmation |
| One page the owner considers good | The intended result, in the owner's own judgement | The audit reads rules and cannot read intent |
| One page the owner dislikes | The anti-patterns, which are otherwise invisible | Anti-patterns are inferred from absence |

Rules for the folder itself:

- One folder, flat enough to walk. Rename nothing. The audit cites paths, and the owner will need to open them.
- Keep the folder as it was received, and audit a copy if you plan to tidy it.
- A PDF guideline is evidence for a human, not for the tool. The audit does not read PDFs. Read the PDF yourself and add what you learn to the spec by hand, marked as you would mark any other source.
- The folder is evidence, not law. An old stylesheet in the folder describes what the site did, not what the brand is. That is what the questions in section 6 are for.

---

## 4. Stage two: what an audit must extract

An audit is not a mood board. It produces seven things, each with a value and a source.

### 4.1 Palette, with named roles

A hex list is not a palette. Four roles are what makes the palette usable:

| Role | What it is | How the audit finds it | The failure when it is wrong |
|---|---|---|---|
| **Ground** | The default background | The most used light colour, or a name used in your stylesheet, such as ground, background, paper or canvas | A panel tint becomes the page, and every page looks like a card |
| **Ink** | The colour body text is set in | The most used dark colour, or a name used in your stylesheet, such as ink, text or foreground | Muted grey becomes body text, and long documents are unreadable |
| **Accent** | The one colour that marks a thing | The most used saturated colour, or a name used in your stylesheet, such as accent or highlight | A link colour becomes a heading colour, and headings look clickable |
| **Surface** | The colour of a raised panel, a card, a table | A name used in your stylesheet, such as surface, card or panel, or the second light colour | Panels are invented per document, and no two match |

The audit keeps frequency counts for every colour it finds. That matters: the most used colour is a signal, the first colour in the file is not. A stylesheet opens with its oldest declaration as often as its most important one.

### 4.2 Type hierarchy, with sizes and weights

The audit collects every `font-family` declaration, every type setting, every `font-size` and every `font-weight`, then ranks them. What the built skill needs is smaller than what the audit collects:

- The brand faces, in order, with the fallbacks named separately.
- The scale in pixels, with the number of distinct sizes. Six is a scale. Eleven is a drift.
- The weights in use, and which of them is the body weight.
- The smallest size that appears, which becomes the floor for the skill.

Sizes declared in `rem`, `em` or `pt` are converted at a 16px root and marked inferred, because the conversion is the tool's assumption, not the brand's declaration.

### 4.3 Logo variants and clear space

The audit reads every logo file it can identify by name: primary, mark, wordmark, monogram, stacked, horizontal, reverse, mono, light, dark. The variant word usually comes from the filename, which is why a variant's name is marked read only when the filename states it.

Clear space is almost never declared. The audit derives it as half the tallest logo height and marks it inferred. Every clear space figure in every spec you build needs the owner's answer, because the derived figure is a convention and the brand may have a rule.

### 4.4 Imagery rules

From the files, not from taste: orientation, aspect ratios, the number of images, and the treatment that is present or absent. Then three rules that a skill can apply: which ratios are available, that an image is never stretched, and what the images are for.

### 4.5 Safe pairings

The audit computes contrast for each of the six strongest dark colours against each of the six strongest light colours in the palette, using WCAG relative luminance. Two thresholds matter:

- **4.5:1** for body text.
- **3.0:1** for large text and for a shape that carries no text.

A pair that clears 4.5:1 is safe. A pair between 3.0 and 4.5 is safe for a heading and not for a paragraph. A pair below 3.0 is not a pairing, and the audit drops it.

### 4.6 Anti-patterns

The rules the brand never breaks. The audit can only infer these from absence and from conflict:

- A colour that appears nowhere in the assets.
- A second accent, when the folder holds one saturated colour.
- A gradient, when no gradient appears in any declaration.
- The accent as body text, when the accent does not clear 4.5:1 on the ground.
- A portrait crop, when every image is landscape.
- The logo on a dark ground, when no reverse variant exists.

Each one is inferred. Each one is worth confirming, because absence in a folder is not absence in the brand.

### 4.7 What the audit cannot get

Say this to the owner before you start, not after:

- The brand's voice. Tone is not in a stylesheet.
- Photography direction. The audit reads ratios, not intent.
- Logo construction. The audit reads dimensions, not the grid the logo was drawn on.
- The reason for any rule. A spec records what, and the owner holds why.
- Anything that exists only in print, in a PDF, or in a designer's head.

---

## 5. The inferred-value problem

Every value in `brand-spec.json` carries three keys.

- `value`: the value itself.
- `source`: `read` when a declaration states it, `inferred` when the tool worked it out.
- `evidence`: `file:line` for a declaration, `file` for a header or a derived value.

Read means the asset says it: a hex in a declaration, a family in a `font-family`, a width in a PNG header. Inferred means the tool worked it out: a role assigned by frequency, a clear space derived from artwork, a colour sampled from pixels, a name taken from a folder.

**Inferred values are wrong often enough to matter.** They are wrong in a specific pattern, which is why the problem is predictable:

1. **The role is wrong, not the value.** A panel tint is a real brand colour and it is not the ground. Frequency and luminance cannot tell the difference. The colour is right and the job is wrong.
2. **The absence is not real.** The audit sees one logo file. The brand has four. The folder is thin, not the brand.
3. **The convention is not the brand.** Half the logo height is a reasonable clear space. The brand may require the height of the letter N.
4. **The sample is not the colour.** Pixel sampling of a photograph gives the colour of the light in that photograph. A warm afternoon and a grey morning produce two different "brand colours".

An illustrative ceramics asset set shows the fourth kind. In that set the ground is declared as `#f6f2ea`. The sampler, reading the pixels of a PNG, returns `#f4f4ec`. The two differ by two levels in two channels, which is inside the checker's tolerance of 6, so nothing fails. A skill built on the sampled value would print a ground that no stylesheet in the folder uses, and the difference would never show up in a check.

A sharper example sits in the same spec. Because the folder holds no file with "reverse" or "mono" in its name, the audit infers the rule "do not place the logo on a dark ground". The folder does contain `mark.svg`, which is a light mark on a dark square and works perfectly on a dark ground. Confirm the inference and the skill refuses a correct placement for the rest of its life. Leave it unconfirmed and the skill ships with a rule nobody agreed to.

**The confirmation gate.** No rule in the built skill may cite a value that is still unconfirmed. `brand-spec.json` lists every inferred path in `unconfirmed`. To confirm one:

1. Put the question to the owner, using `references/owner-questions.md`.
2. Record the answer next to the value: add `"confirmed": "<name>, <date>"` to that value object.
3. Remove its path from `unconfirmed`.
4. If the answer contradicts the audit, change the value. If it agrees, the value stays and the source stays `inferred`, because the source records where the value came from and the confirmation records that a person agreed to it.
5. Audit again only if the assets changed. A re-run rebuilds `unconfirmed` from scratch, which is the point: the gate is manual because a confirmation is a human act.

`brand_check.py` rule R11 reads `unconfirmed`. A description that relies on an unconfirmed value fails, and so does one that uses a colour that appears only in an inferred field. That is the gate, enforced at the end of the process rather than trusted at the start.

---

## 6. The owner questions

An audit must put twelve questions to the owner before the spec is trusted. The tool raises the subset its own gaps make unavoidable, which can be one question on a clean folder and six on a thin one. The method requires all twelve regardless.

| # | Question | Why it matters |
|---|---|---|
| QA01 | What is the registered brand name, spelled exactly as it must appear? | Every output carries the name. A near miss is the most visible break there is. |
| QA02 | Which colour is ground, which is ink, and which is accent? | Roles are the difference between a palette and a list of hexes. |
| QA03 | Which typeface is the brand face, and is the file licensed for this use? | A skill that names a face it cannot embed ships a fallback and calls it the brand. |
| QA04 | Is one accent enough, and how many times may it appear on a page? | An unbudgeted accent becomes a second brand colour within a quarter. |
| QA05 | What clear space and minimum size does the logo require? | Clear space is the rule most often derived and most often wrong. |
| QA06 | Which logo variants exist, and which one goes on a dark ground? | A skill with one variant refuses legitimate placements or breaks the mark. |
| QA07 | What may appear in a photograph, and what must never appear in one? | Imagery rules are the least documented and the most noticed. |
| QA08 | What are the exact type sizes and weights, and the smallest permitted size? | Without a scale, every document invents one, and the smallest size creeps down. |
| QA09 | What does the brand sound like, and what does it never say? | Voice is not in the folder. A skill without it applies the look and breaks the tone. |
| QA10 | Who owns the logo and the typefaces, and what may be reproduced? | Reproduction rights decide what an AI tool may generate and what it may only place. |
| QA11 | Who approves a new template, and which folder holds the master assets? | A skill with no owner drifts. A skill with two folders of truth drifts faster. |
| QA12 | What contrast pair carries body text, and may the accent carry text at all? | Contrast is a floor, not a taste, and the accent usually fails it. |

Full wording, with what goes wrong when a question is skipped, is in `references/owner-questions.md`.

---

## 7. The rule set that goes into the built skill

Six groups. Each one is written as instructions an AI tool can follow, in `references/skill-rules.md`, ready to paste.

| Group | What it contains | What it stops |
|---|---|---|
| **Output types** | Which output type is which, and what each one must contain before the brand rules apply | The brand applied to the wrong kind of document, or to nothing at all |
| **Palette** | The four roles, the closed list of colours, the tolerance, ink for body, the accent budget | Drift, invented shades, accent inflation |
| **Type** | The faces, the scale, the weights, the floor size, no substitution | A fourth typeface, a size that is nearly on the scale |
| **Logo** | One placement, clear space, which variant for which ground, the file as the only source | Two logos, a squeezed logo, a redrawn logo |
| **Imagery** | Available ratios, no stretch, treatment, what must not appear | Stretched photographs and invented crops |
| **Refusals and checks** | The five refusals, and the twelve checks before delivery | The output that is nearly right and ships |

The spec supplies the values. The blocks supply the instructions. Do not copy values into prose: the blocks refer to the spec, so a corrected spec corrects every output.

---

## 8. The first ten outputs

Review in this order, on real work, before the skill is handed over. Each step isolates one variable, and the cheap failures come first.

1. **A palette-only page.** Four colour blocks with their roles named. Nothing else. If the roles are wrong, everything after this is wrong.
2. **A type-only page.** The scale, set in the brand faces, at every size. Check the floor size and the body weight.
3. **A logo placement sheet.** The logo on ground, on surface, and on the darkest colour, at the minimum size and with clear space marked. This is where a missing variant shows up.
4. **One page with everything.** A real page with a heading, body text, one accent use, one logo and one image.
5. **A long document.** Six pages. This is where the ground, the ink and the surface have to hold for more than a screen.
6. **A deck.** Landscape, projected, viewed from three metres. Type sizes and contrast fail here first.
7. **A social post.** Square or portrait. This is where an imagery rule that was never confirmed becomes a stretched photograph.
8. **An email.** Narrow, image-light, often viewed in dark mode. Check ink on surface and the logo variant.
9. **A document with two images and a table.** The commonest real page, and the one that breaks the surface colour.
10. **A refusal.** Ask for something the spec forbids: a logo redraw, a fifth colour, a typeface substitution. The skill must refuse and say why. A skill that cannot refuse is not finished.

For each output, run the checker and read the failures. A warning is a decision you have not made yet.

---

## 9. What a brand skill must refuse to do

Five refusals. They are not politeness; each one protects something the brand cannot get back.

1. **Invent a logo.** Not a variant, not a "simplified mark", not a redraw from a description. A drawn logo is a new logo, and it will be used.
2. **Restretch a logo.** Scaling one axis to fit a space changes the mark. If it does not fit, the space is wrong.
3. **Substitute a font it does not have.** A fallback is a fallback. Presenting Arial as the brand face makes the output look approved when it is not. Say the face is unavailable and stop.
4. **Apply the brand to a third party's material.** A partner's document, a reseller's page, a customer's site: the brand does not go there without permission, and a brand skill is not a permission.
5. **Produce a document that looks like the brand's own official document.** An invoice, a certificate, a policy notice, a letter on letterhead. A skill that can make a convincing internal document can make a convincing fraudulent one.

The refusal needs a sentence, not a lecture: what was asked, why it is not done, and what can be done instead. `references/skill-rules.md` carries that wording.

---

## 10. Limits

- **An audit of a folder is not an audit of a brand's strategy.** It records what the assets do. It cannot tell you whether the brand is pointed at the right market, whether the name still fits, or whether the palette is doing its job. Those are decisions above the folder.
- **The audit reads declarations, not pixels, for colour.** Photographic colour is sampled only from PNG files, and always marked inferred. A JPEG's pixels are not decoded at all. If the palette exists only in photographs, the audit cannot find it.
- **No PDF, no named CSS colours, no webp or avif dimensions.** Keep declarations in hex, and keep guidelines as text you read yourself.
- **Contrast is a floor.** A pair at 4.6:1 is legible and may still be ugly. The checker says "allowed", not "good".
- **The spec is only as complete as the folder.** A thin folder produces a spec with thirteen inferred values, and the audit will say so. That is the honest outcome, not a failure of the tool.
- **A brand skill does not make a brand consistent.** It makes inconsistency visible before it ships. The decisions stay with the owner.

---

## Sources and reuse

Source reference: a public walkthrough of collecting brand assets, auditing them and creating a brand skill. No third-party prompt text, template wording or brand assets are included. See `README.md` for the product licence and reuse terms.
