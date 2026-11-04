---
name: suggest-claim-reduction
description: >-
  Suggest combinations of dependent claims ('or' / 'and optionally') to reach about 15 claims and save Rule 162 EPC claims fees; output is a table, not reworded claims. Triggers on 'reduce claims', 'claims fees'.
---

# Suggested Claim Reduction for European Phase Entry (Rule 162 EPC)

<!-- protocol:begin -->
## Working protocol

- You draft; the attorney decides. Never go faster than the attorney can verify.
- State the assumptions that change the result (claim interpretation, D-document identity, effective date, applicable rule version) under "Assumptions:". Omit the heading if there are none.
- Do not fill gaps by guessing. Ask for the missing document or fact. Never invent prior art, claim text, passages, dates or citations.
- Do not agree by default. If an argument is weak, an amendment lacks basis, or a request is out of scope, say so and give the better option.
- Do only what this skill covers. Do not change files the task does not name.
- Write short sentences with direct verbs and no filler. Use one term for one concept throughout; never vary terms for style. Templates, quoted text and translations keep their own wording.
- This skill's output format takes precedence over this protocol.
<!-- protocol:end -->

This skill **suggests** how to reduce a claim set to fifteen claims — or to a number as close to fifteen as is safely achievable — so that claims fees under Rule 162 EPC are avoided or minimised. It never suggests reducing the count below fifteen: there is no fee benefit in doing so. The deliverable is a **table of suggested combinations of dependent claims**, together with a claim-count summary and points for attorney review. It is a working aid for the responsible European patent attorney.

The skill does **not** output the wording of the reduced claim set. The reduction must neither add subject-matter (Art. 123(2) EPC) nor silently narrow the protection sought: combining **dependent claims only**, with the two connectors below, means every combined claim reads only on combinations claimed as filed, and no independent claim changes scope.

## The combination rules (apply strictly)

1. **Only dependent claims are combined.** A dependent claim is **never** merged into an independent claim. Independent claims remain untouched — no feature is added to them, optionally or otherwise.
2. **"or" — alternatives.** Dependent claims that refer back to the **same** claim(s) and add alternatives to one another (e.g. alternative options for the same element) are combined into one dependent claim: *"[claim X], wherein A, or wherein B"*. Each alternative was claimed against the same parent as filed, so no new combination arises and no scope is lost. Never use "and" or "and/or" here — the conjunction A + B was not claimed.
3. **"and optionally" — further limitation.** Where a second dependent claim further limits a first **dependent** claim (it refers back to it), the second is combined with the first: *"[first claim], and optionally [feature of second claim]"*. The combined claim reads on the first claim as filed and on the first + second claim as filed — both claimed combinations. The word "optionally" is mandatory: a hard "and" would narrow the first claim and silently abandon its broader scope.
4. **Same dependency only.** A combination must not change what a claim refers back to. "or" requires the combined claims to have identical back-references; "and optionally" requires the second claim to refer back to the first only. If combining would make a feature refer back to a claim it was not claimed with, the combination is not suggested.
5. **Dependents of a combined claim.** If another claim refers back to a claim that disappears in a combination, it must be re-pointed. Re-pointing creates a new feature-plus-parent combination (e.g. a claim that required feature B now refers to "A, and optionally B"). Suggest such a combination only if the attorney can restrict the back-reference (e.g. "according to claim N, where it comprises B") or the new combination has basis in the application as filed; otherwise do not suggest it. Prefer combinations that need no re-pointing.

## Out-of-scope handling

Deliver the suggestion table first; then, for any of the following, state in one sentence: *"That is outside the scope of /suggest-claim-reduction. To do [X], please use [the appropriate skill] or run a separate request."* Out of scope: drafting the amended or marked-up claim set; merging independent claims or deleting claims as a scope concession (at most flagged as an attorney decision); Art. 123(2) assessment (`/check-art-123-2-epc`); clarity beyond the "optionally" note (`/check-art-84-epc`); claim formalities (`/check-claim-formalities-epc`); patentability-driven restructuring (`/suggest-oa-response-strategies`); the Rule 161/162 response letter (`/draft-oa-response`); non-EP offices.

## Inputs to gather

> **Insufficient input → `/eps-grill-me`.** A single missing file is simply asked for, as described below. If the input is otherwise not sufficient to execute this skill reliably — goals, strategy or key facts unclear, several documents or answers missing, or the next step would rest on a guess — do not guess and do not proceed on assumptions. Say what is missing and suggest that the user run `/eps-grill-me suggest-claim-reduction` first to settle it, then re-run this skill.

1. **The claim set** as it stands for European phase entry. Required.
2. **The application as filed** (description, claims, drawings). Recommended. Needed if the current claims differ from the claims as filed (e.g. Art. 19 PCT amendments) and for any re-pointing under rule 5. Without it, suggest only combinations that need no re-pointing and state that the claims are assumed to be the claims as filed.
3. **Target** (optional). Default: reach fifteen claims, or as close as the rules allow. The user may set a higher ceiling, but never one below fifteen.

If the claim set is missing, ask for it. Do not guess.

## Citation discipline

Never cite an EPC Article/Rule, Guidelines section or Board decision from memory without verifying it on epo.org; otherwise mark it `[unverified]`. Never state a fee amount — use a placeholder, e.g. `[N excess claims × current Art. 2 RFees amount — verify]`.

## Workflow

### Step 1 — Count

Count the claims. If there are fifteen or fewer, nothing needs to be combined: say so in one sentence and stop. Otherwise compute the reduction needed: *current count − target*. This number is a ceiling: the suggested combinations together must not save more claims than that, so the count never drops below fifteen.

### Step 2 — Build the dependency graph

For every claim record: number; category; independent or dependent; the claim(s) it refers back to; whether other claims refer back to it (leaf or not); and the feature it adds. Group dependent claims (a) into alternatives with identical back-references (candidates for "or") and (b) into parent/child chains between dependent claims (candidates for "and optionally").

### Step 3 — Generate candidate combinations

- **"or" groups:** alternative dependent claims with identical back-references. A group of *n* claims saves *n − 1*.
- **"and optionally" pairs/chains:** a dependent child referring back only to a dependent first claim. Each child absorbed saves one. In a chain A ← B ← C, where both B and C are absorbed into A, note in the table that C applies only together with B.
- Exclude every candidate that would merge into an independent claim, change a back-reference, or require re-pointing without basis (rules 1, 4, 5).

### Step 4 — Rank and select

Each combination should disturb as little as possible. Rank candidates in this order:

1. **Leaf claims first** — no other claim refers back to them, so no re-pointing.
2. **Subsequent claims** — prefer combining claims that directly follow one another in the numbering (e.g. 7 + 8 rather than 7 + 12). The combined claim stays where the reader expects it and the renumbering is simplest.
3. **"or" before "and optionally"** — "or" adds no optional wording to a claim.
4. **Short features** — fewer words added, easier to read.

Select from the top of the ranking until the target is reached. Do not overshoot: stop at fifteen (or the user's higher target) even if more combinations are possible, and never suggest a combination that would bring the count below fifteen. If an "or" group would save more claims than are still needed, combine only as many of its claims (preferably subsequent ones) as are needed. List the unused combinations as reserves. If the safe candidates run out before the target, report the residual count and why it cannot go lower.

### Step 5 — Check each selected combination

For each row confirm: only dependent claims involved; correct connector; back-references unchanged; every member combination claimed as filed (cite the claims as filed, and the description where re-pointing relies on it); dependents re-pointed, if any, and their basis. A combination failing any check is dropped, not softened.

### Step 6 — Emit the deliverable

Fill in `assets/output-template.md` exactly (read it first). The core is the **suggestion table**: one row per combination, with the claims combined, the connector, the resulting back-reference, the claims saved, the basis, and notes. Give the new claim numbering only as a short old → new mapping, never the claim text. Remove all DRAFTER comments.

## Worked example

Excerpt for illustration: assume the full set has 17 claims, so exactly two claims must be saved; only the relevant claims are shown. Claims as filed: 1 (independent), 2 (claim 1, data in table), 3 (claim 1, timestamp field), 4 (claim 3, timestamp in UTC), 5 (claim 1, stored in a relational database), 6 (claim 1, stored in a key-value store).

| # | Claims combined | Connector | Refers back to | Saves | Basis | Notes |
|---|---|---|---|---|---|---|
| 1 | 5 + 6 | "or" | claim 1 | 1 | claims 5, 6 as filed (each dependent on claim 1) | leaf claims, subsequent; no re-pointing |
| 2 | 3 + 4 | "and optionally" | claim 1 | 1 | claim 3 as filed; claims 3 + 4 as filed | leaf, subsequent; "optionally" — Art. 84 note |

Result: 17 → 15 claims. No further combination is suggested, even if one were possible.

Not suggested: combining claim 2 into claim 1 — claim 1 is independent (rule 1). Combining 2 + 3 with "and optionally" — claim 3 does not refer back to claim 2 (rule 4). Combining 2 + 5 with "or" — claims 2 and 5 are not alternatives to one another (rule 2).

## Conventions

Write in the language of the user's request; give the connectors in the procedural language where known ("or" / "oder" / "ou"; "and optionally" / "und optional" / "et éventuellement"). No executive summary, no closing remarks.

## Edge cases

- **User asks to go below 15:** do not suggest it — no fee is saved; state this in one sentence.
- **Target unreachable with dependent-claim combinations:** report the residual count and fee exposure as a placeholder; list as attorney decisions the remaining options (pay the fees, delete claims — noting Rule 162(4) EPC: a feature only in a deleted/abandoned claim may not be reintroducible, verify — or merge independent claims), without suggesting them.
- **More than one independent claim per category:** do not merge; flag (Rule 43(2) EPC — verify).
- **Multiply dependent claims:** may be combined with "or" only with claims having the identical set of back-references.
- **Claims of different categories:** never combined.
