# Brief: glossaries for the ASTRA Test 3 (internal T05) FDA Kannada edition

*Claude Code, 23-11-2026. Adapted from the Test 2 brief (`ASTRA/T03/GLOSSARY_BRIEF.md`).*

**Basis:**
- The owner shipped FDA English v5 and ordered the Kannada FDA edition by the Test 2 process (23-11-2026; `PRODUCTION_STATE.md` §514).
- The English is frozen: `05_ANALYSIS/ASTRA_2026/T05/ENGLISH_MASTER_FREEZE_FDA.md`.

**Purpose:** the glossary fixes one Kannada form per term before the translation batches start. The whole paper then uses the same word for the same concept. Lessons file §4: "Use the same Kannada term for a concept in a question and in its solution."

There are two glossaries, built by two agents in parallel. You are told which one is yours:
- **HISTORY:** the 75 Part A items (`n` 1–75: Ancient and Medieval History, Indian and Karnataka). Write `HISTORY_GLOSSARY.tsv`.
- **CA:** the 25 Part B items (`n` 76–100: current affairs, September 2026). Write `CA_GLOSSARY.tsv`.

## Input
`SAMARTHA_2.0/KANNADA_TRANSLATION/ASTRA/T05/EN_FOR_KN_FDA.jsonl`, 100 items. In each, `text` is the question and `sol` the solution.

## Already fixed: reuse it, do not re-decide it
- the stem, closing and solution-lead vocabulary in `SAMARTHA_2.0/KANNADA_TRANSLATION/ASTRA/T01/TERM_CHOICES.tsv` (rows with id `ALL`);
- the fixed solution vocabulary in `ASTRA/T01/GLOSSARY_BRIEF.md`;
- the general administrative terms in `ASTRA/T01/POLITY_GLOSSARY.tsv`;
- the Test 2 current-affairs terms in `ASTRA/T03/CA_GLOSSARY.tsv`.
  - **CA agent:** this is your base. Copy every row your items use, unchanged.

Copy any of these that your items use without changing them, and mark the source `T1 glossary` or `T2 CA glossary`.

**Owner rule on labels:** the Exam Fact heading is **ಪರೀಕ್ಷಾ ಸಂಗತಿ** and the Result heading is **ತೀರ್ಮಾನ**. **Never use ಪರೀಕ್ಷಾ ಸತ್ಯ** anywhere.

## Where the Kannada comes from (in this order; lessons file §1)
1. **DSERT Social Science, Kannada medium, 2026-27.** This is the official Kannada of the very textbooks the English solutions cite ("DSERT Class 8 Social Science Part 2, 2026-27 …").
   - **Files:** Unicode text in `05_ANALYSIS/ASTRA_2026/T05_SOURCE_TRACE/source_text/DSERT_<class>_SS<part>_KN2627.txt`, with the matching English in `DSERT_<class>_SS<part>_EN2627.txt`.
   - **Method:** find the English passage, then read the Kannada book at the same chapter for the term.
   - **Text quality:** the text was converted from the Nudi font, so a few glyphs may be off. Prefer a form you see spelled the same way twice.
   - **Use it first** for dynasties, kings, titles, monuments, administrative terms (mandala, nadu), religious and literary terms.
2. **KEA and KPSC official Kannada papers,** which show how an exam setter words a term:
   - `05_ANALYSIS/KEA_CA_SOURCES_2026-11/population/OCT_STEMS.jsonl`;
   - `SAMARTHA_2.0/KANNADA_TRANSLATION/P1_CORPUS/PARALLEL_CORPUS.jsonl`.
3. **Kannada history reference books.** These are **LOCATOR-ONLY:** use them for language and spelling only, never for a fact, a date or a number. The OCR is one file per page (`pNNNN.txt`):
   - Kamath, *Karnatakada Sankshipta Itihasa*: `04_SOURCES/STUDY/REFERENCE_BOOKS/KANNADA_KAS_SET/01_Karnatakada_Sankshipta_Itihasa_Kamath.pdf.ocr/`;
   - Ashwathappa, *Madhyakaleena Bharatada Itihasa*: `…/02_Madhyakaleena_Bharatada_Itihasa_Ashwathappa.pdf.ocr/`;
   - Ashwathappa, *Bharatiya Kale mattu Samskruti*: `…/04_Bharatiya_Kale_mattu_Samskruti_Ashwathappa.pdf.ocr/`.
4. **CA only:** Karnataka Government Kannada, as in the Test 2 brief:
   - the Budget speeches `04_SOURCES/STUDY/ECONOMICS/KARNATAKA/*_KAN.pdf`;
   - the Kannada Economic Survey;
   - `SAMARTHA_2.0/KANNADA_TRANSLATION/ECONOMIC_SURVEY/GEMINI_QUALIFICATION/REFERENCE_LIST_FINAL.tsv`.
5. **Fallback:** if none of these has the term, use the plain, common Kannada word or the established form Karnataka school history uses. Put the English in brackets at first use where a candidate needs it.
   - Never coin a Sanskritised word where a common one exists.
   - **Persian, Arabic and Turkish names and titles** take the Kannada-script forms the DSERT Kannada book uses, for example Jagir, Mansab, Iqta and Sultan.

## Task
1. **List every recurring term** in your items' questions and solutions.
   - **HISTORY:** dynasties, rulers and their titles; places and capitals; monuments and temple parts; administrative units and offices; religious sects and texts; literary works and authors; battles; coins and taxes; art styles.
   - **CA:** ministries, departments, schemes, missions, awards, bodies, events, places and posts.
2. **Names:** give one Kannada-script form for each person, place, dynasty, work and scheme.
   - **Kannada works and authors:** use their established Kannada spelling. Examples: ಪಂಪ, ಆದಿಪುರಾಣ, ಕವಿರಾಜಮಾರ್ಗ, ಹಳೆಗನ್ನಡ.
   - **Karnataka places:** use the official Kannada spelling. Examples: ವಿಜಯಪುರ, ಬನವಾಸಿ, ಐಹೊಳೆ, ಹಳೇಬೀಡು.
3. **Expected size:** HISTORY roughly 400–700 terms; CA roughly 100–200.
4. **Mark the source of each term exactly**, using one of:
   - a DSERT file and the nearby English phrase (`DSERT_8_SS2_KN2627 "Rashtrakutas"`);
   - a KEA question id;
   - a book page (`KAMATH_KN p0123`);
   - a Budget speech page or reference-list row;
   - `T1 glossary` or `T2 CA glossary`;
   - `common`.

## Output
`SAMARTHA_2.0/KANNADA_TRANSLATION/ASTRA/T05/<HISTORY|CA>_GLOSSARY.tsv`, with the columns `english`, `kannada`, `source` and `note`.
- **One row per concept.** Write it in UTF-8 with the Write tool; never shell-echo Kannada.
- **Check the file:** every row must have four tab-separated fields.
  - Run Python with `python -I`.
  - Never print Kannada to the console, which is cp1252. Write it to a file and Read that file.
- **End with a short report:**
  - the count of terms;
  - the terms where sources disagree, and your choice;
  - the terms you could not source.

Do not commit. Edit no other file.
