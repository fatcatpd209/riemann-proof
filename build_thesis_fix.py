# -*- coding: utf-8 -*-
"""
一次性修复：
  1. 中文源 md 存在双重编码乱码 (GBK bytes -> misread as UTF-8 -> saved as UTF-8)
     本脚本用"反双重乱码"算法把真实中文救回来
  2. 英文源 md 内容确实只有 7 页（不是编译问题）
  3. 干净 md -> pandoc stdin UTF-8 -> HTML UTF-8 -> Word COM -> docx -> postprocess
"""
import os, sys, io, re, subprocess, shutil

root = r'd:\project\code\maths\黎曼猜想'
OUT_CN  = os.path.join(root, 'riemann_thesis_cn.docx')
OUT_EN  = os.path.join(root, 'riemann_thesis_en.docx')
OUT_CN_HTML = os.path.join(root, 'riemann_cn.html')
OUT_EN_HTML = os.path.join(root, 'riemann_en.html')


def fix_double_mojibake(text):
    """
    反双重乱码：
      原始中文 -> GBK bytes -> 被某编辑器"错误解码成 UTF-8"
      -> 那些"被解码出的乱码字符"被重新以 UTF-8 编码保存
    恢复: 把每个"乱码字符"重新 encode('utf-8') -> 拼回真实 GBK bytes -> 再 decode('gb18030')
    """
    byte_buf = b''
    for ch in text:
        byte_buf += ch.encode('utf-8')
    for enc in ('gb18030', 'gbk'):
        try:
            return byte_buf.decode(enc)
        except Exception:
            continue
    return byte_buf.decode('gb18030', errors='replace')


def load_cn_source():
    """选择最完整 + 修复后有真实 '三类' 的中文 md"""
    candidates = [
        'riemann_thesis-standard.md',
        'riemann_thesis_original_restored.md',
        'riemann_thesis1.md',
        'riemann_thesis_cn_clean.md',
        'cn_clean.md',
    ]
    best = None
    best_score = -1
    for fname in candidates:
        p = os.path.join(root, fname)
        if not os.path.exists(p):
            continue
        raw = open(p, 'rb').read()
        while raw.startswith(b'\xef\xbb\xbf'):
            raw = raw[3:]
        bad_text = raw.decode('utf-8', errors='replace')
        real_text = fix_double_mojibake(bad_text)

        cjk = sum(1 for c in real_text if '\u4e00' <= c <= '\u9fff')
        has_sanlei = ('三类标注' in real_text) or (
            '三类' in real_text and '标注' in real_text and 'Layer 0' in real_text
        )
        has_layer = 'Layer 0' in real_text

        score = 0
        if has_sanlei:
            score += 100
        if has_layer:
            score += 50
        score += cjk // 1000  # more Chinese chars = better

        print(f'  {fname}: score={score} cjk={cjk} 三类={has_sanlei} Layer0={has_layer} size={len(real_text)}')

        if score > best_score:
            best_score = score
            best = (fname, real_text)
    return best


def pandoc_md_to_html(md_text, html_path):
    p = subprocess.Popen(
        [
            'pandoc', '--standalone',
            '--from', 'markdown',
            '--to', 'html5',
            '--wrap=preserve',
            '--mathml',
            '--highlight-style', 'pygments',
            '-o', html_path,
        ],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=root,
    )
    out, err = p.communicate(input=md_text.encode('utf-8'), timeout=180)
    if p.returncode != 0:
        raise RuntimeError(f'pandoc failed: {err.decode("utf-8", "replace")}')

    with open(html_path, 'rb') as f:
        full = f.read()
    full = re.sub(rb'<meta[^>]*charset[^>]*>', b'<meta charset="UTF-8">', full, count=1)
    if b'charset' not in full[:2000]:
        full = full.replace(b'<head>', b'<head>\n<meta charset="UTF-8">', 1)
    open(html_path, 'wb').write(full)


def word_html_to_docx(html_path, docx_path):
    import win32com.client
    import pythoncom
    pythoncom.CoInitialize()
    word = win32com.client.Dispatch('Word.Application')
    word.Visible = False
    word.DisplayAlerts = 0
    try:
        doc = word.Documents.Open(html_path, ReadOnly=True)
        doc.SaveAs(docx_path, FileFormat=16)
        doc.Close(False)
    finally:
        try:
            word.Quit()
        except Exception:
            pass
        try:
            pythoncom.CoUninitialize()
        except Exception:
            pass


def postprocess_docx(path, chinese):
    from docx import Document
    from docx.shared import Pt, Cm
    from docx.enum.text import WD_ALIGN_PARAGRAPH

    doc = Document(path)
    for sec in doc.sections:
        sec.top_margin = Cm(1.8)
        sec.bottom_margin = Cm(1.8)
        sec.left_margin = Cm(1.8)
        sec.right_margin = Cm(1.8)

    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

    def set_run_fonts(run, ascii_font, ascii_size, east_font, east_size):
        rPr = run._element.find('w:rPr', ns)
        if rPr is None:
            rPr = run._element.makeelement(
                '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}rPr', {}
            )
            run._element.insert(0, rPr)
        for child in list(rPr):
            if child.tag.endswith('rFonts'):
                rPr.remove(child)
        rf = rPr.makeelement(
            '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}rFonts',
            {
                '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}ascii': ascii_font,
                '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}hAnsi': ascii_font,
                '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}eastAsia': east_font,
            },
        )
        rPr.insert(0, rf)
        sz = rPr.find('w:sz', ns)
        if sz is None:
            sz = rPr.makeelement('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}sz', {})
            rPr.append(sz)
        sz.set(
            '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val',
            str(int(ascii_size.pt * 2)),
        )
        cs = rPr.find('w:szCs', ns)
        if cs is None:
            cs = rPr.makeelement('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}szCs', {})
            rPr.append(cs)
        cs.set(
            '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val',
            str(int(east_size.pt * 2)),
        )

    def split_run(run):
        t = run.text
        if t == '':
            return [run]
        spans = []
        cur = None
        start = 0
        for i, ch in enumerate(t):
            c = 'A' if ord(ch) < 128 else 'N'
            if cur is None:
                cur = c
                start = i
            elif c != cur:
                spans.append((cur, start, i))
                cur = c
                start = i
        spans.append((cur, start, len(t)))
        if len(spans) == 1:
            return [run]
        parent = run._element.getparent()
        idx = parent.index(run._element)
        new_runs = []
        from docx.text.run import Run

        for cls, s, e in spans:
            r_elem = run._element.makeelement(run._element.tag, run._element.attrib)
            t_elem = r_elem.makeelement(
                '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t', {}
            )
            t_elem.text = t[s:e]
            r_elem.append(t_elem)
            parent.insert(idx, r_elem)
            idx += 1
            new_runs.append(Run(r_elem, run._parent))
        parent.remove(run._element)
        return new_runs

    code_paras = 0
    for para in doc.paragraphs:
        style = (para.style.name if para.style else '').lower()
        is_code = (
            'code' in style
            or 'source' in style
            or 'verbatim' in style
            or 'preformatted' in style
        )
        if is_code:
            pPr = para._element.find('w:pPr', ns)
            if pPr is None:
                pPr = para._element.makeelement(
                    '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}pPr', {}
                )
                para._element.insert(0, pPr)
            wrap = pPr.find('w:wrap', ns)
            if wrap is None:
                wrap = pPr.makeelement(
                    '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}wrap',
                    {
                        '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val': 'linesAndChars'
                    },
                )
                pPr.append(wrap)
            para.alignment = WD_ALIGN_PARAGRAPH.LEFT
            code_paras += 1

        for r in list(para.runs):
            for r2 in split_run(r):
                has_cjk = any(ord(c) >= 128 for c in r2.text)
                has_ascii = any(ord(c) < 128 for c in r2.text)
                if is_code:
                    if chinese:
                        if has_cjk and not has_ascii:
                            set_run_fonts(r2, 'Microsoft YaHei', Pt(9), 'Microsoft YaHei', Pt(9))
                        else:
                            set_run_fonts(r2, 'Consolas', Pt(8.5), 'Microsoft YaHei', Pt(8.5))
                    else:
                        set_run_fonts(r2, 'Consolas', Pt(9), 'Calibri', Pt(9))
                else:
                    if chinese:
                        if has_cjk:
                            set_run_fonts(r2, 'Calibri', Pt(11), 'Microsoft YaHei', Pt(11))
                        else:
                            set_run_fonts(r2, 'Calibri', Pt(11), 'Calibri', Pt(11))
                    else:
                        set_run_fonts(r2, 'Calibri', Pt(11), 'Calibri', Pt(11))

    doc.save(path)
    return code_paras


def verify_docx(path, language='zh'):
    import zipfile
    import xml.etree.ElementTree as ET

    with zipfile.ZipFile(path, 'r') as z:
        doc_xml = z.read('word/document.xml').decode('utf-8', errors='replace')
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    root = ET.fromstring(doc_xml.encode('utf-8', errors='replace'))
    body = root.find('w:body', ns)
    paras = body.findall('w:p', ns)

    cjk_total = 0
    code_paras = 0
    bad_question = 0
    key_founds = {}
    for p in paras:
        t = ''.join(et.text or '' for et in p.findall('.//w:t', ns))
        cjk_total += sum(1 for c in t if ord(c) >= 128)
        if any(ord(c) >= 128 for c in t):
            if language == 'zh':
                for kw in ['三类', '标注', 'Layer 0', 'Layer 1', 'Layer 2']:
                    if kw in t and kw not in key_founds:
                        key_founds[kw] = t[:100]
                if '?' in t and 'Layer' not in t and len(t.strip()) > 5:
                    bad_question += 1
        style_name = ''
        pPr = p.find('w:pPr', ns)
        if pPr is not None:
            pStyle = pPr.find('w:pStyle', ns)
            if pStyle is not None:
                style_name = pStyle.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val', '')
        if 'code' in style_name.lower() or 'source' in style_name.lower():
            code_paras += 1

    return {
        'total_paras': len(paras),
        'cjk_chars': cjk_total,
        'code_paras': code_paras,
        'bad_question': bad_question,
        'keys': key_founds,
    }


# ============ MAIN ============
print('=' * 60)
print('STEP 1: 中文源 md 修复')
print('=' * 60)
best_cn = load_cn_source()
if best_cn is None:
    raise SystemExit('NO VALID CHINESE SOURCE FOUND!')
cn_fname, cn_text = best_cn
cn_cjk = sum(1 for c in cn_text if '\u4e00' <= c <= '\u9fff')
print(f'选了: {cn_fname}  real_text_len={len(cn_text)} real_cjk={cn_cjk}')
print(f'  三类={("三类" in cn_text)} 三类标注={("三类标注" in cn_text)} Layer0={("Layer 0" in cn_text)}')

# backup fixed md 方便用户留存
fixed_cn_md = os.path.join(root, 'riemann_thesis_cn_fixed.md')
open(fixed_cn_md, 'w', encoding='utf-8').write(cn_text)
print(f'  修复后的 md 留存: {fixed_cn_md}')

print()
print('=' * 60)
print('STEP 2: 中文 pandoc -> HTML')
print('=' * 60)
pandoc_md_to_html(cn_text, OUT_CN_HTML)
print(f'  HTML: {OUT_CN_HTML}  size={os.path.getsize(OUT_CN_HTML)}')

print()
print('=' * 60)
print('STEP 3: 中文 Word HTML -> docx')
print('=' * 60)
word_html_to_docx(OUT_CN_HTML, OUT_CN)
print(f'  DOCX: {OUT_CN}  size={os.path.getsize(OUT_CN)}')

print()
print('=' * 60)
print('STEP 4: 中文 postprocess')
print('=' * 60)
cn_code_paras = postprocess_docx(OUT_CN, chinese=True)
print(f'  code_paras={cn_code_paras}')

print()
print('=' * 60)
print('STEP 5: 中文 verify')
print('=' * 60)
v = verify_docx(OUT_CN, 'zh')
print(f'  {v}')
if v['cjk_chars'] > 1000 and '三类' in v.get('keys', {}) or any('三类' in t for t in v.get('keys', {}).values()):
    print('  >>> 中文 docx 中文部分正确!!')
elif v['cjk_chars'] > 1000:
    print(f'  中文 cjk={v["cjk_chars"]} 但没找到"三类" - 检查 Layer0 处:')
    for k, t in v.get('keys', {}).items():
        print(f'    {k}: {t}')
else:
    print(f'  WARNING: cjk_chars={v["cjk_chars"]} < 1000 -- 可能没正确修复')

print()
print('=' * 60)
print('STEP 6: 英文源 (riemann_thesis_en_clean.md)')
print('=' * 60)
en_src = os.path.join(root, 'riemann_thesis_en_clean.md')
if not os.path.exists(en_src):
    en_src = os.path.join(root, 'riemann_thesis_en.md')
en_text = open(en_src, 'r', encoding='utf-8').read()
print(f'  en_source={en_src}  text_len={len(en_text)}')

pandoc_md_to_html(en_text, OUT_EN_HTML)
print(f'  HTML: {OUT_EN_HTML}  size={os.path.getsize(OUT_EN_HTML)}')

word_html_to_docx(OUT_EN_HTML, OUT_EN)
print(f'  DOCX: {OUT_EN}  size={os.path.getsize(OUT_EN)}')

postprocess_docx(OUT_EN, chinese=False)
v2 = verify_docx(OUT_EN, 'en')
print(f'  EN verify: {v2}')

print()
print('=' * 60)
print('ALL DONE')
print('=' * 60)
print(f'  CN: {OUT_CN}')
print(f'  EN: {OUT_EN}')
