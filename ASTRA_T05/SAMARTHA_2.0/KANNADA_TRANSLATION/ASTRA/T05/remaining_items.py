"""Resume helper (§516): list what is translated and cut what is not into new input files, so a second machine
translates only the remaining items.
- **Translated:** an item counts as translated if any OUT_NN*.jsonl in its folder holds it with both kn_text and kn_sol.
- **Merge:** every batch's parts are merged into OUT_NN.jsonl, in input order. Items still missing are simply absent.
- **Remaining:** for each batch with missing items, writes <folder>/IN_NN_REST.jsonl with only those items.
- **Status:** writes RESUME_STATUS.tsv.
Usage: python -I -X utf8 remaining_items.py"""
import json, glob, os
H = os.path.dirname(os.path.abspath(__file__))
rows = []
for d in ('kn_batches', 'kn_batches_SDA'):
    for nn in ('01', '02', '03', '04', '05'):
        inp = os.path.join(H, d, f'IN_{nn}.jsonl')
        items = [json.loads(l) for l in open(inp, encoding='utf-8') if l.strip()]
        got = {}
        for f in sorted(glob.glob(os.path.join(H, d, f'OUT_{nn}*.jsonl'))):
            if f.endswith('.v1.jsonl'): continue
            for l in open(f, encoding='utf-8'):
                try: r = json.loads(l)
                except Exception: continue
                if r.get('kn_text') and r.get('kn_sol'): got[r['id']] = r
        done = [got[x['id']] for x in items if x['id'] in got]
        rest = [x for x in items if x['id'] not in got]
        with open(os.path.join(H, d, f'OUT_{nn}.jsonl'), 'w', encoding='utf-8', newline='\n') as o:
            for r in done: o.write(json.dumps(r, ensure_ascii=False) + '\n')
        rp = os.path.join(H, d, f'IN_{nn}_REST.jsonl')
        if rest:
            with open(rp, 'w', encoding='utf-8', newline='\n') as o:
                for x in rest: o.write(json.dumps(x, ensure_ascii=False) + '\n')
        elif os.path.exists(rp): os.remove(rp)
        rows.append((d, nn, str(len(done)), str(len(items)), ' '.join(str(x['n']) for x in rest)))
with open(os.path.join(H, 'RESUME_STATUS.tsv'), 'w', encoding='utf-8', newline='\n') as o:
    o.write('folder\tbatch\tdone\ttotal\tremaining_question_numbers\n')
    for r in rows: o.write('\t'.join(r) + '\n')
for r in rows: print(*r)
print('TOTAL done', sum(int(r[2]) for r in rows), 'of', sum(int(r[3]) for r in rows))
