# Back-check brief: ASTRA Test 3 (internal T05) Kannada edition (FDA and SDA), batch NN

*An internal Claude Code check, run before the owner and Gemini see the paper. Adapted from `ASTRA/T03/KN_BACKCHECK_BRIEF.md`.*

You are an independent checker. You did not write this Kannada, and no session verifies its own work (lessons §5). Your only job is to **find defects**. You do not rewrite the batch.

## Files
- **Your batch folder is given in your task:** `ASTRA/T05/kn_batches/` (FDA) or `ASTRA/T05/kn_batches_SDA/` (SDA).
- **English** (authoritative, frozen): `<folder>/IN_NN.jsonl`. `text` is the question and `sol` the solution.
- **Kannada under check:** `<folder>/OUT_NN.jsonl`, with `kn_text` and `kn_sol`.
- **Binding terms:** `KN_GLOSSARY_T3.tsv` (the one glossary shared by both papers) in `ASTRA/T05/`, and the `ALL` rows of `ASTRA/T01/TERM_CHOICES.tsv`. The translator's `<folder>/NEW_TERMS_NN.tsv` lists the terms not in the glossary; judge those as terminology too.
- **Owner rule on labels:** ಪರೀಕ್ಷಾ ಸಂಗತಿ (Exam Fact) and ತೀರ್ಮಾನ (Result). **Any ಪರೀಕ್ಷಾ ಸತ್ಯ is a QUEUE A defect.**
- **Register, for language only (no facts):**
  - DSERT Kannada-medium Social Science: `05_ANALYSIS/ASTRA_2026/T05_SOURCE_TRACE/source_text/DSERT_<class>_SS<part>_KN2627.txt`;
  - KEA's own Kannada: `05_ANALYSIS/KEA_CA_SOURCES_2026-11/population/OCT_STEMS.jsonl` and `SAMARTHA_2.0/KANNADA_TRANSLATION/P1_CORPUS/PARALLEL_CORPUS.jsonl`.

## Method, per item
Back-translate each Kannada line into English yourself **before** you look at the English line. Then compare the two.

## What to check
1. **Key and option order:** unchanged. Both the `ಸರಿಯಾದ ಆಯ್ಕೆ` letter and the "ಆದ್ದರಿಂದ…" line give the English key.
2. **Truth value:** every statement, row, pair, option and solution sentence has the same meaning and truth value as the English. Look in particular for:
   - dropped or added negation, "only", "except", "first", "most", "traditionally";
   - changed quantifiers, tense or modality;
   - changed names, numbers, dates, centuries, BCE/CE and relations: who built, who wrote, who defeated whom, which dynasty.
3. **Unique answer:** reading only the Kannada question, a candidate reaches the same single answer. Report wording that makes a second option defensible, or that makes the key obvious through case endings, agreement or one smoother option.
4. **Stem and closing:** the Kannada asks the same question as the English: "correct" or "NOT correct", "correctly" or "INCORRECTLY matched", "how many", "chronological order".
5. **Solution agreement:**
   - The solution says what the English solution says. It adds no fact and no note about ambiguity (owner R12).
   - It uses the same Kannada term for a concept as the question does.
   - It carries the deciding keywords in bold where the English has them.
6. **Terminology:** report deviations from the glossaries and wrong or misleading history terms.
   - **A wrong term is QUEUE A when it changes the fact.** Examples: a different king of the same name (Pulakeshi I vs II); a confused dynasty (Kalyana Chalukya vs Badami Chalukya); a wrong title; ಕ್ರಿ.ಪೂ. and ಕ್ರಿ.ಶ. swapped.
7. **Language:** Kannada so ungrammatical or garbled that the meaning is obscured.
8. **Naturalness:** the owner wants nothing "artificial, soulless & AI-like". Flag lines that read as translated: English word order, word-for-word calques, stiff coinages, overlong sentences. These are QUEUE B; give a natural Kannada line that keeps the meaning exactly.

## Severity
- **QUEUE A (blocker):**
  - changed truth value or fact;
  - wrong key or option order;
  - a second defensible option;
  - a leaked key;
  - a solution fact that differs from the English;
  - a term that changes the fact;
  - ಪರೀಕ್ಷಾ ಸತ್ಯ anywhere.
- **QUEUE B:**
  - a non-standard term or glossary deviation where the meaning is still recoverable;
  - awkward grammar;
  - unnatural Kannada.

## Output
Write `<folder>/CHECK_NN.tsv` with this header:

`id	part	line_no	kannada_text	back_translation	problem	suggested_kannada	queue`

- `part`: `Q` for the question, `S` for the solution.
- `line_no`: the 1-based line number within `kn_text` or `kn_sol`.
- `kannada_text`: **the exact full line** as it stands, so that a script can replace it.
- `suggested_kannada`: **the full corrected line**, keeping the line's labels, its `**` bold markers and its `*` italics.
- `queue`: `A` or `B`.
- No tab characters inside a field.

Write one row per defect. After the defects, write one row per clean item: `id`, `-`, `-`, `-`, `-`, `CLEAN`, `-`, `-`.

End your reply with the counts: Queue A N, Queue B N, clean N.

## Working rules
- Use the Write tool, in UTF-8.
- Never print Kannada to the console, which is cp1252. Write it to a UTF-8 file and Read that file.
- Run Python with `python -I -X utf8`.
- Do not commit. Edit no file other than `CHECK_NN.tsv`.
