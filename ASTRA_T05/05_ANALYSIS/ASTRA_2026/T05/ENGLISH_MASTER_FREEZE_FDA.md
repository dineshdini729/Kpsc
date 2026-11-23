# ASTRA Test 3 (internal T05) FDA: English master FROZEN and SHIPPED

*Claude Code, 23-11-2026. The chat surface cleared FDA English v5 (`drafts/ASTRA_T3_FDA_EN_RELEASE_VERIFICATION_v4_GEMINI.md`, "CLEARED TO SHIP"). The owner's instruction of 23-11-2026: "Ship it. Start the Kannada FDA edition from the v5 master." The freeze is at commit 22c96a32 (§513). The repository's Word file and master equal the cleared `ASTRA_T05_FDA_RELEASE_v5.zip` byte for byte (checked).*

## Frozen files
These are the sha256 hashes at 22c96a32. Any later change is a post-freeze edit and needs a recorded reason.

```
0d1feb32a05b34dc7255d67cbb5722c663dbb630b7aa7bf643f71bd609bf51ee *05_ANALYSIS/ASTRA_2026/T05/T05_FDA_EN_QS.md
f67bb80c35ecc2770520bbc021248bc8fb7ca771040fa582faf192f5ac7852b2 *05_ANALYSIS/ASTRA_2026/T05/ASTRA_T3_FDA_EN_Questions_and_Solutions.docx
6d5f4a9018785ac3a86ab2999ec4e305936170365467cb18a7b3eb1c038327dd *05_ANALYSIS/ASTRA_2026/T05/out/T05_FDA_FINAL.jsonl
b66d52273ce79d41b22facb8266277b9bf0c66b04fc4c96745c3fe295bc88f8f *SAMARTHA_2.0/KANNADA_TRANSLATION/ASTRA/T05/EN_FOR_KN_FDA.jsonl
```

`out/T05_FINAL_KEYS.tsv` and `solutions/SOLUTION_PATCHES.json` are shared with the SDA paper, which is still open. Their FDA rows and FDA patches are frozen with this paper; SDA rows may still change.

## Kannada input
- **Source:** the Kannada FDA edition is translated from `EN_FOR_KN_FDA.jsonl` only. It holds 100 items, cut from `T05_FDA_EN_QS.md` above: `text` is the question, `sol` the solution, plus the id, the key and the part.
- **One input line differs from the English master, by owner instruction of 23-11-2026:**
  - **Where:** Q100's Salient Features introduction.
  - **English master:** "The Chief Minister cited these figures …".
  - **Kannada input:** "The Chief Minister cited this reservation …".
  - **Why:** chat verification v4 noted this as not blocking for the English, to be fixed in the Kannada build. The English Word file keeps its cleared wording.

## Status
- **FDA English:** SHIPPED (owner).
- **SDA English:** awaits the chat surface's clearance of `ASTRA_T05_SDA_RELEASE_v3`. Kannada SDA starts only after that (owner, 23-11-2026).
