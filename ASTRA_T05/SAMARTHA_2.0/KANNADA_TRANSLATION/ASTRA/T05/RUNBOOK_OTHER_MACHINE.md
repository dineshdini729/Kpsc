# RUNBOOK: finish the ASTRA Test 3 Kannada edition (FDA and SDA) on another machine, standalone

*Claude Code, 23-11-2026, §517.*

**Owner rulings of 23-11-2026 this runbook follows:**
- The other machine completes the edition **independently**, from this package alone. It needs no repository copy, no git, and no return to the main machine.
- The **Gemini verification is skipped**. The Kannada papers this run produces are the final deliverables.
- The machine runs a **different Claude account**.

## 0. What is already done, and what this run does
**Already done** (checked on the main machine, and again in a standalone copy of this package):
- **Translation:** all 200 items (FDA 100, SDA 100) are translated into Kannada.
- **Gate:** 0 issues.
- **Release check on the draft Word files:** 0 hard issues on both papers; the Kannada key letter equals the English letter 100/100 in both.
- **Shared glossary:** `KN_GLOSSARY_T3.tsv`, 2,655 terms.

**This run, in order:**
1. Verify the package.
2. **Back-check** all 10 batches. Each batch gets a NEW agent that did not translate it. This is the only meaning check left, since Gemini is skipped. Do not skip it.
3. Apply the corrections and the settled fixes.
4. Rebuild, and pass the gate and the release check.
5. Run the cross-paper term check.
6. Zip each paper as soon as it passes. **The zips are the final output.**

**Binding rules:**
- **Labels:** **ಪರೀಕ್ಷಾ ಸಂಗತಿ** (Exam Fact) and **ತೀರ್ಮಾನ** (Result). **Never ಪರೀಕ್ಷಾ ಸತ್ಯ.**
- **One shared glossary for both papers.** A new or changed term is settled once, for both papers.
- **The English is frozen:**
  - never change a key, an option order or a fact;
  - never rebuild the English Word files (run `build_t05_docx.py` only with `KN`).
- **Every judgement call:** `DECISIONS_FOR_CONTINUATION.md`. It is binding. Its section B gives the order of work.

## 1. Set up (once)
**Short way:** put the zip alone in an empty folder, open Claude Code there on Opus 5.5, and paste `00_main_session.txt` (sent alongside the zip). Claude extracts the zip and installs the libraries itself. The manual steps below are the fallback.

1. **Make a new, empty folder**, for example `C:\ASTRA_T05_KN\`. Unzip `ASTRA_T05_KANNADA_RESUME_PACKAGE.zip` into it.
   - The zip already contains the folder tree the scripts expect (`SAMARTHA_2.0\…`, `05_ANALYSIS\…`).
   - Nothing else is needed: no repository, no git.
2. **Install Python 3**, then the libraries:
   ```powershell
   pip install python-docx pymupdf
   ```
3. **Open Claude Code** (the desktop app's Code tab, or the CLI) with that folder as the working folder.
   - Choose **Claude Opus 5.5** in the model picker.
   - A plain claude.ai chat cannot do this; the work runs Python scripts and writes files.
4. **Paste the full text of `SAMARTHA_2.0\KANNADA_TRANSLATION\ASTRA\T05\PROMPTS\00_main_session.txt` as the first message.** That is all you paste. Claude reads every other file from the folder.

All paths below are relative to `SAMARTHA_2.0/KANNADA_TRANSLATION/ASTRA/T05/`, unless they start with `05_ANALYSIS` or `EXPORT_FOR_PROJECT`. **Run every command from the folder you unzipped into.**

**Working rules for every step:**
- Kannada is written only with the Write tool, in UTF-8.
- Never print Kannada to a Windows console (cp1252). Write it to a file and Read that file.
- Python runs as `python -I -X utf8`.
- **Each agent keeps its scratch files in its own subfolder.**

## 2. Verify
```
python -I -X utf8 SAMARTHA_2.0/KANNADA_TRANSLATION/ASTRA/T05/verify_package.py
```
- **It must print `PACKAGE OK`.**
- It checks every file against `PACKAGE_MANIFEST.sha256` and the Python libraries.
- It also re-runs the main machine's gate on the packaged translations, which must show `MISSING 0 other 0`.
- If it fails, re-unzip into an empty folder. Never edit files to make it pass.

Then create the two output folders the build needs:
```
python -I -c "import os; [os.makedirs(p, exist_ok=True) for p in ('05_ANALYSIS/ASTRA_2026/T05/out', 'EXPORT_FOR_PROJECT/ASTRA_T05')]"
```

## 3. Back-check every batch (10 NEW agents, in parallel)
There are 5 FDA batches (folder `kn_batches/`) and 5 SDA batches (`kn_batches_SDA/`), numbered 01–05:
- batch 01: Q1–20;
- batch 02: Q21–40;
- batch 03: Q41–58;
- batch 04: Q59–75;
- batch 05: Q76–100.

For each batch, start a new subagent (type general-purpose) with the text of `PROMPTS/02_backcheck.txt`. Fill in:
- `{PAPER}`: FDA or SDA;
- `{NN}`: 01–05;
- `{FOLDER}`: `kn_batches` or `kn_batches_SDA`.

Each agent writes `<folder>/CHECK_NN.tsv`.

## 4. Settle, apply, fix
1. **New terms.** Run `python -I -X utf8 SAMARTHA_2.0/KANNADA_TRANSLATION/ASTRA/T05/cross_paper_terms.py`. It gathers every translator's `NEW_TERMS_*.tsv` into `KN_NEW_TERMS_ALL.tsv`.
   - Settle each new-term CONFLICT, and each term the two papers wrote differently, by `DECISIONS_FOR_CONTINUATION.md` section C.
   - Record each settled term in `KN_GLOSSARY_T3_ADDITIONS.tsv`, then run `merge_glossary.py`.
2. **Dispose of the check rows** by section D:
   - every Queue A is applied or explicitly fixed;
   - Queue B is applied unless one of section D's skip reasons holds;
   - each skip goes in `KN_SKIP_ROWS.tsv` with its reason.
3. **The settled fixes** (section H), written as rows in `KN_MANUAL_FIXES.tsv` (`id \t field \t old \t new \t reason`; `field` is `kn_text` or `kn_sol`):
   - **Bijapur:** "Bijapur" alone is ಬಿಜಾಪುರ. Fix SDA Q13 and Q18, and any other batch that used ವಿಜಯಪುರ for "Bijapur".
   - **PIB:** expand PIB at the first citation in each SDA Q76–100 solution, as FDA does.
   - **Dam:** ಅಣೆಕಟ್ಟೆ everywhere.
   - **SDA Q77:** no ರಾಜ್ಯ added for Delhi.
   - **Partial names:** written in full, both papers alike.
   - **Settled terms from step 4.1:** any batch line that differs from the settled term.
4. **Apply:**
   ```
   python -I -X utf8 SAMARTHA_2.0/KANNADA_TRANSLATION/ASTRA/T05/apply_kn_checks.py kn_batches
   python -I -X utf8 SAMARTHA_2.0/KANNADA_TRANSLATION/ASTRA/T05/apply_kn_checks.py kn_batches_SDA
   ```
   - Read `KN_CHECK_APPLIED_<folder>.tsv`.
   - Re-express every `LINE_NOT_MATCHED`, `BOLD_COUNT_CHANGED` or `NOT_FOUND` row in `KN_MANUAL_FIXES.tsv`, then re-run.
   - Never hand-edit `OUT_NN.jsonl`. The script rebuilds it from `OUT_NN.v1.jsonl` on every run.

## 5. Build, gate, release check
```
python -I -X utf8 SAMARTHA_2.0/KANNADA_TRANSLATION/ASTRA/T05/build_kn_full.py
python -I 05_ANALYSIS/ASTRA_2026/T05/check_release_docx_t05.py
```
- **The gate (`KN_GATE1.tsv`) must show 0 issues.** Section E says how to fix each kind of issue.
- **The release check (`05_ANALYSIS/ASTRA_2026/T05/out/RELEASE_CHECK.tsv`):**
  - 0 hard issues on the FDA KN and SDA KN rows;
  - "KN letter == EN letter: 100/100" for both papers.
- **The Word files:** `ASTRA_T3_FDA_KN_Questions_and_Solutions.docx` and `ASTRA_T3_SDA_KN_Questions_and_Solutions.docx`, in this folder.

## 6. Cross-paper term check
Run `cross_paper_terms.py` again. Read every FLAG row (section G):
- fix real inconsistencies through `KN_MANUAL_FIXES.tsv`;
- re-run step 4.4 and step 5.

A FLAG that is only an inflection or a rephrase is a false alarm. List it in the final note.

## 7. Final deliverables (one zip per paper, each as soon as it is ready)
For each paper that has passed steps 5 and 6, write `EXPORT_FOR_PROJECT/ASTRA_T05/ASTRA_T3_<P>_KN_FINAL.zip` with:
- `ASTRA_T3_<P>_KN_Questions_and_Solutions.docx` (the paper);
- `05_ANALYSIS/ASTRA_2026/T05/T05_<P>_KN_QS.md` (the Kannada master);
- `KN_GATE1.tsv` and `05_ANALYSIS/ASTRA_2026/T05/out/RELEASE_CHECK.tsv`;
- the paper's `CHECK_NN.tsv` files, `KN_CHECK_APPLIED_<folder>.tsv`, `KN_MANUAL_FIXES.tsv` and `KN_SKIP_ROWS.tsv`;
- `KN_CROSS_PAPER_TERMS.tsv` and `KN_GLOSSARY_T3.tsv`;
- `FINAL_NOTE.md`.

**`FINAL_NOTE.md`** (in this folder) covers:
- the gate and release-check results;
- the Queue A and Queue B counts per batch;
- the rows skipped, and why;
- the terms settled;
- the cross-paper false alarms;
- anything left undone.

**Send the FDA zip as soon as FDA passes. Do not wait for SDA.**

**Done:** both zips exist, the gate is 0, the release check shows 0 hard issues and 100/100 letters for both papers, and every Queue A is closed.

## File map (`SAMARTHA_2.0/KANNADA_TRANSLATION/ASTRA/T05/`)
| File | What it is |
|---|---|
| `PROMPTS/00_main_session.txt` | the first message to Claude Code |
| `PROMPTS/02_backcheck.txt` | the back-check prompt (one per batch) |
| `PROMPTS/01_translate_rest.txt` | only if `remaining_items.py` ever shows a missing item |
| `DECISIONS_FOR_CONTINUATION.md` | every judgement call (binding) |
| `KN_EDITION_BRIEF.md`, `KN_BACKCHECK_BRIEF.md`, `GLOSSARY_BRIEF.md` | the standards |
| `EN_FOR_KN_FDA.jsonl`, `EN_FOR_KN_SDA.jsonl` | the frozen English |
| `KN_GLOSSARY_T3.tsv` (+ `_ADDITIONS`, `_CONFLICTS`, `merge_glossary.py`) | the one glossary |
| `kn_batches/`, `kn_batches_SDA/` | `IN_NN` (English), `OUT_NN` (Kannada), `NEW_TERMS_NN`, `CHECK_NN` (written in step 3) |
| `verify_package.py`, `PACKAGE_MANIFEST.sha256` | the integrity check |
| `apply_kn_checks.py`, `build_kn_full.py`, `cross_paper_terms.py`, `remaining_items.py` | the scripts |
