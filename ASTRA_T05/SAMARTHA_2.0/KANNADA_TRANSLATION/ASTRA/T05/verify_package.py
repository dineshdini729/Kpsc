"""Verify the continuation package on the second machine before any work starts (§516).
1. Every file listed in PACKAGE_MANIFEST.sha256 exists and has the recorded sha256. These are the frozen inputs, the glossary, the
   briefs, the scripts, the reference files and the translations at packaging time.
2. Python can import docx (python-docx) and pymupdf, and the Python version is printed for the record.
3. Self-test: build_kn_full.py --no-docx reproduces the main machine's gate on the packaged translations. Every issue must be MISSING
   (an untranslated item), never a defect in a translated item.
Prints PACKAGE OK, or the reasons it is not. Usage (from the repository root): python -I -X utf8 SAMARTHA_2.0/KANNADA_TRANSLATION/ASTRA/T05/verify_package.py"""
import hashlib, os, sys, subprocess, csv
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.normpath(os.path.join(H, '..', '..', '..', '..'))
bad = []
man = os.path.join(H, 'PACKAGE_MANIFEST.sha256')
n = 0
for line in open(man, encoding='utf-8'):
    if not line.strip(): continue
    h, p = line.rstrip('\n').split('  ', 1); n += 1
    fp = os.path.join(R, p)
    if not os.path.exists(fp): bad.append('missing ' + p); continue
    if hashlib.sha256(open(fp, 'rb').read()).hexdigest() != h: bad.append('changed ' + p)
print('manifest files checked', n)
for mod in ('docx', 'pymupdf'):
    try: __import__(mod)
    except Exception as e: bad.append(f'cannot import {mod}: {e} (pip install python-docx pymupdf)')
print('python', sys.version.split()[0])
r = subprocess.run([sys.executable, '-I', '-X', 'utf8', os.path.join(H, 'build_kn_full.py'), '--no-docx'], capture_output=True, text=True, encoding='utf-8')
if r.returncode: bad.append('build_kn_full.py failed: ' + r.stderr[-400:])
else:
    issues = list(csv.DictReader(open(os.path.join(H, 'KN_GATE1.tsv'), encoding='utf-8'), delimiter='\t'))
    other = [x for x in issues if x['issue'] != 'MISSING']
    print('self-test gate: MISSING', len(issues) - len(other), 'other', len(other))
    if other: bad.append(f'{len(other)} gate issues on translated items (see KN_GATE1.tsv)')
print('PACKAGE OK' if not bad else 'PACKAGE NOT OK:\n  ' + '\n  '.join(bad))
sys.exit(1 if bad else 0)
