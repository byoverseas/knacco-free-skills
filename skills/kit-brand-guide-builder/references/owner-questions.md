# Owner questions

Twelve questions an audit must put to the brand owner before the spec is trusted. Ask all twelve, in this order, even when the audit raises only one. The tool reports the questions its gaps make unavoidable; the method does not depend on the tool's estimate of what is missing.

Put the questions in writing and keep the answers. A spoken answer is a decision that will be remembered differently by the two people in the room.

For each question: what to ask, why it is asked, what goes wrong when it is skipped, and which spec fields the answer settles.

---

## QA01. What is the registered brand name, spelled exactly as it must appear?

**Why it is asked.** The name is the one element that appears in every output, and the audit can only read it if a file states it. A folder name is a guess.

**Skipped.** The skill ships a name that is almost right: a missing accent, a wrong plural, a hyphen where the brand uses a space. It is the first thing a customer notices and the last thing anyone checks.

**Settles.** `brand.name`.

---

## QA02. Which colour is ground, which is ink, and which is accent?

**Why it is asked.** A palette is a set of jobs, not a set of hexes. The audit assigns the jobs by frequency and luminance, and a panel tint can outrank a page ground.

**Skipped.** Every page looks like a card, body copy is set in the muted grey, and the link colour becomes the heading colour. The colours are all correct and the brand is unrecognisable.

**Settles.** `colours.roles.ground`, `.ink`, `.accent`, `.surface`.

---

## QA03. Which typeface is the brand face, and is the file licensed for this use?

**Why it is asked.** A family name in a stylesheet is not a licence, and an agent that cannot embed the face will use a fallback and call it the brand.

**Skipped.** The skill names a face nobody can install, every output falls back to Arial, and the brand looks like a template for a year before anyone says so.

**Settles.** `type.families`, `type.font_files`.

---

## QA04. Is one accent enough, and how many times may it appear on a page?

**Why it is asked.** The accent is the only unbounded element in most brands. The audit can find the colour and cannot know the budget.

**Skipped.** The accent appears five times on the first page, then becomes a field colour, then a second accent appears to distinguish the field from the mark. Nobody decided any of it.

**Settles.** `colours.roles.accent`, and the accent budget in the built skill.

---

## QA05. What clear space and minimum size does the logo require?

**Why it is asked.** Clear space is almost never written down, so the audit derives it from the artwork. A derived figure is a convention, not the brand's rule.

**Skipped.** The logo collides with a heading in a tight layout, or shrinks to a size where the wordmark is a smudge. Both look like carelessness because both are.

**Settles.** `logo.clear_space`, `logo.clear_space_rule`.

---

## QA06. Which logo variants exist, and which one goes on a dark ground?

**Why it is asked.** A folder usually holds one or two variants. The brand usually has more, and the one that works on a dark ground is the one that is missing.

**Skipped.** The skill refuses a correct placement because no reverse variant was in the folder, or it places a dark mark on a dark ground and the logo disappears.

**Settles.** `logo.variants`, `logo.variant_count`, and the anti-pattern about dark grounds.

---

## QA07. What may appear in a photograph, and what must never appear in one?

**Why it is asked.** The audit reads ratios and orientation. It cannot read intent, and the prohibition is the part that matters most.

**Skipped.** A competitor's product appears in a crop, or a hand with a visible watch, or a location the brand is not associated with. The skill had no rule to apply, so it applied none.

**Settles.** `imagery.rules`, and the subject and prohibition lines in the skill.

---

## QA08. What are the exact type sizes and weights, and the smallest permitted size?

**Why it is asked.** A stylesheet often holds fewer sizes than the brand actually uses, and the floor size is a decision rather than a reading.

**Skipped.** Every document invents a size for the one awkward line, and the smallest size creeps down until the legal note is unreadable.

**Settles.** `type.scale`, `type.weights`, and the floor size in the skill.

---

## QA09. What does the brand sound like, and what does it never say?

**Why it is asked.** Voice is not in a folder. A skill that applies the look and ignores the tone produces output that is visually on brand and audibly wrong.

**Skipped.** The skill writes in the voice of the last document it saw, which is usually a legal page, and the brand reads as though it has been taken over.

**Settles.** The tone block in the built skill. It adds no field to the spec, and it is the answer most often skipped.

---

## QA10. Who owns the logo and the typefaces, and what may be reproduced?

**Why it is asked.** Ownership decides what an agent may generate and what it may only place. It is also the answer behind every refusal rule.

**Skipped.** The skill embeds a licensed typeface into a document that leaves the organisation, or reproduces a mark it has no right to reproduce, and the problem arrives as a letter.

**Settles.** The refusal rules, and the note on font files in the spec.

---

## QA11. Who approves a new template, and which folder holds the master assets?

**Why it is asked.** A skill with no owner drifts. A skill with two folders of truth drifts faster, because each folder can be argued to be current.

**Skipped.** Two versions of the logo circulate, both approved by someone, and the skill is rebuilt from whichever folder the last person opened.

**Settles.** The audit's own folder choice, and the handover note in the skill.

---

## QA12. What contrast pair carries body text, and may the accent carry text at all?

**Why it is asked.** Contrast is a floor, not a taste. The accent is the colour most likely to fail it, and it is the colour people most want to use for a headline.

**Skipped.** Body text is set in the accent at 2.3:1. It looks fine on the designer's screen and is unreadable on a phone in daylight.

**Settles.** `pairings`, and the contrast rule in the skill.

---

## How to record an answer

For each answered question:

1. Open `brand-spec.json` and find the value the question settles.
2. If the answer contradicts the audit, change `value`.
3. Add `"confirmed": "<name>, <date>"` to that value object.
4. Remove the value's path from `unconfirmed`.
5. If the question settles something the spec does not hold, such as voice or the floor size, write it in the skill body and note it in the spec's `audit.notices` by hand.

Leave `source` alone. It records where the value came from, which stays `inferred` even after a person has agreed to it. That distinction is the reason the file is worth keeping.

---

## A short version, for a fifteen minute call

If the owner has fifteen minutes, ask these six, in this order. They settle the values that break the most outputs.

1. QA02, colour roles.
2. QA03, the typeface and its licence.
3. QA05, clear space.
4. QA06, logo variants.
5. QA08, the scale and the floor size.
6. QA09, the voice.

Then send the other six in writing and give a date by which you need them. A spec with six answers and six outstanding questions is honest. A spec with twelve assumptions is not.
