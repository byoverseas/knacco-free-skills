# The build spec shape

A build spec is the handover document. It is written for a coding tool that has never met the business, will not ask a follow-up question, and will fill every gap with an invention. The spec has eleven fields, and each one exists because leaving it out produces a specific, predictable mistake.

The checker enforces this file:

```sh
python3 tools/spec_check.py my-spec.json
```

`tools/spec_check.py --example` prints a complete spec that passes, so you can start from a working shape rather than a blank page.

## The eleven fields at a glance

| # | Field | Answers |
| --- | --- | --- |
| 1 | `niche` | Who is this for, in one trade and one place |
| 2 | `paid_offer` | What the magnet bridges to, with a price |
| 3 | `pain` | The problem in the user's words |
| 4 | `promise` | The sentence the tool can honour |
| 5 | `inputs` | The numbers the user supplies, five at most |
| 6 | `screens` | The first screen, the empty state, the mobile rule |
| 7 | `logic` | The computation, step by step |
| 8 | `output` | The result the user receives |
| 9 | `gate` | Where the email gate sits and what it holds back |
| 10 | `cta` | What happens after the result |
| 11 | `success_measure` | The metric, the target and the window |

---

## 1. `niche`

**What belongs.** One trade, one size, one country, and the constraint that shapes the buyer's day. A stranger should be able to name three businesses that fit and three that do not.

**A bad answer.** "Small businesses who want to grow." It names no trade, so every later field drifts: the inputs are wrong for a plumber, the output is wrong for a shop, and the offer behind it cannot be described.

**A filled example.** "Independent physiotherapy clinics in the UK with two to six therapists and no practice manager, where the owner still treats patients four days a week."

## 2. `paid_offer`

**What belongs.** The thing being sold, what it costs, and how it is delivered. One sentence with a number in it.

**A bad answer.** "Our premium consulting package." No price, no delivery, no way to judge whether the magnet's result is worth the next step.

**A filled example.** "A 90 minute clinic operations review at 450 pounds, which becomes a monthly retainer at 220 pounds a month for the clinics that want the changes held in place."

## 3. `pain`

**What belongs.** The problem as the buyer would say it out loud, including what they currently do about it. The word "currently" matters: a pain with no workaround is usually not a pain yet.

**A bad answer.** "They lack data-driven insight." That is your diagnosis of their situation, not their sentence, and it will produce copy nobody recognises.

**A filled example.** "The owner knows some appointments are lost to no-shows and late cancellations, and cannot put a monthly figure on it. The problem stays a feeling in the staff room rather than a line in the accounts."

## 4. `promise`

**What belongs.** One sentence, in the form "this takes your numbers and gives you this result". It names the computation, not an outcome. It must be a sentence the tool can keep on its worst day.

**A bad answer.** "Discover how much more you could earn." It promises an outcome, it names no computation, and any result the tool produces will be judged against a number nobody defined.

**A filled example.** "The calculator multiplies the clinic's own weekly appointment count, average fee and missed appointments into a monthly and an annual revenue figure, then repeats the same arithmetic at a miss rate one fifth lower. It reports arithmetic the owner can check by hand."

## 5. `inputs`

**What belongs.** One to five items. For each: the name as the user sees it, the type, and one line on why the result needs it. The "why" is not decoration: an input whose why is weak is an input to cut.

**A bad answer.** Seven fields including "patients seen once and never rebooked" and "hours per week on admin". Both need a report, so the owner stops at field five and the first four answers are lost.

**A filled example.** Four items: appointments booked per week, average fee, no-shows in a typical week, late cancellations in a typical week. Each has a type of number and a one-line reason.

## 6. `screens`

**What belongs.** Three short blocks.

- `first`: what the user sees before doing anything. Fields, order, the sentence under the heading, the button label, and what is deliberately absent from this screen.
- `empty_state`: what the result area holds before any input, and what the button does while fields are empty.
- `mobile`: the layout at narrow width, the minimum size of the main figure, and the width the tool is tested at.

**A bad answer.** "Standard form page, responsive." It leaves the empty state, the button behaviour and the narrow-width layout to the coding tool, which will invent all three, usually as a blank box and a live button that returns errors.

**A filled example.** First screen: "One page with the clinic name at the top, four number fields in a single column, one plain sentence saying what the calculator will do with them, and one button reading Show the monthly cost. There is no email field on this screen."

## 7. `logic`

**What belongs.** The computation as an ordered list, one operation per line, with rounding and units stated, and the cases that suppress a result. If a rule is a judgement rather than arithmetic, say so and say who makes it.

**A bad answer.** "Calculate the lost revenue based on the inputs." That is the promise again, not the method. The coding tool will choose the formula, and you will discover which one it chose at review time.

**A filled example.** "Missed per week equals no-shows plus late cancellations. The miss rate equals missed per week divided by appointments per week, shown as a percentage to one decimal place and capped at 100. The monthly cost equals missed per week multiplied by the average fee, multiplied by 4.33."

## 8. `output`

**What belongs.** Every field the result shows, in order, with its unit and its rounding. Then the format: layout, what is largest, what is grouped, and what the result can be copied as.

**A bad answer.** "A nice results page with a chart." No fields, no units, so the tool invents a chart of something, and the numbers on it cannot be checked against the clinic's own arithmetic.

**A filled example.** Five fields, the first being "monthly cost of missed appointments, in pounds, one decimal place, set as the largest figure on the page", and a format sentence describing a single results panel that can be copied as plain text with labels attached.

## 9. `gate`

**What belongs.** Three things.

- `position`: `after-partial`. Not a free choice; the checker accepts only this value.
- `shown_before`: which part of the result appears with no email given.
- `held_back`: which part waits for the address, and what the panel says about it.

**A bad answer.** "Email capture before results." That is the gate at the door, and the visitor is asked to pay before seeing the calculator work.

**A filled example.** Shown before: monthly cost, miss rate, missed appointments per week. Held back: the annual cost and the lower-rate block, with the panel saying what is behind the gate before it asks.

## 10. `cta`

**What belongs.** The sentence the user reads, the named destination it points at, and whether it appears with the result, after the email, or in both places. If the result passes a figure to the destination, say so.

**A bad answer.** "Link to contact page." No sentence, no destination, and no connection between the number the user just saw and the page they land on.

**A filled example.** "If the annual figure is worth fixing, book the 90 minute review. Bring the four numbers and the review starts from them." Destination: the booking page, with the monthly figure and miss rate passed in the query string.

## 11. `success_measure`

**What belongs.** One metric, one target, one window. Optionally, the review points inside the window.

**A bad answer.** "Track engagement." Nothing here can fail, so nothing will be fixed.

**A filled example.** Metric: completed calculations as a share of visits, and review bookings that name the calculator. Target: a quarter of visits reach a result, two bookings a month. Window: eight weeks, reviewed at four and at eight.

---

## The gate, in order

The rule is gate after value. The order of events on the page is fixed:

```
1. First screen        four fields, no email field anywhere on it
2. Press the button    result area fills, no address given
3. Partial result      one or two figures that prove the thing works
4. Gate                the address is asked for, and the panel says what is behind it
5. Full result         the rest of the figures, on the same page
6. Call to action      the sentence and the destination, next to the full result
```

Two failure modes to name. A gate at step 1 is a door tax: most visitors leave, and the ones who stay never saw the tool work. A gate with nothing behind it, because the partial result was already the whole result, is a lie the visitor can see.

The call to action sits at step 6, next to the result, not in the footer. A result page with the next step in the footer is a page that hides its own offer.

## The output format a vibe-coding tool reads best

The format follows from what a coding tool can execute without asking questions. These are recommendations, not laws.

1. **One page.** A single HTML file with inline style and inline script. No build step, no framework, no dependency to install, so the result can be opened, checked and sent without a toolchain.
2. **No server for the calculation.** The arithmetic runs in the page. The only network call is the email submission at the gate, and the spec should name that endpoint or say it is a placeholder.
3. **State written down.** Four states: empty, partial, gated, full. Each has a line in the spec. A coding tool that is given four states builds four states; one that is given a "results page" builds one and invents the rest.
4. **Copy in the spec, not in the design.** Button labels, the heading, the sentence under it, the gate wording and the call to action sentence all appear verbatim in the spec. Design decisions can be left open. Words cannot.
5. **Numbers with units and rounding.** Every figure in `output` carries both. "12.4 pounds" is reviewable. "12.44444" is a support ticket.
6. **A stated test width.** The mobile rule names a width in pixels. A rule that says "responsive" is not testable.

## Before you hand it over

Run the checker, then read the spec once as if you were the coding tool:

```sh
python3 tools/spec_check.py my-spec.json
```

A pass at 100 means the eleven fields are filled and the seven build-stopping omissions are absent. It does not mean the magnet is good. It means the build has enough to build the thing you meant, which is the most a spec can promise.
