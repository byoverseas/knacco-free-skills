# Prompt Writing Guide

A prompt that earns its name is a small specification. It says who is answering, what is true, what must come back, and what good looks like. Four parts, in that order.

The aim is not a better sentence. The aim is a request you can run again next month with different facts and get work of the same shape and the same depth. That is the difference between a prompt and a question.

## The words this guide uses

Nothing below needs learning before you start. Come back when a word gets in the way.

| Word | What it means here |
| --- | --- |
| Role | Who the assistant is answering as, including the field it works in |
| Input | The facts and material the assistant is given |
| Task | What must come back, named as a deliverable rather than a wish |
| Example | A sample of good output, which is what teaches the standard |
| Deliverable | The finished thing: a list, a draft, a table, a decision |
| Register | How formal the writing should be |

---

---

## 1. The problem this solves

Four failures. They are one failure seen from four sides.

1. **The answer is plausible and unusable.** It reads well, covers the topic, and cannot be sent to anyone. You cannot tell whether the model failed or the request did, so you rewrite the request and hope.
2. **The good result cannot be repeated.** Run one was sharp. Run two is a summary. Nothing changed except the wording you typed, and you did not keep the wording.
3. **Two people write the same job differently.** The studio, the agency, the team of four: each person asks in their own words and gets a different standard. Nobody can review the request because there is nothing to review.
4. **The model fills what you did not supply.** Ask for a customer profile with no material and you get a plausible customer, invented in the shape of the last profile the model read. The invention is invisible because it is fluent.

Each failure is a missing part. The fix is structural: name the parts, fill them, and check the prompt before you spend a run on it. A prompt can be checked in a way an answer cannot.

---

## 2. The four parts at a glance

| Part | The question it answers | What it changes in the output | What goes wrong without it |
|---|---|---|---|
| **Role** | Who is answering? | Vocabulary, the knowledge it treats as relevant, and how far it commits to a judgement | A general answer in general language, with every option left open |
| **Input** | What is true, what are the edges, what is missing? | The specifics the answer is built from, and the invention it does instead | Fluent generalities, or invented facts dressed as findings |
| **Task** | What must come back? | The shape, the length, the register and the level of detail | The right topic in the wrong form, at the wrong length, for nobody in particular |
| **Example** | What does good look like? | The quality bar: depth, sentence length, how much detail one point gets | The model's default style, which is the average of everything it has read |

Write them in this order. The order matters on the page as well as in the prompt: a reader, human or model, can find any instruction without hunting.

---

## 3. Role

### What a role changes

A role changes three things. Nothing else.

- **Vocabulary.** A pricing analyst says "list price", "margin", "band". A general assistant says "cost" and "price point". The words carry the precision, and the precision carries the thinking.
- **Knowledge domain.** The role decides what counts as relevant. A client services consultant treats a missed sign-off as a scheduling fact. A lawyer treats the same event as a contractual one. Both are right, and they are different answers.
- **Decisiveness.** A named practitioner commits. "In most cases you should raise it in writing before the third miss" is a judgement. A generic assistant lists five options and recommends none, because it has no practice to draw on.

### Why a role without a domain is a costume

"You are a brilliant marketing expert" changes the accent, not the knowledge. It adds confidence words to an answer that has no more information in it. The model has no way to turn praise into a domain, so it performs the praise instead.

The same happens with a field without a job. "You are an expert in marketing" names a subject, not a practice. There is no such thing as a marketing expert in general. There are pricing analysts, brand strategists, media planners and retention marketers, and they disagree.

A costume is easy to spot in the output: the answer is confident, uses the vocabulary of the field, and contains no decision that a practitioner would recognise as theirs.

### The test

A good role passes two questions.

1. **Could you hire this person?** If the phrase names a job you could advertise, it names a discipline. "Customer research analyst" passes. "Creative thinker" does not.
2. **Does it say how much practice?** Years, or a rank, or a scope. "Eleven years" and "senior" both pass. "Experienced" is a claim with no size.

A role that passes both is short enough to remember. One sentence is usually right.

**Weak:** You are a creative thinker with a passion for brands.

**Strong:** You are a pricing analyst with nine years of experience setting list prices for independent retail suppliers. You write to shop owners, not to procurement teams.

The strong version tells the model what to know and who it is talking to. The second sentence is doing real work: it rules out procurement language, which is the failure this prompt would otherwise produce.

### The six role failures

| Failure | Symptom in the output | Fix |
|---|---|---|
| **Field for discipline** | Confident commentary about the subject, no practice in it | Replace the field with a job title you could advertise |
| **No level** | Explains the basics, hedges every judgement | Add years or a rank |
| **Praise adjective** | Sounds assured, decides nothing | Delete the adjective, add the discipline it stood in for |
| **Two roles at once** | The answer changes voice mid-way, or argues with itself | Keep one role; move the second voice into the task as a check |
| **Role against the task** | It edits the copy you asked it to write, or reviews the plan you asked it to make | Make the role the one who produces the deliverable |
| **Decoration with no effect** | Warm, friendly, enthusiastic, none of which shows in the output | Cut it; keep only what changes a choice |

Full symptoms, causes and repairs: `references/failure-list.md`.

---

## 4. Input

### Context is not instruction

Context tells the model what is true. Instruction tells it what to do. They belong in different parts, and mixing them is the most common structural fault in a long prompt.

When instructions sit inside the input, they compete with the task. The model reads two sets of orders and follows whichever is nearer the end, or blends them. When facts sit inside the task, they get rewritten as the model paraphrases the order.

There is one exception. A constraint that describes the material belongs with the material: "we have no churn data, so do not estimate it" is a fact about the evidence, not an order about the format. Keep it with the input.

### The four kinds of input

| Kind | What it is | What it changes | What happens without it |
|---|---|---|---|
| **The situation** | Who is asking, what is true right now | Turns a topic into a case | The answer is about everyone, so it is for no one |
| **The constraints** | The edges: what must not happen, what must fit | Removes the options the model would otherwise take | A correct answer you cannot use, at the wrong length or the wrong scope |
| **The material** | The notes, numbers, quotes, files the answer must stand on | Grounds the specifics and gives the answer something to cite | Invented specifics in the same confident tone as real ones |
| **The missing thing** | What you do not have, and what to do about it | Stops the model filling the gap | A gap filled with a plausible average, and no seam to show it |

The fourth kind is the one people leave out, because naming a gap feels like admitting the brief is weak. It is the opposite. A named gap is the only gap a model will respect.

### What to do when there is no material

Say so, in the input, with the instruction attached.

```
We have no churn figures and no win-loss record. Ask for them if they matter.
Do not estimate them and do not substitute a typical range.
```

That is two sentences and it changes the answer more than any adjective. Without it, the model produces a number because a number belongs there. With it, the model either asks or writes around the hole.

A thin brief is worse than an honest gap. A thin brief looks complete, so nobody checks it, and the invention arrives inside a confident paragraph.

### The six input failures

| Failure | Symptom in the output | Fix |
|---|---|---|
| **Topic for situation** | General answer about "businesses like yours" | Add who is asking and what is true now |
| **No constraint** | Right answer at the wrong length or scope | Name the edges as directives |
| **Material promised, not supplied** | Specifics appear that you never gave | Paste the notes, or say what is missing |
| **Gap named, no instruction** | The gap is filled anyway, politely | Add what to do: ask, omit, or mark it unknown |
| **Instruction in the input** | The task is half-followed, or followed twice | Move the instruction into the task |
| **Undated facts** | The answer treats last year's numbers as current | Date every figure you supply |

---

## 5. Task

### A named deliverable beats a verb

"Write about our pricing" is a verb and a topic. It has no shape, so the model chooses one, and its choice is the average of the shapes it has seen: a short explainer with a heading or two.

"A one-page pricing note with three sections, 400 to 500 words, for the four people who run sales calls" is a deliverable. The model now has something to be right or wrong about. You can read the output against the request and see the gap.

### The five things a task states

| Element | What it fixes | Example |
|---|---|---|
| **The deliverable** | The form, named as a noun | A one-page ideal-customer profile |
| **The sections** | The order and the boundaries | Five sections: who they are, what they want, what gets in the way, what they have tried, what to say first |
| **The length** | The depth per point | 380 to 450 words, no section over 120 |
| **The register** | Person, formality, diction, spelling | Plain business English, third person, no marketing adjectives |
| **What it is usable for** | The level of detail, and the reader | Usable as a briefing sheet before a sales call and as page one of a proposal |

The fifth element does the most work per word, and it is the one most often missing. "Usable as a briefing sheet" tells the model that a reader will scan it in ninety seconds. That single fact removes more bad sentences than any instruction about tone.

### The six task failures

| Failure | Symptom in the output | Fix |
|---|---|---|
| **Verb for deliverable** | A form nobody asked for | Name the deliverable as a noun |
| **Deliverable with no sections** | One block of prose, or invented headings | List the sections in order |
| **No length** | 200 words one run, 900 the next | Give a range and a per-section ceiling |
| **No register** | Chatty where it should be formal, or the reverse | Name person, formality, diction and spelling |
| **No stated use** | Correct content at the wrong depth | Say who reads it, and when |
| **Task and input disagree** | A recommendation with no criteria, or criteria with no decision | Make the task ask for what the input can support |

---

## 6. Example

The example is the part most people skip. It is also the part that sets the quality of the answer.

### Why an example teaches quality

A model matches the level of the sample it is given. An instruction says "high quality" and means nothing measurable. A sample shows what high quality is: how far one point goes, how long a sentence runs, whether a claim carries a number.

So an average example teaches averageness, and it teaches it more reliably than a good instruction teaches quality. If you paste a 90-word summary and ask for a 900-word analysis, you get a long summary. The sample outranks the adjective every time.

### What a good example contains

Three things, and nothing else.

- **The shape.** The section order, the line structure, whether a section opens with a claim or a scene.
- **The depth.** How far one point is taken, and what is deliberately left out. Depth is the hardest thing to describe and the easiest thing to show.
- **The register.** Sentence length, person, vocabulary, spelling. A sample in the right register removes the need for most tone instructions.

Nothing else means: no praise for the sample, no explanation of why it works, no meta commentary, no second example unless the task has two genuinely different outputs. Commentary inside an example teaches the model to comment.

### An example of the exact output beats a description of it

"An email that politely explains the increase and gives the new price" is a description. It tells the model the ingredients and lets it choose the quantities. A real email of 140 words fixes the quantities.

The description is also unfalsifiable. Any email that mentions the increase satisfies it. The passage can be checked: either the paragraph order matches or it does not.

This is the single cheapest improvement available to most prompts. One real passage, at the length you want, in the register you want, and the answer arrives in that shape.

### The six example failures

| Failure | Symptom in the output | Fix |
|---|---|---|
| **No example** | The model's house style, at its own length | Add one passage of the output |
| **Description for passage** | The right ingredients, the wrong quantities | Replace the description with real text |
| **Average example** | Competent, flat, nothing you would send | Rerun, repair by hand, keep the repaired passage |
| **Wrong length** | A summary where you wanted an analysis | Match the example to the depth of the deliverable |
| **Wrong register** | Chatty sample, formal task, chatty answer | Write the sample in the register you asked for |
| **Wrong shape** | Sections the task never named, or bullets the task banned | Make the sample demonstrate the task, not a neighbour of it |

Deeper treatment, including a weak and a strong example of the same deliverable: `references/example-craft.md`.

---

## 7. The reuse test

One test decides whether you have written a prompt or asked a question.

**Run it again with different input. If the output has the same shape and the same depth, it is a prompt. If you have to rewrite the task to make the second run work, it was a question with a long answer.**

The test is cheap and it is brutal. Most one-off requests fail it. "What should I say to a client who keeps missing deadlines?" cannot be rerun: the second client changes the answer, and so does the second situation, and so does your mood. There is nothing fixed to compare.

A reusable prompt fixes three things and varies one. The role, the task and the example stay. The input changes. That is the whole design, and it is why the four parts are separated: three of them are the instrument, one is the material.

---

## 8. The voice route

Dictating is faster than typing and it loses structure. You speak in one long stream, the labels disappear, and the transcript reads like a person thinking aloud. The four parts survive dictation only if you say them.

Keep the four beats and say the label before each one.

- "Role. You are a pricing analyst with nine years of experience."
- "Input. We supply greetings cards to 140 independent shops. Right now we are raising the list price by six per cent."
- "Task. Write a price-increase email of 150 to 180 words in four paragraphs."
- "Example. Our list price goes up by six per cent on 1 April."

Then the habit that keeps a dictated prompt usable: **say the label, then the content, then stop.** A dictated paragraph that begins with the label can be cut into parts later without guessing. A paragraph that begins mid-thought cannot.

Dictation adds filler ("sort of", "you know", "kind of"). The checker does not care about filler, but the model does, so read the transcript once and cut the filler before you assemble. If you dictate straight into a text file with the labels in it, `rit_grade.py` can read the file as it stands and tell you which part is thin.

---

## 9. Where an example comes from when there is not one yet

The first time you write a prompt for a new job, you have no example, because you have not seen the output. You are not stuck. You run a loop.

1. **Run once without an example.** Fill role, input and task properly. Accept that the shape will be wrong.
2. **Judge the output against the task.** Not against your taste: against the five task elements. Wrong sections, wrong length, wrong register, invented facts.
3. **Repair the worst part by hand.** Rewrite one section until it is what you would send. One section is enough.
4. **Keep the repair as the example.** Paste the repaired passage into the example field, unchanged. Remove anything you added to explain it.
5. **Run again, with the same input.** The second output should be closer. If it is not, the example is teaching the wrong depth or the wrong register, and you repair it again.

### The risk in the loop

The loop copies your own blind spots. If your hand repair is average, the example teaches averageness, and the prompt now reliably produces the thing you would have written on a tired afternoon.

Three guards:

- **Use the run you would show a client**, not the run that was easiest to fix.
- **Have a second person read the example** before it becomes the standard. If they cannot tell what is good about it, the model will not either.
- **Keep the first example until you have a better one.** Replace it with a real output you have read line by line, never with a generated passage you skimmed.

The loop is also how a prompt improves over months: each time an output is better than the example, the example is replaced. A prompt with a stale example quietly holds the quality at the level of the day it was written.

---

## 10. Running the tools

Both tools are standard-library Python 3.9 or newer.

```sh
python3 tools/rit.py --example > brief.json
python3 tools/rit.py brief.json --out prompt.txt
python3 tools/rit.py brief.json --check-only
python3 tools/rit_grade.py prompt.txt
```

`rit.py` assembles the four parts into one labelled prompt and checks it against 14 rules: three for the role, three for the input, four for the task, three for the example, one for hygiene. It exits 0 when every rule passes and 2 when any rule fails. The score counts rules. Presence of an example is the heaviest single rule, at 18 points of 100, because it is the part most often left out.

The rules read the text, and reading text means word lists. R01 looks for a discipline noun, R02 for years or a rank, R05 for a constraint marker, R09 for a register marker, R10 for a phrase about use. The lists are at the top of `tools/rit.py` and none of them is hidden. If your discipline is missing, add the word to `DISCIPLINES` and the rule will find it next run. A false failure is a list to extend, not a rule to argue with.

`rit_grade.py` reads the same brief, or a plain-text prompt with the four labels, and scores each part out of 25. It names the weakest part, the reason, the highest-value repair and the second. It exits 0 for any prompt it can read, because a grade is information, not a gate.

The two scores are not the same number, and they are not meant to be. The checker asks whether each rule passes. The second tool asks how much of each part is present. Use the checker before a run, and the second tool to decide what to fix first.

---

## 11. Limits

This improves the odds. It does not guarantee the output.

- **It cannot add knowledge the model does not have.** A precise role and a good example make the model use what it knows; they do not give it a fact it never saw.
- **It cannot verify a claim.** If the input is wrong, the output will be wrong in better prose.
- **It cannot make a judgement for you.** A clearer prompt produces a clearer answer to check, not a correct one.
- **It cannot rescue a job that should not be given to a model.** If the work needs accountability, sign-off or a relationship, a prompt is not the tool.
- **The checker reads the prompt, not the answer.** A prompt at 100/100 is a well-formed request. Whether the answer is any good is a separate act of reading.
- **The example carries your taste, including your errors.** A prompt is a standard. A standard written by one person, unread by a second, is a habit.

---

## Sources and reuse

Source reference: the R.I.T Prompt Framework, which separates role, input and task. This product also makes the example explicit. No third-party prompt text is included. See `README.md` for the product licence and reuse terms.
