# Skill rules

Paste-ready blocks for the skill you build. Each block is written as an instruction to an agent. Replace every `<...>` with a confirmed value from `brand-spec.json`, and delete any placeholder the spec does not hold.

Copy the blocks into the skill body in this order. Keep the headings: an agent routes on them.

Two rules about the values themselves:

- A value may be pasted only if it is not in `unconfirmed`. If it is, ask the owner first.
- If a value is missing from the spec, stop. Do not fill the gap with a sensible default. A sensible default is how a brand acquires a fifth colour.

---

## Block 0: The brand, in one paragraph

> You work for `<brand name>`. `<one sentence on what the brand does and for whom, from QA09>`. Its look is: ground `<ground>`, surface `<surface>`, ink `<ink>`, one accent `<accent>`. Its type is `<brand face one>` for display and `<brand face two>` for text. This paragraph is orientation, not permission: the rules below decide what you may do.

---

## Block 1: Routing

> Before you write anything, name the output type. The types are: one page, long document, deck, social post, email, template.
>
> - **One page.** One heading, body text, at most one image, one logo, at most two accent uses.
> - **Long document.** Six pages or more. Every page carries the ground and the ink. The surface colour marks a panel, never a page.
> - **Deck.** Landscape. Type sizes are read from three metres, so the floor is `<deck floor size>`, not the document floor.
> - **Social post.** Square or portrait. Check the imagery rules before you choose a crop.
> - **Email.** Narrow and often viewed in dark mode. Use the variant that survives a dark ground.
> - **Template.** A file another person will fill. Leave the fields empty and marked, and write the rules into the file's notes.
>
> If the output is none of these, say so and ask which rules apply. Do not invent a seventh type.

---

## Block 2: Palette

> - Only these colours may appear: `<ground>`, `<surface>`, `<ink>`, `<accent>`, and the neutral `<muted>`. The list is closed.
> - `<ground>` is the page. `<surface>` is a panel, a card or a table. `<ink>` is type. `<accent>` is a mark, not a field.
> - Body text is set in `<ink>`. Captions and secondary notes may use `<muted>`. Nothing else carries body text.
> - Use `<accent>` no more than twice on a page. A rule, a single figure, one underline. An accent that appears three times is a second brand colour.
> - Do not tint, lighten, darken or blend a brand colour. If a lighter panel is needed, use `<surface>`.
> - Do not use a gradient, a transparency or a blend mode on a brand colour.
> - The allowed drift is 6 of 255 per channel, which exists so a rendered file still passes. It is not a licence to pick a nearby shade.

---

## Block 3: Type

> - Display type is `<brand face one>`. Text type is `<brand face two>`. There is no third face.
> - Sizes come from this scale and no other: `<size 1>`, `<size 2>`, `<size 3>` and so on. `1px` either side is allowed. Nothing else is.
> - Weights in use: `<weight list>`. Body copy is `<body weight>`. Do not synthesise a bold or an italic the family does not have.
> - The smallest size in any output is `<floor size>`. If the copy does not fit at the floor, cut the copy.
> - Line length is `<measure>`. Line height is `<leading>`.
> - Do not substitute a font. If `<brand face one>` is unavailable, say so and stop. Do not present a fallback as the brand face.
> - Do not letter-space lower-case text. Do not set a paragraph in capitals. Do not use more than one alignment in a single block.

---

## Block 4: Logo

> - The logo appears once. Two placements is a decoration, not a brand.
> - The only sources are: `<logo variant list with paths>`. Never draw, trace, rebuild, recolour or restretch the mark.
> - Clear space is `<clear space>` on all four sides. Nothing enters it: no type, no rule, no image edge, no page edge.
> - Use `<variant>` on the ground and the surface. Use `<variant>` on `<dark ground>`. If the needed variant does not exist, the logo does not go there.
> - Never place the logo over an image unless the image is flat enough to hold it and the variant is the one approved for that.
> - Never set the brand name in a substitute typeface as a stand-in wordmark.

---

## Block 5: Imagery

> - Available ratios are `<ratio list>`. Do not invent a crop the brand does not use.
> - Never stretch, squash or distort an image. Scale it and crop it, keeping the ratio.
> - Do not add a filter, a duotone, a grain or a coloured overlay unless it is in the spec.
> - Do not place an image so that the subject is cut by a fold, a page break or a crop edge.
> - `<subject rule from QA07>`. `<prohibition from QA07>` may not appear in an image.
> - If no image in the spec fits the slot, use the surface colour as a field. Do not find a substitute image.

---

## Block 6: Refusals

> Refuse these five, every time, in one short paragraph.
>
> 1. **Inventing a logo.** Not a variant, not a simplified mark, not a redraw from a description.
> 2. **Restretching a logo.** If the mark does not fit the space, the space is wrong.
> 3. **Substituting a font you do not have.** Say the face is unavailable. Do not ship a fallback as though it were approved.
> 4. **Applying the brand to a third party's material.** A partner, a reseller, a customer. The brand does not go there without written permission, and you cannot grant it.
> 5. **Making a document that looks like the brand's own official document.** An invoice, a certificate, a policy notice, a letter on letterhead, a receipt.
>
> When you refuse, give three things: what was asked, why it is not done, and what can be done instead. Do not lecture. Do not refuse the whole request when one part of it is the problem.

---

## Block 7: Checks before delivery

> Run these twelve checks on the output, in this order. Fix what fails. Report what warns.
>
> 1. Every colour in the output is in the spec palette, within 6 of 255 per channel.
> 2. Body text is `<ink>`, not the muted colour and not the accent.
> 3. The accent appears twice or fewer.
> 4. Every family is a declared brand face.
> 5. The logo appears exactly once.
> 6. Clear space around the logo is `<clear space>` or more.
> 7. The logo is a spec file, unedited.
> 8. Every image keeps its ratio, and its orientation exists in the spec.
> 9. Every size is on the scale, within 1px.
> 10. The text and background pair is on the safe pairings list at 4.5:1 or better.
> 11. Nothing in the output depends on a value still listed in `unconfirmed`.
> 12. The brand name is spelled and cased exactly as `<brand name>`.
>
> If a check cannot be run, say which one and why. A check you skipped is not a check you passed.

---

## Block 8: Reporting a break you find late

> If the output has shipped and a break is found, report four things and nothing else: which rule broke, where it appears, what the correct value is, and whether the break changes meaning or only appearance. Do not offer a redesign. Do not apologise twice.

---

## What to leave out

Do not paste these into the skill:

- The audit's evidence strings. They belong in the spec, and they will date.
- The ranked palette. It is a reading, not a rule, and a skill that holds a ranked list will eventually use a colour because it was third.
- The inferred values. If a value is still in `unconfirmed`, it is a question, not a rule.
