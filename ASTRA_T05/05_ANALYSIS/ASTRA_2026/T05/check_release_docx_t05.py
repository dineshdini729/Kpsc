"""Release checks on the ASTRA Test 3 (internal T05) Word files; copied from T03/check_release_docx_t03.py (§494).
Changed from T1: test number, file names, the key file (out/T03_FINAL_KEYS.tsv), T03 item ids; a Kannada file not yet built is
skipped, so the English masters can be checked as soon as they are assembled.
Reads the .docx files themselves, not the markdown masters.
 1 questions: 100 autonumbered stems (List Number, one numbering list), options a)-d), key == ASTRA_T1_ANSWER_KEY.tsv
 2 Kannada 'ಸರಿಯಾದ ಆಯ್ಕೆ' letter == English key, every question
 3 solution structure: Correct Option, Justification, closing line, Result, Salient Features, Exam Fact, in that order
   (blank lines inside the solution are reported, not required: the binding spec says none)
 4 no internal text: process notes, item IDs, 'Gram Swaraj', relabel leftovers
 5 layout: match items carry a real table between stem and options; bullets are real list paragraphs
 7 no literal markdown ('*', '`', '# ') anywhere in the document (added 17-11-2026)
 8 no untypeset notation: \d^, raw mapped formulas, " x " between digits, raw units (added 18-11-2026)
Usage: python -I check_release_docx_t03.py [<out.tsv>]"""
import re, os, sys, csv, docx
from docx.text.paragraph import Paragraph
from docx.table import Table
H = os.path.dirname(os.path.abspath(__file__))
KN_DIR = os.path.normpath(os.path.join(H, '..', '..', '..', 'SAMARTHA_2.0', 'KANNADA_TRANSLATION', 'ASTRA', 'T05'))
FILES = {('FDA', 'EN'): os.path.join(H, 'ASTRA_T3_FDA_EN_Questions_and_Solutions.docx'),
         ('SDA', 'EN'): os.path.join(H, 'ASTRA_T3_SDA_EN_Questions_and_Solutions.docx'),
         ('FDA', 'KN'): os.path.join(KN_DIR, 'ASTRA_T3_FDA_KN_Questions_and_Solutions.docx'),
         ('SDA', 'KN'): os.path.join(KN_DIR, 'ASTRA_T3_SDA_KN_Questions_and_Solutions.docx')}
LAB = {'EN': dict(co=r'^Correct Option: \(([a-d])\)$', ju=r'^Justification:', cl=r'^Hence the correct answer is option \(([a-d])\)\.',
                  re_=r'^Result:', sf=r'^Salient Features:', ef=r'^Exam Fact:'),
       'KN': dict(co=r'^ಸರಿಯಾದ ಆಯ್ಕೆ: \(([a-d])\)$', ju=r'^ಸಮರ್ಥನೆ:', cl=r'^ಆದ್ದರಿಂದ ಸರಿಯಾದ ಉತ್ತರ ಆಯ್ಕೆ \(([a-d])\)\.',
                  re_=r'^ತೀರ್ಮಾನ:', sf=r'^ಪ್ರಮುಖ ಅಂಶಗಳು:', ef=r'^ಪರೀಕ್ಷಾ ಸಂಗತಿ:')}
ORDER = ['co', 'ju', 'cl', 're_', 'sf', 'ef']
FORBID = [(r'(?i)\bblind\b', 'process'), (r'(?i)\bsolvers?\b', 'process'), (r'(?i)\bcard [0-9a-f]{6}', 'process'),
          (r'(?i)\bcards?\b', 'process?'), (r'(?i)\bgate\b', 'process?'), (r'(?i)\bpacket\b', 'process?'),
          (r'ಕಾರ್ಡ್ [0-9a-f]{6}|ಬ್ಲೈಂಡ್|ಸಾಲ್ವರ್|ಗೇಟ್ ?\d', 'process'),
          (r'ಪ್ಯಾಕೆಟ್', 'process?'),   # review only, as 'packet' is in English (T2 SDA Q1: cigarette packets)
          (r'\bMP\d\d-Q\d+', 'item-id'), (r'T0[13]-|HKGA\d|NHKG', 'item-id'), (r'\b[0-9a-f]{6}#\d', 'item-id'),
          (r'(?i)Gram Swaraj|ಗ್ರಾಮ ಸ್ವರಾಜ್', 'act-title?'),
          (r'\bgives (?:only )?[a-d](?:,| and)\b', 'relabel'), (r'\bfor (?:pair )?[a-d]\b(?![\)\.])(?! \w)', 'relabel?'),
          (r'\bcl\. \d', 'relabel'), (r'\bclauses \d and \d', 'relabel'), (r'\bproviso \d\b', 'relabel'),
          (r'\([a-h]\)–\d', 'relabel'), (r'^\(\d\) ', 'relabel'), (r'(?i)\boption \(\d\)', 'relabel'),
          (r'\([a-e], [a-e]', 'relabel'),                                     # F1
          (r'\b(Statement|List)-(I{1,3}|IV)\b', 'label'),                     # F5
          (r'(?<=\S) -- (?=\S)|(?<=[^\s|]) - (?=[^\s|])', 'dash'),            # F6
          (r'statement\(s\)', 'wording'),                                    # F6
          (r'\*|`|^#{1,6} ', 'markdown')]                                   # 7: literal markdown (17-11-2026)

def body_items(d):
    for el in d.element.body.iterchildren():
        t = el.tag.split('}')[1]
        if t == 'p': yield Paragraph(el, d)
        elif t == 'tbl': yield Table(el, d)

def numid(p):
    n = p._p.pPr.numPr if p._p.pPr is not None else None
    return (n.numId.val if n is not None and n.numId is not None else 'style')

def split_questions(d):
    qs, cur = [], None
    for it in body_items(d):
        if isinstance(it, Paragraph) and it.style.name == 'List Number':
            cur = {'stem': it, 'items': []}; qs.append(cur)
        elif cur is not None:
            cur['items'].append(it)
    return qs

def main(out):
    key = {}
    for r in csv.DictReader(open(os.path.join(H, 'out', 'T05_FINAL_KEYS.tsv'), encoding='utf-8'), delimiter='\t'):
        key[(r['paper'], int(r['q']))] = r['key'].strip()
    rows, summary, letters = [], [], {}
    for (P, L), fn in FILES.items():
        if not os.path.exists(fn): summary.append(f'{P} {L}: not built yet, skipped'); continue
        d = docx.Document(fn); qs = split_questions(d); lab = LAB[L]
        issues = 0
        def bad(q, check, msg):
            nonlocal issues; issues += 1; rows.append((P, L, q, check, msg))
        if len(qs) != 100: bad(0, '1', f'{len(qs)} autonumbered stems')
        # F4: document properties and parts
        cp = d.core_properties
        props = ' '.join(str(x) for x in (cp.author, cp.last_modified_by, cp.comments, cp.title, cp.subject, cp.keywords, cp.category))
        if 'python-docx' in props.lower() or cp.author != 'InstaKAS' or not cp.title.startswith('ASTRA Test 3'):
            bad(0, '6', f'document properties: author={cp.author!r} title={cp.title!r} comments={cp.comments!r}')
        if not cp.created or cp.created.year < 2026 or not cp.modified or cp.modified.year < 2026:
            bad(0, '6', f'document dates created={cp.created} modified={cp.modified}')
        if any('thumbnail' in str(pt.partname) for pt in d.part.package.iter_parts()):
            bad(0, '6', 'thumbnail part present')
        heads = [p.text for p in d.paragraphs if re.match(r'^(Part [AB]:|ಭಾಗ [AB]:)', p.text)]
        if len(heads) != 2: bad(0, '5', f'part headings {len(heads)} (want Part A and Part B)')
        # 7: literal markdown anywhere in the document (paragraphs, headers, table cells): the T1 converter printed
        # '*italic*' and nested '***' runs literally; the chat surface found 2, the full scan found 52 (17-11-2026)
        allp = list(d.paragraphs) + [pp for t in d.tables for r in t.rows for c in r.cells for pp in c.paragraphs]
        for sec in d.sections: allp += list(sec.header.paragraphs) + list(sec.footer.paragraphs)
        md = [pp.text for pp in allp if re.search(r'\*|`|^#{1,6} ', pp.text)]
        if md: bad(0, '7', f'{len(md)} paragraphs with literal markdown, first: {md[0][:80]}')
        # 8: untypeset scientific notation (format re-verification 18-11-2026 §B): '\d^', a mapped formula in raw form,
        # ' x ' between digits, raw units. Names with digits (K-1 cultivar, B12, PSLV-C30, S2I2, F2 ...) are not in the map.
        RAW = r'\d\^|(?<![A-Za-z0-9])(?:NaHCO3|Na2CO3|CaSO4|CuSO4|CaOCl2|CuFeS2|ZnCO3|BeF2|Cu2S|BCl3|CH4|NH3|H2O|CO2|IP3|O2|N2|H2)(?![A-Za-z0-9])' \
              r'|(?<=\d) x (?=\d)|kg-1|ohm m|deg C'
        raw = [(pp.text, m.group()) for pp in allp for m in [re.search(RAW, pp.text)] if m]
        if raw: bad(0, '8', f'{len(raw)} paragraphs with untypeset notation, first: {raw[0][1]!r} in {raw[0][0][:80]}')
        nids = {numid(q['stem']) for q in qs}
        if len(nids) != 1: bad(0, '1', f'stems use {len(nids)} numbering lists {nids}')
        spread = {}
        for n, q in enumerate(qs, 1):
            items = q['items']; paras = [i for i in items if isinstance(i, Paragraph)]
            texts = [p.text for p in paras]
            # options
            ci = next((k for k, t in enumerate(texts) if re.match(lab['co'], t)), None)
            qpart = texts[:ci] if ci is not None else texts
            opts = [t[:2] for t in qpart if re.match(r'^[a-d]\) ', t)]
            if opts != ['a)', 'b)', 'c)', 'd)']: bad(n, '1', f'options {opts}')
            if any(re.match(r'^\(?[1-4]\) ', t) for t in qpart): bad(n, '1', 'numeric option label')
            # key
            if ci is None: bad(n, '3', 'no Correct Option line'); continue
            k = re.match(lab['co'], texts[ci]).group(1)
            letters[(P, L, n)] = k; spread[k] = spread.get(k, 0) + 1
            if k != key[(P, n)]: bad(n, '1', f'key {k} != answer key {key[(P, n)]}')
            # structure
            pos = {}
            for tag in ORDER:
                hit = [j for j, t in enumerate(texts) if re.match(lab[tag], t)]
                if len(hit) != 1: bad(n, '3', f'{tag} found {len(hit)}x')
                elif tag != 'co' or True: pos[tag] = hit[0]
            if all(t in pos for t in ORDER):
                seq = [pos[t] for t in ORDER]
                if seq != sorted(seq): bad(n, '3', f'section order {seq}')
                m = re.match(lab['cl'], texts[pos['cl']])
                if m and m.group(1) != k: bad(n, '3', f'closing line {m.group(1)} != {k}')
                # F3 layout: two blanks before Correct Option; exactly one blank before Justification, Result,
                # Salient Features, Exam Fact; none elsewhere inside the solution; two blanks after the question
                def blanks_before(par):
                    j = items.index(par); c = 0
                    while j - 1 - c >= 0 and isinstance(items[j - 1 - c], Paragraph) and not items[j - 1 - c].text.strip(): c += 1
                    return c
                if blanks_before(paras[pos['co']]) != 2: bad(n, '3', f"{blanks_before(paras[pos['co']])} blank lines before Correct Option (want 2)")
                for tag in ('ju', 're_', 'sf', 'ef'):
                    b = blanks_before(paras[pos[tag]])
                    if b != 1: bad(n, '3', f'{b} blank lines before {tag} (want 1)')
                gap_heads = {pos[t] for t in ('ju', 're_', 'sf', 'ef')}
                stray = [j for j in range(pos['co'] + 1, pos['ef']) if not texts[j].strip() and j + 1 not in gap_heads
                         and not (isinstance(items[items.index(paras[j]) - 1], Table))]
                if stray: bad(n, '3', f'{len(stray)} stray blank line(s) inside solution')
                tail = items[items.index(paras[pos['ef']]) + 1:]
                tb = 0
                while tb < len(tail) and isinstance(tail[tb], Paragraph) and not tail[tb].text.strip(): tb += 1
                nxt_head = tb < len(tail) and isinstance(tail[tb], Paragraph) and re.match(r'^(Part [AB]:|ಭಾಗ [AB]:)', tail[tb].text)
                if tail[tb:] and not nxt_head: bad(n, '3', 'content after Exam Fact')
                elif not nxt_head and tb != 2: bad(n, '3', f'{tb} blank lines after the solution (want 2)')
            # F2: Statement I/II items: bold lead line as the stem, plain statements, bold operative line before the options
            s1 = 'Statement I:' if L == 'EN' else 'ಹೇಳಿಕೆ I:'
            si = [p for p in paras[:ci] if p.text.startswith(s1) or p.text.startswith(s1.replace(' I:', ' II:'))]
            if si or re.search(r'^(\*\*)?(Statement|ಹೇಳಿಕೆ) I\b', q['stem'].text):
                lead = 'Consider the following statements:' if L == 'EN' else 'ಈ ಕೆಳಗಿನ ಹೇಳಿಕೆಗಳನ್ನು ಪರಿಗಣಿಸಿ:'
                if q['stem'].text.strip() != lead: bad(n, '5', f'Statement I/II item: stem is not the lead line')
                if len(si) != 2: bad(n, '5', f'Statement I/II item: {len(si)} statement lines outside the stem')
                if any(r.bold for p in si for r in p.runs if r.text.strip()): bad(n, '5', 'Statement I/II item: statements printed bold')
                fo = next((k for k, p in enumerate(paras) if re.match(r'^a\) ', p.text)), None)
                op = paras[fo - 1] if fo else None
                opre = r'^Which one of the following is correct (in respect of|with respect to) the above statements\?$' if L == 'EN' else r'^ಮೇಲಿನ ಹೇಳಿಕೆಗಳಿಗೆ ಸಂಬಂಧಿಸಿದಂತೆ'
                if op is None or not re.match(opre, op.text) or not all(r.bold for r in op.runs if r.text.strip()):
                    bad(n, '5', 'Statement I/II item: no bold operative line before the options')
            # blank lines inside the question part (spec: none, except one after a table)
            for j, t in enumerate(qpart):
                if not t.strip() and j < len(qpart) - 2:
                    prev = items[items.index(paras[j]) - 1] if items.index(paras[j]) > 0 else None
                    if not isinstance(prev, Table): bad(n, '5', 'blank line inside question')
            # tables: match items
            stem = q['stem'].text
            # T2: a List I / List II item, not any stem with the word "match" (direct items such as "Select the INCORRECT match ..."
            # were false positives on the T1 rule)
            is_match = bool(re.search(r'List[- ]I\b|ಪಟ್ಟಿ I\b|ಪಟ್ಟಿ-I', stem))
            first_opt = next((i for i in items if isinstance(i, Paragraph) and re.match(r'^a\) ', i.text)), None)
            pre = items[:items.index(first_opt)] if first_opt is not None else []
            has_tbl = any(isinstance(i, Table) for i in pre)
            if is_match and not has_tbl: bad(n, '5', 'match item without a table')
            if any(re.match(r'^\s*\|', t) for t in texts) or '|---' in stem: bad(n, '5', 'markdown table text')
            if any(re.match(r'^[-*•] ', t) for t in texts): bad(n, '5', 'typed bullet, not a list paragraph')
            # forbidden text, whole question + solution incl. tables
            alltext = [stem] + texts
            for i in items:
                if isinstance(i, Table):
                    alltext += [c.text for r in i.rows for c in r.cells]
            for t in alltext:
                for pat, kind in FORBID:
                    for m in re.finditer(pat, t, flags=re.M):
                        ctx = t[max(0, m.start() - 50):m.end() + 50].replace('\t', ' ')
                        if kind.endswith('?'): rows.append((P, L, n, '4-review', f'{kind} | {ctx}'))
                        else: bad(n, '4', f'{kind} | {ctx}')
        summary.append(f'{P} {L}: stems {len(qs)}, numbering lists {len(nids)}, key spread {dict(sorted(spread.items()))}, hard issues {issues}')
    for P in ('FDA', 'SDA'):
        diff = [n for n in range(1, 101) if letters.get((P, 'KN', n)) != letters.get((P, 'EN', n))]
        if not any(k[1] == 'KN' for k in letters): continue
        summary.append(f'{P} KN letter == EN letter: {100 - len(diff)}/100' + (f' differ {diff}' if diff else ''))
        if diff: rows.append((P, 'KN', 0, '2', f'letters differ {diff}'))
    with open(out, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, delimiter='\t'); w.writerow(['paper', 'lang', 'q', 'check', 'detail'])
        for s in summary: w.writerow(['SUMMARY', '', '', '', s])
        w.writerows(rows)
    print('\n'.join(s.encode('ascii', 'replace').decode() for s in summary))

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(H, 'out', 'RELEASE_CHECK.tsv'))
