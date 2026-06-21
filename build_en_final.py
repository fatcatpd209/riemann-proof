import sys, io, os, re, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
root = r'd:\project\code\maths\黎曼猜想'

en_src = os.path.join(root, 'riemann_thesis_en_clean.md')
if not os.path.exists(en_src):
    en_src = os.path.join(root, 'riemann_thesis_en.md')
en_text = open(en_src, 'r', encoding='utf-8').read()
print('=== 英文 md ===')
print('源文件:', en_src)
print('字符数:', len(en_text))
print('has Layer 0:', 'Layer 0' in en_text)

en_html = os.path.join(root, 'riemann_en.html')
p = subprocess.Popen(
    ['pandoc', '--standalone', '--from', 'markdown', '--to', 'html5',
     '--wrap=preserve', '--mathml', '--highlight-style', 'pygments',
     '-o', en_html],
    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    cwd=root,
)
out, err = p.communicate(input=en_text.encode('utf-8'), timeout=180)
print('pandoc rc=', p.returncode)
if p.returncode != 0:
    print('stderr:', err.decode('utf-8','replace'))
else:
    with open(en_html, 'rb') as f:
        full = f.read()
    full = re.sub(rb'<meta[^>]*charset[^>]*>', b'<meta charset="UTF-8">', full, count=1)
    if b'charset' not in full[:2000]:
        full = full.replace(b'<head>', b'<head>\n<meta charset="UTF-8">', 1)
    open(en_html, 'wb').write(full)
    print('HTML size:', len(full), 'bytes')

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
    print('Docx saved:', os.path.getsize(en_docx), 'bytes')
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

print('\n=== 英文后处理 ===')
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
print('英文后处理完成: code_paras=', code_para, ' size=', os.path.getsize(en_docx))
print('\n最终英文:', en_docx)
