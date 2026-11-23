"""Release polish for the ASTRA T1 question-and-solution masters (chat-surface verification of b01634f7, fixes F1, F2, F5, F6).
Applied to the whole markdown master just before it is written, English (build_t01_papers.py) and Kannada (build_kn_full.py).
No key, statement, option or fact changes: labels, layout lines and punctuation only.
 F1  one leftover letter list in FDA Q71's solution, exact replacement (count asserted)
 F2  Statement I/II items printed as two bold stem lines get the FDA Q6 layout: lead line, plain statements, operative line
 F5  English 'Statement-I', 'List-II' and the like become 'Statement I', 'List II'
 F6  spaced hyphen or ' -- ' used as a dash becomes an en dash; 'statement(s) is/are' becomes 'statements is/are'"""
import re

F1 = {'EN': [('Three pairs (a, b, c) are correct, which is option (c).', 'Three pairs (1, 2 and 3) are correct, which is option (c).')],
      'KN': [('ಮೂರು ಜೋಡಿಗಳು (a, b, c) ಸರಿ;', 'ಮೂರು ಜೋಡಿಗಳು (1, 2 ಮತ್ತು 3) ಸರಿ;')]}
LEAD = {'EN': ('Statement I', 'Statement II', 'Consider the following statements:',
               'Which one of the following is correct in respect of the above statements?'),
        'KN': ('ಹೇಳಿಕೆ I', 'ಹೇಳಿಕೆ II', 'ಈ ಕೆಳಗಿನ ಹೇಳಿಕೆಗಳನ್ನು ಪರಿಗಣಿಸಿ:',
               'ಮೇಲಿನ ಹೇಳಿಕೆಗಳಿಗೆ ಸಂಬಂಧಿಸಿದಂತೆ ಕೆಳಗಿನವುಗಳಲ್ಲಿ ಯಾವುದು ಸರಿ?')}

def polish(text, lang, paper, log=None):
    log = log if log is not None else []
    for old, new in (F1[lang] if paper == 'FDA' else []):
        n = text.count(old)
        if n != 1: raise SystemExit(f'F1 {lang}: expected 1 occurrence, found {n}: {old}')
        text = text.replace(old, new); log.append(('F1', 1))
    s1, s2, lead, op = LEAD[lang]
    pat = re.compile(r'^(\*\*\d+\.\*\* )\*\*' + s1 + r':\*\* (.+)\n\*\*' + s2 + r':\*\* (.+)\n\n(?=a\) )', re.M)
    text, n = pat.subn(lambda m: f'{m[1]}{lead}\n{s1}: {m[2]}\n{s2}: {m[3]}\n{op}\n', text); log.append(('F2', n))
    if lang == 'EN':
        text, n = re.subn(r'\b(Statement|List)-(I{1,3}|IV)\b', r'\1 \2', text); log.append(('F5', n))
    text, n1 = re.subn(r'(?<=\S) -- (?=\S)', ' – ', text)
    text, n2 = re.subn(r'(?<=[^\s|]) - (?=[^\s|])', ' – ', text)
    text, n3 = re.subn(r'statement\(s\) is/are', 'statements is/are', text)
    log.append(('F6', n1 + n2 + n3))
    return text
