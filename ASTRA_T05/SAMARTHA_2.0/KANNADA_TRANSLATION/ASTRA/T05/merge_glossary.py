"""Merge the four candidate glossaries (HISTORY_GLOSSARY, SDA_HISTORY_GLOSSARY, CA_GLOSSARY, SDA_CA_GLOSSARY) into the ONE shared
glossary KN_GLOSSARY_T3.tsv for both T05 Kannada papers (owner, 23-11-2026, §515).

Key: the English term, case-folded and space-normalised. Rows that agree are merged, and their papers are joined.
Rows that disagree are settled by source rank:
  1 T1/T2 glossaries (series continuity);
  2 DSERT Kannada-medium;
  3 KEA/KPSC papers (incl. the parallel corpus);
  4 Kannada Economic Survey / Budget / reference list;
  5 Kannada reference books (Kamath, Ashwathappa, Gangadhar, Ranganath, Garani);
  6 common.
A tie goes to the HISTORY lists for history terms and to the FDA list otherwise. Every conflict and its choice is logged in
KN_GLOSSARY_T3_CONFLICTS.tsv. House overrides (binding series forms) are applied last and logged too.
Later additions (translators' NEW_TERMS_NN.tsv, adopted by Claude Code) go in KN_GLOSSARY_T3_ADDITIONS.tsv and are merged on
every run with rank 0, so an adopted term is never re-decided.
Usage: python -I -X utf8 merge_glossary.py"""
import csv, os, re, collections
H = os.path.dirname(os.path.abspath(__file__))
SRC = [('HISTORY_GLOSSARY.tsv', 'HISTORY', 'FDA'), ('SDA_HISTORY_GLOSSARY.tsv', 'HISTORY', 'SDA'),
       ('CA_GLOSSARY.tsv', 'CA', 'FDA'), ('SDA_CA_GLOSSARY.tsv', 'CA', 'SDA')]
def rank(src):
    s = src.lower()
    if s.startswith('claude code adopted'): return 0
    if 't1 ' in s or 't2 ' in s or 't1glossary' in s or s.startswith('t1') or s.startswith('t2') or 'term_choices' in s: return 1
    if 'dsert' in s: return 2
    if re.search(r'\bkea\b|kpsc|par[:_ ]|parallel|oct_stems|kas-p', s): return 3
    if re.search(r'survey|\bes\b|es p\d|budget|reference|ref list|ref_list', s): return 4
    if re.search(r'kamath|ashwathappa|gangadhar|ranganath|garani|vrs|_kn p', s): return 5
    return 6
norm = lambda e: re.sub(r'\s+', ' ', e.strip().casefold())
OVERRIDE = {  # house forms binding across the ASTRA series (T1/T2 editions; edition brief); applied after the merge
    'statement i': 'ಹೇಳಿಕೆ I', 'statement ii': 'ಹೇಳಿಕೆ II', 'statement-i': 'ಹೇಳಿಕೆ I', 'statement-ii': 'ಹೇಳಿಕೆ II',
    'exam fact': 'ಪರೀಕ್ಷಾ ಸಂಗತಿ', 'result': 'ತೀರ್ಮಾನ'}
rows = collections.defaultdict(list)
files = [(f, d, p) for f, d, p in SRC if os.path.exists(os.path.join(H, f))]
if os.path.exists(os.path.join(H, 'KN_GLOSSARY_T3_ADDITIONS.tsv')): files.append(('KN_GLOSSARY_T3_ADDITIONS.tsv', None, None))
for f, dom, pap in files:
    for r in csv.DictReader(open(os.path.join(H, f), encoding='utf-8'), delimiter='\t', quoting=csv.QUOTE_NONE):
        e, k = (r.get('english') or '').strip(), (r.get('kannada') or '').strip()
        if not e or not k: continue
        d = dom or (r.get('domain') or 'ADDED'); p = pap or (r.get('papers') or 'FDA+SDA')
        rows[norm(e)].append(dict(english=e, kannada=k, source=(r.get('source') or '').strip(), note=(r.get('note') or '').strip(), domain=d, paper=p, file=f))
out, conf = [], []
for key, rs in rows.items():
    forms = collections.OrderedDict()
    for r in rs: forms.setdefault(r['kannada'], []).append(r)
    if len(forms) == 1: win = rs[0]
    else:
        def score(item):
            k, rr = item; best = min(rank(r['source']) for r in rr)
            hist = any(r['domain'] == 'HISTORY' for r in rr); fda = any(r['paper'] == 'FDA' for r in rr)
            return (best, 0 if hist else 1, 0 if fda else 1, -len(rr))
        k, rr = sorted(forms.items(), key=score)[0]; win = rr[0]
        conf.append((rs[0]['english'], k, ' | '.join(f"{kk} [{'; '.join(r['file'] + ': ' + r['source'][:60] for r in v)}]" for kk, v in forms.items() if kk != k), f"rank {min(rank(r['source']) for r in rr)}"))
    papers = '+'.join(sorted({p for r in rs for p in r['paper'].split('+')}))
    doms = sorted({r['domain'] for r in rs}); dom = 'FIXED' if any(rank(r['source']) == 1 and r['english'].lower() in ('exam fact', 'result') for r in rs) else '/'.join(doms)
    kn = win['kannada']
    if key in OVERRIDE and OVERRIDE[key] != kn: conf.append((win['english'], OVERRIDE[key], kn, 'house override')); kn = OVERRIDE[key]
    out.append(dict(english=win['english'], kannada=kn, source=win['source'], note=win['note'], domain=dom, papers=papers))
assert not any('ಪರೀಕ್ಷಾ ಸತ್ಯ' in r['kannada'] for r in out), 'banned label in glossary'
out.sort(key=lambda r: (r['domain'], r['english'].casefold()))
with open(os.path.join(H, 'KN_GLOSSARY_T3.tsv'), 'w', encoding='utf-8', newline='\n') as o:
    o.write('english\tkannada\tsource\tnote\tdomain\tpapers\n')
    for r in out: o.write('\t'.join(r[c].replace('\t', ' ') for c in ('english', 'kannada', 'source', 'note', 'domain', 'papers')) + '\n')
with open(os.path.join(H, 'KN_GLOSSARY_T3_CONFLICTS.tsv'), 'w', encoding='utf-8', newline='\n') as o:
    o.write('english\tchosen\trejected\twhy\n')
    for c in conf: o.write('\t'.join(x.replace('\t', ' ') for x in c) + '\n')
print('files', [f for f, _, _ in files], 'terms', len(out), 'conflicts settled', len(conf),
      'by paper', dict(collections.Counter(r['papers'] for r in out)))
