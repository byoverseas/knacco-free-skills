# Part library

Paste-ready blocks for all four parts. There are five variants of each part, one per kind of job: research, writing, analysis, a build task, and a decision.

**How to use it.** Pick the kind of job you have. Take the four blocks from that kind, in the order role, input, task, example, and replace every `<angle-bracket>` field. The four blocks from one kind are written to fit together. You can also mix: the role from analysis with the task from writing is fine, as long as the example matches the task.

Every block below carries the element the checker looks for in its part. Replace the fields and the blocks satisfy the rules they touch. A field left in place is the one thing that fails: rule R14 rejects an unresolved placeholder.

**What not to do.** Do not paste all five variants. Do not keep a field you did not fill. Do not add a sentence that praises the example.

---

## 1. Role

A role names a discipline and a level. One or two sentences. The second sentence is where you say what the practitioner is careful about, and that is usually what fixes the output.

### For research

```
You are a research librarian with <n> years of experience running structured searches in <field>. You are judged on coverage, and you mark what you could not find rather than filling it.
```

### For writing

```
You are a technical writer with <n> years of experience turning engineering notes into <form> for <reader>. You write for people who will read the page once.
```

### For analysis

```
You are a data analyst with <n> years of experience in <domain>, working from spreadsheets that other people built. You check the shape of the data before you answer the question.
```

### For a build task

```
You are a solutions architect with <n> years of experience specifying internal tools that a small team has to maintain. You write specifications a developer can start from without a meeting.
```

### For a decision

```
You are an operations consultant with <n> years of experience advising <type of organisation> on <decision type>. You separate the decision from the analysis that supports it.
```

---

## 2. Input

Four things: the situation, the constraints, the material, and the gap. Put the gap last; it is the line the model reads most closely.

### For research

```
We are <who> and we need to know <question> by <date>. <Why the answer is needed now.>

Constraints: the review must stay inside <scope>, use sources from <period>, and exclude <what to exclude>.

We have <what you already hold: databases, a reading list, an internal report>. <One line on its quality.>

We have no access to <missing source>. Say so where it would change the answer. Do not cite anything you cannot name.
```

### For writing

```
We are <who> and we publish <what> for <reader>. Right now <the situation that needs the page>.

Constraints: the piece has to fit <format and length>, it must not <what to avoid>, and it has to stay accurate to <the source of truth>.

We have <notes, transcript, an existing page, a product sheet>.

We have no <missing input>. Leave that section out rather than inventing an example.
```

### For analysis

```
We are <who> and we are deciding <decision> this <period>. Right now <the state of the business in one sentence>.

Constraints: the answer has to use <data set> only, cover <period>, and exclude <rows, regions, or products that do not belong>.

We have <file, export, sheet>, covering <period>, with <known defect: duplicates, missing weeks, a changed category>.

We have no <missing measure>. Name any conclusion that depends on it as provisional. Do not model it.
```

### For a build task

```
We are <who> and we are building <thing> for <users>. Right now <how the work is done, and what breaks>.

Constraints: it must run on <platform>, be maintainable by <team size>, cost no more than <budget>, and ship by <date>.

We have <existing system, schema, sample data, screenshots>.

We have no <missing access, API, or decision>. Ask before you design around it.
```

### For a decision

```
We are <who> and we have to choose <decision> by <date>. Right now <the pressure that forces a choice>.

Constraints: the choice must stay inside <budget, policy, contract>, be reversible within <period>, and be defensible to <audience>.

We have <the two quotes, the trial results, the last three months of figures>.

We have no <missing evidence>. Say which option the missing evidence would change. Do not score it.
```

---

## 3. Task

Five elements: the deliverable, the sections, the length, the register, and what it is usable for. Name all five. Use decides the depth.

### For research

```
Write a research brief of <n> to <n> words.
Use four sections: the question, what the evidence says, what the evidence does not settle, and what to read next.
Register: plain English, third person, no adjectives that rate a study.
It must be usable as the reading pack for a <meeting or decision>, so every claim carries a source and a date.
```

### For writing

```
Write <the deliverable> of <n> to <n> words.
Use <n> sections: <section list>.
Register: <person>, <formality>, <diction>, <spelling>.
It must be usable as <where it will appear>, read by <reader> who has <how much time>.
```

### For analysis

```
Write a findings note of <n> to <n> words.
Use three sections: what changed, where it changed, and what we cannot tell from this data.
Register: plain business English, past tense for what happened, no hedging where the numbers are clear.
It must be usable as the first page of <report or meeting pack>, so a reader who skips the appendix still gets the number.
```

### For a build task

```
Write a build specification of <n> to <n> pages.
Use five sections: the job, the screens, the data, the failure cases, and what is out of scope.
Register: plain technical English, present tense, no marketing words.
It must be usable by a developer starting work on Monday without a follow-up meeting.
```

### For a decision

```
Write a decision note of <n> to <n> words.
Use four sections: the decision, the options, the criterion, and the recommendation.
Register: plain business English, past tense for evidence, present tense for the recommendation.
It must be usable as the paper that <audience> reads before they approve or reject.
```

---

## 4. Example

One passage of the output, at the depth you want. Not a description of the passage, and not an explanation of why it is good. If the deliverable is short, show all of it.

### For research

```
What the evidence does not settle
None of the four studies separates the effect of the reminder from the effect of the person sending it, so the size of the reminder's own contribution is unknown. Two studies measure the outcome at four weeks and one at twelve; the longer measure is the one that matters for a renewal decision, and it is also the one with the smallest sample. No study covers accounts below <threshold>.
```

### For writing

```
To reset the device, hold the button for eight seconds. The light turns amber after four and white after eight. Release when it turns white. If the light never turns white, the battery is below 5 per cent, and the device needs twenty minutes on charge before a reset will work.
```

### For analysis

```
Orders fell by 6 per cent between March and April, and the fall sits in one group: the two-shop accounts. The four larger accounts were flat. The drop is 41 orders, and 38 of them come from three shops that moved their order day from Tuesday to Thursday in the same month. We cannot tell from this data whether the order day or the delivery slot caused the move, because both changed in the same week.
```

### For a build task

```
Screen: current orders
One table, newest first, with four columns: account, order date, value, status. Status is one of three words: placed, packed, collected. The table shows 25 rows and pages after that. There is no search field: the list is short enough to scan, and a search field would need an index we do not have.
```

### For a decision

```
Recommendation
Take the second option: move the print slot to Thursday and keep the current printer. It costs 4 per cent more per unit and removes the late-collection risk that has cost us two jobs this quarter. The first option is cheaper on paper, and it depends on a delivery promise the printer has missed twice.
```

---

## 5. Assembling without a tool

If you are writing the prompt into a chat window rather than a file, keep the four labels in capitals on their own lines. The labels are not decoration: they let a reader, and a later reviewer, see which part a sentence belongs to.

```
ROLE
<one or two sentences>

INPUT
<situation>

Constraints:
<the edges>

<material>

<the gap>

TASK
<deliverable, sections, length, register, use>

EXAMPLE
<one passage of the output>
```

Then paste it as one message. If you keep the labels, `tools/rit_grade.py` can read the same text later and tell you which part is thin.
