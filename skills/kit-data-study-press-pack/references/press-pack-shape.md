# Press pack shape

The pack exists to get a busy person to open the findings. It is not the evidence. It is one page, plus three charts, plus a line they can paste.

Write the pack after the findings, never before. A pack written first decides the answer, and the count then has to agree with it.

---

## The release, section by section

| Section | Job | Length | The failure |
|---|---|---|---|
| Headline | The finding, with its number and its denominator | One line | A mood instead of a count |
| Standfirst | The second number, or the reason it matters | One or two sentences | A restatement of the headline |
| Dateline | Place, date, embargo | One line | No date, so nothing can be dated later |
| The finding | The count in plain words | Two short paragraphs | The number buried in paragraph three |
| Evidence | Two or three figures a desk can build on, each with its base | One paragraph | A figure with no base |
| Quote | One person, with a role, saying something only they could say | Two sentences | A generic quote with no attribution |
| Charts | Three, named, with what each shows | Three lines | No chart, so the desk makes one badly |
| Boilerplate | Who you are, third person | Three sentences | Adjectives instead of facts |
| Contact | Name, role, address that answers | Two lines | A contact form URL |
| Citation | A line a journalist can paste | One line | No citation, so the study cannot be referenced |

### A filled example

> **# 118 of 300 adverts for one role state no salary (39.3% of 300)**
>
> Two thirds name a benefit. One in twenty says "competitive" and nothing else.
>
> London, 4 March 2026. Embargoed until 09:00.
>
> **The finding**
>
> Of the 300 adverts for a single job title on one board, 118 (39.3% of 300) give no salary or range. A further 14 of the 300 (4.7%) give the word "competitive" and no figure.
>
> Where a salary is given, it is a range in 151 of the 168 adverts that give one (89.9% of 168).
>
> **Why it matters**
>
> Pay transparency rules apply to adverts above a size threshold, and this board carries both. The count shows what the adverts say, and it does not show why any individual advert is silent.
>
> **Quote**
>
> "We expected silence to be concentrated in small firms. It was spread almost evenly across the board." R. Patel, lead analyst, Example Analytics.
>
> **Charts**
>
> Chart 1: the split, stated against a salary, stated as competitive, silent. Chart 2: range width against stated minimum. Chart 3: silence by month of posting.
>
> **About Example Analytics**
>
> Example Analytics counts what public pages say. It has published four studies of job adverts since 2024. It does not sell recruitment services.
>
> **Contact**
>
> R. Patel, lead analyst, press@example.org, +44 20 0000 0000.
>
> **Cite this study**
>
> Patel, R. (2026). Salary disclosure in 300 adverts for one role. Example Analytics. https://example.org/studies/salary-disclosure

Read that as a journalist: the number is in the headline, the base is beside every rate, the quote has a role, and the citation is one paste away. Nothing in it asks the reader to trust a claim they cannot check, because the method is one link away.

---

## The three charts

A desk will use three charts, and they are not the three you would put in a deck.

### Chart 1, the split

- **Type:** horizontal bar, one bar per category, sorted by count.
- **Data:** the tally, untouched.
- **Axis:** counts on the bar ends, not percentages, with the denominator in the subtitle.
- **Subtitle:** "n = 300 adverts, one board, retrieved 2 March 2026".
- **Do not:** use a pie. Do not merge the two smallest categories. Do not truncate the axis.

This is the chart that runs. It has to be legible as a thumbnail, which means four bars at most and a label a reader can read on a phone.

### Chart 2, the comparison

- **Type:** two bars, or a paired bar if there are two populations.
- **Data:** the two categories the finding turns on, with any overlap shown as its own bar rather than folded into a total.
- **Axis:** counts, with the denominator in the subtitle.
- **Subtitle:** the same denominator as chart 1, even though it feels repetitive. It is not repetitive to the reader who sees only this chart.
- **Do not:** show an overlap inside two totals that both contain it. That is how a 47 becomes a 94.

### Chart 3, the movement

- **Type:** line, or a small multiple of bars, one panel per period.
- **Data:** the same split across time, or across a second dimension such as region or size band.
- **Axis:** share of that period's denominator, with each period's n printed under it.
- **Subtitle:** "each point is n = 25 adverts".
- **Do not:** draw a trend line through four points. If the pattern is flat, write "flat" in the caption rather than inventing a direction.

Every chart carries three lines below it: the denominator, the date, and the source. If the data is synthetic, partial or a subset, the third line says so.

---

## The quote

One quote. Three rules.

1. **A named person with a role.** "R. Patel, lead analyst" is usable. "A spokesperson" is not, and a name with no role is a phone call the desk will not make.
2. **Something the data cannot say.** The quote carries the judgement, the surprise or the reason, because the numbers cannot. A quote that repeats a number wastes the slot.
3. **Approved by the person.** Never write a quote for someone who has not seen it. Never attribute a quote to a role you cannot evidence.

If nobody will say anything on the record, run the pack without a quote and say why. An invented quote is the fastest way to lose the story and the relationship.

---

## The boilerplate

Three sentences. Who you are, what you do, one verifiable fact.

> Example Analytics counts what public pages say. It has published four studies of job adverts since 2024. It does not sell recruitment services.

The third sentence is the one that does the work, because it answers the question a journalist asks silently: what does this person gain. If your answer is "we sell the solution", say so, and let the reader weigh it.

---

## The contact

A name, a role, and an address that answers within a day. A phone number if you will actually pick up.

Not a contact form. Not a generic inbox that routes to a ticket. Not "DM us". A journalist on deadline will use the first route that works, and if it does not work they will use someone else's study.

---

## The citation line

One line, in this order, and nothing else:

```
Author, A. (Year). Title of the study in sentence case. Publisher. https://address
```

Filled:

```
Patel, R. (2026). Salary disclosure in 300 adverts for one role. Example Analytics. https://example.org/studies/salary-disclosure
```

Rules:

- The year is the publication year, not the retrieval year.
- The title is sentence case, and it is the same title as the findings document.
- The address resolves to the page that holds the method and the data, not to a landing page with a form.
- If there are two authors, both are named. If there are more than three, the first is named and "et al." follows.
- The same line appears in the pack, on the page, and in the dataset's own README. Three places, one wording.

---

## Before the pack goes out

Run the checker, then read the pack once as if you were the reporter receiving it.

```sh
python3 tools/press_pack.py FINDINGS.md PRESS-PACK.md
```

### What the checker cannot see

The seven rules are a floor. Four gaps are worth knowing, because each one passes the checker and fails an editor.

- **A quote with nothing after it.** The quote rule reads a quoted span followed by a capitalised attribution. A quotation left dangling at the end of a line is not detected, and it is worse than a bad role.
- **A cause in a sentence with no number.** The causation rule looks at sentences that carry a digit. "Collection is clearly the preference here" passes, and it is still a claim the count cannot support.
- **A cause in words the rule does not know.** The word list is finite. "Because", "causes", "leads to", "drives", "results in" and "explains why" are on it. "Underpins", "reflects", "points to" and "tells you" are not, and all four are causal in practice.
- **Tone.** Contempt for the subject passes every rule, and a pack that sneers gets dropped. No rule catches it.

Then answer these five, out loud, in this order:

1. Can I find the number in the first line?
2. Can I find the base beside every percentage?
3. Can I find a person to call?
4. Can I find the method without emailing anyone?
5. Is there anything in here I would not want quoted back at me?

A pack that passes all five and the checker is ready. A pack that passes the checker and fails question 5 is not.

---

## What the pack must not do

- It must not carry the limitations. It links to the document that does.
- It must not claim a cause. "Because", "drives", "leads to" and "proves" are all the same mistake in a pack, and the checker flags them when a number sits in the same sentence.
- It must not round a rate until it sounds better. 38.1% is not "nearly 40%".
- It must not describe the data as a sample of a population it never sampled.
- It must not use a percentage as a headline without the base in the same line.
- It must not go out with a quote nobody approved.
