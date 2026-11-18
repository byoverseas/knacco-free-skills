# The memory card, field by field

One card per scope. Five sections, always present, in this order. The order is the contract: a reader, human or model, can find any field without hunting through prose.

## The shape

```markdown
# memory: <name>

Level: workspace | project | campaign
Scope: <one sentence on what this card covers and what it refuses>
Owner: <who keeps it>
Owns: <proper nouns, comma separated>
Runs until: YYYY-MM-DD

## Purpose

Confirmed: YYYY-MM-DD

- <what this is for>
- <what finished looks like>

## Current state

Confirmed: YYYY-MM-DD

- key: value
- key: value

## Decisions and why

Confirmed: YYYY-MM-DD

- YYYY-MM-DD <what was decided>, because <what forced it>

## What's next

Confirmed: YYYY-MM-DD

- <next move>
- <next move>

## Key links

Confirmed: YYYY-MM-DD

- <where the work lives> and what it is
```

`Owner:` is written on a workspace card only. `Owns:` is written on a project or campaign card only. `Runs until:` is written on a campaign card only. Everything else is on every card.

Everything above is required. A card with a section missing is a card with a hole in it, and the audit reports the hole as a warning. A card with a section present and empty is reported as an error, because an empty heading is a promise that the section is handled.

## The header block

| Line | Who needs it | What it does |
|---|---|---|
| `Level:` | Every card | Tells the audit which comparisons are across levels and which are not |
| `Scope:` | Every card | One sentence. It is the rule you read before adding a line |
| `Owner:` | Workspace | A name, not a role. Someone has to be able to change the line |
| `Owns:` | Project, campaign | The proper nouns this card owns. The audit looks for these on the workspace card |
| `Runs until:` | Campaign | The date the folder is archived. A campaign without one is a project that will not close |

`Scope:` is the line people skip and then need. A workspace scope might read: "every project in this folder. A fact that is true of one project only does not belong here." A project scope might read: "this project only. Level one facts stay out. They are already true everywhere." Both sentences are rules, not descriptions, and both are checkable by the person about to add a line.

`Owns:` is a list of names that must not appear outside the card. Keep them distinctive: a client name, a product name, a codename. Do not list a common word, or every card that uses the word will be flagged.

## The Confirmed line

One per section, under the heading:

```
Confirmed: 2026-10-24
```

It is a claim with a date: on that day, someone read this section and it was still true. The audit reads it three ways. No line, or a line with no readable date, is an error when the section has content. A date older than the horizon is stale. A date in the future is not a confirmation, so do not write one.

Leave a section you did not check alone. A card where every date moved at once is a card where nothing was checked.

---

## Field 1: Purpose

**The question:** what is this for, and what does finished look like?

Two bullets, usually. The first says what the work is. The second says what closed looks like, because "done" is the thing a project forgets first and argues about last.

**Works**

```
- New packaging for a rye loaf range: three bag sizes, a shelf-ready crate, and a one-page print spec.
- Finished means the printer holds the files, the client has signed the second proof, and the spec is filed.
```

**Useless**

```
- Packaging project for a bakery client. Various deliverables. Ongoing.
```

Why it fails: "various" and "ongoing" are the two words that make a card unclosable. Nothing here can be checked, so nothing here can be finished, so the card stays open and grows.

**The test:** could a person who has never spoken to you read this and say whether the work is done? If not, rewrite the second bullet.

---

## Field 2: Current state

**The question:** what is true today?

One bullet per fact, in the form `key: value`. Present tense. No dates in the past, no reasoning, no history. When a fact changes, change the value; when a fact stops being true, delete the line.

**Works**

```
- client: Adeyemi & Roe
- deadline: 2026-11-14, print slot held
- stage: second proof with the client
- print method: two-colour flexo on kraft, no foil
- contact: Mira, buyer, replies on Tuesdays
```

**Useless**

```
- 2026-09-08 sent first proof, Mira asked for a bigger wordmark on the 11th, then we
  tried 44 mm which worked, then the second proof went out on the 13th and we are
  waiting to hear.
```

Why it fails: it is a paragraph of history in the field that has to be read first. A model reading it cannot tell what is true now. A person reading it has to reconstruct the state from the events.

**The test:** does the line read as true today, with no date in front of it? If it has a past date, it is a decision or a log entry, and neither belongs here.

The key-value form is not decoration. It is what lets the audit compare this card against the workspace card, and it is what lets you scan the section in five seconds.

**Size:** a section past 40 lines is reported as an error. Forty lines is about one screen and about the point where a state section has started to keep history. The usual cause is an appended log of what happened, which is the same information the decisions list should hold, minus the reasons.

---

## Field 3: Decisions and why

**The question:** what did we decide, and what forced it?

One bullet per decision. The date first, then the decision, then the reason on the same line, introduced by **because**, **since**, **so that**, **so we**, **so i**, **otherwise**, **to avoid**, or the word **reason**. The audit requires one of those clauses; the standard is higher than the requirement.

**Works**

```
- 2026-09-22 Dropped the foil stamp from the crate, because the held print slot cannot take a second pass before the 14th.
- 2026-10-01 Wrote the handbook as one file per section, because we edit one section at a time and a long document makes every edit a merge.
- 2026-10-20 Left invoicing out of this pass, because the accounting tool already answers it and a second answer would drift.
```

**Useless**

```
- 2026-10-21 Moved the studio call to Thursday.
- 2026-10-10 Varnish dropped.
```

Why it fails: both lines record an outcome and neither records the constraint. In month six the first one cannot be evaluated at all, and the second one cannot be distinguished from a decision that was reversed on the 11th.

**What makes a reason good.** It names the thing that forced the choice: a date, a cost, a client's sentence, a physical limit, a rule you set. A reason you could have written before the decision was made is not a reason.

| Reason | Verdict |
|---|---|
| "because the print slot cannot take a second pass before the 14th" | Good. A fact with a handle |
| "because Mira said the shelf sits next to two white competitors" | Good. Names the source |
| "because it looked better" | Useless. Reversible by anyone, including you tomorrow |
| "because it is best practice" | Useless. Names nothing |
| "because of budget" | Weak. Which budget, whose, and is it the same one this quarter |

**When a decision is reversed.** Write the reversal as the decision and delete the line it replaces:

```
- 2026-10-10 Dropped the matte varnish, because the quote came back at 340 and the client would not fund it on top of the second pass.
```

Two lines that say opposite things, one above the other, is the contradiction failure inside a single card. Keep the newest line and the reason that produced it. If the old reason explains why the reversal was needed, fold it into the new line. Otherwise it is gone, which is the correct outcome: it is no longer the reason for anything.

---

## Field 4: What's next

**The question:** what are the next moves, in order?

Three bullets is the useful number. The list is short because it is read at the start of a session and closed at the end of one. Anything longer is a backlog, and a backlog in a memory card is a list of things you have decided not to do yet, which is not memory.

**Works**

```
- Send the revised crate dieline with the reduced glue flap.
- Ask Mira to confirm that the ampersand survives at bag scale.
- File the print spec after sign-off, then confirm this card.
```

**Useless**

```
- Continue working on the project.
- Various follow-ups as needed.
- Waiting on client.
```

Why it fails: none of the three is a move. "Waiting on client" is a state, and it belongs in `Current state` as `blocked on: client sign-off`. A move starts with a verb and ends when it is done.

**The test:** could you start the first bullet now, without asking a question? If not, the missing question is the next move.

---

## Field 5: Key links

**The question:** where does the work actually live?

Folders, files, URLs, thread names, job numbers. One bullet each, with what the thing is.

**Works**

```
- `deliverables/` in this folder: bag artboards, the dieline, the print spec.
- Printer portal: the job number is the folder name, and the portal link is in the job email.
```

**Useless**

```
- Various files in Drive.
- https://example.com/very/long/link/that/nobody/can/identify
```

Why it fails: a link with no description is a link you have to open to identify, which is the same work as finding it. A link that no longer opens is worse than no link, because it reads as current.

**The test:** does the bullet say what is behind the link? If it does not, add four words or delete the line.

`Key links` is also the section most likely to be stale, because a link keeps working long after the thing it pointed at has moved. That is why it carries a date like every other section.

---

## Size and shape rules

| Rule | Value | Why |
|---|---|---|
| Sections per card | 5, plus `Wind-down` on a campaign | The five questions do not change with the project |
| Content lines per section | 40 or fewer | Past that, the section is holding history or two subjects |
| Cards per project | 1 | A second card is a second place to edit |
| Dates | Absolute, `YYYY-MM-DD` | "Last week" stops being true and cannot be checked |
| Tense | `Current state` in the present, decisions in the past | Mixed tense in a state section hides what is true now |

## What never goes in a card

- A transcript, or a pasted conversation. The card is the record of what the session decided, not the session.
- Credentials, keys, tokens, card numbers. A card is read into a session and often synced. Use the name of the password entry instead.
- A whole document. Put the file in `Key links` and keep the card short.
- A fact that already lives at another level. This is the failure the whole product is about.
- A date you did not check. A confirmation is a claim.

## A filled card

A complete project card, 46 lines, every field doing its job. The comments that a scaffold leaves in place are gone, because this card is in use.

```markdown
# memory: Spring catalogue

Level: project
Scope: this project only. Level one facts stay out. They are already true everywhere.
Owns: Marrow Press, Spring List

## Purpose

Confirmed: 2026-10-19

- A twelve-page catalogue for the spring list, print and a matching web page.
- Finished means the printer holds the file, the web page is live, and the title list is signed off.

## Current state

Confirmed: 2026-10-19

- client: Marrow Press
- deadline: 2027-01-09, print slot held
- stage: page grid approved, titles still open
- deliverable: twelve printed pages, one web page, one title list
- print method: litho, four colour, 5,000 copies
- contact: Ines, editor, replies within a day

## Decisions and why

Confirmed: 2026-10-19

- 2026-09-30 Chose a two-column grid over three, because the longest title on the list runs to fourteen words and three columns broke it twice.
- 2026-10-07 Kept the web page as a single scroll rather than a page-per-title, because the list changes every season and a page per title is a rebuild each time.
- 2026-10-15 Dropped the spot varnish, because the quote put it at 610 and the client would not fund it on top of the paper upgrade.

## What's next

Confirmed: 2026-10-19

- Get the title list signed off, which unblocks the grid.
- Set the twelve pages once the list is fixed.
- Send the print file by the 3rd.

## Key links

Confirmed: 2026-10-19

- `pages/` in this folder: the twelve artboards and the grid file.
- `titles.csv`: the current list, which is the only version that counts.
```

To test the boundary, duplicate a card in your own workspace and deliberately extend its current-state section beyond the stated limit. Run the audit on that copy and check the finding before changing your working record.
