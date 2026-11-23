"""Render T05_<PAPER>_EN_QS.md (ASTRA Test 3, internal T05; copied from T03/build_t03_docx.py, test number and file names changed, §494) to Word per 05_ANALYSIS/ASTRA_2026/ASTRA_PRESENTATION_SPEC.md (SAMARTHA/YASHASVI presentation).
Question: stem autonumbered (List Number, one continuous list 1-100) and bold; statements and options plain; any other line
(operative / Select / Codes) bold; match table straight after the stem, Table Grid, bold header row, one blank after it;
no other blank inside a question. Solution: two blanks; bold 'Correct Option: (x)'; bold 'Justification:'; lines with
**bold** leads and keywords rendered as runs; 'Hence the correct answer is **option (x)**.'; Result / Exam Fact bold leads;
'Salient Features: ...' bold; bullets as List Bullet with bold lead; markdown tables as Word tables; two blanks between
questions. Times New Roman 11 (English); Nirmala UI 11 for the Kannada edition (T05_<P>_KN_QS.md, OR-AI precedent).
Usage: python -I build_t03_docx.py [KN]"""
import re, os, sys, docx, datetime
from docx.shared import Pt
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
H =os.path.dirname(os.path.abspath(__file__))
LANG = 'KN' if 'KN' in sys.argv[1:] else 'EN'
FONT = 'Nirmala UI' if LANG == 'KN' else 'Times New Roman'
CO = r'(?:Correct Option|ಸರಿಯಾದ ಆಯ್ಕೆ)'
HEADS = r'^\*\*(Correct Option|Justification|Salient Features|ಸರಿಯಾದ ಆಯ್ಕೆ|ಸಮರ್ಥನೆ|ಪ್ರಮುಖ ಅಂಶಗಳು)'
SECTION_GAP = r'^\*\*(Justification|Result|Salient Features|Exam Fact|ಸಮರ್ಥನೆ|ತೀರ್ಮಾನ|ಪ್ರಮುಖ ಅಂಶಗಳು|ಪರೀಕ್ಷಾ ಸಂಗತಿ)(?=[:*])'
# Notation typesetting (format re-verification 18-11-2026 §B), applied to the whole master text before rendering, both languages.
# Explicit map only: names with digits (Pusa Snowball K-1, vitamins B1/B3/B12, PSLV-C30, LVM3-M5, VIKRAM3201, T2T, F57, A24,
# K-15, S2I2, F1/F2 generations, C4 plants, N6-furfurylamino, ratios such as 1:8) are not in the map and are left as written.
FORMULAS = ['NaHCO3', 'Na2CO3', 'CaSO4', 'CuSO4', 'CaOCl2', 'CuFeS2', 'ZnCO3', 'BeF2', 'Cu2S', 'BCl3', 'CH4', 'NH3', 'H2O',
            'CO2', 'IP3', 'O2', 'N2', 'H2']
SUB = str.maketrans('0123456789', '₀₁₂₃₄₅₆₇₈₉'); SUP = str.maketrans('0123456789-', '⁰¹²³⁴⁵⁶⁷⁸⁹⁻')
def typeset(t):
    t = re.sub(r'·(\d+|½)H2O', lambda m: '·' + m[1] + 'H₂O', t)               # hydrates: coefficient stays, H2O typeset
    for f in FORMULAS:
        t = re.sub(r'(?<![A-Za-z0-9])' + f + r'(?![A-Za-z0-9])', f.translate(SUB), t)
    t = re.sub(r'(?<=\d)\^(-?\d+)', lambda m: m[1].translate(SUP), t)           # 10^8 -> 10⁸, 10^-3 -> 10⁻³
    t = re.sub(r'(?<=\d) x (?=\d)', ' × ', t)
    t = t.replace('kg-1 K-1', 'kg⁻¹ K⁻¹').replace('ohm m', 'Ω m').replace('deg C', '°C')
    return t
def runs(p, text, bold_all=False):
    """Markdown emphasis to Word runs: '**' toggles bold, '*' toggles italic (species names), nested runs included.
    A '***' closes italic first when italic is open ('*Papaver somniferum***'), else opens bold then italic
    ('***Mangifera* is the genus**'). Fixed 17-11-2026: the T1 converter handled '**' only, so italics printed as literal '*'."""
    bold = ital = False; buf = []; segs = []
    def flush():
        if buf: segs.append((''.join(buf), bold, ital)); buf.clear()
    i = 0
    while i < len(text):
        if text.startswith('***', i):
            flush()
            if ital: ital = False; bold = not bold
            else: bold = not bold; ital = not ital
            i += 3
        elif text.startswith('**', i): flush(); bold = not bold; i += 2
        elif text[i] == '*': flush(); ital = not ital; i += 1
        else: buf.append(text[i]); i += 1
    flush()
    for s, b, it_ in segs:
        r = p.add_run(s); r.bold = bold_all or b; r.italic = it_ or None; r.font.name = FONT
        r._element.get_or_add_rPr().get_or_add_rFonts().set(qn('w:cs'), FONT)
def para(d, text='', bold=False, style=None):
    p = d.add_paragraph(style=style) if style else d.add_paragraph()
    pf = p.paragraph_format; pf.space_before = Pt(0); pf.space_after = Pt(0)
    if text: runs(p, text, bold)
    return p
def table(d, rows):
    t = d.add_table(rows=len(rows), cols=max(len(r) for r in rows)); t.style = 'Table Grid'
    for i, row in enumerate(rows):
        for j, c in enumerate(row):
            cell = t.cell(i, j); cell.text = ''
            p = cell.paragraphs[0]; runs(p, c, bold_all=(i == 0))
    return t
def md_rows(lines):
    return [[c.strip() for c in l.strip().strip('|').split('|')] for l in lines if not re.fullmatch(r'\|[\s:\-|]+\|?', l.strip())]
def build(P):
    src = typeset(open(os.path.join(H, f'T05_{P}_{LANG}_QS.md'), encoding='utf-8').read())
    d = docx.Document()
    st = d.styles['Normal']; st.font.name = FONT; st.font.size = Pt(11)
    st.element.rPr.rFonts.set(qn('w:eastAsia'), FONT); st.element.rPr.rFonts.set(qn('w:cs'), FONT)
    if LANG == 'KN':
        paper = 'ಪ್ರಥಮ ದರ್ಜೆ ಸಹಾಯಕ (FDA)' if P == 'FDA' else 'ದ್ವಿತೀಯ ದರ್ಜೆ ಸಹಾಯಕ (SDA)'
        title = ('ಅಸ್ತ್ರ (ASTRA) — KEA FDA/SDA ಪರೀಕ್ಷಾ ಸರಣಿ', f'ಪರೀಕ್ಷೆ 3 | {paper} | ಸಾಮಾನ್ಯ ಜ್ಞಾನ', 'ಪ್ರಶ್ನೆಗಳು ಮತ್ತು ಪರಿಹಾರಗಳು')
    else:
        paper = 'First Division Assistant (FDA)' if P == 'FDA' else 'Second Division Assistant (SDA)'
        title = ('ASTRA — KEA FDA/SDA Test Series', f'Test 3 | {paper} | General Knowledge', 'Questions and Solutions')
    for t in title:
        para(d, t, bold=True)
    blocks = re.split(r'\n---\n', src)
    for blk in blocks:
        blk = blk.strip()
        if not blk: continue
        for line in blk.split('\n'):
            if line.startswith('## Part') or line.startswith('## ಭಾಗ'):
                para(d); h = para(d, line[3:], bold=True); b = para(d)
                h.paragraph_format.keep_with_next = True; b.paragraph_format.keep_with_next = True   # §C: heading stays with Q1 of its part
        m = re.search(r'^\*\*(\d+)\.\*\* (.*?)\n\n(\*\*' + CO + r'.*)$', blk, re.M | re.S)
        if not m: continue
        q, sol = m[2], m[3]
        qlines = q.split('\n'); i = 0; stem_done = False; qp = []   # F1 (release verification, §501): keep each question together to option d)
        while i < len(qlines):
            l = qlines[i]
            if not l.strip(): i += 1; continue
            if l.strip().startswith('|'):
                tl = []
                while i < len(qlines) and qlines[i].strip().startswith('|'): tl.append(qlines[i]); i += 1
                t = table(d, md_rows(tl))
                for row in t.rows:
                    row._tr.get_or_add_trPr().append(OxmlElement('w:cantSplit'))
                    for cell in row.cells:
                        for cpar in cell.paragraphs: cpar.paragraph_format.keep_with_next = True
                qp.append(para(d)); continue
            if not stem_done:
                qp.append(para(d, l.strip(), bold=True, style='List Number')); stem_done = True
            elif re.match(r'^(\d+\.|[a-d]\)|(?:Statement|ಹೇಳಿಕೆ)[ -]?(?:I|II|III):?)\s', l.strip()):
                qp.append(para(d, l.strip()))
            else:
                qp.append(para(d, l.strip(), bold=True))
            i += 1
        for qpar in qp:
            if not qpar.text.startswith('d) '): qpar.paragraph_format.keep_with_next = True
        para(d); para(d)
        slines = sol.split('\n'); i = 0
        while i < len(slines):
            l = slines[i].rstrip()
            if not l.strip(): i += 1; continue
            if l.strip().startswith('|'):
                tl = []
                while i < len(slines) and slines[i].strip().startswith('|'): tl.append(slines[i]); i += 1
                table(d, md_rows(tl)); continue
            s = l.strip()
            if re.match(SECTION_GAP, s): para(d)   # F3: one blank line before Justification, Result, Salient Features, Exam Fact
            if re.match(r'^[-*] ', s):
                para(d, s[2:], style='List Bullet')
            elif re.match(HEADS, s):
                para(d, s.replace('**', ''), bold=True)
            elif s.startswith('Hence the correct answer is'):
                para(d, re.sub(r'\**option \(([a-d])\)\**', r'**option (\1)**', s))
            elif s.startswith('ಆದ್ದರಿಂದ ಸರಿಯಾದ ಉತ್ತರ'):
                para(d, re.sub(r'\**ಆಯ್ಕೆ \(([a-d])\)\**', r'**ಆಯ್ಕೆ (\1)**', s))
            else:
                para(d, s)
            i += 1
        para(d); para(d)
    fn = os.path.join(H, f'ASTRA_T3_{P}_{LANG}_Questions_and_Solutions.docx')
    clean_properties(d, P)
    d.save(fn); return fn
def clean_properties(d, P):
    """F4: no python-docx traces in File > Properties; no stock thumbnail."""
    cp = d.core_properties
    cp.title = f"ASTRA Test 3 – {P} – Questions and Solutions ({'Kannada' if LANG == 'KN' else 'English'})"
    cp.author = cp.last_modified_by = 'InstaKAS'
    cp.comments = cp.subject = cp.keywords = cp.category = ''
    stamp = datetime.datetime.combine(datetime.date.today(), datetime.time(0, 0))
    cp.created = cp.modified = stamp; cp.revision = 1
    pkg = d.part.package
    for rId, rel in list(pkg.rels.items()):
        if rel.reltype.endswith('/thumbnail'): pkg.rels.pop(rId)
for P in [p for p in ('FDA', 'SDA') if os.path.exists(os.path.join(H, f'T05_{p}_{LANG}_QS.md'))]:
    print(build(P))
