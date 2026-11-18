# The audit rules

`tools/memory_audit.py` reads a tree of cards and reports what would make them useless. Every rule below is a failure that has already cost someone an hour.

## How to run it

```sh
python3 tools/memory_audit.py ./memory
python3 tools/memory_audit.py ./memory --horizon 60 --as-of 2026-10-26
python3 tools/memory_audit.py ./memory --json
```

| Flag | Default | What it changes |
|---|---|---|
| `ROOT` | required | The folder that holds the tree. It finds every file named `memory.md` under it |
| `--horizon` | 90 | How many days a section may go unconfirmed before it is stale |
| `--as-of` | today | Treat this date as today, so a run can be reproduced |
| `--max-lines` | 40 | Content lines one section may hold |
| `--json` | off | Print the cards and the findings as JSON |

Exit `2` if there is at least one error. Exit `0` otherwise, warnings allowed. That makes it usable as a gate: `python3 tools/memory_audit.py ./memory || echo "fix the card"`.

## What it reads

Only files named `memory.md`. It parses `##` headings, bullet lists, `Confirmed:` lines, the header block above the first heading, and HTML comments (removed before parsing, so an instruction comment does not count as content). It never looks at `index.md`, and it never guesses: a fact it cannot parse is a fact it cannot check, and rule S02 exists so that silence is not treated as freshness.

A folder with no cards in it reports `0 cards` and exits 0. A mistyped path therefore looks like a clean tree, so read the card count on the first line of every run, not just the findings.

Passing the audit does not mean the memory is true. It means the memory is in a shape where you can tell whether it is true.

## The rules

| Rule | Severity | Finds |
|---|---|---|
| S01 | error | A section confirmed longer ago than the horizon |
| S02 | error | A section with content and no readable `Confirmed:` date |
| C01 | error | One subject stated two ways across levels |
| D01 | error | A decision line with no reason clause |
| L01 | error | A project-owned name on the workspace card |
| O01 | error | A section past the line limit |
| E01 | error | A heading with no content |
| X01 | error | A file named `memory.md` with no sections at all |
| W01 | warning | A card missing one of the five canonical sections |

Each rule's worked example below is a real run on a two-card tree with one fault in it. The block shows the table and the count line as printed; the run's first line, which reports the date and the card counts, is left out. A workspace can trigger several of these rules at once.

---

## S01: stale

**What it checks.** The section's `Confirmed:` date is more than `--horizon` days before the audit date.

**Why it is a real failure.** A memory line does not announce that it expired. It reads exactly as confidently in month three as it did on the day it was written. The date is the only signal, and nobody reads the date. A link section written in May and read in October is six months of dead links that still look like infrastructure.

**Worked example.** A workspace card whose `Key links` was last confirmed on 2 May:

```
FILE       LINE  RULE  SEV      FINDING
memory.md    32  S01   error    'Key links' was last confirmed 2026-05-02, 177 days ago, past the 90-day horizon

1 error, 0 warnings
```

The fix is one of two things, and the audit does not care which: confirm the section by reading it, or cut it. What it will not accept is a third session that touches nothing.

---

## S02: undated

**What it checks.** A section has content and no `Confirmed:` line with a readable `YYYY-MM-DD` date.

**Why it is a real failure.** It is the way a person defeats S01 without meaning to. Delete the date, or write "recently", and the stale check has nothing to compare, so the section passes by being unmeasurable. An undated section with content is a claim with no evidence, and the two failures are close enough to report in the same family.

**Worked example.** The same card, with the `Confirmed:` line removed from `Current state`:

```
FILE       LINE  RULE  SEV      FINDING
memory.md    12  S02   error    'Current state' has content but no readable Confirmed date (no line)

1 error, 0 warnings
```

A section with no content and no date is not reported here. It is reported as E01, because an empty heading is the more accurate description of the problem.

---

## C01: contradiction

**What it checks.** One subject stated differently on two cards at different levels. Two mechanisms:

1. **Key-value comparison.** Every bullet in `Current state` of the form `key: value` is compared between the workspace card and each project or campaign card. A shared key with a different value is a finding. A value that means "not applicable" (`none`, `n/a`, `tbd`, `unknown`, `not set`, `no`) is skipped, because a project that has no client is not contradicting a project that has one.
2. **Name pairs.** A list at the top of the tool, `CONTRADICTION_PAIRS`, holds triples of a subject and two names for it. A pair fires when one card uses the left name and a card at another level uses the right name. It exists for subjects that are named rather than keyed: a provider, a company, a person.

Both mechanisms report under the same subject, so one subject that both mechanisms see is one finding with both pieces of evidence on it.

**Why it is a real failure.** The model does not stop and ask when two levels disagree. It reads both, one of them wins, and you find out in the output. The audit cannot tell you which one is right. It tells you that you have to decide.

**Worked example, key-value.** A workspace card with `client: Autumn and Roe` and a project card with `client: Adeyemi & Roe`:

```
FILE       LINE  RULE  SEV      FINDING
memory.md    17  C01   error    'client' is stated differently across levels: memory.md:17 has 'client: Autumn and Roe'; projects/autumn/memory.md:17 has 'client: Adeyemi & Roe'

1 error, 0 warnings
```

**Worked example, name pair.** A workspace card with `model provider: ChatGPT` and a project card with `model provider: Claude`, using the shipped pair list:

```
FILE       LINE  RULE  SEV      FINDING
memory.md    17  C01   error    'model provider' is stated differently across levels: memory.md:17 has 'model provider: ChatGPT'; projects/autumn/memory.md:19 has 'model provider: Claude' (name pair 'Claude' against 'ChatGPT')

1 error, 0 warnings
```

The note on the end says which second mechanism also saw it. Edit `CONTRADICTION_PAIRS` for your own workspace: two names for the same client, a product with a short name and a long one, a company that renamed itself mid-project.

---

## D01: decision with no reason

**What it checks.** Every bullet in a section whose heading starts with `Decision` must contain one of the reason clauses: **because**, **since**, **so that**, **so we**, **so i**, **otherwise**, **to avoid**, or the word **reason**.

**Why it is a real failure.** The decision is recoverable from the deliverable. The reason is not. A list of outcomes is a changelog, and a changelog cannot tell you whether the constraint that produced it still holds, so it cannot tell you whether the decision can be revisited. This is the rule that earns the product.

**Worked example.** One decision appended without a reason:

```
FILE       LINE  RULE  SEV      FINDING
memory.md    23  D01   error    decision with no reason: '2026-10-21 Moved the studio call to Thursday.'

1 error, 0 warnings
```

The check is mechanical and the standard is higher than the check. A line that passes with "because it looked better" is still a line that will have to be decided again. Rewrite until the reason names the thing that forced the choice: a date, a cost, a client's sentence, a physical limit.

---

## L01: leak

**What it checks.** Each project and campaign card declares the proper nouns it owns, on its `Owns:` line. The audit looks for each of those names anywhere on the workspace card. A hit is a finding.

**Why it is a real failure.** The workspace card is read during every session, including sessions about other work. A client name there ends up in an unrelated draft, a price there is quoted to the wrong person, and a confidential detail there leaves the sandbox. The second cost is quieter: the project cannot maintain a fact that sits on a card it does not own, so the line goes stale and nobody is responsible for it.

**Worked example.** A workspace card whose `What's next` says "Send Adeyemi & Roe the second proof", where the project card owns that name:

```
FILE       LINE  RULE  SEV      FINDING
memory.md    28  L01   error    'Adeyemi & Roe' belongs to projects/autumn, so it does not belong at workspace level

1 error, 0 warnings
```

Two details make the check predictable. A name that matches the project's own title is not reported, because naming a project on the workspace card is legitimate: the index has to name it. And the match is on the exact owned string, so `Adeyemi and Roe` does not match an owned `Adeyemi & Roe`. That is why the four-fault example reports its client-name fault as C01 and not as L01. If you need both forms caught, list both on the `Owns:` line.

---

## O01: oversize

**What it checks.** A section holds more content lines than `--max-lines` allows, 40 by default. Content lines are non-blank lines that are not comments and not the `Confirmed:` line.

**Why it is a real failure.** Past about a screen, a section stops being read whole. A model spends its attention on the oldest text and the newest fact is somewhere in the middle. You stop reading it too, which means you stop checking it, which is how the section got that long. The usual cause is a state section used as a log: every event appended, nothing removed.

**Worked example.** A project card whose `Current state` grew to 44 lines:

```
FILE                       LINE  RULE  SEV      FINDING
projects/autumn/memory.md    13  O01   error    'Current state' holds 44 content lines, over the 40-line limit

1 error, 0 warnings
```

The fix is not to raise the limit. It is to move the dated lines into `Decisions and why` with their reasons, or to notice that the section is holding two subjects and needs two cards.

---

## E01: empty section

**What it checks.** A `##` heading with no content under it. A heading, its instruction comment, and a `Confirmed:` line do not count as content, and neither does a bare bullet with nothing after it.

**Why it is a real failure.** An empty heading is a promise that the field is handled. A card with an empty `Decisions and why` looks like a project with no decisions, which is never true. The section is either not started or it was emptied during a prune and never refilled, and both need a decision from you.

**Worked example.** A card whose `Decisions and why` holds only a comment:

```
FILE       LINE  RULE  SEV      FINDING
memory.md    17  E01   error    'Decisions and why' has a heading and no content

1 error, 0 warnings
```

A brand-new scaffold audits as five E01 findings, one per section, because every section is still a comment and a fill marker:

```
FILE       LINE  RULE  SEV      FINDING
memory.md    10  E01   error    'Purpose' has a heading and no content
memory.md    18  E01   error    'Current state' has a heading and no content
memory.md    26  E01   error    'Decisions and why' has a heading and no content
memory.md    34  E01   error    'What's next' has a heading and no content
memory.md    42  E01   error    'Key links' has a heading and no content

5 errors, 0 warnings
```

A scaffold is not a memory. It is the shape of one.

---

## X01: not a memory card

**What it checks.** A file named `memory.md` with no `##` sections.

**Why it is a real failure.** A file called `memory.md` that is actually a page of notes will be trusted as a card and it is not one. It has no fields, no dates and no state, so nothing on it can be checked, and the person reading it will believe the tree is in better shape than it is.

**Worked example.**

```
FILE                       LINE  RULE  SEV      FINDING
projects/autumn/memory.md     1  X01   error    no '##' sections found, so this file cannot be read as a memory card

1 error, 0 warnings
```

Either give it the five sections, or rename it. A file that is not a card should not be called one.

---

## W01: missing canonical section

**What it checks.** One of the five canonical sections is absent from a card.

**Why it is a real failure.** A missing field cannot be checked and cannot be filled at the end of a session, because there is nowhere to put the line. The usual case is a card built by hand that skipped `Key links`, so the folder has no route back to the actual work.

**Worked example.** A workspace card with the `Key links` section deleted:

```
FILE       LINE  RULE  SEV      FINDING
memory.md     1  W01   warning  canonical section 'Key links' is missing

0 errors, 1 warning
```

It is a warning, not an error, because a card can add sections of its own: a campaign card adds `Wind-down`, and a card for a regulated project might add `Approvals`. It cannot drop one of the five.

---

## What the audit cannot see

- **Whether a date is honest.** `Confirmed: 2026-10-24` on a section nobody read is a lie that passes every rule.
- **Whether a reason is real.** The check reads for the clause, not for the thinking.
- **Levels one and two.** They live in a provider's interface. The audit covers level three, which is the part you own.
- **The index.** A row with no card, or a card with no row, is not reported. That is the review step at the end of a session, by eye.
- **Meaning.** Two lines about the same subject in different words are not a contradiction to a string comparison. A shared key on two cards that describe genuinely different things will be reported, and you have to read the finding before you change the line.
- **A contradiction inside one level.** Two project cards that disagree with each other are not compared, because different projects are allowed to differ. Within one card, a decision that survived its own reversal is not caught at all.
