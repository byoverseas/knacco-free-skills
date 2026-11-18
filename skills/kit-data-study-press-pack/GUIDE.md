# Data Research & Press Kit

A method for turning one question into a count that a journalist can cite, with the evidence and the pitch kept in separate files.

Most "data PR" fails in one of two ways. The number is invented to fit the headline, or the study is real and nobody can find it, read it or check it. This workflow fixes both by making the count the thing you sell and by making the count auditable.

Eight stages. Each one produces a file and contains one decision. The decision is the part that cannot be automated.

## The words this guide uses

Nothing below needs learning before you start. Come back when a word gets in the way.

| Word | What it means here |
| --- | --- |
| Study | A count you did yourself, on a question you chose, with the method written down |
| Coding sheet | The table holding one row per thing counted, plus its category |
| Coded | A row that has had its category decided and written in |
| Denominator | The number you divide by. Here, only the rows that are coded |
| Sample | A subset of your own rows, re-read to see whether you agree with yourself |
| Disagreement rate | The share of the sample you categorised differently the second time |
| Findings | The evidence document. Kept separate from the press pack |
| Press pack | The marketing document: release, charts, boilerplate, citation |

---

---

## 1. Find the question

A press question is not a topic. It is a sentence with a number at the end of it. "Delivery in small business" is a topic. "Of 118 maker listings in one directory, 45 say nothing about how a buyer gets the item" is a question with an answer.

### What makes a question press-worthy

Three tests. A question needs all three.

1. **The answer is a number.** A count, a share, a median, a range. If the answer is a judgement, there is no study.
2. **It concerns a group journalists already write about.** Small makers, jobseekers, charity trustees, council tenants, app users. The group is the peg. A finding about a group nobody covers has no home.
3. **The answer could plausibly be surprising.** You should be able to say what you expect and then be wrong. If both possible answers are equally unsurprising, the story is thin.

### What makes a question unpublishable

Three shapes fail no matter how well you count.

1. **It is an opinion.** "Are small businesses bad at customer service?" has no count, and any number you produce will be read as a verdict on people. Ask what is written, not what is good.
2. **It is about the publisher.** "Is our platform the best place to find makers?" answers itself, and a journalist will say so in the reply.
3. **The answer is known in advance.** "Do people like free delivery?" No editor will run it, and the count becomes decoration.

### Three strong questions

- Of 300 adverts for the same job title on one board, how many state a salary or a range?
- How many of the 100 most-downloaded free apps request location access before the first screen?
- Of 250 charity annual reports, how many give trustees' expenses as a single figure?

Each has a number, each concerns a group with a reporter on it, and each can come out either way.

### Three weak questions

- Are small businesses bad at customer service? *(an opinion, and a moral one)*
- Is our directory the most useful in the region? *(about the publisher)*
- Do people prefer free delivery? *(known in advance)*

Read `references/question-tests.md` before you collect anything. It turns the three tests into a checklist with a worked pass and a worked fail, and it lists the shapes that always fail.

**Produces:** one sentence with a number in it, written down before any data is touched.
**Decision:** whether this is a study at all, or a blog post wearing a study's clothes.

---

## 2. Choose the data source

Five source types. Each one can prove something different, and each one lies in its own direction.

| Source type | What it costs | What it can prove | The bias it carries |
|---|---|---|---|
| Public records | Time, sometimes a fee, sometimes a waiting period for a request | What is on the record, dated, in the language of the record | It records compliance, not reality. What nobody filed is invisible |
| A platform's own listing pages | Hours to read and copy, plus re-checking when the pages change | What the platform displayed on the day you looked | The platform chose what exists, and the ranking chose what you saw first |
| An open dataset | Almost nothing in money, real time in learning their column names | Whatever the publisher measured, using their definitions | Someone else's categories, someone else's sample, someone else's vintage |
| A survey you run | Money for a panel, or weeks of your own time for a small one | What people say about themselves | Self-selection, question wording, and the composition of who answered |
| A sample you collect | Roughly an hour per hundred short rows | What is written in the rows you read | Your selection rule and your attention, and nothing beyond your frame |

### The rule

**A source you cannot describe in one paragraph is not a source.**

The paragraph has to say what it is, who made it, when, what it covers, what it leaves out, and how you got it. If you cannot write that paragraph, you do not know what your number means, and neither will the journalist who asks.

Here is a paragraph that passes:

> The 120 maker listings on the public index of one directory, copied with their published text and date on 2 February 2026. The index showed 132 records; 12 were event notices and were excluded as out of scope before coding. Nothing was edited. The directory chooses who is listed, so this is not a sample of makers.

Here is a paragraph that fails:

> Data from various online sources.

**Produces:** a source paragraph, pasted later into the method note.
**Decision:** which source is worth its bias. Cheap and biased beats expensive if you say which way it leans.

---

## 3. Collect

Three things are recorded before a single row is filtered, and they are recorded in a file, not in your memory.

1. **The retrieval date.** The day you looked. Not the day you finished coding.
2. **The query.** The search string, the URL, the filter you applied, the report you downloaded. Enough that someone else could repeat it.
3. **The total population before any filtering.** The number that existed, not the number you kept.

Then keep the raw rows exactly as retrieved. Do not tidy, shorten, spell-correct or reorder. If a row says "colleciton only", the row says that, and your coding sheet copies it.

Filtering is allowed. Silent filtering is not. If 132 records become 120, the method note says 132, says 120, and says why. An unexplained gap between those two numbers is the first thing a careful reader will find.

Keep two files: the raw rows as retrieved, and the coding sheet the tool writes. The raw file is evidence. The sheet is work.

**Produces:** the raw rows file, plus three recorded facts: date, query, population.
**Decision:** what counts as in scope. Decide it now, write it down, and apply it to every row.

---

## 4. Analyse

The categories are defined before counting starts. This is the stage where studies are quietly cooked, usually without malice: you see the data, you notice a nicer cut, and the cut becomes the finding.

Write the categories down and keep them. Then write the counting rule as two tests.

### The counting rule

- **The positive test.** What has to be present for a row to count. Name the words, the field, the marker.
- **The negative test.** What has to be absent for a row to count as not present. This is the test people skip, and its absence is why so many counts are inflated.
- **The ambiguous case.** What happens when a row half qualifies.

A rule that passes:

> Positive: the listing names a method a buyer could act on. A posting, a courier, a delivery, a collection, a pickup, or a handover at a named place.
> Negative: the listing names no such method, and does not gesture at one.
> Ambiguous: the listing gestures at a handover without naming one. Held separately, then decided in writing.

A rule that fails:

> We counted listings that mention delivery.

That sentence has no negative test, no ambiguous case, and no way to disagree with the coder.

### Why ambiguous rows are counted separately

Folding an ambiguous row into a category is a decision disguised as a count. If you fold it into "present", the finding grows. If you fold it into "absent", the finding shrinks. Either way the reader cannot see the seam.

Hold ambiguous rows in their own bucket. The tally refuses while any row is ambiguous, which forces you to decide each one and write the reason. After the decision, the row carries a note a reader can argue with.

Use `tools/study_sheet.py` for the sheet. It refuses to print a percentage until every row carries a decision, and it prints the denominator with every count. The denominator is the number you divide by, which here means only the rows you finished. A percentage over a half-finished sheet is the most common way a study gets its first wrong number.

**Produces:** a coded sheet, a counting rule, and a decision on every ambiguous row.
**Decision:** whether a half qualifying row is in, out, or excluded, and why. Write the why in the note.

---

## 5. Verify

Re-read a sample of your own coding against the raw rows. Not all of it, and not the rows you remember as tricky.

### The sampling rule

The sample is drawn by a fixed rule, written down before the draw, and the rule travels with the sample file.

`tools/verify_sample.py` uses this one:

1. Take every row that carries a counting decision. Excluded rows are out of frame.
2. Sort by a stable key: the source id, the raw text, the date, the sheet row number. Sorting on the record's own content means the sample does not depend on the order you collected in.
3. Stride N = round(population / sample size), halves rounded up.
4. Start at the offset, take every Nth row until the sample is full.

### Why the rule has to be fixed

A sample you can re-draw is not a check. If the first draw finds four disagreements and the second finds none, and you keep the second, you have measured your patience rather than your accuracy. The tool writes the stride, the offset and the population into the sample file, so the draw cannot be repeated inside the same file. Drawing again means a new file, and a new file is a new check that has to be reported as one.

### What the disagreement rate means

The rate is the share of sampled rows where the re-read disagreed with the code. It measures the coding, not the question. A high rate does not mean the finding is uninteresting. It means you cannot say what the finding is.

| Disagreement rate | What it means |
|---|---|
| 0% in 20 or more rows | Publish, and state the sample size and the bound |
| 0% in fewer than 20 rows | Publish only with the wide bound stated, or sample more first |
| Up to 5% | Recode the disagreed rows, re-tally, then publish with the correction noted |
| 5% to 10% | Narrow the claim, or count again with a tighter rule |
| Over 10% | Unusable. Do not publish the finding |

### The bound nobody mentions

A clean sample is not proof of clean coding. When a sample of n rows shows no disagreements, the upper 95% bound on the true disagreement rate is about 3/n, which is the rule of three. At 20 rows that bound is 15 per cent. At 60 rows it is 5 per cent.

So a 20 row sample with zero disagreements licenses one sentence: "a sample of 20 found no disagreements, with an upper bound of 15 per cent." It does not license "the coding is accurate". `tools/verify_sample.py report` prints both the rate and the bound, and names the verdict band.

**Produces:** a sample file with a verdict on every row, and a reported rate.
**Decision:** whether the finding survives the rate. Over 10 per cent, the finding is dead, and no amount of rewriting the pack saves it.

---

## 6. Write the findings

The findings document is the evidence. It is not the pitch, and it is not marketing. Write it so that a hostile reader with the raw rows can follow every number.

### Lead with the number

The first line is the count, not the adjective.

- Fails: *Makers are woefully behind on telling buyers how to get their work.*
- Passes: *45 of the 118 maker listings (38.1%) state no way for a buyer to receive the item.*

The judgement version cannot be checked. The count version can, and it is the sentence a journalist will quote.

### Separate observation from interpretation

The observation is what the rows say. The interpretation is what you think it means. Keep them in different paragraphs, and make the second one shorter.

- Observation: *Collection is named in 47 of the 118 listings (39.8%), 38 of them as the only method.*
- Interpretation: *Collection is the option makers do name. Whether that reflects workshop size, courier cost or something else is not in the data.*

The second sentence is allowed. What is not allowed is the two blurred together, because then a challenge to the interpretation looks like a challenge to the count.

### State the limitations in the document

Not in the pack, not in a footnote, not in an email. In the findings, under a heading called Limitations, with the things that would change the answer:

- the frame and what it is not a sample of
- who coded it and whether anyone checked
- what the count measures (statements, not behaviour)
- what the categories hide
- what the result would look like if the rule were tightened

### Run the checker

`tools/press_pack.py` reads the findings and the pack and scores seven errors and four warnings. An error is one of the things that makes a study unusable: no number in the headline, no dated method note, no sample size, no limitations section, a percentage with no denominator, a cause claimed from a count, a quote with no role. Fix every error before the pack goes anywhere.

**Produces:** the findings document, dated, with a method note, a denominator, a limitations section and a verification note.
**Decision:** how far the claim travels. A count supports a description. It does not support a cause.

---

## 7. Build the press pack

The pack is a different document with a different job. It exists to get a busy person to read the findings. It is not evidence, and it should never be the only thing you publish.

### The release shape

| Part | What it does | Length |
|---|---|---|
| Headline | The finding, with its number and its denominator | One line |
| Standfirst | One sentence that adds the second number | One or two sentences |
| Dateline | Place, date, embargo | One line |
| The finding | The count in plain words, then the second count | Two short paragraphs |
| Evidence | Two or three numbers a desk can build a piece on, each with its base | One paragraph |
| Quote | One person, with a role, saying something only they could say | Two sentences |
| Charts | Three, named, with what each shows | Three lines |
| Boilerplate | Who you are, in the third person | Three sentences |
| Contact | A name, a role, an address that answers | Two lines |
| Citation | A line a journalist can paste | One line |

### The three charts

A journalist will use three charts, and they are not the three you would choose for a slide.

1. **The split.** Every category as a bar, sorted, with the denominator in the subtitle. This is the chart that runs.
2. **The comparison.** The two categories your finding is really about, with the overlap shown separately rather than buried inside a total.
3. **The movement.** The same split over time, or across a second dimension, so a desk can answer "is this new". If the pattern is flat, say it is flat. A flat chart is still an answer.

Each chart carries its denominator, its dates and, if the data is synthetic or partial, a note saying so.

### The quote

One quote, from a person with a role, saying something the data cannot. Not "this is interesting". Something like "we expected delivery to be the omission, and it was collection".

Never write a quote for someone who has not approved it. Never attribute a quote to a role you cannot evidence. `press_pack.py` checks for the role; only you can check the person.

### The contact and the boilerplate

A contact is a name, a role and an address that a journalist can use at 4pm on a Friday. A pack with no contact is a document, not a pitch.

The boilerplate is three sentences about who you are, written in the third person, with no adjectives you would not put on an invoice.

### The citation line

One line, pasteable, containing author, year, title and address. Use `references/press-pack-shape.md` for the exact shape and a filled example.

**Produces:** the pack, the charts and the citation line.
**Decision:** what the pack leaves out. The pack is not the place for limitations, method detail or caveats, because the pack links to the findings that hold them.

---

## 8. Publish the page

The page is where the study lives. A journalist who receives the pack will open the page before replying, and will decide in about forty seconds whether you are worth quoting.

The page holds five things, in this order:

1. **The study.** The finding, at the top, in the same words as the pack headline. A journalist who lands here from a search should see the same number.
2. **The method.** The source paragraph from stage 2, the retrieval date, the query, the population before filtering, the denominator. This is the section that decides whether you get quoted or ignored.
3. **The raw data.** A download of the raw rows and the coding sheet. Not a summary, not a dashboard, the actual files. This is rarer than it should be, and it is the single strongest signal that the study is real.
4. **The date.** Published, and if it matters, retrieved. A study with no date is a study nobody can cite.
5. **The citation line.** The same line as the pack, in a copyable block, with the address of the page itself.

Add a short "what this does not show" block on the page too. It costs you nothing and it pre-empts the first objection.

**Produces:** a page that a journalist can check without emailing you.
**Decision:** whether you are willing to publish the rows. If not, the study is not ready.

---

## The overriding rule

**The findings are evidence. The pack is marketing. They are never the same document.**

This is the rule that holds the rest together, and it is the one most often broken for convenience. A single document that carries the pitch and the caveat gets quoted as if it were the evidence, and then the caveat is the thing that gets dropped.

Keep them apart and each one gets better:

- The findings document can be dull, long and precise, because nobody has to enjoy it.
- The pack can be sharp and selective, because it links to the document that carries the caveats.
- When a figure is challenged, you send the findings, not the pack.
- When a journalist is deciding whether to reply, you send the pack, not the findings.

`tools/press_pack.py` reads both files at once and refuses to pass while a percentage in either one has no denominator. That is the mechanical part. The separation itself is a filing decision, and it takes five seconds: two files, two names, one link between them.

---

## Limits of this method

This is a coding and counting method. It is not a statistics course, and it is not a substitute for one.

It handles: how many of a defined population have a property you can see, with a stated rule and a stated denominator.

It does not handle, and you should not pretend otherwise:

- **Weighting.** Any claim that the sample represents a wider population needs a sampling design and weights.
- **Significance.** "The difference is real" needs a test, and a test needs an assumption about the data.
- **Projection.** "This means 40,000 businesses nationally" needs a multiplier you do not have.
- **Small counts.** A category with four rows in it is a story about four rows, not about a trend.
- **Change over time.** Comparing two retrievals needs the same rule applied twice, by the same people, and even then a shift can be drift in the source.
- **Causal claims.** A count shows what is written. It cannot show why.

If a result needs any of those, say so in the findings and get a statistician to read it before the pack goes out. A sentence that names what the study cannot do is worth more than a confident sentence that turns out to be wrong.

Two smaller limits worth stating on the page:

- One coder is one opinion. A second reader on a shared slice is the cheapest improvement available to any counting study.
- Categories are coarse. Every bucket hides the distance between its easiest and hardest member.

---

## What this workflow does not do

- It does not choose your question, your source or your categories. Those are the decisions, and they are yours.
- It does not collect data. You retrieve, or you pay for a panel, and you keep the rows.
- It does not tidy your raw data. Tidying is where the count starts drifting.
- It does not guarantee that a finding is interesting, or that a journalist will reply.
- It does not make a result statistically valid. It makes it checkable, which is a different and smaller promise, and the one this method can keep.

## Sources and reuse

Source reference: a public walkthrough of a PR campaign using an AI assistant. No source text, prompts or template wording are included. See `README.md` for the product licence and reuse terms.
