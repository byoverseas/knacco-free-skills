# Lead Magnet Planner

A method for deciding what lead magnet to build, and for writing the build spec that a coding tool can actually execute.

The order is fixed: define, generate, score, choose, specify. Five stages. The first four are thinking and cost nothing. The fifth is a document. Nothing is built until all five are done.

The reason for a fixed order is that every other order produces a familiar failure: a checklist built in an afternoon because it was easy, a calculator built in a week because it was clever, a build that stalls because the spec left a gap, and a magnet that collects addresses for an offer nobody can name.

## The words this guide uses

Nothing below needs learning before you start. Come back when a word gets in the way.

| Word | What it means here |
| --- | --- |
| Lead magnet | Something free you give away in exchange for an email address |
| Criterion | One of the six things an idea is scored on |
| Weight | How much a criterion counts towards the total. Fixed, and printed |
| Build spec | The written brief a developer or coding tool works from |
| Gate | The form where someone gives you their email address |
| Consent | What the person understood they were agreeing to when they signed up |
| Conversion | The share of visitors who sign up. Not measured here, and not claimed |

---

---

## 1. The problem this solves

Four failure modes, in the order they usually happen.

1. **The easy thing gets built.** A checklist or a swipe file takes an afternoon, so it gets made. It proves no skill, so the list it builds has no reason to trust the offer behind it.
2. **The clever thing gets built.** A calculator with nine inputs and a chart takes a fortnight, and the owner abandons it at input five. The cleverness was never the constraint.
3. **The spec cannot be executed.** The idea is good and the handover is a paragraph. The coding tool invents the output, the empty state, the gate and the error handling, and the build comes back looking finished and being wrong.
4. **The offer was never named.** The magnet collects a thousand addresses for a business that has nothing to sell them. A bridge with no far bank is a quiz.

All four are ordering problems. Fixing the order fixes most of them, and the tools in this product catch the rest.

---

## 2. Stage 1: Define the niche and the paid offer

Two lines and a bridge. Write them in `inputs/niche.md` before you write a single idea.

### The niche line

One trade, one size, one place, and the constraint that shapes the buyer's day.

```
Independent physiotherapy clinics in the UK with two to six therapists and no
practice manager, where the owner still treats patients four days a week.
```

That sentence passes a test: a stranger can name three businesses that fit and three that do not. "Small businesses who want to grow" fails the same test, and every later stage inherits the failure.

### The offer line

What is sold, what it costs, how it is delivered.

```
A 90 minute clinic operations review at 450 pounds, which becomes a monthly
retainer at 220 pounds a month for the clinics that want the changes held in place.
```

A price is not optional. The magnet has to be worth more than the effort of using it and less than the offer, and only a number tells you where that window sits.

### The bridge line

```
The calculator turns the clinic's own appointment numbers into a monthly figure
for money lost to no-shows and late cancellations, and the review starts by
explaining how to get that figure back.
```

### Why the paid offer must exist first

The lead magnet is a bridge. A bridge with no far bank is a quiz.

Three consequences follow, and all three are practical.

**The offer decides the output.** If the offer starts from a monthly loss figure, the magnet must produce a monthly loss figure. If the offer were a six week patient programme, the same calculator would produce a number with nowhere to go. You cannot choose the output until you know what the next conversation opens with.

**The offer decides the audience.** The magnet is for the person who buys the offer, not for everyone in the trade. A clinic's patients and a clinic's owner are two different audiences with two different pains, and one magnet cannot serve both.

**The offer decides the ceiling.** A magnet can only be as specific as the offer behind it. If the offer is vague, the magnet will be vague in a way that no amount of design fixes.

### The bridge test

Cover the offer line and read the bridge sentence aloud. If it still makes complete sense, it is not a bridge. It is a free tool that happens to be in the same industry.

Then cover the niche line and read it again. If it could be said to any trade, the result will be generic and the scores in Stage 3 will be guesses.

---

## 3. Stage 2: Generate ideas, fifteen minimum

Fifteen is the minimum. Write them before you score any of them, because scoring while writing pulls every idea towards the same shape.

The first three ideas are always the same three, in every niche: a checklist, a guide, and a quiz. Fifteen forces you past them.

### The seven shapes

A shape is a promise about how value arrives. Each shape has a cost, a moment where it is right, and a way it fails.

| Shape | Good for | Cost to build | Failure mode |
| --- | --- | --- | --- |
| Calculator | Making a problem visible with a number the user did not have | One long day | Answers a question nobody asks |
| Assessment | Judgement problems, and buyers who want to know where they sit | Two to four days | A quiz with a score and no consequence |
| Swipe file | Audiences who know what they want to say and want it written | An afternoon | Proves no skill, and dates quickly |
| Template pack | Recurring work with a shape | One to three days | Needs discipline the user does not have |
| Checklist | Reducing a fear of missing something | Two hours | Obvious items, or a list too long to finish |
| Short course | Building a relationship before the ask | Three to five days | Five emails that restate one idea |
| Data lookup | A factual answer the user cannot find | Two days to a week, plus upkeep | Goes stale quietly and still looks authoritative |

Full detail, including the smallest honest version of each, is in `references/shape-library.md`.

### Rules for generation

1. **At least one idea from every shape.** Not because all seven are worth building, but because the discipline forces range.
2. **No idea that needs data the user cannot produce in two minutes.** If the input needs a report, the idea belongs in the paid offer.
3. **Write each idea as a sentence the user would recognise.** "A calculator that shows what no-shows cost a month" is an idea. "A value tool" is a category.
4. **No idea that needs a decision the user cannot make alone.** A tool that requires a partner's agreement before the result means anything has a built-in dead end.
5. **No idea whose result is a document you would have to keep updating.** Updating is a cost that never ends.
6. **One line of reasoning per idea, written at the same time as the idea.** You will need it when the ranking surprises you.

Fifteen ideas in a file is the target. `references/shape-library.md` ends with the mapping from what the offer starts from to which shape usually wins.

---

## 4. Stage 3: Score

Six criteria, fixed weights, scores from 1 to 5.

| Criterion | Weight | Why it holds that share |
| --- | --- | --- |
| Closeness to the paid offer | 25 | The magnet exists to sell one thing. Nothing else compensates for its absence. |
| Speed to value | 20 | A lead magnet is used in a distracted minute. An unfinished calculator sells nothing. |
| Breadth of appeal | 15 | A result that lands for a narrow slice caps the list it builds. |
| Build cost | 15 | Scored 5 for cheapest. Held below closeness and speed: a cheap idea that sells nothing is still a loss. |
| Durability | 10 | Lowest, because most magnets are replaced before they decay. |
| Differentiation | 15 | A copied magnet still works, it just costs more to keep in front of people. |

### Why a fixed weight set beats a gut call

Three reasons, and the third is the one that matters.

**Comparability.** A fixed model lets a ranking from March be compared with a ranking from September. Change the weights between runs and no two rankings can be read together.

**Auditability.** Every score has a printed consequence. When someone says "the swipe file is obviously better", the conversation moves from taste to a number, and a number can be changed.

**It stops the loudest idea from winning.** A gut call is usually a preference for the idea the person can picture. The weights make closeness worth more than build cost, which is the opposite of what a tired owner prefers at 9pm.

### Why the weights are arguable on purpose

The model is a starting position with reasons attached, not a law. Change a weight only in the script, write the reason next to it, and rerun every ranking you still rely on.

The argument itself is the useful part. If someone insists build cost should be 25, they are usually saying the build has to ship this week. That is a real constraint, and naming it is better than quietly inflating a score.

### The arithmetic

Each criterion contributes its weight multiplied by its score, divided by 5. The contributions add to a total out of 100.

```
closeness        25 x 5 / 5 = 25.0
speed            20 x 5 / 5 = 20.0
breadth          15 x 4 / 5 = 12.0
build cost       15 x 4 / 5 = 12.0
durability       10 x 4 / 5 =  8.0
differentiation  15 x 3 / 5 =  9.0
                             ------
total                          86.0
```

The anchors for each point on each scale are in `references/scoring-model.md`, along with a fully scored idea and the reason for every score.

### The five point band

A margin under five points is not a decision. It is an argument.

Five points is one notch of a single criterion at the heaviest weight, and one notch is inside the error of a judgement made on a Tuesday. So the total sorts the shortlist and the three questions in Stage 4 decide the winner.

### Running the tool

```sh
python3 tools/score_ideas.py ideas.json --explain
python3 tools/score_ideas.py ideas.json --top 3
python3 tools/score_ideas.py ideas.json --json
```

`--explain` prints the weights, the reason for each weight, and every contribution. The reason the ranking can be argued with is that it shows its working.

---

## 5. Stage 4: Choose

Take the top five and ask three questions. In this order.

**1. Does the result name the problem the paid offer fixes?** Not the same industry, the same job. A message pack is the fix without the diagnosis, and it leaves the offer to introduce itself.

**2. Can the buyer produce the inputs from memory in under two minutes?** From memory, not from a report. A field that needs a report is three fields in a coat.

**3. Would the buyer show the result to a colleague?** A figure gets forwarded. A policy document does not. If the result is interesting enough to send, the magnet does the distribution for you.

A single no does not remove an idea from the shortlist, but it removes it from the decision. An idea with a no is a fallback.

### The rule that cuts ideas needing more than five inputs

Any idea that needs more than five inputs is cut, whatever it scores.

Every field you add is a reason to leave. The first field carries the most weight, because that is where the visitor decides whether the thing is worth starting at all. The fields that cost the most are the ones the buyer cannot answer without looking something up, and those are usually the fifth and sixth rather than the first.

The cap is also a design tool. With five slots you must choose the number that matters, and choosing the number that matters is what makes the output sharp. A tool with nine inputs computes something nobody asked for.

### What to do instead of cutting

Three moves, in order of preference.

1. **Prefill it.** Anything you can look up (a region, a rate, a fee band) should not be a field.
2. **Split it.** Put the first result behind four fields, and offer the refined result as a second step after the gate. The visitor who is still interested at step two is the visitor worth having.
3. **Move it to the offer.** A number that needs a report belongs in the review, where a person can ask for the report.

### Recording the decision

Write the top five, the three answers, the choice and the reason. If the choice goes against the ranking, name the criterion that was rescored and show the rerun. That record is the difference between arguing with the tool and bypassing it.

---

## 6. Stage 5: Write the build spec

Eleven fields. The full shape, with a bad answer and a filled example for each, is in `references/build-spec-shape.md`.

| Field | Holds |
| --- | --- |
| `niche` | One trade, one size, one place, one constraint |
| `paid_offer` | What is sold, the price, the delivery |
| `pain` | The problem in the buyer's words, including the workaround |
| `promise` | One sentence naming the computation, not an outcome |
| `inputs` | One to five, each with a name, a type and a reason |
| `screens` | First screen, empty state, mobile rule |
| `logic` | The computation as ordered steps, with rounding and suppression |
| `output` | Every field, with unit and rounding, plus the layout |
| `gate` | Position, what is shown before, what is held back |
| `cta` | The sentence, the destination, where it appears |
| `success_measure` | Metric, target, window |

Write the fields in a different order from the table: output first, then inputs, then gate, then call to action, then success measure. The output is the decision. The inputs exist to feed it, so writing them first guarantees a tool that collects more than it uses.

### The gate after value rule

Show part of the result, then gate the rest. The order on the page is fixed.

```
1. First screen        fields only, no email field anywhere on it
2. Press the button    the result area fills, no address given
3. Partial result      one or two figures that prove the thing works
4. Gate                the address is asked for, next to a note on what is behind it
5. Full result         the rest of the figures, on the same page
6. Call to action      one sentence and a named destination
```

Two ways this fails. A gate at step 1 is a door tax: most visitors leave and the ones who stay never saw the tool work. A gate with nothing behind it, because the partial result was already everything, is a lie the visitor can see.

### Where the call to action sits

Next to the full result, not in the footer. One sentence, one named destination, and where possible the figure the visitor just saw passed along with them.

```
If the annual figure is worth fixing, book the 90 minute review. Bring the four
numbers and the review starts from them.
```

A result page with the offer in the footer is a page that has hidden its own offer.

### The output format a coding tool reads best

One page, inline style and inline script, no build step. The arithmetic runs in the page. Four states are named: empty, partial, gated, full. Copy that must not be invented, including the button label and the gate wording, appears verbatim in the spec. Every figure carries a unit and a rounding rule. The mobile rule names a width in pixels.

These are recommendations, not laws. The law is that a coding tool given a gap will fill it with something you did not choose.

---

## 7. What a lead magnet must not promise

| Never | Because | Write instead |
| --- | --- | --- |
| A result it cannot compute | Any number would be a guess with a chart | The figure the inputs actually support |
| A guarantee | It is a promise about other people's future behaviour | The arithmetic, labelled as arithmetic |
| A diagnosis | Clinical, legal and financial judgement needs a person accountable for it | Counting and describing the process |
| A number not calculated from the user's input | An average is a fact about a group, not a result for a person | The comparison figure beside the user's own number, both labelled |

`references/ethics-and-limits.md` covers the claims, the consent rules at the gate, and the data the tool must not collect.

---

## 8. The review order before handing to a coding tool

Run these in order. Each one catches a different mistake.

1. **Read the promise aloud.** If it names an outcome rather than a computation, rewrite it now.
2. **Enter the inputs in your head.** Any field you would have to look up is a field to cut.
3. **Check every output field for a unit and a rounding rule.** A figure without a unit is a support ticket.
4. **Read the empty state.** It must say what the result area holds before the first number, and what the button does while fields are empty.
5. **Check the gate.** Partial result first, full result after, and the panel says what is behind it.
6. **Check the call to action.** One sentence, one destination, placed next to the result.
7. **Check the success measure.** One metric, one target, one window. If it cannot fail, it is not a measure.
8. **Run the checker.**

```sh
python3 tools/spec_check.py build-spec.json
```

A pass at 100 means the eleven fields are filled and the seven build-stopping omissions are absent. It does not mean the magnet is good. It means the build has enough to build the thing you meant.

---

## 9. What this product does not do

- It does not build the app. It decides what to build and writes the spec. The build is yours, or your coding tool's.
- It does not host, send email or run the list.
- It does not verify your claims. The checker warns about claim words in the promise; it cannot tell whether a sentence is true.
- It does not replace a lawyer, an accountant or a clinician where the trade needs one.
- It does not promise leads, conversion or revenue. Nothing in the examples reports traffic or income, and the success measure is a target written before launch.

---

## Sources and reuse

Source reference: a public AI recipe describing idea generation, scoring, selection and a build brief. No third-party prompt text, template wording or scoring values are included. See `README.md` for the product licence and reuse terms.
