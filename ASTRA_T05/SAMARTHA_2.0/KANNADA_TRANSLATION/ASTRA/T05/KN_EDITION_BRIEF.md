# Brief: ASTRA Test 3 (internal T05) Kannada edition (FDA and SDA), batch NN

*Claude Code, 23-11-2026. Adapted from the Test 2 brief (`ASTRA/T03/KN_EDITION_BRIEF.md`); its method passed the T2 release checks.*

**Standing rules:**
- **Owner, 23-11-2026:** both English papers are shipped (FDA v5, SDA v3), and the Kannada FDA and SDA editions run in parallel by the Test 2 process (§514–§515).
- **One shared glossary for both papers (owner, 23-11-2026):** `KN_GLOSSARY_T3.tsv` in this folder is the ONLY term list. If a term you need is not in it, do not invent a form silently. Choose one by the glossary brief's source order, use it, and record it in your batch's `NEW_TERMS_NN.tsv` (see Output). Claude Code adds it to the shared file once, so both papers use the same form.
- **OR-C:** Claude is the sole author. A different agent back-checks each batch (lessons §5), and Gemini checks the assembled paper (R1).
- **Owner R12 (G-1):** never add a note about ambiguity. The Kannada says what the English says, no more.
- **Owner rule on labels:** the Exam Fact heading is **ಪರೀಕ್ಷಾ ಸಂಗತಿ** and the Result heading is **ತೀರ್ಮಾನ**. **Never write ಪರೀಕ್ಷಾ ಸತ್ಯ.**

## Input
Your batch folder is given in your task:
- FDA: `SAMARTHA_2.0/KANNADA_TRANSLATION/ASTRA/T05/kn_batches/`;
- SDA: `SAMARTHA_2.0/KANNADA_TRANSLATION/ASTRA/T05/kn_batches_SDA/`.

Your input is `<folder>/IN_NN.jsonl`, 17–25 items. Each item has:
- `id`, `paper` (FDA or SDA), `n` (the question number), `key` (a–d) and `part` (A or B);
- `text`: the English question;
- `sol`: the English solution, in markdown.

**The English is frozen and authoritative** (`05_ANALYSIS/ASTRA_2026/T05/ENGLISH_MASTER_FREEZE_<P>.md`). Translate it as it stands. If you think an English line is wrong, translate it faithfully anyway and report it at the end.
- **One exception, already in your input:** FDA Q100's Salient introduction reads "cited this reservation". That is the owner's change for the Kannada.

**What the paper covers:**
- Part A (`n` 1–75): Ancient and Medieval History, Indian and Karnataka.
- Part B (`n` 76–100): Current Affairs, September 2026.

## Read before writing (in this order)
1. **Glossary:** `KN_GLOSSARY_T3.tsv` in this folder, shared by both papers. **It is binding:** use its Kannada for every term it lists. Its `domain` column tells you whether a row is HISTORY, CA or FIXED.
2. **Fixed vocabulary:**
   - the `ALL` rows of `ASTRA/T01/TERM_CHOICES.tsv` (stem and closing forms);
   - the fixed solution vocabulary in `ASTRA/T01/GLOSSARY_BRIEF.md`.
3. **Lessons:** `SAMARTHA_2.0/KANNADA_TRANSLATION/KANNADA_TRANSLATION_LESSONS.md`, §2 and §4.
4. **For flow, Part A:** the DSERT Kannada-medium Social Science text on your batch's topics.
   - **Files:** `05_ANALYSIS/ASTRA_2026/T05_SOURCE_TRACE/source_text/DSERT_<class>_SS<part>_KN2627.txt`.
   - **Why:** these are the Kannada versions of the very books the solutions cite. Their sentences show how Karnataka school history is written in Kannada.
   - **Use them for language only,** never for a fact. The text was converted from the Nudi font, so a few glyphs may be off.
5. **For register:** about 20 KEA/KPSC bilingual questions, to see how stems, statements, closings and options read:
   - `05_ANALYSIS/KEA_CA_SOURCES_2026-11/population/OCT_STEMS.jsonl`;
   - `SAMARTHA_2.0/KANNADA_TRANSLATION/P1_CORPUS/PARALLEL_CORPUS.jsonl`.
6. **The T2 model:** `05_ANALYSIS/ASTRA_2026/T03/T03_FDA_KN_QS.md`. Read a Statement I/II item, a match item and two or three solutions to see the house style.

## The standard (all binding)
1. **Same meaning, same truth value (OR-AJ).** Add, drop, strengthen, weaken or invent nothing.
   - **Keep every negation and qualifier:** "only", "not", "except", "at least", "more than", "first", "most", "about", "was to", "set to", "traditionally", "is said to".
   - **Keep tense and modality.** "Was to take effect" never becomes "took effect".
   - **Keep every name, number, date, century, era (BCE/CE), unit and relation.**
   - **The key and the option order never change.** Exactly one option stays correct in the Kannada.
2. **Natural Kannada.** The owner's words: "don't make the translation sound artificial, soulless & AI-like please".
   - Write as a Kannada-medium history teacher or KEA setter would: verb last, Kannada idiom, short sentences.
   - Avoid stiff calques.
   - The Kannada must read on its own, without the English beside it.
3. **Question text, translated into `kn_text`:**
   - **Lines:** keep exactly the same lines as `text`: the same number of lines, the same blank lines, and the same markdown table shape (`| … | … |` rows, with the `|---|---|` separator kept).
   - **Labels:** the English is in the final release labels. Keep them exactly as they are and where they are:
     - options `a)`–`d)` at the line start;
     - statements `1.` `2.` `3.` `4.`;
     - table row labels such as `A.` and `I.`;
     - Statement I / II.
   - **Statement I/II items:**
     - lead and statement labels: "ಈ ಕೆಳಗಿನ ಹೇಳಿಕೆಗಳನ್ನು ಪರಿಗಣಿಸಿ:", "ಹೇಳಿಕೆ I:", "ಹೇಳಿಕೆ II:";
     - operative line: "ಮೇಲಿನ ಹೇಳಿಕೆಗಳಿಗೆ ಸಂಬಂಧಿಸಿದಂತೆ ಕೆಳಗಿನವುಗಳಲ್ಲಿ ಯಾವುದು ಸರಿ?";
     - the four options, exactly as in T1 FDA Q6:
       - a) ಹೇಳಿಕೆ I ಮತ್ತು ಹೇಳಿಕೆ II ಎರಡೂ ಸರಿ ಮತ್ತು ಹೇಳಿಕೆ II, ಹೇಳಿಕೆ Iಕ್ಕೆ ಸರಿಯಾದ ವಿವರಣೆಯಾಗಿದೆ
       - b) ಹೇಳಿಕೆ I ಮತ್ತು ಹೇಳಿಕೆ II ಎರಡೂ ಸರಿ, ಆದರೆ ಹೇಳಿಕೆ II, ಹೇಳಿಕೆ Iಕ್ಕೆ ಸರಿಯಾದ ವಿವರಣೆಯಲ್ಲ
       - c) ಹೇಳಿಕೆ I ಸರಿ, ಆದರೆ ಹೇಳಿಕೆ II ತಪ್ಪು
       - d) ಹೇಳಿಕೆ I ತಪ್ಪು, ಆದರೆ ಹೇಳಿಕೆ II ಸರಿ
   - **Codes:**
     - "1 and 3 only" → "1 ಮತ್ತು 3 ಮಾತ್ರ";
     - "1, 2 and 4" → "1, 2 ಮತ್ತು 4";
     - "1, 2, 3 and 4" → "1, 2, 3 ಮತ್ತು 4";
     - order codes such as "3-4-1-2" and match codes such as "A-III, B-I, C-IV, D-II" are copied exactly.
   - **Match items:** "Match List I with List II" uses "ಪಟ್ಟಿ-I ಅನ್ನು ಪಟ್ಟಿ-II ರೊಂದಿಗೆ ಹೊಂದಿಸಿ:". Table headers translate the List I and List II captions.
   - **Stems and closings:** use KEA's Kannada forms (the `ALL` rows of `TERM_CHOICES.tsv`). For example:
     - "ಮೇಲಿನ ಹೇಳಿಕೆಗಳಲ್ಲಿ ಯಾವುವು ಸರಿಯಾಗಿವೆ?";
     - "ಕೆಳಗೆ ನೀಡಿರುವ ಆಯ್ಕೆಗಳಿಂದ ಸರಿಯಾದ ಉತ್ತರವನ್ನು ಆಯ್ಕೆಮಾಡಿ:";
     - "ಕೆಳಗೆ ನೀಡಿರುವ ಸಂಕೇತಗಳನ್ನು ಬಳಸಿ ಸರಿಯಾದ ಉತ್ತರವನ್ನು ಆಯ್ಕೆಮಾಡಿ:" for "Select the correct answer using the code given below:".
     - **The polarity must match:** "correct" vs "NOT correct"; "correctly matched" vs "INCORRECTLY matched".
     - **Capitals:** keep the English's capitals as bold, or as the Kannada emphasis T1 and T2 used.
   - **No answer leaks:** case endings, agreement, or one option translated more smoothly than the others must not point to the answer. Keep option lengths balanced.
   - **Chronology items:** the Kannada must not make the order easier or harder; dates and centuries stay as given.
4. **Solution, translated into `kn_sol` for every item:**
   - **Lines:** one Kannada line per English line, with the same blank lines, the `- ` bullets kept, and tables in the same shape.
   - **Fixed leads:**
     - `**ಸರಿಯಾದ ಆಯ್ಕೆ: (c)**` and `**ಸಮರ್ಥನೆ:**`;
     - `**ಹೇಳಿಕೆ 1: ಸರಿ.**` and `**ಆಯ್ಕೆ (a): ತಪ್ಪು.**`;
     - `**ಜೋಡಿ 1: ಸರಿಯಾಗಿ ಹೊಂದಿದೆ.**`;
     - `ಆದ್ದರಿಂದ ಸರಿಯಾದ ಉತ್ತರ **ಆಯ್ಕೆ (c)**.`, keeping the bold exactly where the English has it;
     - `**ತೀರ್ಮಾನ:**`;
     - `**ಪ್ರಮುಖ ಅಂಶಗಳು: <Kannada title>**`;
     - `**ಪರೀಕ್ಷಾ ಸಂಗತಿ:**`.
   - **Bold:** every `**…**` span in the English becomes a `**…**` span around the equivalent Kannada phrase. **Keep the same number of `**` markers**, with no bold nested inside bold.
   - **Italics:** keep every `*…*` italic span (titles of works, if the English italicises them) with the same count.
   - **Copy exactly:** numbers, years, centuries ("5th century CE" → "ಕ್ರಿ.ಶ. 5ನೇ ಶತಮಾನ"), page numbers and Article numbers.
     - Use ಕ್ರಿ.ಪೂ. for BCE and ಕ್ರಿ.ಶ. for CE, as DSERT Kannada does.
     - The digit runs must survive.
   - **Names:**
     - persons, places, dynasties and works take the glossary's Kannada-script form;
     - schemes and bodies take the glossary name, with the English in brackets at first mention in each solution where a candidate needs it.
   - **Source citations:** translate the ordinary words and keep the rest:
     - "(DSERT Class 8 Social Science Part 2, 2026-27, Ch 20, PDF p. 35)" → "(DSERT 8ನೇ ತರಗತಿ ಸಮಾಜ ವಿಜ್ಞಾನ ಭಾಗ 2, 2026-27, ಅಧ್ಯಾಯ 20, PDF ಪು. 35)";
     - "(II PUC History, Ch 4, PDF p. 78)" → "(ದ್ವಿತೀಯ ಪಿಯುಸಿ ಇತಿಹಾಸ, ಅಧ್ಯಾಯ 4, PDF ಪು. 78)";
     - "(Kamath, A Concise History of Karnataka, p. 28)" → "(ಕಾಮತ್, A Concise History of Karnataka, ಪು. 28)";
     - "(NCERT Class 7 Exploring Society Part 1, Ch 4, PDF p. 6)" → "(NCERT 7ನೇ ತರಗತಿ Exploring Society ಭಾಗ 1, ಅಧ್ಯಾಯ 4, PDF ಪು. 6)";
     - "(PIB, 12 Sep 2026)" → "(PIB, 12 ಸೆಪ್ಟೆಂಬರ್ 2026)";
     - "(March of Karnataka, Nov 2026, p. 7)" → "(ಮಾರ್ಚ್ ಆಫ್ ಕರ್ನಾಟಕ, ನವೆಂಬರ್ 2026, ಪು. 7)";
     - English book titles, and the names Satish Chandra and R.S. Sharma, may stay in Latin letters, as T2 kept titles.
5. **Numbers:** keep the English's numerals, ₹, crore (ಕೋಟಿ), lakh (ಲಕ್ಷ) and per cent ("ಶೇ. 7.5" or "7.5%", as the English has it). Write dates as KEA writes them ("10 ಸೆಪ್ಟೆಂಬರ್ 2026").
6. **Student-facing only:** no translator notes inside `kn_text` or `kn_sol`.

## Output
1. **Write the parts.** Write the batch in parts with the Write tool (UTF-8), five items per part: `<folder>/OUT_NN_p1.jsonl` …
   - Each item is one JSON line: `{"id": …, "paper": …, "n": …, "key": …, "kn_text": "…", "kn_sol": "…"}`.
   - Never shell-echo Kannada.
2. **Merge and validate.** Merge the parts with a short Python script (run with `python -I -X utf8`) into `<folder>/OUT_NN.jsonl`, in input order. Fix until every check passes:
   - every line is valid JSON, and the ids and order match the input;
   - `kn_text` has the same number of lines as `text`, and `kn_sol` the same number as `sol`;
   - `kn_sol` contains `ಸರಿಯಾದ ಆಯ್ಕೆ: (<key>)` and `ಆದ್ದರಿಂದ ಸರಿಯಾದ ಉತ್ತರ` followed by `ಆಯ್ಕೆ (<key>)`;
   - `kn_sol` contains `ಸಮರ್ಥನೆ:`, `ತೀರ್ಮಾನ:`, `ಪ್ರಮುಖ ಅಂಶಗಳು:` and `ಪರೀಕ್ಷಾ ಸಂಗತಿ:`, and **does not contain ಪರೀಕ್ಷಾ ಸತ್ಯ**;
   - the count of `**` in `kn_sol` equals the count in `sol`, and the count of single `*` (italics) equals the English's;
   - every number (digit run) in `sol` occurs in `kn_sol`, and every number in `text` occurs in `kn_text`;
   - every label at a line start in `text` (`a)`–`d)`, `1.`–`4.`, `|`) occurs at the same line start in `kn_text`.
3. **New terms:** write `<folder>/NEW_TERMS_NN.tsv` with the header `english	kannada	source	note`. List every term you used that is not in `KN_GLOSSARY_T3.tsv`, with the Kannada you used. If there are none, write the header only.
4. **Report at the end:**
   - the items you found hard;
   - any English line you think is wrong or ambiguous (do not resolve it by changing the meaning);
   - any term not in the glossaries that you had to choose, with its source;
   - the validation result.

**Working rules:**
- On this Windows machine the console is cp1252, so never print Kannada to the console. Write it to a UTF-8 file and Read it.
- Do not commit.
- Edit no file other than your own `OUT_NN*` and `NEW_TERMS_NN.tsv` files. Never edit `KN_GLOSSARY_T3.tsv`.
