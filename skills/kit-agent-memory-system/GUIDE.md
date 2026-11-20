# AI Project Memory

A method for giving an agent a memory you can inspect and check for stale information, and a folder you can carry to the next provider.

Most memory advice stops at "tell the model about yourself". That is level one, and on its own it makes a model that knows your job title and forgets your project. The work is in the boundary between three levels, and in the one field that makes a memory file worth opening half a year later: the reason behind a decision.

## The words this guide uses

Nothing below needs learning before you start. Come back when a word gets in the way.

| Word | What it means here |
| --- | --- |
| Agent | An AI assistant such as Claude Code, Codex or Antigravity CLI, which starts each session with no memory |
| Context | Everything the assistant can see in one session |
| Level | One of the three layers of memory, each with a single job |
| Memory file | A plain text file holding confirmed facts, kept on your own disk |
| Stale | Still written down, but no longer true |
| Prune | Removing an entry that is no longer true, on a stated schedule |
| Provider | The company whose AI assistant you use |

---

---

## 1. The problem this solves

An agent starts every session with nothing. Four things go wrong when you try to fix that by piling context into one place.

1. **The context grows until nobody reads it.** Every session adds a line. Nothing is ever removed. In three months the file is 500 lines, the current state is buried in the middle, and the model spends its attention on a decision you reversed in April.
2. **The levels disagree.** Your account memory says you write in British English and your project says American. The project says the deadline is the 14th and the workspace says the 21st. The model picks one, silently, and you find out in the output.
3. **The outcomes are recorded and the reasons are not.** The file says "dropped the foil stamp". In month six nobody can tell whether that was a budget call that has since changed or a printer constraint that still holds. So it gets reversed by accident.
4. **One project leaks into another.** A client name, a price, a codename sits in a place that is read during every session, including the sessions about other clients.

None of these is a prompting problem. They are a filing problem. The fix is three levels, one boundary, and one card per project that says what changed and why.

---

## 2. The three levels

| Level | Where it lives | Scope | How often it changes | What it is for |
|---|---|---|---|---|
| One | Account memory in the tool: personalisation, custom instructions, a user profile | You, everywhere | Monthly at most | Who you are, how you write, what is always true |
| Two | Project memory in the tool: a project, a saved instruction set, a scoped context | One project | Every session | The working context for this piece of work |
| Three | A folder on your disk, plain Markdown | Every project, as a record | At the end of each session | The decisions, the reasons, the links, the state, in a form you own |

**Level one is who the person is.** Role, the work you do, the languages you work in, spelling and units, the voice you want back, standing rules ("never invent a citation", "no exclamation marks", "ask before you spend money"). It is stable and slow-changing. It is read in every session, including sessions about work you have not started yet.

**Level two is one project, sandboxed.** What this piece of work is for, what finished looks like, the current state, the constraints that only apply here, the vocabulary of this client. The tool loads it when you are inside that project and not otherwise. It is the level that changes fastest, and the level that is easiest to bloat, because it is the one you are staring at while you work.

**Level three is a folder on disk.** One card per project, one card for the workspace, and an index that lists them. Plain Markdown. No database, no export format, no account. It is written at the end of a session and read at the start of the next one, and it is the only level that survives a change of provider, a change of tool, or a change of mind about which model you use.

Level three is the level people skip. It is also the only one they can keep.

---

## 3. The boundary between them

The rule is one sentence: **one fact, one home.** Everything below follows from it.

| Rule | Why it exists |
|---|---|
| Level one carries no project state | Level one is read in every session. A project fact there is read during unrelated work, goes stale without anyone noticing, and cannot be corrected by the project that owns it |
| Level two does not restate level one | Two copies drift. The copy inside the project is the one the model reads, so a change to level one never reaches the work |
| Level three records the summary and the reasons, not the working context | A duplicate is a second place to edit. The card is the record of what a session decided, not a copy of the session |
| A project's proper nouns do not appear on the workspace card | The workspace card is read while you work on something else. A client name there is a leak waiting for the wrong session |

Two questions decide almost every case.

1. **Is this true of me everywhere, or only inside one piece of work?** Everywhere goes to level one. One piece of work goes to level two.
2. **Will I need it after the session ends, or after I change tools?** If yes, it goes on a card. If it is only useful inside the conversation, it stays in level two and dies there, which is correct.

The test that catches most mistakes: **would this still be true in a different project?** A rate card is true everywhere. A rate quoted to this client is not. British spelling is true everywhere. This client's preference for the Oxford comma is not.

`references/level-boundaries.md` has a row for every kind of fact that turns up in working memory, the level that owns it, and the row it usually gets misfiled into.

---

## 4. The card

Every card has the same five sections, in the same order. The order is the contract: a reader, human or model, can find any field without hunting.

| Field | The question it answers | What it must not become |
|---|---|---|
| `Purpose` | What is this for, and what does finished look like? | A mission statement |
| `Current state` | What is true today? | A history |
| `Decisions and why` | What did we decide, and what forced it? | A changelog |
| `What's next` | What are the next moves, in order? | A backlog |
| `Key links` | Where does the work actually live? | A bookmark dump |

Above the sections, a short header block: the level (`workspace`, `project` or `campaign`), the scope in one sentence, and the owner. A project card also names the proper nouns it owns. A campaign card also carries the date it ends. Under each heading, one line: `Confirmed: YYYY-MM-DD`. That date is what makes staleness visible, and it is the first thing the audit reads.

`references/memory-md-shape.md` gives the standard shape, a filled card, and for each field an example of an entry that works and an entry that is useless.

---

## 5. Decisions and why: the field that earns the file

The first four fields are recoverable. You can reconstruct the purpose from the deliverable, the state from the folder, the next moves from the last email. You cannot reconstruct a reason. It was in the conversation, and the conversation is gone.

That is why the third field carries its reason on the same line:

```
- 2026-09-22 Dropped the foil stamp from the crate, because the held print slot cannot take a second pass before the 14th.
```

In month six this line does three jobs that nothing else in your system does.

1. **It tells you whether the constraint still holds.** "Held print slot" is a fact with a date. You can check it. "Dropped the foil stamp, budget" is a fact with no handle: which budget, whose, and does it still apply?
2. **It stops the decision being reversed by accident.** A new model, a new freelancer, or you after a holiday will re-propose the thing that was already rejected. The reason says why it was rejected, so the second conversation starts where the first one ended.
3. **It shows you the shape of your own judgement.** After forty of these lines you can see what you actually optimise for when a deadline and a finish conflict. That is not available from a list of outcomes.

A decisions list without reasons is a changelog. A changelog tells you what happened in the order it happened. A decisions list tells you what would have to change for the decision to be wrong.

The rule the audit enforces is mechanical: the line has to contain a reason clause, one of **because**, **since**, **so that**, **so we**, **so i**, **otherwise**, **to avoid**, or the word **reason**. That is a floor, not a standard. The standard is that the reason names the thing that forced the choice: a constraint, a cost, a date, a client's sentence. If the reason is "it seemed better", delete the line and decide again.

---

## 6. When to update

Three triggers, and no others. Adding to a card at any other time is how a record turns into a log.

1. **A decision is made.** Write it the same day, in the decisions list, with the reason and the date. Same day, because the reason is the part you forget first.
2. **A deliverable lands.** Change the state line, remove the item from `What's next`, and change the date on both sections you touched.
3. **The session ends.** Add or reorder `What's next`. Confirm the sections you relied on, even if you did not change them, because a confirmation is a claim that the line is still true and you have just tested it. Then open `index.md` and check it by eye: every row points at a card that exists, every card has a row, and the one-line summary still describes the state rather than the purpose.

A section you did not touch is not confirmed by a session that did not look at it. Leave its date alone. A card where every date moved at once is a card where nobody checked anything, and the audit will not catch that for you.

The index check is the one part of the routine with no tool behind it. It takes twenty seconds, and it is the only place that tells you what you have. A tree where the cards are current and the index is two months old is a tree you will stop opening.

---

## 7. When to prune

**Prune anything that is no longer true, at the moment you notice.** Not at the end of the month, not into an archive. A line that is no longer true is worse than a missing line, because it reads as current.

**The staleness horizon.** A section that has not been confirmed for 90 days is treated as unverified. Ninety days is a judgement, not a law: it is the shortest interval at which a fact in this kind of work is likely to have changed and still be load-bearing. The audit defaults to 90 and takes `--horizon`, and a studio with quarterly cycles might use 120.

What pruning looks like, concretely:

| Situation | Do this |
|---|---|
| A fact stopped being true | Delete the line. Do not add "no longer X" beside it |
| A decision was reversed | Replace the line with the reversal and its reason. Keep the old reason only if it explains why the reversal was needed |
| A decision expired with its deadline | Delete it, and keep the lesson if there is one, on the workspace card |
| A section passed the horizon | Re-confirm it or cut it. Both are answers. A third session without touching it is not |
| A section passed 40 lines | Move the history into the decisions list as decisions, or split the card. Never just keep appending |
| A project closed | Archive the folder, do not delete it. Move the one lesson worth keeping up to the workspace card first |

The one thing you do not prune is a decision with its reason. It is the only part of the file that cannot be rebuilt, and it stays useful long after the project is over.

---

## 8. The four failure modes

### 8.1 A memory that grows without pruning

Symptom: the current state is a running log, with dates from six months ago above the fact you need. The section is 80 lines. Nobody reads past the first screen.

What it costs: attention. A model reading that section spends most of it on history, and the newest fact, which is the one that matters, is in the middle. Your own reading is slower too, so you stop reading it, so it stops being checked.

The fix is structural, not editorial: a state line is present tense and undated. Anything with a date in the past is a record of something that happened, and it belongs in the decisions list if it changed a choice, with the reason attached. If it changed nothing, it belongs in the project's own files or nowhere. The audit reports a section past 40 lines as an error for this reason.

### 8.2 A memory that contradicts itself across levels

Symptom: the workspace says the client is one name and the project says another. The account memory says metric and the project says imperial. The deadline is the 14th in one place and the 21st in another.

What it costs: silent divergence. The model does not stop and ask. It reads both, and one of them wins, and you cannot predict which. You find out in an email to a client.

The fix is one home per fact, plus a check that compares the levels mechanically. The audit compares key-value lines between the workspace card and each project card, and it also takes a list of name pairs, for the subjects that are named rather than keyed.

### 8.3 A memory that records outcomes but not reasons

Symptom: a decisions list where every line starts with a date, a verb and an object, and stops there. "Moved the call to Thursday." "Dropped the varnish."

What it costs: the file looks complete and answers nothing. In month six you cannot tell whether the reason still holds, so you either keep a dead constraint forever or break a live one.

The fix is the reason clause on the same line, and a check that fails a decision line without one. A line the check fails is not a style problem. It is a decision that will have to be made twice.

### 8.4 A memory that leaks one project into another

Symptom: a client name on the workspace card, a price from one project quoted in another, a codename that means nothing to anyone outside one folder appearing in a session about something else.

What it costs: the wrong name in an email, a confidential detail in an unrelated draft, and a slow erosion of the separation that made the levels worth having. It also quietly makes the workspace card stale, because a project fact on it cannot be maintained by the project.

The fix is the ownership line on each project card and a check that looks for those names on the workspace card. The deeper fix is the habit: if a line would need the project's folder to make sense, it is not a workspace line.

---

## 9. Portability: why level three is the one that lasts

A provider's memory belongs to the provider. It is stored in their format, read by their retrieval, and exported, if at all, as a document that has already lost its structure. Level three is a folder of Markdown files that you own, that any editor opens, that any agent can be pointed at, and that diffs cleanly in git.

The argument is not about today's tool. It is that the card you write now has to be readable by a tool that does not exist yet, and the only format with a chance of that is plain text with headings.

### What moves unchanged

- Every `memory.md` card, byte for byte. It is Markdown with headings, bullets and one date line.
- `index.md`, the list of cards.
- The folder layout: one folder per project, one card inside it.
- The tools in this product. `memory_audit.py` reads Markdown and nothing else, so it runs the same on the new provider's machine.
- Every decision and every reason. This is the part that is actually being moved.

### What has to be re-entered

- **Level one.** The new tool has its own place for account memory, personalisation or custom instructions, and it starts empty. You retype it from your own summary. This is the strongest argument for keeping that summary short and on disk.
- **Level two.** The project's instruction set belongs to the old tool's project. You create the project in the new tool and paste in the card, or the part of it that is working context.
- **Connections and permissions.** Connectors, authorisations, folder access. These are not memory and they do not travel.
- **Saved prompts and skills.** If they lived in the old tool's library, they stay there.

### What is lost

- Every conversation the provider remembered and you never wrote down. This is the bulk of it, and it is why the end-of-session write matters more than the migration.
- Anything the provider inferred about you and never showed you. You cannot audit a preference that was never stated, and you cannot move it.
- Attachments that were links into the provider's own storage. The card can say where the file is, but the link dies with the account.
- The provider's retrieval index. The new tool will not know which parts of the card you look at most.

### What breaks

- **Context size.** A card written for a tool that holds a lot at once is not automatically read whole by one that holds less. This is the practical reason for the 40-line limit per section: it keeps the card small enough to be read in full, not summarised.
- **Folder reading.** Some tools read a folder; some read the one file you attached. A card that relied on a sibling file being read will lose that file. Put anything essential in the card and keep the sibling as the long form.
- **Model behaviour.** A different model may follow the same card differently. The card records what you decided, not what the model does with it.

---

## 10. Migrating a bloated level one

The common starting position: a year of account memory that has become the whole business, with client names, deadlines and project state in it. Do this in order.

1. **Freeze.** Stop adding to level one. Nothing goes in until the migration is done.
2. **Export and read it.** Copy the whole thing into one text file. Read every line and mark it `P` (true of the person, everywhere) or `W` (true of one piece of work).
3. **Cut the `W` lines out.** Put them in a scratch list, one bucket per project. Do not write them into anything yet.
4. **Create the workspace card.** Run `memory_init.py --workspace` and fill only the `P` lines that are true of all work. If a `P` line needs a caveat for one project, it is a `W` line.
5. **Create one card per bucket.** Run `memory_init.py --project` for each. Fill `Purpose`, then `Current state`, then the decisions with their reasons. The reasons are the part the old memory does not have, so this step is the real work.
6. **Rewrite level one.** From the `P` list, one short paragraph of identity and a short list of standing rules. Target under 30 lines. If it is longer, some `W` lines survived step 3.
7. **Delete the old level one.** Not archive. An archived copy gets pasted back into a session within a month, and then you have two levels one that disagree.
8. **Run the audit.** `python3 tools/memory_audit.py ./memory --horizon 90`. Fix what it names before you use the tree for real work.
9. **Set a review date.** One line in `What's next` on the workspace card: review the horizon and the level one summary on a named date.

Two things go wrong in this migration often enough to name. The first is keeping a "misc" project for facts that would not sort, which becomes the new bloated level one under a different name. The second is writing the reasons from memory a week later, which produces reasons that sound right and are not. Do step 5 in the same sitting as step 2.

---

## 11. Limits

- **A memory file is not a guarantee that the model reads it.** It is evidence you can check. You can open the card, read the line, and know what the agent was given. You cannot know what it attended to.
- **The audit reads structure, not truth.** It can tell that a section is dated, that a decision line has a reason clause, and that two cards disagree. It cannot tell whether the date is honest, whether the reason is real, or whether the decision was followed.
- **The audit cannot see levels one and two.** They live in a provider's interface, not on your disk. The checks cover level three. The boundary rules are for the levels the tool cannot read.
- **The audit does not check `index.md`.** A row with no card, or a card with no row, is caught by the review step in section 6, by eye. Do that review; the index is the only list of what you have.
- **The audit cannot read meaning.** Two lines that say the same thing in different words are not a contradiction to a string comparison, and two lines that share a key but describe different things will be reported as one. Read the finding before you fix the line.
- **No method makes a model reliable.** This one makes the memory inspectable, which is the part you can control.

---

## Sources and reuse

Source reference: a public workflow separating account memory, project memory and a file-based record. No third-party prompt text, template wording or course material is included. See `README.md` for the product licence and reuse terms.
