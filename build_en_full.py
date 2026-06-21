import sys, io, os, re, subprocess, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
root = r'd:\project\code\maths\黎曼猜想'
chunk_dir = os.path.join(root, 'chunks')

chunks = []
for name in ['en_chunk_A.md','en_chunk_B.md','en_chunk_C.md','en_chunk_D.md','en_chunk_E.md']:
    p = os.path.join(chunk_dir, name)
    if os.path.exists(p):
        c = open(p, 'r', encoding='utf-8').read()
        chunks.append(c)
        print(f'{name}: {len(c)} chars')
    else:
        print(f'MISSING: {name}')
full_en = '\n\n'.join(chunks)
en_md_full = os.path.join(root, 'riemann_thesis_en_full.md')
open(en_md_full, 'w', encoding='utf-8').write(full_en)
print(f'\nFull EN md: {len(full_en)} chars -> {en_md_full}')
print(f'  has Layer 0: {"Layer 0" in full_en}')
print(f'  has Axiomatic Foundation: {"Axiomatic Foundation" in full_en}')
cjk_count = sum(1 for c in full_en if 0x4E00 <= ord(c) <= 0x9FFF)
print(f'  CJK remaining: {cjk_count}')

en_html = os.path.join(root, 'riemann_en_full.html')
p = subprocess.Popen(
    ['pandoc', '--standalone', '--from', 'markdown', '--to', 'html5',
     '--wrap=preserve', '--mathml', '--highlight-style', 'pygments',
     '-o', en_html],
    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    cwd=root,
)
out, err = p.communicate(input=full_en.encode('utf-8'), timeout=240)
print(f'\npandoc rc={p.returncode}')
if p.returncode != 0:
    print('stderr:', err.decode('utf-8','replace'))
else:
    with open(en_html, 'rb') as f:
        full = f.read()
    full = re.sub(rb'<meta[^>]*charset[^>]*>', b'<meta charset="UTF-8">', full, count=1)
    if b'charset' not in full[:2000]:
        full = full.replace(b'<head>', b'<head>\n<meta charset="UTF-8">', 1)
    open(en_html, 'wb').write(full)
    print(f'HTML size: {len(full)} bytes')

import win32com.client, pythoncom
pythoncom.CoInitialize()
word = win32com.client.Dispatch('Word.Application')
word.Visible = False
word.DisplayAlerts = 0
en_docx = os.path.join(root, 'riemann_thesis_en.docx')
try:
    doc = word.Documents.Open(en_html, ReadOnly=True)
    doc.SaveAs(en_docx, FileFormat=16)
    doc.Close(False)
    print(f'\nWord saved: {en_docx}  {os.path.getsize(en_docx)} bytes')
except Exception as e:
    print('Word failed:', e)
finally:
    try:
        word.Quit()
    except Exception:
        pass
    try:
        pythoncom.CoUninitialize()
    except Exception:
        pass

from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.text.run import Run

doc = Document(en_docx)
for sec in doc.sections:
    sec.top_margin = Cm(1.8)
    sec.bottom_margin = Cm(1.8)
    sec.left_margin = Cm(1.8)
    sec.right_margin = Cm(1.8)
ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

def set_run_fonts(run, ascii_font, ascii_size, east_font, east_size):
    rPr = run._element.find('w:rPr', ns)
    if rPr is None:
        rPr = run._element.makeelement('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}rPr', {})
        run._element.insert(0, rPr)
    for child in list(rPr):
        if child.tag.endswith('rFonts'):
            rPr.remove(child)
    rf = rPr.makeelement('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}rFonts', {
        '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}ascii': ascii_font,
        '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}hAnsi': ascii_font,
        '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}eastAsia': east_font,
    })
    rPr.insert(0, rf)
    sz = rPr.find('w:sz', ns)
    if sz is None:
        sz = rPr.makeelement('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}sz', {})
        rPr.append(sz)
    sz.set('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val', str(int(ascii_size.pt*2)))
    cs = rPr.find('w:szCs', ns)
    if cs is None:
        cs = rPr.makeelement('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}szCs', {})
        rPr.append(cs)
    cs.set('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val', str(int(east_size.pt*2)))

def split_run(run):
    t = run.text
    if t == '':
        return [run]
    spans = []
    cur = None; start = 0
    for i, ch in enumerate(t):
        c = 'A' if ord(ch) < 128 else 'N'
        if cur is None:
            cur = c; start = i
        elif c != cur:
            spans.append((cur,start,i)); cur = c; start = i
    spans.append((cur,start,len(t)))
    if len(spans) == 1:
        return [run]
    parent = run._element.getparent()
    idx = parent.index(run._element)
    new_runs = []
    for cls, s, e in spans:
        r_elem = run._element.makeelement(run._element.tag, run._element.attrib)
        t_elem = r_elem.makeelement('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t', {})
        t_elem.text = t[s:e]
        r_elem.append(t_elem)
        parent.insert(idx, r_elem); idx += 1
        new_runs.append(Run(r_elem, run._parent))
    parent.remove(run._element)
    return new_runs

code_para = 0
for para in doc.paragraphs:
    style = (para.style.name if para.style else '').lower()
    is_code = ('code' in style or 'source' in style or 'verbatim' in style or 'preformatted' in style)
    if is_code:
        pPr = para._element.find('w:pPr', ns)
        if pPr is None:
            pPr = para._element.makeelement('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}pPr', {})
            para._element.insert(0, pPr)
        wrap = pPr.find('w:wrap', ns)
        if wrap is None:
            wrap = pPr.makeelement('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}wrap', {'{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val': 'linesAndChars'})
            pPr.append(wrap)
        para.alignment = WD_ALIGN_PARAGRAPH.LEFT
        code_para += 1
    for r in list(para.runs):
        for r2 in split_run(r):
            has_cjk = any(ord(c)>=128 for c in r2.text)
            if is_code:
                set_run_fonts(r2, 'Consolas', Pt(9), 'Calibri', Pt(9))
            else:
                set_run_fonts(r2, 'Calibri', Pt(11), 'Calibri', Pt(11))
doc.save(en_docx)
print(f'\n后处理完成: code_paras={code_para}  size={os.path.getsize(en_docx)}')

import zipfile, xml.etree.ElementTree as ET
with zipfile.ZipFile(en_docx,'r') as z:
    doc_xml = z.read('word/document.xml').decode('utf-8', errors='replace')
ns2 = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
root_xml = ET.fromstring(doc_xml.encode('utf-8','replace'))
body = root_xml.find('w:body', ns2)
paras = body.findall('w:p', ns2)
print(f'\n=== VERIFY ===')
print('paragraphs:', len(paras))
found = {}
for k in ['Layer 0','Axiomatic Foundation','S-Axiom','Palais-Smale','Friedrichs','DBN','self-adjoint']:
    found[k] = 0
for p in paras:
    t = ''.join(et.text or '' for et in p.findall('.//w:t', ns2))
    for k in list(found.keys()):
        if k in t:
            found[k] += 1
for k,v in found.items():
    print(' ', k, ':', v)

print(f'\n最终英文: {en_docx}')
