"""Build PACKAGE_MANIFEST.sha256 and the continuation zip (§516). Run from anywhere: python -I -X utf8 make_package.py <commit>
The manifest covers this folder (minus regenerated gate logs) and every outside file the briefs and scripts read. The zip holds the
same files plus the manifest, with paths relative to the repository root, so it unzips over a copy of the repository."""
import glob, os, hashlib, sys, zipfile
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.normpath(os.path.join(H, '..', '..', '..', '..')); os.chdir(R)
K = 'SAMARTHA_2.0/KANNADA_TRANSLATION/ASTRA/T05/'
rel = lambda f: f.replace(os.sep, '/')
SKIP = ('PACKAGE_MANIFEST.sha256', 'KN_GATE1.tsv', 'KN_HARMONISED.tsv', 'PACKAGE_INFO.txt')
fs = [rel(f) for f in glob.glob(K + '**/*', recursive=True) if os.path.isfile(f) and not f.endswith(SKIP)]
EXT = ['SAMARTHA_2.0/KANNADA_TRANSLATION/ASTRA/T01/TERM_CHOICES.tsv', 'SAMARTHA_2.0/KANNADA_TRANSLATION/ASTRA/T01/GLOSSARY_BRIEF.md',
       'SAMARTHA_2.0/KANNADA_TRANSLATION/ASTRA/T01/POLITY_GLOSSARY.tsv', 'SAMARTHA_2.0/KANNADA_TRANSLATION/KANNADA_TRANSLATION_LESSONS.md',
       '05_ANALYSIS/ASTRA_2026/T03/T03_FDA_KN_QS.md', '05_ANALYSIS/ASTRA_2026/T03/T03_SDA_KN_QS.md',
       '05_ANALYSIS/ASTRA_2026/T05/build_t05_docx.py', '05_ANALYSIS/ASTRA_2026/T05/check_release_docx_t05.py', '05_ANALYSIS/ASTRA_2026/T01/release_polish.py',
       '05_ANALYSIS/ASTRA_2026/T05/T05_FDA_EN_QS.md', '05_ANALYSIS/ASTRA_2026/T05/T05_SDA_EN_QS.md', '05_ANALYSIS/ASTRA_2026/T05/out/T05_FINAL_KEYS.tsv',
       '05_ANALYSIS/ASTRA_2026/T05/ENGLISH_MASTER_FREEZE_FDA.md', '05_ANALYSIS/ASTRA_2026/T05/ENGLISH_MASTER_FREEZE_SDA.md',
       '05_ANALYSIS/ASTRA_2026/T05/ASTRA_T3_FDA_EN_Questions_and_Solutions.docx', '05_ANALYSIS/ASTRA_2026/T05/ASTRA_T3_SDA_EN_Questions_and_Solutions.docx',
       '05_ANALYSIS/KEA_CA_SOURCES_2026-11/population/OCT_STEMS.jsonl', 'SAMARTHA_2.0/KANNADA_TRANSLATION/P1_CORPUS/PARALLEL_CORPUS.jsonl']
EXT += [rel(f) for f in glob.glob('05_ANALYSIS/ASTRA_2026/T05_SOURCE_TRACE/source_text/DSERT_*_2627.txt')]
fs = sorted(set(fs + [f for f in EXT if os.path.exists(f)]))
with open(K + 'PACKAGE_MANIFEST.sha256', 'w', encoding='utf-8', newline='\n') as o:
    for f in fs: o.write(hashlib.sha256(open(f, 'rb').read()).hexdigest() + '  ' + f + '\n')
commit = sys.argv[1] if len(sys.argv) > 1 else 'uncommitted'
open(K + 'PACKAGE_INFO.txt', 'w', encoding='utf-8', newline='\n').write(
    f'ASTRA T05 Kannada continuation package, 23-11-2026 (§516). Built from repository state after commit {commit}.\n'
    'Start: PROMPTS/00_main_session.txt and RUNBOOK_OTHER_MACHINE.md. Verify first: verify_package.py must print PACKAGE OK.\n')
zp = 'EXPORT_FOR_PROJECT/ASTRA_T05/ASTRA_T05_KANNADA_RESUME_PACKAGE.zip'
with zipfile.ZipFile(zp, 'w', zipfile.ZIP_DEFLATED) as z:
    for f in fs + [K + 'PACKAGE_MANIFEST.sha256', K + 'PACKAGE_INFO.txt']: z.write(f)
print('manifest files', len(fs), 'zip KB', os.path.getsize(zp) // 1024)
