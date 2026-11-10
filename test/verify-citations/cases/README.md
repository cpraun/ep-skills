# Citation test cases

Each folder here is one case for `test_locate_citation.py`:

```text
cases/
  NN-<label>/
    sources/          the documents cited (PDF — text or scanned — DOCX, TXT, MD)
    citations.yaml    the citations to check, with the expected result
```

`01-example/` shows every feature; copy it as a starting point.

## Adding your own case

1. Create `cases/02-<label>/sources/` and put your source documents in it
   (e.g. `D1.pdf`, `Description.docx`, a scanned `D2.pdf`).
2. Write `cases/02-<label>/citations.yaml` — one entry per citation:

   ```yaml
   - id: d2-claim-1-feature          # unique within the case
     source: D2.pdf                  # file in sources/
     quote: "a closure member biased against the valve seat"
     cited: {para: "[0034]"}         # or {claim: 1} | {page: 7} | {page: 7, lines: "12-14"}
     expect: verbatim                # see below
     found_at: {para: 34, page: 7}   # optional: where it must actually be
     lang: deu                       # optional: OCR language for scanned PDFs (default eng)
   ```

   `expect` is one of `verbatim`, `minor-divergence` (punctuation / case /
   spacing only), `ellipsis` (fragments around `…` / `[...]` in order),
   `wrong-location` (in the source, but not where cited), `not-found`.
3. Run `pytest test/verify-citations`. A failure prints what the locator
   actually reported, including the closest passage for `not-found`.

Include citations that should fail as well as ones that should pass — wrong
paragraph numbers, altered numerals, quotes of deleted tracked-change text — since
those are what the check exists for.

## Confidentiality

Everything under `cases/` is committed to the repository. Use **published or
fictitious documents only** — no unpublished applications, client
correspondence or drafts. For real case material, keep a local case folder whose
name starts with `local-` (excluded from git) — the test runs it like any other.
