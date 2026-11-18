---
name: kit-data-study-press-pack
description: "Plan a focused data study, check a sample of the records, and prepare findings and press materials with a documented method."
---

# Data Research & Press Kit

One question becomes one count, and the count becomes evidence a journalist can check. The findings document and the press pack are separate files, because evidence and marketing are different jobs.

Status: **v1.0** | Category: **Workflows** | Price: **Free**

Read [the product guide](GUIDE.md) before you count anything. Run the included tools from this product folder. Keep your raw rows, your coding sheet and your outputs in your own workspace.

## What this skill does

1. Tests a question against the three things that make it press-worthy, and the three that make it unpublishable.
2. Picks one of five source types and writes the one paragraph that describes it.
3. Records the retrieval date, the query and the population before any filtering, and keeps the raw rows untouched.
4. Counts with a rule that names a positive test, a negative test and a separate bucket for ambiguous rows.
5. Draws a verification sample by a fixed stride, reports the disagreement rate and the rule of three bound, and refuses a finding over 10 per cent.
6. Writes the findings, builds the pack, and checks both with `tools/press_pack.py`.

## Route

- **Start a study** → read `GUIDE.md`, then run the three question tests in `references/question-tests.md` before touching any data.
- **Choose a source** → `references/source-types.md`, then write the source paragraph. No paragraph, no source.
- **Build and code the sheet** → `python3 tools/study_sheet.py init`, `add-row`, `code`, then `tally`.
- **Check your own coding** → `python3 tools/verify_sample.py sample`, `record`, `report`. The stride rule is in the script and in `references/verification-protocol.md`.
- **Write the pack** → `references/press-pack-shape.md` for the release structure, the three charts, the boilerplate and the citation line.
- **Check before publishing** → `python3 tools/press_pack.py FINDINGS.md PRESS-PACK.md`.

## Rules that are not negotiable

- No percentage appears anywhere without its denominator in the same line or paragraph.
- Every row carries a decision. Ambiguous rows are held separately, never folded into a category.
- The sample is drawn by the stride rule written into the sample file. It is never re-drawn to get a better result.
- The raw rows are kept as retrieved. No tidying, no reordering, no silent filtering. A filter is recorded with its count.
- A count supports a description. It never supports a cause.
- The findings document and the press pack are two files. The pack links to the evidence; it does not carry it.
- If a result needs weighting, significance, projection or a causal design, it goes to a statistician before it goes out.
- A quote is attributed to a named person with a role, and only after that person has approved the words.

## Files

| File | Use |
|---|---|
| `GUIDE.md` | The full method: eight stages, the decision inside each one, and the limits |
| `references/question-tests.md` | The tests a question passes before any data is collected, with a worked pass and a worked fail |
| `references/source-types.md` | The five source types: access, cost, what each can support, the bias, and the paragraph you write |
| `references/press-pack-shape.md` | The release section by section, three chart specs, boilerplate and citation line |
| `references/verification-protocol.md` | The sampling rule, sample size, how to record a disagreement, and what each rate means |
| `tools/study_sheet.py` | Builds and codes the CSV sheet, and refuses to tally an unfinished count |
| `tools/verify_sample.py` | Draws a fixed sample and reports the disagreement rate with its bound |
| `tools/press_pack.py` | Scores a findings document and a pack: 7 errors, 4 warnings, out of 100 |
