# The scoring model

Six criteria, fixed weights, a scale from 1 to 5, and one worked score so the scale is unambiguous. The weights total 100 and the tool stores them in `tools/score_ideas.py`. They cannot be changed from the command line, which is the point: a ranking is only comparable with another ranking if the model is the same one.

## The six weights, and why each holds its share

| Criterion | Weight | The reason it holds that share |
| --- | --- | --- |
| Closeness to the paid offer | 25 | The magnet exists to sell one thing. If the result does not point at that thing, the build is a hobby with an email list. It carries the largest weight because nothing else can compensate for its absence. |
| Speed to value | 20 | A lead magnet is used in a distracted minute. The less the user does before something useful appears, the more of them finish and the more of them see the offer. Second largest because an unfinished calculator sells nothing. |
| Breadth of appeal | 15 | A result that lands for a narrow slice caps the list you can build. Equal to build cost and differentiation because it multiplies everything else rather than replacing any of it. |
| Build cost | 15 | Time and money to build once, scored 5 for cheapest. Held below closeness and speed on purpose: a cheap idea that sells nothing is still a loss. |
| Durability | 10 | How long the magnet stays true before a rule, a price or a platform changes it. Lowest weight because most magnets are replaced inside a year anyway, and because a stale magnet is obvious to the person using it. |
| Differentiation | 15 | How hard the result is to copy in an afternoon. A copied magnet still works, it just costs more to keep in front of people, which is why it sits level with breadth rather than above it. |

Two features of this table are deliberate.

**The weights are arguable.** A reader can make a case for durability at 15 and differentiation at 10, or for build cost at 20. The argument is the useful part. If you change a weight, change it in the script, write the reason in the file, and rerun every ranking you still rely on, because old rankings are no longer comparable.

**The scores are opinions and the arithmetic is not.** The tool does not make a score more true. It makes the consequence of a score visible, so a disagreement can be about a number instead of about taste.

## How to score, in general

Score every criterion from 1 to 5. Five is always the better outcome, including build cost, where 5 means cheapest. Use whole numbers only. A half point is a way of avoiding a decision, and the tool rejects it.

Score in the same order every time: closeness, speed, breadth, build cost, durability, differentiation. Scoring in a fixed order stops the first strong idea from setting the tone for the rest.

Write a one-line reason for each idea. The reason is not for the tool. It is for the reread, three weeks later, when the ranking looks wrong.

---

## 1. Closeness to the paid offer (25)

**What it measures.** Whether the result the user gets is the same thing your paid offer works on, or a different thing that happens to come from the same trade.

**The common mistake.** Scoring a magnet highly because it is for the same audience. Audience is not closeness. A free stretching guide for a physiotherapy clinic's patients is perfectly on-audience and points at nothing the clinic sells.

| Score | Anchor |
| --- | --- |
| 1 | The result could be sold by anyone in any trade. Nothing in it points at your offer. |
| 2 | The result points at a general problem you also solve, in general words. The offer could be swapped for a competitor's without changing the magnet. |
| 3 | The result points at your category, but at a different part of the job than the offer covers. |
| 4 | The result points at the same job the offer does, in a weaker form: a document where the offer installs a process, a checklist where the offer does the work. |
| 5 | The result produces the exact figure or artefact your offer starts from, and the offer cannot be explained without referring to it. |

## 2. Speed to value (20)

**What it measures.** The distance between arriving and seeing something useful, counted in inputs and in waiting.

**The common mistake.** Counting the fields on the form and forgetting the ones the user has to go and find. A field that needs a report is worth three fields that need a memory.

| Score | Anchor |
| --- | --- |
| 1 | Needs an upload, an account, or a wait of a day or more. |
| 2 | Needs data from another system, or more than five inputs. |
| 3 | Five inputs, and about a minute of typing. |
| 4 | Three or four inputs the user can answer from memory, in under a minute. |
| 5 | One or two inputs, or a single choice, with a result in seconds. |

## 3. Breadth of appeal (15)

**What it measures.** How much of the target trade wants this result at the moment they see it, not how interesting the result is.

**The common mistake.** Confusing breadth with size of market. A tool for every clinic in the country that only fits clinics with an online booking system has narrow breadth, and the narrower number is the honest one.

| Score | Anchor |
| --- | --- |
| 1 | A handful of named businesses. |
| 2 | One sub-segment of the trade, defined by a condition most do not meet. |
| 3 | The trade, but only owners at one stage or with one setup. |
| 4 | Most owners in the trade, at most stages. |
| 5 | The trade plus adjacent trades that share the same problem. |

## 4. Build cost (15)

**What it measures.** The work to build a first honest version, scored 5 for cheapest. Not the cost of the design, the copy or the hosting: those are roughly constant across ideas and do not help choose between them.

**The common mistake.** Scoring the idea you find interesting as cheap. Write the build spec first for one idea, then score the rest against what a day actually bought.

| Score | Anchor |
| --- | --- |
| 1 | A data product that needs maintaining weekly, or a build of a month or more. |
| 2 | More than a week of work, or a dependency on data you do not own. |
| 3 | Two to four days, with rules to write and edge cases to handle. |
| 4 | About a day: one page, a small amount of arithmetic, a few states. |
| 5 | An afternoon: one page, no data to maintain, no edge cases worth naming. |

## 5. Durability (10)

**What it measures.** How long the result stays correct before a rule, a price or a platform changes underneath it.

**The common mistake.** Scoring a tax or fee table as durable because it is only numbers. Numbers with a year attached expire; a calculation with a stated year in the output does not.

| Score | Anchor |
| --- | --- |
| 1 | Wrong within a month: prices, platform behaviour, campaign rules. |
| 2 | Wrong within a quarter: provider terms, local fees, seasonal rules. |
| 3 | Wrong within a year, or useful only while a current offer lasts. |
| 4 | Holds for a year or more, with the rule date printed in the output. |
| 5 | Holds until the trade itself changes: arithmetic over the user's own numbers, or a process the clinic controls. |

## 6. Differentiation (15)

**What it measures.** How hard the result is for a competent competitor to reproduce next week, given that they have seen it.

**The common mistake.** Scoring novelty instead of difficulty. A new angle on a checklist is still a checklist, and it copies in an afternoon.

| Score | Anchor |
| --- | --- |
| 1 | The same tool exists free from three competitors, in the same shape. |
| 2 | A common shape on a common angle. Nothing in it is yours. |
| 3 | A common shape with your data or your angle in it. |
| 4 | The result is specific to this trade and this offer, and copying it means copying your method. |
| 5 | Nobody else can build it without your data, your method or your client base. |

---

## A fully scored example

The idea: a no-show cost calculator for independent physiotherapy clinics. Four inputs the owner already knows, one monthly figure out, and the figure is the first thing the paid review talks about.

| Criterion | Score | Reason for the score | Points |
| --- | --- | --- | --- |
| Closeness | 5 | The monthly loss figure is the number the review starts from. The offer cannot be explained without it. | 25.0 |
| Speed | 5 | Four numbers, all on the practice diary, and a result on one button press. | 20.0 |
| Breadth | 4 | Most owners in this trade have the four numbers. The few who do not are the very small clinics with paper diaries. | 12.0 |
| Build cost | 4 | One page, one multiplication chain, an empty state and a gate. About a day, not an afternoon, because the suppression rule and the one fifth comparison both need testing. | 12.0 |
| Durability | 4 | Arithmetic over the clinic's own numbers, so nothing external expires. It loses a point because the average fee is a moving number the owner will update, and the 4.33 weeks multiplier is an approximation that should be stated. | 8.0 |
| Differentiation | 3 | A cost calculator is a known shape and competitors run one. What is specific here is the pairing with a review that starts from the same figure, which is a 3 rather than a 2. | 9.0 |

**The arithmetic.** Each criterion contributes its weight multiplied by the score, divided by 5. The six contributions add to the weighted total:

```
closeness        25 x 5 / 5 = 25.0
speed            20 x 5 / 5 = 20.0
breadth          15 x 4 / 5 = 12.0
build cost       15 x 4 / 5 = 12.0
durability       10 x 4 / 5 =  8.0
differentiation  15 x 3 / 5 =  9.0
                             ------
total                          86.0 / 100
```

The tool prints the same numbers from the same file:

```sh
python3 tools/score_ideas.py ideas.json --top 1 --explain
```

**Reading the result.** 86.0 is a strong score with one visible weakness: differentiation. If a competitor already gives away a no-show calculator, this idea competes on the bridge rather than on the tool, which is a real position but a thinner one. The honest response is not to inflate the score. It is to note in the decision that the differentiation comes from the offer behind the calculator, and to keep the reminder message pack (79.0) as the second magnet for the same list.

**What would move the score.** A fifth input for therapist count would let the result carry a per-therapist split. Speed would fall to 4 and closeness would stay at 5, so the total would fall by 4 points to 82.0. That is a real trade, and the worked run declined it.
