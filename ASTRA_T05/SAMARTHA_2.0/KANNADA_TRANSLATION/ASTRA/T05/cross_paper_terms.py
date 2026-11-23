"""Cross-paper term consistency check for the ASTRA Test 3 Kannada edition (owner, 23-11-2026, §515 item 4):
the same English term must have the same Kannada form in the FDA and SDA papers.

1. Glossary terms in both papers. For every KN_GLOSSARY_T3.tsv term whose English occurs (whole word, case-insensitive) in items of
   BOTH papers, count per paper the items whose Kannada (question + solution) contains the glossary's Kannada form (its first
   alternative when the row has " / "; any bracketed English is ignored). A term is FLAGGED when it is used in both papers and one
   paper renders it with the glossary form in every such item while the other misses it in at least one. That is a candidate
   inconsistency for a human read; a miss can be a legitimate inflection or rephrase.
2. New terms. Terms the translators recorded in NEW_TERMS_NN.tsv (both folders). The same English with different Kannada across
   the runs is a conflict; it must be settled once in KN_GLOSSARY_T3_ADDITIONS.tsv and fixed in the text.
Writes KN_CROSS_PAPER_TERMS.tsv and KN_NEW_TERMS_ALL.tsv. Usage: python -I -X utf8 cross_paper_terms.py"""
import csv, json, glob, os, re, collections
H = os.path.dirname(os.path.abspath(__file__))
def load(P, folder):
    en = {json.loads(l)['id']: json.loads(l) for l in open(os.path.join(H, f'EN_FOR_KN_{P}.jsonl'), encoding='utf-8')}
    kn = {}
    for f in sorted(glob.glob(os.path.join(H, folder, 'OUT_[0-9][0-9].jsonl'))):
        for l in open(f, encoding='utf-8'):
            if l.strip(): r = json.loads(l); kn[r['id']] = r.get('kn_text', '') + '\n' + r.get('kn_sol', '')
    return [(en[i]['text'] + '\n' + en[i]['sol'], kn[i]) for i in en if i in kn]
papers = {'FDA': load('FDA', 'kn_batches'), 'SDA': load('SDA', 'kn_batches_SDA')}
gl = list(csv.DictReader(open(os.path.join(H, 'KN_GLOSSARY_T3.tsv'), encoding='utf-8'), delimiter='\t', quoting=csv.QUOTE_NONE))
def kform(k):
    k = k.split(' / ')[0]; k = re.sub(r'\s*\([^)]*[A-Za-z][^)]*\)', '', k)   # drop bracketed English
    return k.strip()
STOP = {'a', 'an', 'the', 'of', 'and', 'or', 'in', 'to', 'is'}
rows = []
for g in gl:
    e = re.sub(r'\s*\(.*?\)', '', g['english']).strip()
    if len(e) < 4 or e.casefold() in STOP or g['domain'] == 'FIXED': continue
    pat = re.compile(r'(?<![A-Za-z])' + re.escape(e) + r'(?![A-Za-z])', re.I)
    k = kform(g['kannada'])
    if not k or not re.search('[ಀ-೿]', k): continue
    stem = k[:max(3, len(k) - 2)]   # tolerate a case ending on the last word
    stat = {}
    for P, items in papers.items():
        hits = [(en, kn) for en, kn in items if pat.search(en)]
        ok = sum(1 for en, kn in hits if stem in kn)
        stat[P] = (len(hits), ok)
    if stat['FDA'][0] and stat['SDA'][0]:
        full = {P: stat[P][1] == stat[P][0] for P in stat}
        flag = 'FLAG' if full['FDA'] != full['SDA'] else ('BOTH_MISS' if not full['FDA'] else 'OK')
        rows.append((g['english'], g['kannada'], f"{stat['FDA'][1]}/{stat['FDA'][0]}", f"{stat['SDA'][1]}/{stat['SDA'][0]}", flag))
with open(os.path.join(H, 'KN_CROSS_PAPER_TERMS.tsv'), 'w', encoding='utf-8', newline='\n') as o:
    o.write('english\tglossary_kannada\tFDA_items_with_form\tSDA_items_with_form\tresult\n')
    for r in sorted(rows, key=lambda r: (r[4] != 'FLAG', r[4] != 'BOTH_MISS', r[0].casefold())): o.write('\t'.join(r) + '\n')
nt = collections.defaultdict(set)
for folder, P in (('kn_batches', 'FDA'), ('kn_batches_SDA', 'SDA')):
    for f in sorted(glob.glob(os.path.join(H, folder, 'NEW_TERMS_[0-9][0-9].tsv'))):
        for r in csv.DictReader(open(f, encoding='utf-8'), delimiter='\t', quoting=csv.QUOTE_NONE):
            if (r.get('english') or '').strip() and (r.get('kannada') or '').strip():
                nt[r['english'].strip().casefold()].add((r['kannada'].strip(), P + ' ' + os.path.basename(f)))
with open(os.path.join(H, 'KN_NEW_TERMS_ALL.tsv'), 'w', encoding='utf-8', newline='\n') as o:
    o.write('english\tkannada_forms\twhere\tresult\n')
    for e, v in sorted(nt.items()):
        forms = sorted({k for k, _ in v})
        o.write('\t'.join([e, ' | '.join(forms), ' | '.join(sorted(w for _, w in v)), 'CONFLICT' if len(forms) > 1 else 'ok']) + '\n')
c = collections.Counter(r[4] for r in rows)
print('terms in both papers', len(rows), dict(c), 'new terms', len(nt), 'new-term conflicts', sum(1 for v in nt.values() if len({k for k, _ in v}) > 1))
