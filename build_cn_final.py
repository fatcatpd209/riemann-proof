import sys, io, os, re, subprocess, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
root = r'd:\project\code\maths\黎曼猜想'

cn_src = os.path.join(root, 'riemann_thesis-standard.md')
cn_text = open(cn_src, 'r', encoding='utf-8').read()
print('=== 中文 md 确认 ===')
print('大小:', len(cn_text), '字符')
print('真实三类标注:', '三类标注' in cn_text)
print('Layer 0:', 'Layer 0' in cn_text)
idx = cn_text.find('Layer 0')
print('Layer 0 上下文:', cn_text[idx:idx+120])

cn_html = os.path.join(root, 'riemann_cn.html')
p = subprocess.Popen(
    ['pandoc', '--standalone', '--from', 'markdown', '--to', 'html5',
     '--wrap=preserve', '--mathml', '--highlight-style', 'pygments',
     '-o', cn_html],
    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    cwd=root,
)
out, err = p.communicate(input=cn_text.encode('utf-8'), timeout=180)
print('\n=== pandoc ===')
print('rc=', p.returncode)
if p.returncode != 0:
    print('stderr:', err.decode('utf-8','replace'))
else:
    with open(cn_html, 'rb') as f:
        full = f.read()
    full = re.sub(rb'<meta[^>]*charset[^>]*>', b'<meta charset="UTF-8">', full, count=1)
    if b'charset' not in full[:2000]:
        full = full.replace(b'<head>', b'<head>\n<meta charset="UTF-8">', 1)
    open(cn_html, 'wb').write(full)
    html_txt = full.decode('utf-8', errors='replace')
    print('HTML size:', len(full), 'bytes')
    print('HTML 真实三类标注:', '三类标注' in html_txt)
    print('HTML Layer 0:', 'Layer 0' in html_txt)

print('\n=== Word COM ===')
import win32com.client, pythoncom
pythoncom.CoInitialize()
word = win32com.client.Dispatch('Word.Application')
word.Visible = False
word.DisplayAlerts = 0
cn_docx = os.path.join(root, 'riemann_thesis_cn.docx')
try:
    doc = word.Documents.Open(cn_html, ReadOnly=True)
    doc.SaveAs(cn_docx, FileFormat=16)
    doc.Close(False)
    print('Docx saved:', os.path.getsize(cn_docx), 'bytes')
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

print('\n=== python-docx 后处理 ===')
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.text.run import Run

doc = Document(cn_docx)
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
            has_ascii = any(ord(c)<128 for c in r2.text)
            if is_code:
                if has_cjk and not has_ascii:
                    set_run_fonts(r2, 'Microsoft YaHei', Pt(9), 'Microsoft YaHei', Pt(9))
                else:
                    set_run_fonts(r2, 'Consolas', Pt(8.5), 'Microsoft YaHei', Pt(8.5))
            else:
                if has_cjk:
                    set_run_fonts(r2, 'Calibri', Pt(11), 'Microsoft YaHei', Pt(11))
                else:
                    set_run_fonts(r2, 'Calibri', Pt(11), 'Calibri', Pt(11))
doc.save(cn_docx)
print('后处理完成: code_paras=', code_para, ' size=', os.path.getsize(cn_docx))

import zipfile, xml.etree.ElementTree as ET
with zipfile.ZipFile(cn_docx,'r') as z:
    doc_xml = z.read('word/document.xml').decode('utf-8', errors='replace')
ns2 = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
root_xml = ET.fromstring(doc_xml.encode('utf-8','replace'))
body = root_xml.find('w:body', ns2)
paras = body.findall('w:p', ns2)
print('\n=== 验证 ===')
print('段落数:', len(paras))
found = {}
for k in ['三类','Layer 0','可形式化消去','紧性','零点单阶']:
    found[k] = False
for p in paras:
    t = ''.join(et.text or '' for et in p.findall('.//w:t', ns2))
    for k in list(found.keys()):
        if k in t:
            found[k] = True
for k,v in found.items():
    print(' ', k, ':', 'OK' if v else 'MISSING')
print('\n最终中文:', cn_docx)
