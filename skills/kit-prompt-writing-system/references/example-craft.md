# Example craft

The example is the part most prompts leave out, and the part that sets the quality of the answer. This note is about writing one.

An example is not a sample of the topic. It is a sample of the standard: the depth you want, in the voice you want, in the shape you want. The model copies the standard, not the topic.

---

## 1. Length

Match the example to the unit of the deliverable, not to its total length.

| Deliverable | What to show | Why |
|---|---|---|
| Under 200 words | The whole thing | There is no unit smaller than the deliverable |
| 200 to 800 words | One section, at full depth, 100 to 150 words | Depth transfers; a longer sample mostly adds bulk |
| Over 800 words | One section at full depth, plus the opening two lines | The opening sets the register for everything after it |
| A table or a specification | One complete screen, record or screen section | Structure and field order transfer, not the content |
| A decision note | The recommendation section | It is the section people get wrong |

One section at full depth beats a whole deliverable summarised. A 900-word report shown as a 200-word summary teaches the model to write summaries.

If the task asks for two genuinely different outputs, such as a note and the email that sends it, two examples are correct. Otherwise, one.

---

## 2. Specificity

A specific example contains things that could be wrong. A number, a date, a named role, a consequence with a cost. An example full of generalities cannot be wrong, so it teaches nothing.

Three tests:

1. **The stranger test.** Could a stranger tell your example apart from one written for a different company in the same sector? If not, it is a template, not an example.
2. **The number test.** Does it contain at least one figure, date or named thing that carries weight? If not, the model will write around the specifics.
3. **The placeholder test.** Is every field filled? An example with `<client name>` in it teaches the model to leave gaps, and the checker fails it under R14.

Specificity is not decoration. "The third move has taken two days of studio time that was booked for another job" is specific and it also shows the depth: the cost is named in the unit the reader cares about.

---

## 3. Register

Register is the part people describe and then fail to demonstrate. Four things carry it:

- **Sentence length.** A sample with 12-word sentences teaches 12-word sentences, whatever the task says.
- **Person.** "We will send the artwork" and "the artwork will be sent" produce different answers.
- **Vocabulary.** Whether the sample says "customers" or "accounts", "cost" or "unit cost", sets the dictionary for the answer.
- **Spelling and punctuation.** British spelling in the sample produces British spelling in the answer, with no instruction needed.

The read-aloud test: read the example aloud. If you would not say it in the room where the output will be read, the register is wrong, and the answer will be wrong in the same way.

---

## 4. What to leave out

- **Praise for the example.** "Here is a strong example" teaches the model to announce quality rather than demonstrate it.
- **Explanation.** "Notice how the recommendation comes last" is an instruction, not an example. Put it in the task.
- **Meta commentary.** "This shows the tone we want" is a description of the example, one layer out.
- **A second example of the same output.** Two standards produce the average of both.
- **Headings the task did not ask for.** The example is where invented structure enters.

The example field holds the passage and nothing else. Everything you want to say about the passage belongs in the task.

---

## 5. Three ways a bad example poisons a prompt

### It teaches the wrong depth

A 40-word paragraph pasted as the example for a 900-word analysis produces a 900-word answer with 40 words of content and 860 words of padding. The model has been shown that one point gets one sentence, so it spreads one sentence over a page.

This is the most common failure, and the hardest to see, because the output is the right length. The tell is that every section is the same size and none of them goes anywhere.

### It teaches the wrong register

A sample written quickly in a chat window arrives with chat-window habits: contractions, "let's", "really", a question at the end. Ask for a formal board paper and you get a board paper that opens with "So, here's the thing". The task said formal; the sample said otherwise; the sample wins.

### It teaches the wrong shape

A sample with four sections for a task that names three produces four. A sample in bullets for a task that bans bullets produces bullets. A sample borrowed from a neighbouring job carries that job's structure, and the model has no reason to prefer your sentence about sections over the concrete shape in front of it.

The three failures compound. A borrowed example is usually wrong in depth, register and shape at once, which is why a prompt with a borrowed example is harder to repair than a prompt with no example at all.

---

## 6. The same deliverable, written weakly and strongly

The deliverable: a 120-word risk note for a project board, on a migration that may slip.

### Weak

```
The note should set out the main risk, how likely it is, what it would cost if it happened, and what we propose to do. Keep it formal, keep it short, and put the decision at the end.
```

Forty words. It lists the ingredients and lets the model choose the quantities. It is also impossible to fail: any note that mentions a risk, a cost and a decision satisfies it. What comes back is a risk-register entry with no dates, no figures and no recommendation, written in whatever register the model defaults to.

### Strong

```
Risk: the migration slips past the May release window

The supplier's test environment is not ready, and their last two dates each moved by three weeks. If the migration slips past 12 May, the old system has to be supported for another quarter at £14,000, and the two staff who know it leave in June.

We propose to freeze the migration scope on 30 April and move the customer-history tables into a second phase. That protects the May date at the cost of four reports, which can run on the old system until July.

Decision needed by 24 April.
```

About 100 words, which is what 120 looks like once the title and the decision line are counted. Four things make it teach:

- **Depth.** One risk, traced to two dated facts, priced, and answered with a proposal. Nothing else is introduced.
- **Register.** Plain, past tense for what happened, present for the proposal, no adjective rating the risk.
- **Shape.** Title that names the consequence, two body paragraphs, a decision line. A reader can copy that shape.
- **Specificity.** 12 May, £14,000, 30 April, four reports. None of these could be guessed, so the answer has to work for the facts rather than around them.

Notice what is absent: no explanation of why the note works, no second example, no praise. The passage is the whole example.

---

## 7. Five questions before you paste it

1. Is it a passage of the output, or a description of the output?
2. Is it at the depth I want, in the unit I asked for?
3. Would I send it? If not, repair it before it becomes the standard.
4. Is every field filled with something that could be wrong?
5. Does it demonstrate the sections and the format the task names, and nothing else?

A no at question 1 or 3 is a stop. A no at the others is a repair.
