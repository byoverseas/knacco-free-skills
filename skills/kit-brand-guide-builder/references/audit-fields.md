# Audit fields

Every field in `brand-spec.json`: what it is, how the tool derives it, and whether it is read or inferred. Paths use dots for objects and `[n]` for list entries, the same way `unconfirmed` cites them.

Every value object has three keys and may carry extras:

| Key | Type | Meaning |
|---|---|---|
| `value` | string, number, list or dict | The value |
| `source` | `"read"` or `"inferred"` | Read means a declaration states it. Inferred means the tool worked it out |
| `evidence` | string | `file:line` for a declaration, `file` and the method for a header or a derived value |

`read` covers a hex in a stylesheet, a family in a `font-family`, a size in a `font-size`, a colour in an SVG attribute, a key in a JSON theme, a pair in a Tailwind config, and a pixel width in a PNG, JPEG or SVG header. `inferred` covers role assignment, conversion, sampling, renaming from a filename, folder-name guessing, derived clear space and derived rules. There is no third category.

Three top-level keys hold metadata rather than values: `schema_version`, `tool`, `tool_version`, `folder` and `all_questions`. Everything else is a value object or a list of them.

---

## audit

| Path | Type | Derived from | Source |
|---|---|---|---|
| `audit.files_scanned` | int | The number of files the walk visited, after hidden files, skipped folders and `brand-spec.json` are excluded | read |
| `audit.by_extension` | object | Count per lower-case extension, keys sorted | read |
| `audit.unreadable` | list | Files that could not be decoded as text, sorted by path | read |
| `audit.notices` | list | One entry per notable event: an unparsable JSON file, a sampled image. Sorted by text | inferred |

The walk skips `node_modules`, `dist`, `build`, `out`, `vendor`, `coverage`, `.git` and any folder whose name starts with a dot. It also skips the file it is about to write, plus any `brand-spec.json` already in the folder, so a second run does not audit the first run's output.

---

## brand

| Path | Type | Derived from | Source |
|---|---|---|---|
| `brand.name` | string | The first `Brand:` line in a text or Markdown file, else the `name` key in a JSON file, else a `<title>` in a logo SVG, else the folder name | read, except the folder name, which is inferred |
| `brand.tagline` | string or null | A `Tagline:` or `Strapline:` line, or a `tagline` key in JSON | read, or inferred with a null value |

Candidates are ranked: a labelled line beats a JSON key, which beats an SVG title. The rank is not written to the spec, only the winner and its evidence.

---

## colours

| Path | Type | Derived from | Source |
|---|---|---|---|
| `colours.ranked` | list, most used first | Every colour literal in a declaration, grouped by value and sorted by `uses` then by value | read |
| `colours.ranked[n].uses` | int | How many times the value appears across all declarations | read |
| `colours.ranked[n].files` | list | Every file that declares the value, sorted | read |
| `colours.ranked[n].token` | string or null | The custom property or key name attached to the first occurrence | read |
| `colours.roles.ground` | string or null | A token named ground, background, bg, paper, canvas, base or page. Else the most used colour with luminance at or above 0.80 | read from a token, else inferred |
| `colours.roles.ink` | string or null | A token named ink, text, fg, foreground or copy. Else the most used colour with luminance at or below 0.30 | read from a token, else inferred |
| `colours.roles.accent` | string or null | A token named accent, highlight or spot. Else the most used colour with saturation at or above 0.30 and luminance between 0.15 and 0.80 | read from a token, else inferred |
| `colours.roles.surface` | string or null | A token named surface, card, panel or layer. Else the most used colour with luminance between 0.55 and 0.95 that is not already a role. Else the ground, reused | read from a token, else inferred |
| `colours.roles.*.uses` | int | Occurrence count for the chosen colour | read |
| `colours.tolerance` | int | Fixed at 6. The per-channel distance the checker allows, so a render with rounding still passes | inferred |

Sources scanned for colour: `css`, `scss`, `sass`, `less` and `html` files, the `fill`, `stroke`, `stop-color`, `color` and `flood-color` attributes and style blocks in SVG, string values in JSON theme files under a colour-like key, and `key: '#hex'` pairs in a JS or TS file whose name contains `tailwind`, `theme` or `token`.

Named CSS colours such as `white` or `tomato` are not counted. Alpha is dropped, so `#11223380` is recorded as `#112233`. A three-digit hex is expanded.

---

## type

| Path | Type | Derived from | Source |
|---|---|---|---|
| `type.families` | list | Every family in a `font-family` declaration and in a type token, grouped, brand faces first, then by use count | read |
| `type.families[n].uses` | int | How many declarations name the family | read |
| `type.families[n].role` | `"brand face"` or `"fallback"` | A family that is first in at least one declaration is a brand face. A family that only ever appears after a comma is a fallback | inferred |
| `type.scale` | list, smallest first | Every `font-size` declaration and every size token, grouped by pixel value | read in px, inferred for rem, em or pt |
| `type.scale[n].value` | string | The size in pixels, for example `"16px"` | read or inferred as above |
| `type.scale[n].uses` | int | How many declarations set that size | read |
| `type.weights` | list, lightest first | Every `font-weight` declaration and weight token, with `normal` mapped to 400 and `bold` to 700 | read |
| `type.font_files` | list | Files with `woff2`, `woff`, `ttf`, `otf` or `eot` extensions | read |

A font file entry carries `format`, plus `family_guess` and `weight_guess`, both inferred from the filename. The tool never opens a font binary. `rem` and `em` are converted at a 16px root and `pt` at 4/3 px, and a converted size is marked inferred because the conversion is the tool's assumption.

Generic families (`serif`, `sans-serif`, `monospace`, `system-ui`) are dropped: they are not a type choice.

---

## logo

| Path | Type | Derived from | Source |
|---|---|---|---|
| `logo.variants` | list | Image files whose filename or directory contains logo, mark, wordmark, lockup, brandmark, monogram or symbol, except `og-` and `favicon-` files | read |
| `logo.variants[n].value` | string | The file path, relative to the audited folder | read |
| `logo.variants[n].variant` | string | The first variant word found in the filename: primary, wordmark, monogram, symbol, icon, mark, stacked, horizontal, reverse, mono, light, dark. Else `unspecified` | read when the filename states it, else inferred |
| `logo.variants[n].variant_basis` | string | `filename`, or the reason no word was found | read |
| `logo.variants[n].width`, `height`, `aspect` | int, int, float | The image header | read |
| `logo.variant_count` | int | The number of logo files | read |
| `logo.clear_space` | string | Half the height of the tallest logo, in pixels | inferred |
| `logo.clear_space.minimum_px` | int | The same figure as a number, for the checker | inferred |
| `logo.clear_space_rule` | string | The rule in one sentence: clear space on all four sides equal to half the logo height | inferred |

Images that are not logos stay in `imagery.files`.

---

## imagery

| Path | Type | Derived from | Source |
|---|---|---|---|
| `imagery.files` | list | Image files that are not logos, sorted by path | read |
| `imagery.files[n].value` | string | `widthxheight`, for example `"1600x1000"` | read |
| `imagery.files[n].format` | string | The extension, lower case | read |
| `imagery.files[n].bytes` | int | File size | read |
| `imagery.files[n].width`, `height`, `aspect`, `orientation` | int, int, float, string | PNG IHDR, JPEG SOF, or SVG width and height or viewBox | read |
| `imagery.files[n].path` | string | The relative path, repeated from `value` so the entry reads well on its own | read |
| `imagery.count` | int | The number of image files that are not logos | read |
| `imagery.sampled_colours` | list | The three most common colours in a PNG, quantised to five bits per channel, sampled every seventh pixel | inferred |
| `imagery.sampled_colours[n].share` | float | The share of sampled pixels in that cluster, to three places | inferred |
| `imagery.rules` | list | Rules derived from the files present: available orientation, no stretch, the status of photographic colour | inferred |

Only PNG pixels are decoded, and only 8-bit, non-interlaced, greyscale or RGB or with alpha, up to two million pixels. Anything else returns no sample and a notice. JPEG content is never decoded. A file whose header cannot be read gets `value: "unknown"` and inferred source.

---

## pairings

| Path | Type | Derived from | Source |
|---|---|---|---|
| `pairings` | list, highest contrast first | Every dark colour (luminance at or below 0.40) against every light colour (luminance at or above 0.60), keeping pairs at 3.0:1 or better | read when both colours are read, else inferred |
| `pairings[n].value` | string | `"<dark> on <light>"` | as above |
| `pairings[n].ratio` | float | WCAG relative luminance, to two places | as above |
| `pairings[n].use` | string | `body` at 4.5:1 or better, `large text only` between 3.0 and 4.5 | as above |

The list is capped at six dark and six light candidates, which keeps a large palette from producing hundreds of rows.

---

## anti_patterns

| Path | Type | Derived from | Source |
|---|---|---|---|
| `anti_patterns` | list | Rules the folder implies but never states | inferred |

Every entry is inferred. The rules are produced when the conditions hold:

- No colour outside the ranked palette. Always produced.
- No second accent. When the folder holds one saturated colour or none.
- No gradients. When no `linear-gradient`, `radial-gradient` or `conic-gradient` appears in any stylesheet or SVG.
- No body text in the accent. When the accent against the ground is below 4.5:1.
- No portrait crops. When imagery exists and none of it is portrait.
- No logo on a dark ground. When no reverse or mono variant exists.

---

## questions_raised

| Path | Type | Derived from | Source |
|---|---|---|---|
| `questions_raised` | list | The subset of the twelve questions that this folder's gaps make unavoidable | inferred |
| `questions_raised[n].value` | string | The question ID and its wording, for example `"QA05: What clear space ..."` | inferred |
| `questions_raised[n].id` | string | `QA01` to `QA12` | read |
| `questions_raised[n].reason` | string | Why the audit raised it | inferred |

The triggers, in full:

| Question | Raised when |
|---|---|
| QA01 | The brand name came from the folder name |
| QA02 | Any of ground, ink, accent or surface is inferred |
| QA03 | No font family is declared anywhere |
| QA04 | The accent role is inferred |
| QA05 | Clear space is inferred, which is every audit |
| QA06 | Fewer than two logo variants |
| QA07 | No imagery files |
| QA08 | Fewer than three type sizes |
| QA12 | No pairing reaches 4.5:1 |

Questions that cannot be detected from files are never raised by the tool and are still required by the method: QA09, QA10 and QA11. See `owner-questions.md`.

---

## unconfirmed

`unconfirmed` is a list of dotted paths, one for every value marked inferred, in document order. Paths inside `questions_raised` are excluded, because a question is the record of a gap and not a value to confirm.

`brand_check.py` reads this list in rule R11. To confirm a value:

1. Add `"confirmed": "<name>, <date>"` to the value object.
2. Remove its path from `unconfirmed`.

A re-run of the audit rebuilds the list. That is intentional: confirmation is a human act, and the tool cannot know about it.

---

## The output description the checker reads

`brand_check.py` takes a JSON description of one proposed output. Fields it uses:

| Field | Type | Used by | Meaning |
|---|---|---|---|
| `output_id` | string | none | A label for the report |
| `kind` | string | none | What the output is |
| `brand_name_used` | string | R12 | The name as it appears in the output |
| `colours_used` | list of hex | R01, R11 | Every colour the output uses |
| `body_text_colour` | hex | R01, R02, R11 | The colour body copy is set in |
| `background_colour` | hex | R01, R11 | The main background |
| `accent_uses` | int or list | R03 | How many times the accent appears |
| `fonts_used` | list of strings | R04 | Every family the output sets type in |
| `type_sizes_px` | list of numbers | R09 | Every size in the output |
| `logo.instances` | int | R05 | Placements of the logo |
| `logo.clear_space_px` | number | R06 | The smallest clear space around the logo |
| `logo.source_file` | string | R07 | The logo file used |
| `logo.invented` | bool | R07 | True if the mark was drawn for this output |
| `imagery` | list | R08 | Each entry: `id`, `aspect`, `stretched`, `source_file` |
| `contrast_pair` | object | R10 | `text` and `background` hex values |
| `uses_inferred` | list of paths | R11 | Spec paths the output depends on |
| `text` | string | R01 | The copy, scanned for stray hex values |

A field that is absent produces a warning, not a pass. A warning is a decision that has not been made.
