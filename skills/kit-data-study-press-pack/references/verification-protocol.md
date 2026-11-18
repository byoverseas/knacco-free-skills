# Verification protocol

A count is a person applying a rule to rows. This protocol checks the person against the rows, on a sample fixed in advance, and reports a rate instead of a pass.

It is deliberately not a stamp. A clean sample is not proof of clean coding, and the report says so.

---

## The rule

The sample is drawn by a rule that is written down before the draw, and the rule travels with the sample file.

`tools/verify_sample.py` implements this one:

1. **The frame.** Every row that carries a counting decision. Excluded rows are out of frame, because there is nothing to check against.
2. **The sort.** A stable key: the source id, then the raw text, then the date, then the sheet row. Sorting on the record's own content means the sample does not depend on the order you collected in, so a colleague who re-sorts the sheet gets the same sample.
3. **The stride.** N = round(population / sample size), halves rounded up, and N is at least 1. A population of 118 with a sample of 20 gives a stride of 6.
4. **The offset.** Where the stride starts. Default 0. State it if you change it, because a different offset is a different sample.
5. **The draw.** Take every Nth row from the offset until the sample is full.

The stride, offset, population and drawn count are written into the sample file's own header lines. That is the point: the sample is fixed by the file, not by your memory of what you intended.

### Why a fixed rule matters

If you can re-draw the sample, the check is theatre. The first draw finds four disagreements, the second finds one, you keep the second, and the report says the coding is sound. You have measured how many attempts you were willing to make.

The tool closes that door mechanically: re-drawing writes a new file, and a new file is a new check that must be reported as one. Keep every sample file you draw. If you draw three times, the pack says three times, and the worst rate is the one you report.

---

## How to size a sample

Size decides how much the result can tell you. The bound below is the rule of three, which applies when a sample shows no disagreements: the upper 95% bound is about 3/n.

| Sample size | Zero-disagreement bound | What the sample can support |
|---|---|---|
| 10 | 30% | Almost nothing. Use it as a smoke test, not a check |
| 20 | 15% | "No disagreements found in 20 rows, upper bound 15%" |
| 30 | 10% | A cautious claim, with the bound stated |
| 40 | 7.5% | A firm claim |
| 60 | 5% | A claim you can defend to a sceptical editor |
| 100 | 3% | A claim you can defend in print |

### Choosing a size in practice

- **Minimum:** 20 rows. Below that, report the count as a smoke test and say so.
- **Default:** 60 rows, or every row if the population is smaller than 60. At an hour per hundred rows, a 60 row re-read costs about forty minutes, which is the cheapest insurance in the workflow.
- **Large populations do not need large samples.** The rate you are measuring is a coding error rate, not a market share. A 100 row check on a 4,000 row sheet is a real check.

State the sample size wherever you state the finding. A rate with no sample size is the same failure as a percentage with no denominator.

---

## How to record a disagreement

Every sampled row gets one of two verdicts and a note. No third option, and no blank rows.

| Verdict | When | The note |
|---|---|---|
| `--agree` | Re-reading the raw row, the recorded category follows from the rule | The phrase or field that decided it |
| `--disagree` | Re-reading, the recorded category does not follow, or two categories fit | What the row says and which category it should have |

A note that says "ok" is worthless. The note is what a reader uses to decide whether the disagreement is a typo or a rule problem.

### Reading the disagreements, not just the rate

Sort the disagreements into three kinds before you decide what to do:

1. **Slips.** The wrong category, chosen by accident. Fix the row, re-tally, note the correction.
2. **Rule gaps.** The rule genuinely did not cover this row. The rule was wrong, not the coder. Fix the rule, recode every row the fix touches, and say in the findings that the rule changed after the sample.
3. **Disagreements about the reading.** Two people read the same words differently. This is the important kind, because it means the rule is not tight enough to survive a stranger. Tighten the rule or drop the category.

A rate built from slips and a rate built from rule gaps mean different things even when the number is the same.

---

## What to do at each rate

`tools/verify_sample.py report` prints the band. The bands are these.

| Disagreement rate | Band | What you do |
|---|---|---|
| 0% in 20 or more rows | Holds | Publish, and state the sample size and the bound |
| 0% in fewer than 20 rows | Holds, sample small | Sample more before publishing, or state the wide bound |
| Above 0 to 5% | Usable after correction | Recode the disagreed rows, re-tally, note the correction in the findings |
| Above 5 to 10% | Requalify | Narrow the claim, or count again with a tighter rule. The finding as written does not survive |
| Above 10% | Unusable | Do not publish the finding. The count does not say what it claims to say |

Two refinements that matter:

- **A rate over 10% can kill a finding but not the study.** The rows are still there. A tighter rule often produces a smaller, publishable finding.
- **A zero can hide a bad rule.** If the same person wrote the rule and applied it, zero disagreements may mean the rule is unambiguous, or it may mean the reader has stopped noticing. The only cure is a second person.

---

## The rule of three, stated honestly

When a sample of n rows shows no disagreements, the upper 95% bound on the true disagreement rate is about 3/n.

- n = 20 gives 15%.
- n = 60 gives 5%.

So a clean 20 row sample licenses exactly one sentence: *"a fixed sample of 20 rows found no disagreements, with an upper bound of 15 per cent."* It does not license *"the coding is accurate"*, because a 15% bound is compatible with a lot of error.

This is the number people leave out, and it is the number a careful journalist will ask for. Put it in the findings before they ask.

The tool prints the bound for a zero-disagreement sample, and prints a note instead of a bound when there are disagreements, because the rule of three does not apply once you have a count above zero. With disagreements, the rate you report is a point estimate over the sample, with no upper bound claimed.

---

## What this protocol does not catch

Five failures survive a clean sample.

1. **A rule that does not match the question.** The coding can be perfect and the study still wrong, because it counted something else. Read the question and the rule side by side before you code.
2. **A frame error.** If the population was wrong, every row can be coded correctly and the finding is still false. The population is recorded before filtering for this reason.
3. **Drift.** Coding that starts strict and ends loose. If a sheet was coded over several days, check the last fifty rows as well as the sample.
4. **Systematic misreading.** One person misreading the same phrase in the same way, twenty times. The sample agrees with itself and the error is invisible. Only a second reader or a stranger can find this.
5. **The unasked row.** Rows that were never collected, because the frame missed them. No sample can check a row that is not there.

A study needs one more check that no tool performs: hand the rule and ten rows to someone who has not seen the data, and see whether they reach your categories. If they do, the rule is publishable. If they do not, the rule needs another hour.

---

## The commands

```sh
# 1. Draw the sample once, at a size you can defend
python3 tools/verify_sample.py sample --sheet sheet.csv --size 60 --out sample.csv

# 2. Record every row: agree or disagree, with a reason
python3 tools/verify_sample.py record --sample sample.csv --row 1 --agree --note "names a courier"
python3 tools/verify_sample.py record --sample sample.csv --row 2 --disagree --note "says 'available locally', names no method"

# 3. Report. Refuses while any row is unrecorded
python3 tools/verify_sample.py report --sample sample.csv
```

`report` exits 2 while the sample is incomplete, because a rate over a half-checked sample says nothing about the other half. A completed sample exits 0 and prints the rate, the bound and the band.
