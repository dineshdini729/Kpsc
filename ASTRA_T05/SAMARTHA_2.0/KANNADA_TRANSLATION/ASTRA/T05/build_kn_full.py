"""Assemble the ASTRA Test 3 (internal T05) Kannada edition, one Markdown file per paper, then the Word files.
Adapted from ASTRA/T03/build_kn_full.py (§514). Questions `kn_text` and solutions `kn_sol` come from kn_batches/OUT_NN.jsonl (FDA) and
kn_batches_SDA/OUT_NN.jsonl (SDA, once SDA English is cleared). The English input is EN_FOR_KN_<P>.jsonl (frozen; see
05_ANALYSIS/ASTRA_2026/T05/ENGLISH_MASTER_FREEZE_<P>.md). It is already in the R11 release labels, so the Kannada keeps them.
Gate (mechanical, per item; KN_GATE1.tsv): key line and 'Hence' line match the English key; the five headings; no ಪರೀಕ್ಷಾ ಸತ್ಯ
(owner rule, 23-11-2026); question and solution line counts equal the English; '**' and single '*' counts equal the English;
every number in the English occurs in the Kannada; option and statement labels at line starts; no process notes; no stray
non-Kannada characters. Writes 05_ANALYSIS/ASTRA_2026/T05/T05_<P>_KN_QS.md, then runs build_t05_docx.py KN and moves the .docx here.
Usage: python -I build_kn_full.py [--no-docx]"""
import json, os, re, glob, sys, shutil, subprocess, collections
H = os.path.dirname(os.path.abspath(__file__))
T = os.path.normpath(os.path.join(H, '..', '..', '..', '..', '05_ANALYSIS', 'ASTRA_2026', 'T05'))
sys.path.insert(0, os.path.join(os.path.dirname(T), 'T01'))
from release_polish import polish
NL = '\n'
BATCH = {'FDA': 'kn_batches', 'SDA': 'kn_batches_SDA'}
PAPERS = [P for P in ('FDA', 'SDA') if os.path.exists(os.path.join(H, f'EN_FOR_KN_{P}.jsonl')) and glob.glob(os.path.join(H, BATCH[P], 'OUT_[0-9][0-9].jsonl'))]
issues = []
OKCH = re.compile('[ಀ-೿\x20-\x7E\n‌‍–—‘’“”₹… −×°•→²³⁸⁻₂₃₄µΩλ½¼]')
def nums(s): return re.findall(r'\d+', s)
def ital(s):
    """Italic toggles, read exactly as build_t05_docx.runs() reads them ('***' = one bold + one italic toggle)."""
    n, i = 0, 0
    while i < len(s):
        if s.startswith('***', i): n += 1; i += 3
        elif s.startswith('**', i): i += 2
        elif s[i] == '*': n += 1; i += 1
        else: i += 1
    return n
def check(i, e, q, sol):
    k = e['key']
    if f'ಸರಿಯಾದ ಆಯ್ಕೆ: ({k})' not in sol: issues.append((i, 'KEY_LINE', ''))
    if not re.search(r'ಆದ್ದರಿಂದ ಸರಿಯಾದ ಉತ್ತರ\s*\**\s*ಆಯ್ಕೆ \(' + k + r'\)', sol): issues.append((i, 'HENCE', ''))
    for h in ('ಸಮರ್ಥನೆ:', 'ತೀರ್ಮಾನ:', 'ಪ್ರಮುಖ ಅಂಶಗಳು:', 'ಪರೀಕ್ಷಾ ಸಂಗತಿ:'):
        if h not in sol: issues.append((i, 'HEADING', h))
    if 'ಪರೀಕ್ಷಾ ಸತ್ಯ' in q + sol: issues.append((i, 'BANNED_LABEL', 'ಪರೀಕ್ಷಾ ಸತ್ಯ'))
    if len(sol.split(NL)) != len(e['sol'].split(NL)): issues.append((i, 'SOL_LINES', f"{len(sol.split(NL))} vs {len(e['sol'].split(NL))}"))
    if sol.count('**') != e['sol'].count('**'): issues.append((i, 'BOLD_COUNT', f"{sol.count('**')} vs {e['sol'].count('**')}"))
    if ital(sol) != ital(e['sol']): issues.append((i, 'ITALIC_COUNT', f"{ital(sol)} vs {ital(e['sol'])}"))
    miss = [n for n in set(nums(e['sol'])) if n not in nums(sol)]
    if miss: issues.append((i, 'SOL_NUMBERS', ' '.join(sorted(miss))))
    if len(q.split(NL)) != len(e['text'].split(NL)): issues.append((i, 'Q_LINES', f"{len(q.split(NL))} vs {len(e['text'].split(NL))}"))
    missq = [n for n in set(nums(e['text'])) if n not in nums(q)]
    if missq: issues.append((i, 'Q_NUMBERS', ' '.join(sorted(missq))))
    if ital(q) != ital(e['text']): issues.append((i, 'Q_ITALIC_COUNT', ''))
    ql, el = q.split(NL), e['text'].split(NL)
    if len(ql) == len(el):
        for a, b in zip(el, ql):
            m = re.match(r'^([a-d]\) |[1-4]\. |\||Statement I{1,2}:)', a)
            want = {'Statement I:': 'ಹೇಳಿಕೆ I:', 'Statement II:': 'ಹೇಳಿಕೆ II:'}.get(m.group(1), m.group(1)) if m else None
            if want and not b.startswith(want): issues.append((i, 'Q_LABEL', want))
    if re.search(r'(?i)\bblind\b|\bsolvers?\b|card [0-9a-f]{6}#|[0-9a-f]{6}#\d|ಕಾರ್ಡ್ [0-9a-f]{6}|ಬ್ಲೈಂಡ್ ಪರಿಹಾರ|ಸಾಲ್ವರ್|ಗೇಟ್ ?\d|T05-|MP\d\d-Q', q + sol): issues.append((i, 'PROCESS_NOTE', ''))
    stray = sorted({hex(ord(c)) for c in q + sol if not OKCH.match(c) and c not in e['text'] + e['sol']})   # symbols the English itself uses are allowed
    if stray: issues.append((i, 'STRAY_CHAR', ' '.join(stray)))
# Closing-line harmonisation (whole question lines only), as T2: the T1 Kannada forms win, so the series reads the same.
HARM = {'ಮೇಲಿನ ಯಾವ ಹೇಳಿಕೆಗಳು ಸರಿಯಾಗಿವೆ?': 'ಮೇಲಿನ ಹೇಳಿಕೆಗಳಲ್ಲಿ ಯಾವುವು ಸರಿಯಾಗಿವೆ?',
        'ಕೆಳಗೆ ನೀಡಿರುವ ಆಯ್ಕೆಗಳಿಂದ ಸರಿಯಾದ ಉತ್ತರವನ್ನು ಆರಿಸಿ:': 'ಕೆಳಗೆ ನೀಡಿರುವ ಆಯ್ಕೆಗಳಿಂದ ಸರಿಯಾದ ಉತ್ತರವನ್ನು ಆಯ್ಕೆಮಾಡಿ:',
        'ಮೇಲಿನ ಯಾವ ಜೋಡಿಗಳು ಸರಿಯಾಗಿ ಹೊಂದಿಕೆಯಾಗಿವೆ?': 'ಮೇಲಿನ ಜೋಡಿಗಳಲ್ಲಿ ಯಾವುವು ಸರಿಯಾಗಿ ಹೊಂದಿಕೆಯಾಗಿವೆ?',
        'ಪಟ್ಟಿ-I ನ್ನು ಪಟ್ಟಿ-II ರೊಂದಿಗೆ ಹೊಂದಿಸಿ:': 'ಪಟ್ಟಿ-I ಅನ್ನು ಪಟ್ಟಿ-II ರೊಂದಿಗೆ ಹೊಂದಿಸಿ:'}
FIXED = {'Choose the correct answer from the options given below:': 'ಕೆಳಗೆ ನೀಡಿರುವ ಆಯ್ಕೆಗಳಿಂದ ಸರಿಯಾದ ಉತ್ತರವನ್ನು ಆಯ್ಕೆಮಾಡಿ:',
         'Select the correct answer using the code given below:': 'ಕೆಳಗೆ ನೀಡಿರುವ ಸಂಕೇತಗಳನ್ನು ಬಳಸಿ ಸರಿಯಾದ ಉತ್ತರವನ್ನು ಆಯ್ಕೆಮಾಡಿ:',
         'Select the correct answer using the codes given below:': 'ಕೆಳಗೆ ನೀಡಿರುವ ಸಂಕೇತಗಳನ್ನು ಬಳಸಿ ಸರಿಯಾದ ಉತ್ತರವನ್ನು ಆಯ್ಕೆಮಾಡಿ:'}
TITLE = {'A': '## ಭಾಗ A: ಪ್ರಾಚೀನ ಮತ್ತು ಮಧ್ಯಕಾಲೀನ ಇತಿಹಾಸ', 'B': '## ಭಾಗ B: ಪ್ರಚಲಿತ ವಿದ್ಯಮಾನಗಳು (ಸೆಪ್ಟೆಂಬರ್ 2026)'}
hlog = []
for P in PAPERS:
    en = {json.loads(l)['id']: json.loads(l) for l in open(os.path.join(H, f'EN_FOR_KN_{P}.jsonl'), encoding='utf-8')}
    kn = {}
    for f in sorted(glob.glob(os.path.join(H, BATCH[P], 'OUT_[0-9][0-9].jsonl'))):
        for l in open(f, encoding='utf-8'):
            if l.strip(): r = json.loads(l); kn[r['id']] = r
    for i, r in kn.items():
        if i not in en or not r.get('kn_text'): continue
        el, kl = en[i]['text'].split(NL), r['kn_text'].split(NL)
        for j, l in enumerate(kl):
            new = HARM.get(l.strip())
            if j < len(el) and el[j].strip() in FIXED: new = FIXED[el[j].strip()]
            if new and new != l.strip(): hlog.append((P, i, str(j + 1), l.strip(), new)); kl[j] = new
        r['kn_text'] = NL.join(kl)
    out = [f'# ಅಸ್ತ್ರ (ASTRA) ಪರೀಕ್ಷೆ 3 | {P} | ಪ್ರಶ್ನೆಗಳು ಮತ್ತು ಪರಿಹಾರಗಳು (ಕನ್ನಡ)', '']
    part = None
    for e in sorted(en.values(), key=lambda e: e['n']):
        i = e['id']
        if e['part'] != part: part = e['part']; out += [TITLE[part], '']
        r = kn.get(i)
        if not r or not r.get('kn_sol') or not r.get('kn_text'): issues.append((i, 'MISSING', '')); continue
        check(i, e, r['kn_text'], r['kn_sol'])
        out += [f"**{e['n']}.** " + r['kn_text'], '', r['kn_sol'], '', '---', '']
    plog = []; txt = polish(NL.join(out) + NL, 'KN', 'T3', plog)
    print(P, 'KN polish', plog, 'kannada items', len(kn))
    open(os.path.join(T, f'T05_{P}_KN_QS.md'), 'w', encoding='utf-8', newline=NL).write(txt)
with open(os.path.join(H, 'KN_HARMONISED.tsv'), 'w', encoding='utf-8', newline=NL) as o:
    o.write('paper\tid\tline\tbefore\tafter\n')
    for x in hlog: o.write('\t'.join(x) + NL)
with open(os.path.join(H, 'KN_GATE1.tsv'), 'w', encoding='utf-8', newline=NL) as o:
    o.write('item\tissue\tdetail\n')
    for r in issues: o.write('\t'.join(r) + NL)
print('papers', PAPERS, 'harmonised lines', len(hlog), 'issues', len(issues), dict(collections.Counter(r[1] for r in issues)))
if '--no-docx' not in sys.argv and PAPERS:
    subprocess.run([sys.executable, '-I', os.path.join(T, 'build_t05_docx.py'), 'KN'], check=True)
    for P in PAPERS:
        shutil.move(os.path.join(T, f'ASTRA_T3_{P}_KN_Questions_and_Solutions.docx'), os.path.join(H, f'ASTRA_T3_{P}_KN_Questions_and_Solutions.docx'))
