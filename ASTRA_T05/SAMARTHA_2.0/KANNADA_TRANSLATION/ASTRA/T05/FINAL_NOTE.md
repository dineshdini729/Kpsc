# ASTRA Test 3 (internal T05), Kannada edition (FDA and SDA): final note

*Claude Code, 23-11-2026, standalone run on the second machine (owner rulings of 23-11-2026: no Gemini step, nothing returns to the main machine; the two zips are the final deliverables).*

## 1. Results
| Check | FDA KN | SDA KN |
|---|---|---|
| `verify_package.py` (before any work) | PACKAGE OK (117 files; self-test gate MISSING 0 other 0) | same |
| Gate (`KN_GATE1.tsv`) | **0 issues** | **0 issues** |
| Release check: hard issues | **0** | **0** |
| Release check: KN letter == EN letter | **100/100** | **100/100** |
| Key spread (KN = EN) | a 22, b 27, c 23, d 28 | a 25, b 26, c 27, d 22 |

- **English untouched:** both English Word files still match `PACKAGE_MANIFEST.sha256`. `build_t05_docx.py` ran only through `build_kn_full.py` (KN). No key, option order or fact was changed.
- **Labels:** ಪರೀಕ್ಷಾ ಸಂಗತಿ and ತೀರ್ಮಾನ throughout. ಪರೀಕ್ಷಾ ಸತ್ಯ occurs nowhere; the gate and all ten checkers confirm this.

## 2. Back-check (10 new agents, one per batch; none had translated its batch)
| Paper | Batch | Questions | Queue A | Queue B | Clean items |
|---|---|---|---|---|---|
| FDA | 01 | Q1–20 | 0 | 7 | 13 |
| FDA | 02 | Q21–40 | 0 | 12 | 13 |
| FDA | 03 | Q41–58 | 0 | 13 | 11 |
| FDA | 04 | Q59–75 | 0 | 23 | 5 |
| FDA | 05 | Q76–100 | 0 | 1 | 24 |
| SDA | 01 | Q1–20 | 0 | 23 | 9 |
| SDA | 02 | Q21–40 | 0 | 5 | 17 |
| SDA | 03 | Q41–58 | 1 | 9 | 9 |
| SDA | 04 | Q59–75 | 0 | 9 | 10 |
| SDA | 05 | Q76–100 | 2 | 4 | 20 |
| **Total** | | | **3** | **106** | **131** |

**Every Queue A is closed (applied):**
- **SDA MP10-Q061, S7:** the Kannada read "Salim Chishti's direct descendant", which reverses the English. It now reads that Salim Chishti was Baba Farid's direct descendant.
- **SDA T05-CA-SDA-S13 (Q77), Q3 and S5:** an added ರಾಜ್ಯ ("State") made Statement 2 defensible. It was removed, as section C (§516) requires: Delhi is named alone, with no added noun.

**Queue B:** 101 of the 106 rows were applied (FDA 51, SDA 50). All applied without `LINE_NOT_MATCHED`, `BOLD_COUNT_CHANGED` or `NO_TARGET`.

## 3. Rows skipped (`KN_SKIP_ROWS.tsv`, all FDA batch 04)
| Item | Line | Reason |
|---|---|---|
| MP02-Q083 | Q1 | The row proposes no change. The checker notes that the glossary row "forced (unpaid) labour" = ಬಿಟ್ಟಿ ದುಡಿಮೆ must not be used here: ಬಿಟ್ಟಿ derives from ವಿಷ್ಟಿ, the key, so it would leak the answer. The stem keeps ಬಲವಂತದ (ಸಂಬಳರಹಿತ) ದುಡಿಮೆ. |
| MP05-Q078 | Q1 | Re-opens a recorded decision. `build_kn_full.py` (HARM) sets the house stem "ಪಟ್ಟಿ-I ಅನ್ನು ಪಟ್ಟಿ-II ರೊಂದಿಗೆ ಹೊಂದಿಸಿ:", which the line already has. |
| T05-AM-FDA-G16 | S5, S10 | Would change the glossary form ಬಹಾರ್‌ಖಾನ್ to a spaced form. Fixed the other way instead: option (b) now uses the glossary form (`KN_MANUAL_FIXES.tsv`). |
| MP03-Q022 | Q7 | Would replace a glossary form, ವರಾಹ (ದೈವಿಕ ವರಾಹ), with the non-glossary ದೈವಿಕ ಹಂದಿ. Kept. **Open for the glossary owner:** the gloss repeats its headword. |

## 4. Terms settled (`KN_GLOSSARY_T3_ADDITIONS.tsv`, rows marked "§517"; glossary re-merged to 2,658 terms)
**The four new-term CONFLICTs (section C):**
- **audience hall = ಸಭಾಮಂಟಪ.** There is no glossary row for the concept. The vote was tied (FDA b03 / SDA b01, both HISTORY), so the FDA form wins. SDA MP09-Q028 Q2 and S4 were fixed.
- **Firuz Shah Tughlaq = ಫಿರೋಜ್‌ಷಾ ತುಘಲಕ್.** This re-uses the glossary's DSERT Tughlaq row. FDA G24 was fixed by back-check rows.
- **Lord of the Peninsula = ಪರ್ಯಾಯ ದ್ವೀಪದ ಒಡೆಯ.** The spaced form appears in the most batches. SDA MP01-Q045 S7 was fixed.
- **pillar brackets = ಕಂಬಗಳ ಆಧಾರಪಟ್ಟಿಗಳು.** This re-uses the glossary row "bracket figure". FDA G05 S17 was fixed.

**Partial-name rows expanded to the full name (section H), one form for both papers:**
- **The rows:** ಅಭಿಧಮ್ಮ ಪಿಟಕ, ಅಲಾಯಿ ದರ್ವಾಜ, ಬುಲಂದ್ ದರ್ವಾಜ, ಅಮೀರ್ ಖುಸ್ರು, ಬಾಂಗ್ಲಾದೇಶ, ಚಿಕ್ಕದೇವರಾಜ ಒಡೆಯರ್, ದಾದಾಜಿ ಕೊಂಡದೇವ, ಫತೇಪುರ್ ಸಿಕ್ರಿ, ಗದಾಧರ ಸಿಂಹ, ಘಿಯಾಸುದ್ದೀನ್ ತುಘಲಕ್, ಇಬಾದತ್ ಖಾನಾ, ಇಬ್ರಾಹಿಂ ಲೋದಿ, ಇಂಡೋ-ಸಾರ್ಸೆನಿಕ್, ಜಲಾಲುದ್ದೀನ್ ಖಿಲ್ಜಿ, ಜೇಡರ ದಾಸಿಮಯ್ಯ, ಕದ್ರಿ ಮಂಜುನಾಥ ದೇವಾಲಯ, ಲಚಿತ್ ಬೊರ್ಫುಕನ್, ಲಕ್ಕಣ್ಣ ದಂಡೇಶ, ಮಾರ್ತಾಂಡ ಸೂರ್ಯ ದೇವಾಲಯ, ಹಣಕಾಸು ಮಂತ್ರಿ (a woman minister stays ಹಣಕಾಸು ಸಚಿವೆ), ಮಿತ್ರವಿಂದಾ ಗೋವಿಂದ, ಮಹಮ್ಮದ್ ಬಿನ್ ಕಾಸಿಂ, ಮಹಮ್ಮದ್ ಬಿನ್ ತುಘಲಕ್, ಮುಲ್ಕ್-ಎ-ಮೈದಾನ್, ನಾದಿರ್ ಷಾ, ಆರ್.ಡಿ. ಬ್ಯಾನರ್ಜಿ, ಸಂಚಿ ಹೊನ್ನಮ್ಮ, ಸಿದ್ದರಾಮಪುರಾಣ (joined, as the §516 ಬಸವಪುರಾಣ), ತ್ರಿಭುವನ ತಿಲಕ ಚೂಡಾಮಣಿ, ವೈಕುಂಠ ಪೆರುಮಾಳ್ ದೇವಾಲಯ.
- **Dara Shikoh = ದಾರಾ ಶುಕೋ.** This re-uses the glossary's DSERT "Dara Shukoh" row (section C, rule 1), so both English spellings take one form. SDA G20 was fixed by back-check rows.
- **One spelling of "darwaza":** ದರ್ವಾಜ, the glossary spelling.

**Other rows settled:**
- **railing (stupa) = ಕಟಕಟೆ.** One form, not a slash pair; ವೇದಿಕೆ is kept for "platform".
- **Jami Masjid, Bijapur = ಬಿಜಾಪುರದ ಜಾಮಿ ಮಸೀದಿ** and **Vijayapura (Bijapur) = ವಿಜಯಪುರ (ಬಿಜಾಪುರ).** These bring two DSERT rows into line with H (Bijapur, §516).
- **Ekta Nagar, Kevadia, Gujarat = ಗುಜರಾತ್‌ನ ಕೆವಡಿಯಾದ ಏಕತಾ ನಗರ.** One spelling of Kevadia (FDA form), so SDA Q80 was fixed.

**Glossary forms kept, with no new row:**
- tributary king = ಸಾಮಂತ ರಾಜ (FDA G31 fixed to it);
- pen name (ankita) = ಅಂಕಿತ;
- war booty / judicial fines;
- gopuram / gateway tower = ಗೋಪುರ.

**Translators' NEW_TERMS left as is:** the other ~390 single-form NEW_TERMS entries each occur in one form only. They stay in `KN_NEW_TERMS_ALL.tsv` and were not added to the glossary.

## 5. Settled fixes applied (`KN_MANUAL_FIXES.tsv`, 39 rows, all APPLIED)
- **Bijapur (H):** no line now writes ವಿಜಯಪುರ for an English "Bijapur". The fixes came through back-check rows in FDA b01–b03 and SDA b01, b03 and b04, including SDA Q13 and Q18. A scan of both papers finds no remaining case.
- **PIB (H):** the expansion "(PIB (ಪತ್ರಿಕಾ ಮಾಹಿತಿ ಕಚೇರಿ), …)" was added at the first citation of all 23 SDA Q76–100 solutions that cite PIB. Both papers now expand it exactly once per solution, at the first citation; FDA has 20 such solutions, and 5 cite no PIB.
- **Dam = ಅಣೆಕಟ್ಟೆ:** no ಅಣೆಕಟ್ಟು is left. SDA G01 and G46 were fixed by back-check rows.
- **SDA Q77:** no ರಾಜ್ಯ for Delhi (Queue A, above).
- **Partial names and settled terms:** see §4. Also fixed: Basavapurana joined as ಬಸವಪುರಾಣ (SDA MP05-Q056, G34), ಬುಲಂದ್ ದರ್ವಾಜ (SDA G21), and option (b) ಬಹಾರ್‌ಖಾನ್ (FDA G16).
- **Cross-paper fixes (§6):**
  - ಜೀವನ ಚರಿತ್ರೆ (FDA MP01-Q041);
  - ಮಧ್ಯಶಿಲಾಯುಗ (FDA G02);
  - ನವ ಶಿಲಾಯುಗ (SDA G04);
  - the FIXED line "ಈ ಹೇಳಿಕೆ ತಪ್ಪು, ಆದ್ದರಿಂದ ಇದೇ ಉತ್ತರ." (FDA G31).

## 6. Cross-paper term check (`KN_CROSS_PAPER_TERMS.tsv`): 535 terms; OK 462, FLAG 23, BOTH_MISS 50
I read every FLAG against the item text. Four were real inconsistencies and are fixed (§5). The remaining 23 are false alarms:
- **The English term in another sense:**
  - army: ಭೂಸೇನೆ for "Indian Army", as against the armed forces;
  - capital (of a pillar): ಶಿರೋಭಾಗ;
  - metre (unit): ಮೀಟರ್;
  - title (sports): ಪ್ರಶಸ್ತಿ;
  - author: ಲೇಖಕರ ಸಮಾವೇಶ;
  - painting (one picture): ವರ್ಣಚಿತ್ರ;
  - monk (Buddhist): ಭಿಕ್ಷು;
  - Sanchi (in "Sanchi Honnamma"): ಸಂಚಿ;
  - MSME inside a portal name;
  - Union Minister of State: ರಾಜ್ಯ ಸಚಿವೆ;
  - per cent written in words: ಶೇಕಡಾ ಹತ್ತರಷ್ಟು.
- **The glossary adds a noun the English does not have:**
  - Khalji, Tughlaq: ಸಂತತಿ, where the line is a person's name;
  - Bahmani: ಬಹಮನಿ ರಾಜ್ಯ for "Bahmani kingdom";
  - Guru Arjan: the English has no "Dev";
  - Muhammad (Mahamud) Adil Shah: the English has no "(Mahamud)".
- **Inflection, compound or allowed rephrase:**
  - ರಾಜಾಶ್ರಯ (royal patronage);
  - ಬೌದ್ಧ ಮತ್ತು ಜೈನ ಧರ್ಮಗಳು;
  - ಉತ್ಸವ (an alternative inside the glossary row "festival");
  - ಯುದ್ಧ for a generic "battle", where ಕದನ is for named battles;
  - ಮೊಗಸಾಲೆ for temple corridors.
- **Synonyms used by both papers alike:** "translation" uses ಅನುವಾದ and ಭಾಷಾಂತರ in both papers, so it is not a cross-paper difference.

**BOTH_MISS (50):** I reviewed these by row type. Both papers read the same way, and the rows are template or bracketed glossary rows that a text cannot contain verbatim:
- century and date patterns;
- the Vedas list;
- "Name (gloss)" rows such as Badami (Vatapi) and Kalyana (Basavakalyana);
- NOT-correct stems, which carry the bold that section H requires;
- generic words with case endings.

**New-term "CONFLICT" rows:** the 4 rows still show because the translators' NEW_TERMS files keep both forms. All 4 are settled in the glossary and fixed in the text (§4).

## 7. Notes for the record
- **SDA MP06-Q036 (Jinji/Gingee):** one glossary form, ಜಿಂಜಿ, is used for both English spellings. A distractor therefore visibly repeats the stem name, which is kept as section H directs.
- **Register sources:** the DSERT Kannada source texts and `PARALLEL_CORPUS.jsonl` are not in this package. The checkers judged register without them, and new terms were settled by section C rules 1 and 6 (glossary re-use; most batches; tie-breaks).
- **Gate note:** the checkers expected possible gate flags (an extra `**ಅಲ್ಲ**` bold, and century digits). The gate reports 0, so none arose.

## 8. Left undone
- **MP03-Q022:** the ವರಾಹ (ದೈವಿಕ ವರಾಹ) gloss is a glossary-owner decision (§3).
- **Gemini verification:** skipped, by the owner's ruling. The internal back-check above was the only meaning check.
- **Nothing else is open.** Every Queue A is closed, and the gate and the release check pass for both papers.
