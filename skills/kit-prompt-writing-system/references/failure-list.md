# Failure list

Twenty-four failures, six per part. Each one has a symptom you can see in the output, a cause you can find in the prompt, and a repair that names the edit.

Use it in this order: find the symptom in the output, then the cause in the prompt, then make the repair. Change one failure at a time and run again. A prompt with five repairs is a new prompt, and you will not know which repair worked.

The last section maps each failure to the checker rule that catches it, and lists the ones no rule can catch. Those need a reader.

---

## 1. Role failures: the costume

The role is the part people write first and think about least. A costume is a role that changes the tone without changing the knowledge: praise words, a field instead of a job, or a persona that has no effect on any choice in the answer. The output is confident and empty, and the emptiness is hard to see because the vocabulary is right.

| # | Failure | Symptom in the output | Cause | Repair |
|---|---|---|---|---|
| 1 | **Field for discipline** | Confident commentary about the subject, with no decision a practitioner would recognise | The role names a subject ("expert in marketing") rather than a job | Replace it with a job you could advertise: pricing analyst, brand strategist, retention marketer |
| 2 | **No level** | It explains the basics and hedges every judgement | No experience named, so the model defaults to a generalist | Add years or a rank: "eleven years", "senior", "head of" |
| 3 | **Praise adjective** | An assured tone and no judgement; the adjectives do the work the knowledge should do | Praise cannot be converted into a domain, so the model performs it | Delete the adjective and add the discipline it stood in for |
| 4 | **Two roles at once** | The voice changes mid-answer, or the answer argues with itself | Two practitioners with different priorities in one role | Keep one role; move the second voice into the task as a check ("flag what a finance director would challenge") |
| 5 | **Role against the task** | It edits the copy you asked it to write, or reviews the plan you asked it to make | The role was chosen for authority rather than for the act | Make the role the one who produces the deliverable |
| 6 | **Decoration with no effect** | Warm, friendly, enthusiastic; none of it visible in the output | The trait has no surface in the deliverable | Cut it, or move it into the task as a register instruction |

The repair that fixes most role failures is the second sentence. Say what the practitioner is careful about: "you keep what a customer said separate from what you think it means" changes the answer more than any job title alone.

---

## 2. Input failures: the thin brief

A thin brief is not a short brief. It is a brief that looks complete, so nobody checks what it left out. The model reads a gap as permission, and fills it with the average of what it has seen. The output is fluent, specific and invented, which is the worst combination, because invented specifics are hard to tell from real ones once they are in a sentence.

| # | Failure | Symptom in the output | Cause | Repair |
|---|---|---|---|---|
| 7 | **Topic for situation** | General answer about "businesses like yours" | No actor and no present state | Say who is asking and what is true now |
| 8 | **No constraint** | A correct answer at the wrong scope, length or risk | The request has no edges | Name the edges as directives: must, has to, cannot, no more than |
| 9 | **Material promised, not supplied** | Specifics appear that you never gave | "We have data" is a claim, not material | Paste the material, or point at the exact file and period |
| 10 | **Gap named, no instruction** | The gap is filled anyway, politely | Absence was noted without a rule for it | Add what to do: ask, omit, or mark the claim provisional |
| 11 | **Instruction in the input** | The task is half-followed, or followed twice | Two sets of orders in one prompt | Move every order into the task; keep only facts in the input |
| 12 | **Undated facts** | Last year's numbers treated as current | Figures supplied without a date | Date every figure, and say which period it covers |

The fourth kind of input, the missing thing, is the one to add first. "We have no churn data, ask rather than estimate" is two sentences that remove a whole class of invention.

---

## 3. Task failures: the vague verb

A verb and a topic is not a task. It leaves the shape, the depth, the length and the reader to the model, and the model's choice is the average of every similar request it has seen. That average is always reasonable and almost never what you wanted.

| # | Failure | Symptom in the output | Cause | Repair |
|---|---|---|---|---|
| 13 | **Verb for deliverable** | A form nobody asked for: an explainer where you wanted a memo | The task names an action, not an object | Name the deliverable as a noun |
| 14 | **Deliverable with no sections** | One block of prose, or headings the model invented | The structure was left open | List the sections in the order you want them |
| 15 | **No length** | 200 words one run, 900 the next | No bound on depth | Give a range, and a ceiling per section |
| 16 | **No register** | Chatty where it should be formal, or the reverse | Person, formality and diction left implicit | State person, formality, diction and spelling |
| 17 | **No stated use** | Correct content at the wrong depth for its reader | No reader and no occasion | Say who reads it and when |
| 18 | **Task and input disagree** | A recommendation with no criteria, or criteria with no decision | The task asks for more than the input can support | Either add the criteria to the input or ask for options instead of a recommendation |

The fifth element of the task, what the output is usable for, is the cheapest repair in the whole framework. One clause about the reader removes more bad sentences than a paragraph about tone.

---

## 4. Example failures: the borrowed example

An example is a standard. A borrowed example is someone else's standard, and it arrives with their depth, their register and their shape. The model follows the sample over the instruction every time, because the sample is concrete and the instruction is abstract.

| # | Failure | Symptom in the output | Cause | Repair |
|---|---|---|---|---|
| 19 | **No example** | The model's house style, at the model's own length | The part was skipped | Add one passage of the output at the depth you want |
| 20 | **Description for passage** | The right ingredients, the wrong quantities | The example describes the output instead of showing it | Replace the description with real text |
| 21 | **Average example** | Competent, flat, nothing you would send | The sample came from a mediocre run | Rerun, repair the worst section by hand, keep the repaired passage as the example |
| 22 | **Wrong length** | A summary where you wanted an analysis | The sample is at a different depth from the deliverable | Match the sample to the unit of the deliverable: one section, at full depth |
| 23 | **Wrong register** | A chatty sample, a formal task, a chatty answer | The sample was written quickly, in the voice of the chat window | Rewrite the sample in the register the task asks for |
| 24 | **Wrong shape** | Sections the task never named, or bullets the task banned | The sample was borrowed from a neighbouring job | Make the sample demonstrate this task, not a similar one |

An example of the exact output beats a description of the output, and one passage is enough. More than one example is a second standard, and two standards produce an average of both.

---

## 5. Which failures the checker catches

`tools/rit.py` checks 14 rules. This is what each one catches, and what it cannot.

| Rule | Catches | Failure numbers |
|---|---|---|
| R01 | Role names a discipline | 1 |
| R02 | Role names a level | 2 |
| R03 | Role has no praise adjective | 3 |
| R04 | Input states the situation | 7 |
| R05 | Input names a constraint | 8 |
| R06 | Input supplies material or names the gap | 9, 10 (partly) |
| R07 | Task names a deliverable | 13 |
| R08 | Task states a length or bound | 15 |
| R09 | Task states a register | 16 |
| R10 | Task states what it is usable for | 17 |
| R11 | Example is present | 19 |
| R12 | Example is a passage, not a description | 20 |
| R13 | Example agrees with the task | 24 |
| R14 | No unresolved placeholder | any field left in place |

Ten failures have no rule: 4 (two roles), 5 (role against the task), 6 (decoration), 11 (instruction in the input), 12 (undated facts), 14 (no sections), 18 (task and input disagree), and the three quality failures 21, 22 and 23. No checker can see them, because they need a judgement about the answer rather than a pattern in the prompt.

One failure is only half seen: 10 (a gap named with no instruction) passes R06, because R06 can read that the gap was named but not that nothing was said about what to do with it.

That is the honest boundary of the tool. A prompt at 100 out of 100 is well formed. It can still be a prompt for the wrong job, in the wrong voice, carrying last year's numbers.
