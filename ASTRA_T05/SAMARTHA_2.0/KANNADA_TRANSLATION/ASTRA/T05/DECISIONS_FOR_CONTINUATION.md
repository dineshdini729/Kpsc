# Decisions for the continuation: how Claude Code on the main machine would decide (§516–§517)

**Owner rulings, 23-11-2026 (§517):**
- The other machine completes the edition independently, from the package alone, with no return to the main machine.
- The Gemini verification is skipped.
- Where a step below says "return", "branch", "dock" or "Gemini", it is superseded by `RUNBOOK_OTHER_MACHINE.md` §7: the final zips are the deliverable.
- The internal back-check (step 6) stays. It is now the only meaning check.

*Read with `RUNBOOK_OTHER_MACHINE.md`. The owner wants the other machine to produce the output this machine would have produced. The briefs, the glossary and the scripts already fix most of it. This file fixes the remaining judgement calls the orchestrator makes, so they are made the same way.*

## A. What "the same output" means here, honestly
- **Fixed, and identical on any machine:**
  - the English inputs;
  - the one glossary;
  - the briefs, prompts and scripts;
  - the gate, the order of steps, and every decision below.
- **Not fixed byte for byte:** the exact Kannada wording an agent writes. A language model does not repeat its words exactly, even on this machine. The standard it must meet is fixed, and the gate and back-check enforce it:
  - same meaning;
  - glossary terms;
  - line, bold and number parity;
  - natural Kannada.
- **Use the same model:** Claude Opus 5.5 (`claude-opus-5-5`) as the main session, with the default subagent type `general-purpose`.
  - Check this with `/model`, or the app's model picker, before starting.
  - A weaker model gives weaker Kannada. That is the one variable that changes the output most.

## B. Order of work (do not reorder)
1. Run `verify_package.py`. It must say `PACKAGE OK`.
2. Run `remaining_items.py`.
3. Translate the remaining items. Use one agent per batch with a `IN_NN_REST.jsonl` file, all in parallel, with the exact prompt in `PROMPTS/01_translate_rest.txt`.
4. Run `remaining_items.py` again. Repeat steps 3–4 until both papers are 100/100.
5. Adopt new terms (section C), then run `merge_glossary.py`.
6. Back-check all 10 batches, each by a NEW agent (never the translator), with `PROMPTS/02_backcheck.txt`.
7. Dispose of the check rows (section D). Then run `apply_kn_checks.py kn_batches` and `apply_kn_checks.py kn_batches_SDA`.
8. Run `build_kn_full.py` and get the gate to 0 issues (section E).
9. Run the release check (section F). Zip FDA and send it. Zip SDA and send it. Whichever passes first goes first.
10. Run `cross_paper_terms.py` and settle every FLAG and CONFLICT (section G). If anything changes, rebuild and re-zip as v2.
11. Write the return note and push the branch (runbook §7).

## C. Adopting new terms (`NEW_TERMS_*.tsv` → `KN_GLOSSARY_T3_ADDITIONS.tsv`)
- **One form per English term for both papers,** chosen in this order:
  1. a form already in `KN_GLOSSARY_T3.tsv` for the same concept (re-use it; do not add a second form);
  2. DSERT Kannada (`05_ANALYSIS/ASTRA_2026/T05_SOURCE_TRACE/source_text/DSERT_*_KN2627.txt`);
  3. KEA/KPSC (`OCT_STEMS.jsonl`, `PARALLEL_CORPUS.jsonl`);
  4. the Kannada Economic Survey and Budget;
  5. the Kannada reference books (spelling only);
  6. the form that the most batches already used.
- **Ties:** a tie goes to the HISTORY form for history terms, then to the FDA form.
- **The row:** `english \t kannada \t Claude Code adopted (§517): <source and why> \t <note> \t <HISTORY|CA|FIXED> \t FDA+SDA`.
- **Then fix the text:** every batch line that used a different form gets a row in `KN_MANUAL_FIXES.tsv`: `id \t field \t old \t new \t reason`. `old` is the exact substring in the line, long enough to be unique in that field.
- **Already adopted at §516; apply them in the text too:**
  - **dam = ಅಣೆಕಟ್ಟೆ** everywhere. The coin "dam" stays ದಾಮ್. Any ಅಣೆಕಟ್ಟು in a batch is changed.
  - **SDA Q77, "biggest beneficiary":** no ರಾಜ್ಯ ("State"). Delhi is named as ದೆಹಲಿ alone, with no added noun. Fix any line that adds ರಾಜ್ಯ.
  - **tribute in the sense of homage = ಶ್ರದ್ಧಾಂಜಲಿ.** Tribute paid to a king = ಕಪ್ಪ.

## D. Disposing of back-check rows (as T1 and T2 did)
- **Queue A:** apply it, every time.
  - If the suggested line is itself wrong, write a correct line in `KN_MANUAL_FIXES.tsv` instead. Never leave a Queue A open.
- **Queue B:** apply it by default. Skip it (`KN_SKIP_ROWS.tsv`, with a reason) only when:
  - it adds or drops meaning against the English;
  - it changes a glossary term to a non-glossary form;
  - it breaks a label, bold or number;
  - or it re-opens a decision recorded here or in `KN_GLOSSARY_T3_ADDITIONS.tsv`.
- **A row that fails to apply:**
  - `LINE_NOT_MATCHED`: the line changed. Re-read it and re-express the fix in `KN_MANUAL_FIXES.tsv`.
  - `BOLD_COUNT_CHANGED`: the suggestion broke the `**` count. Re-express it in `KN_MANUAL_FIXES.tsv` with the original bold kept.
- **Never** hand-edit `OUT_NN.jsonl`. `apply_kn_checks.py` keeps the translator's text in `OUT_NN.v1.jsonl` and rewrites `OUT_NN.jsonl` from it on every run.

## E. Getting the gate to 0 (`KN_GATE1.tsv`)
| Issue | Fix |
|---|---|
| `KEY_LINE` / `HENCE` | The key letter in the Kannada differs from the English key. Fix the line; never the key. |
| `HEADING` / `BANNED_LABEL` | Use exactly ಸಮರ್ಥನೆ:, ತೀರ್ಮಾನ:, ಪ್ರಮುಖ ಅಂಶಗಳು:, ಪರೀಕ್ಷಾ ಸಂಗತಿ:. Remove any ಪರೀಕ್ಷಾ ಸತ್ಯ. |
| `SOL_LINES` / `Q_LINES` | Split or join lines to match the English line for line. A blank line counts. |
| `BOLD_COUNT` / `ITALIC_COUNT` | Restore the missing `**` or `*` around the equivalent Kannada phrase. |
| `SOL_NUMBERS` / `Q_NUMBERS` | Restore the digit run exactly. Keep Western digits; never use Kannada numerals. |
| `Q_LABEL` | The line must start with `a) ` … `d) `, `1. ` … `4. `, `|`, or `ಹೇಳಿಕೆ I:` / `ಹೇಳಿಕೆ II:`. |
| `STRAY_CHAR` | Replace the character with a Kannada or ASCII equivalent, unless the English itself has it. |
| `PROCESS_NOTE` | Remove the internal note. |

All of these fixes go through `KN_MANUAL_FIXES.tsv`. Then run `apply_kn_checks.py` (both folders) and `build_kn_full.py`.

## F. Release check (`05_ANALYSIS/ASTRA_2026/T05/check_release_docx_t05.py`)
- **What it must show:** 0 hard issues on the KN rows, and the KN key letter equal to the EN letter in 100/100 for each paper.
- **The EN rows:** they must stay exactly as shipped. Never rebuild the English Word files; run `build_t05_docx.py` only with `KN`.

## G. Cross-paper check (`cross_paper_terms.py`)
- **FLAG** (one paper always uses the glossary form, the other misses it at least once): read the missing items.
  - If the paper used another form for the same concept, it is an inconsistency. Fix it to the glossary form through `KN_MANUAL_FIXES.tsv`.
  - If the paper used an inflected form, a pronoun, or a rephrase the English allows, it is a false alarm. Note it in the return note.
- **BOTH_MISS:** the same reading, for both papers.
- **New-term CONFLICT:** settle it by section C, then fix the text.

## H. Translation choices already made (keep them)
- **PIB citations (settled §516, T2 parity):** the first PIB citation in each solution is "(PIB (ಪತ್ರಿಕಾ ಮಾಹಿತಿ ಕಚೇರಿ), 12 ಸೆಪ್ಟೆಂಬರ್ 2026)". Later citations in the same solution are "(PIB, 12 ಸೆಪ್ಟೆಂಬರ್ 2026)".
  - FDA batch 05 already does this. **SDA batch 05 does not:** add the expansion at the first PIB citation of each SDA Q76–100 solution, through `KN_MANUAL_FIXES.tsv`.
  - The cross-paper check must then show PIB consistent.
  - A zero-padded day ("07") stays as written.
- **"Choose the correct answer from the options given below"** is "ಕೆಳಗೆ ನೀಡಿರುವ ಆಯ್ಕೆಗಳಿಂದ ಸರಿಯಾದ ಉತ್ತರವನ್ನು ಆಯ್ಕೆಮಾಡಿ:". `build_kn_full.py` enforces it from the English line. The glossary's CA match row that gives the "code" wording is wrong for this line; ignore it.
- **Statement I/II labels:** always ಹೇಳಿಕೆ I / ಹೇಳಿಕೆ II, with no hyphen. The gate checks this.
- **Abbreviations:** inside options that test them (SDA Q91: IRDAI, SEBI, PFRDA, NABARD), keep them bare. Expand them only in the solution.
- **Match tables:** do not add a bracketed English gloss inside List I/II cells unless the English has it there.
- **"one million" (passengers):** ಹತ್ತು ಲಕ್ಷ.
- **Feminine forms** where the person is a woman (ಹಣಕಾಸು ಸಚಿವೆ).
- **Leave open what the English leaves open,** for example SDA Q96 "nine announced at the event". Never resolve an English ambiguity in the Kannada (owner R12).
- **Partial-name glossary rows:** some rows give only part of a name, for example ಲೋದಿ, ನಾದಿರ್, ಪ್ರತಾಪ, ದರ್ವಾಜ, ಮಾರ್ತಾಂಡ, ಚೆಲುವನಾರಾಯಣ, ದಶಕುಮಾರ and ಅಕ್ಬರಿ.
  - Write the full name the English gives around that core: ಇಬ್ರಾಹಿಂ ಲೋದಿ, ನಾದಿರ್ ಷಾ, ಐನ್-ಇ-ಅಕ್ಬರಿ.
  - If another glossary row has the full name, use that row.
  - Treat each such expansion as a new term (section C), so both papers end up with the same full form.
- **Spelling variants inside the English** (Haldighati / Haldighat; Solah Khamba / Solahkhamb; Mrichakatika / Mricchakatika; Kavichakravarti / Kavichakravarthi; Hegde / Heggade): use one Kannada form per name, the glossary's.
- **"All four"** in how-many options is ನಾಲ್ಕೂ. ಎಲ್ಲವೂ is for "All of the above".
- **"NOT correct"** in a stem is `**ಸರಿಯಲ್ಲ**`, as in T2.
- **Bijapur (settled §516):** "Bijapur" alone is ಬಿಜಾಪುರ, and "Bijapuri" is ಬಿಜಾಪುರದ. "Vijayapura" is ವಿಜಯಪುರ, and "Vijayapura (Bijapur)" is ವಿಜಯಪುರ (ಬಿಜಾಪುರ).
  - SDA batch 01 (Q13, Q18) used ವಿಜಯಪುರ for "Bijapur". Fix it through `KN_MANUAL_FIXES.tsv`, and check every batch for the same.
- **Same name, two English spellings in one item** (Jinji/Gingee in SDA Q13, Dara Shukoh/Shikoh, Jamia/Jami Masjid): use one glossary form. If that makes a distractor visibly repeat the stem, keep it and note it in the return note. Do not invent a second spelling.
- **FDA Q100:** the Salient introduction says "cited this reservation" (already in the input). Translate it as the input has it.

## I. If something is not covered here
Choose what keeps the Kannada closest to the English's meaning and to the T2 edition's house style (`05_ANALYSIS/ASTRA_2026/T03/T03_FDA_KN_QS.md`). Record the choice in the return note, so the main machine can confirm it or change it.
