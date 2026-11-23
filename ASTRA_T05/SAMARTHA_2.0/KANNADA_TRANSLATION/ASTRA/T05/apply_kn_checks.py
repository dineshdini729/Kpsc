"""Apply the back-check corrections (kn_batches/CHECK_NN.tsv) to kn_batches/OUT_NN.jsonl.
A row is applied only when its `kannada_text` equals the current line exactly (at `line_no`, else the unique equal line in
that part); the suggested line must keep the line's '**' count. Rows listed in KN_SKIP_ROWS.tsv (id, part, line_no, reason) are not
applied (Claude Code's disposition). The first run saves OUT_NN.v1.jsonl (the translator's text) and is never overwritten.
Log: KN_CHECK_APPLIED_<folder>.tsv. Usage: python -I apply_kn_checks.py [kn_batches|kn_batches_SDA]"""
import json, os, glob, shutil, csv, sys
H = os.path.dirname(os.path.abspath(__file__)); FOLD = sys.argv[1] if len(sys.argv) > 1 else 'kn_batches'; B = os.path.join(H, FOLD)
skip = set()
sp = os.path.join(H, 'KN_SKIP_ROWS.tsv')
if os.path.exists(sp):
    for r in csv.DictReader(open(sp, encoding='utf-8'), delimiter='\t'): skip.add((r['id'], r['part'], r['line_no']))
log = []
for cf in sorted(glob.glob(os.path.join(B, 'CHECK_[0-9][0-9].tsv'))):
    nn = cf[-6:-4]; of = os.path.join(B, f'OUT_{nn}.jsonl'); v1 = os.path.join(B, f'OUT_{nn}.v1.jsonl')
    if not os.path.exists(v1): shutil.copy(of, v1)
    items = [json.loads(l) for l in open(v1, encoding='utf-8') if l.strip()]
    by = {x['id']: x for x in items}
    for r in csv.DictReader(open(cf, encoding='utf-8'), delimiter='\t', quoting=csv.QUOTE_NONE):
        q = (r.get('queue') or '').strip().upper()
        if q not in ('A', 'B', 'QUEUE A', 'QUEUE B'): continue
        i, part, ln = r['id'].strip(), r['part'].strip(), (r['line_no'] or '').strip()
        old, new = r['kannada_text'], r['suggested_kannada']
        if (i, part, ln) in skip: log.append((nn, i, part, ln, q, 'SKIPPED_BY_DISPOSITION')); continue
        x = by.get(i); fld = 'kn_text' if part == 'Q' else 'kn_sol'
        if not x or fld not in x or not new or new == '-': log.append((nn, i, part, ln, q, 'NO_TARGET')); continue
        lines = x[fld].split('\n')
        k = int(ln) - 1 if ln.isdigit() else -1
        if not (0 <= k < len(lines) and lines[k] == old):
            hits = [j for j, l in enumerate(lines) if l == old]
            k = hits[0] if len(hits) == 1 else -1
        if k < 0: log.append((nn, i, part, ln, q, 'LINE_NOT_MATCHED')); continue
        if new.count('**') != old.count('**'): log.append((nn, i, part, ln, q, 'BOLD_COUNT_CHANGED')); continue
        lines[k] = new; x[fld] = '\n'.join(lines); log.append((nn, i, part, str(k + 1), q, 'APPLIED'))
    # Claude Code's own recorded fixes (KN_MANUAL_FIXES.tsv: id, field, old, new, reason), applied after the check rows
    mp = os.path.join(H, 'KN_MANUAL_FIXES.tsv')
    if os.path.exists(mp):
        for r in csv.DictReader(open(mp, encoding='utf-8'), delimiter='\t', quoting=csv.QUOTE_NONE):
            x = by.get(r['id'])
            if not x: continue
            if r['old'] in x.get(r['field'], ''):
                x[r['field']] = x[r['field']].replace(r['old'], r['new']); log.append((nn, r['id'], r['field'], '-', 'MANUAL', 'APPLIED'))
            else:
                log.append((nn, r['id'], r['field'], '-', 'MANUAL', 'NOT_FOUND'))
    with open(of, 'w', encoding='utf-8', newline='\n') as o:
        for x in items: o.write(json.dumps(x, ensure_ascii=False) + '\n')
with open(os.path.join(H, f'KN_CHECK_APPLIED_{FOLD}.tsv'), 'w', encoding='utf-8', newline='\n') as o:
    o.write('batch\tid\tpart\tline_no\tqueue\tresult\n')
    for r in log: o.write('\t'.join(r) + '\n')
import collections
print(collections.Counter(r[-1] for r in log))
