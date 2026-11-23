# ASTRA Test 3 (internal T05) SDA: English master FROZEN and SHIPPED

*Claude Code, 23-11-2026. The chat surface cleared SDA English v3 (`drafts/ASTRA_T3_SDA_EN_RELEASE_VERIFICATION_v4_GEMINI.md`, "CLEARED TO SHIP"). The owner's instruction of 23-11-2026: "Ship it. Run the Kannada SDA edition in parallel with Kannada FDA, both from the cleared English masters (FDA v5, SDA v3)."*

## Equality with the cleared zip
- **Master:** the repository's master equals `ASTRA_T05_SDA_RELEASE_v3.zip` byte for byte.
- **Word file:** the §513 build had regenerated it. Its paragraph text was identical (3,070 paragraphs), but the bytes differed because of docx metadata. **The cleared file was restored from the v3 zip**, so the shipped Word file is the one the chat surface checked.

## Frozen files
These are the sha256 hashes at freeze. Any later change is a post-freeze edit and needs a recorded reason.

```
f757f758cde253bb0feabcfbb9951e2bac8f35971f5689e1e08023807f06472f *05_ANALYSIS/ASTRA_2026/T05/T05_SDA_EN_QS.md
d27f580aade4ac7faa9009e19c8af8162941e1a1855b2640121bfbb69d165707 *05_ANALYSIS/ASTRA_2026/T05/ASTRA_T3_SDA_EN_Questions_and_Solutions.docx
f5940f3c18b52c16f273ce3eef7b2abea31996b21e48af6275ad15d33a63d4c0 *05_ANALYSIS/ASTRA_2026/T05/out/T05_SDA_FINAL.jsonl
eae7088a316213532914e9ce0d5f1d56d0aa3a8f507f49053f36afce5cd22513 *SAMARTHA_2.0/KANNADA_TRANSLATION/ASTRA/T05/EN_FOR_KN_SDA.jsonl
```

With both papers frozen, `out/T05_FINAL_KEYS.tsv` and `solutions/SOLUTION_PATCHES.json` are frozen in full.

## Kannada input
- **Source:** the Kannada SDA edition is translated from `EN_FOR_KN_SDA.jsonl` only. It holds 100 items, cut from the master above with no changes.
- **Warning for future builds:** do not rebuild the English Word files of either paper. `build_t05_docx.py` rebuilds every paper whose master exists. It may run only with `KN`, which builds the Kannada Word files.

## Status
- **SDA English:** SHIPPED (owner).
- **Both ASTRA Test 3 English papers:** SHIPPED.
