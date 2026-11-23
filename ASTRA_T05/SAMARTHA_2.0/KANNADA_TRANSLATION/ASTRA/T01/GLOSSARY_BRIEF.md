# Brief: polity glossary for the ASTRA Test 1 Kannada edition

*Claude Code, 14-11-2026, §452. Owner: "Yes, start Kannada" (R7). This glossary fixes one Kannada form per term before ten translation batches start, so that the whole paper uses the same word for the same concept (lessons file §4: "Use the same Kannada term for a concept in a question and in its solution").*

## Input
- `SAMARTHA_2.0/KANNADA_TRANSLATION/ASTRA/T01/EN_FOR_KN.jsonl`: 200 items. `text` is the question; `sol` is the solution. Items with `n` 1–75 are Polity; 76–100 are Current Affairs.
- **Already fixed** (keep these; do not re-decide): `TERM_CHOICES.tsv` in the same folder (the CA half's choices, owner-agreed).

## Where the Kannada comes from (in this order; lessons file §1)
1. **KEA/KPSC official Kannada papers.** These show how an exam setter words polity terms in Kannada.
   - `05_ANALYSIS/KEA_CA_SOURCES_2026-11/population/QUESTIONS.jsonl` and `OCT_STEMS.jsonl`: the recent KEA papers, bilingual.
   - Search them for the English term and read the Kannada side.
2. **Karnataka Government Kannada:** the Budget speeches `04_SOURCES/STUDY/ECONOMICS/KARNATAKA/*_KAN.pdf`, the Kannada Economic Survey, and the ES reference list `SAMARTHA_2.0/KANNADA_TRANSLATION/ECONOMIC_SURVEY/GEMINI_QUALIFICATION/REFERENCE_LIST_FINAL.tsv`.
3. **Dr P. S. Gangadhar, *Bharata Samvidhana mattu Rajakiya* (21st ed.),** OCR per page at `04_SOURCES/STUDY/REFERENCE_BOOKS/KANNADA_KAS_SET/05_Bharata_Samvidhana_mattu_Rajakiya_Gangadhar_21ed.pdf.ocr/p0001.txt … p0659.txt`.
   - It is the standard Kannada polity book; use it for terms and flow.
   - It is **LOCATOR-ONLY**: language only, never a fact or a number. The OCR garbles some characters; prefer a form you see spelled the same way in two places.
4. If none of these has the term, use the plain, common Kannada word, with the English in brackets at first use. Never coin a Sanskritised word where a common one exists.

## Task
1. List every recurring polity, legal and administrative term in the 150 Polity items and all 200 solutions.
   - Examples: Article, clause, Schedule, amendment, Parliament, Lok Sabha, Rajya Sabha, Legislative Assembly/Council, Governor, President, Vice-President, Speaker, Chief Justice, High Court, ordinance, pardon, remission, commute, Panchayat Raj, Grama/Taluk/Zilla Panchayat, Election Commission, statutory body, constitutional body, Directive Principles, Fundamental Rights/Duties, writ, impeachment, money bill, quorum, resolution, notification, Act, Rules, section.
   - Include names of Acts and bodies that recur (e.g. the Karnataka Panchayat Raj Act, 1993; the Karnataka Co-operative Societies Act, written with no year).
   - Expect roughly 200–350 terms.
2. Add the **fixed solution vocabulary** below unchanged (the YASHASVI Kannada house form).
3. Mark each term's source exactly: a KEA question id, a Budget speech page, a reference-list row, a Gangadhar page (`G p0123`), or `common`.

## Fixed solution vocabulary (YASHASVI Kannada; do not change)
| English | Kannada |
|---|---|
| Correct Option: (c) | ಸರಿಯಾದ ಆಯ್ಕೆ: (c) |
| Justification: | ಸಮರ್ಥನೆ: |
| Statement 1: Correct. / Incorrect. | ಹೇಳಿಕೆ 1: ಸರಿ. / ತಪ್ಪು. |
| Option (a): Correct. / Incorrect. | ಆಯ್ಕೆ (a): ಸರಿ. / ತಪ್ಪು. |
| Option (a): Incorrect as an answer. | ಆಯ್ಕೆ (a): ಉತ್ತರವಾಗಿ ತಪ್ಪು. |
| Pair 1: Correctly matched. / Incorrectly matched. | ಜೋಡಿ 1: ಸರಿಯಾಗಿ ಹೊಂದಿದೆ. / ತಪ್ಪಾಗಿ ಹೊಂದಿದೆ. |
| Pair 1: Correct. / Incorrect. | ಜೋಡಿ 1: ಸರಿ. / ತಪ್ಪು. |
| Explanation link: (Established.) | ವಿವರಣೆಯ ಸಂಬಂಧ: (ಸ್ಥಾಪಿತವಾಗಿದೆ.) |
| Hence the correct answer is option (c). | ಆದ್ದರಿಂದ ಸರಿಯಾದ ಉತ್ತರ ಆಯ್ಕೆ (c). |
| Result: | ತೀರ್ಮಾನ: |
| Salient Features: | ಪ್ರಮುಖ ಅಂಶಗಳು: |
| Exam Fact: | ಪರೀಕ್ಷಾ ಸಂಗತಿ: |
| Statement I / Statement II | ಹೇಳಿಕೆ I / ಹೇಳಿಕೆ II |

## Output
`SAMARTHA_2.0/KANNADA_TRANSLATION/ASTRA/T01/POLITY_GLOSSARY.tsv` with the columns:
- `english`
- `kannada`
- `source`
- `note`: for example "abbreviation kept in Latin"; "KEA uses X, Gangadhar uses Y, chose X because…".

One row per concept. UTF-8, written with the Write tool; never shell-echo Kannada. Check that every row has four tab-separated fields.

End with a short report:
- the count of terms;
- the terms where sources disagree, and your choice;
- the terms you could not source.
