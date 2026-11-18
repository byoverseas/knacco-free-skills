# Level boundaries: which level owns which fact

The rule is one sentence: **one fact, one home.**

A fact with two homes will eventually disagree with itself, and the copy inside the session wins. This reference takes every kind of fact that turns up in working memory and names its home, whether it also appears on a card, why, and where it usually gets misfiled.

## How to read the table

| Column | Meaning |
|---|---|
| **Home** | The level that owns the fact and is allowed to change it. `L1` account memory, `L2` project memory, `L3` the folder on disk, `none` means it is not stored |
| **On the card** | Whether a card in the folder also carries it, and which card. A card carries a summary or a record, never a second authoritative copy |
| **Why** | The reason that level owns it |
| **Misfiled as** | Where it usually ends up instead, which is the failure this product exists to stop |

The distinction between **Home** and **On the card** is the one people miss. A fact about you is owned by level one. The workspace card may carry four words of it so that you can rebuild level one on a different provider. Those four words are a record, not a home: when they disagree, level one is right and the card is out of date.

## The table

### About the person

| Fact | Home | On the card | Why | Misfiled as |
|---|---|---|---|---|
| Name, role, what you do | L1 | workspace, summary | Read in every session, changes about once a year | Restated on every project card, in slightly different words |
| Voice and tone rules | L1 | workspace, summary | Applies to every output you ask for | Copied into each project card, then edited in one of them |
| Spelling, units, currency, date format | L1 | workspace, summary | One answer is right everywhere | A project card that says American spelling while the account says British |
| A hard rule ("never invent a citation") | L1 | workspace, summary | It is a rule, not a fact about a project | Project card, so the other project does not have it |
| Accessibility or format needs | L1 | no card | It is about the person, not the work | Project card, where it is lost on the next project |
| Team names and roles | L1 | workspace, summary | Small and stable, and true of all work | Project card, repeated |
| A preference stated once, for one project | L2 | project | One mention is not a pattern | Level one, permanently, after a single sentence in one session |
| A preference stated in three projects | L1 | workspace, summary | Repetition is the promotion test | Left in three project cards with three wordings |

### About the tools

| Fact | Home | On the card | Why | Misfiled as |
|---|---|---|---|---|
| Tool stack used across all work | L1 | workspace, summary | True in every session | Listed per project, and out of date in two of them |
| A tool used on one project only | L2 | project | It matters only inside that work | Level one, where it is read during unrelated sessions |
| A recurring workflow ("how I run a proof round") | L1 | workspace, summary | Reused, and the same each time | Project card, copied for each project |
| A one-off instruction for today | L2, session only | no card | It expires with the session | Level one, where it becomes permanent by accident |

### About one project

| Fact | Home | On the card | Why | Misfiled as |
|---|---|---|---|---|
| Client name | L2 | project | It is part of the project's identity | Workspace card, where it is read during other work |
| Client contact, hours, oddities | L2 | project | Only useful while this work runs | Level one |
| The client's vocabulary and house style | L2 | project | Their words, not yours, and only for their work | Level one, where it fights your own voice |
| Project purpose and what finished looks like | L2 | project | It ends when the work ends | Level one |
| Current state of the project | L2 | project | It changes weekly | Level one, where it goes stale without anyone noticing |
| A deadline for this project | L2 | project | It has a date and it ends | Level one, the most common stale fact in any account memory |
| A decision and the reason for it | L2 | project | The reason only makes sense against this work | Nowhere, which is the failure the whole product is about |
| Where a deliverable lives | L2 | project | A path or a URL for this work | Level one |
| A supplier or printer used here | L2 | project | Specific to the work | Level one |
| Something confidential about this client | L2 | project | It must not travel to another session | Level one, or worse, the workspace card |
| A transcript of the session | none | no card | The card is the record, not the session | Project card, appended, until the card is a log |

### About money

| Fact | Home | On the card | Why | Misfiled as |
|---|---|---|---|---|
| Your rate card | L1 | workspace, summary | True of all work | Project card, where the next project cannot see it |
| A price quoted to this client | L2 | project | Confidential to them, and specific to the scope | Workspace card, which is a leak with money in it |
| Billing terms that bind all work (deposit, balance) | L1 | workspace | True everywhere | Buried in one project card |
| A budget for this campaign | L2 | campaign card | It dies with the campaign | Level one |

### About the past

| Fact | Home | On the card | Why | Misfiled as |
|---|---|---|---|---|
| A lesson from one failure | L2 | project | It needs its context to be applied correctly | Level one, where it becomes a rule nobody can trace back |
| A lesson that recurred in three projects | L1 | workspace, summary | It is now a standing rule | Three project cards, none of them current |
| A closed project's outcome | L3 | archive, one line | Kept for the lesson, not for the work | Level one, which is how account memory reaches 500 lines |
| The list of what exists | L3 | `index.md` | A list, not a fact about the work | Project card |

### Never

| Fact | Home | On the card | Why | Misfiled as |
|---|---|---|---|---|
| Credentials, keys, tokens, card numbers | none | no card | A card is read into a session and often synced | Level one, a project card, and a chat message |
| A whole document | none | no card | The card links to it | Pasted into a section, which then passes 40 lines |
| A date you did not check | none | no card | A confirmation is a claim | A `Confirmed:` line, which the audit cannot catch |

## Three hard cases

**A fact that looks like it belongs to two levels.** "The client prefers no Oxford comma." Is that a voice rule or a client detail? It is a client detail, because it is about them, and your own comma rule is a different fact. Put it on the project card and do not restate your own rule there. If the client's preference contradicts your rule, the project card wins inside that project, and that is the only place a conflict is allowed to resolve.

**A fact that is true now but only for this quarter.** "Working from Lisbon until January." Not identity, because it ends. Not project state, because it is not about a project. Put it in level one with the end date in the same line, and diarise the deletion. A temporary fact with no expiry is how level one grows.

**A fact about a person that is also a project constraint.** "Mira replies on Tuesdays." That is about the client's buyer, so it is a project fact. "I do not take calls before 10." That is about you, so it is level one, even if it was first said during this project.

## When a fact moves

Facts are promoted and demoted. Both moves need a rule, or the levels drift.

**Promote L2 to L1** when one of these is true:

- The fact has appeared in three separate projects. Repetition is evidence; one mention is not.
- A decision was made that binds all future work ("we bill in two stages from now on").
- The fact is about you rather than about the work, even if you first said it during this project.

**Demote L1 to L2** when one of these is true:

- It is no longer true everywhere. A rule with one exception is a project fact plus a general rule.
- It has an end date. Anything temporary belongs one level down, where it is read less.
- It is a preference that turned out to be about one client.

**Delete, in either direction,** when the fact is no longer true. A demoted fact that is copied rather than moved is a second home, and that is the contradiction failure.

## The three misfilings that do the most damage

1. **A client name on the workspace card.** The card is read during every session, including sessions about other clients. The name gets used in the wrong draft, and the project cannot maintain the line because it does not own it.
2. **A deadline in level one.** It is read in every session, so it looks current long after it passed. Nobody notices, because nobody expects a deadline to be in the account memory.
3. **A preference promoted after one mention.** It becomes permanent, and it is wrong, and every output carries it. The promotion test exists for this reason.
