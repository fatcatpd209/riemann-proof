import re, os, shutil, subprocess

root = r'd:\project\code\maths\黎曼猜想'

def md_clean(src_name, dst_name):
    src = os.path.join(root, src_name)
    dst = os.path.join(root, dst_name)
    t = open(src, 'r', encoding='utf-8').read()
    # 1. checkmark -> plain text (docx emoji is fine but keep paper consistent)
    t = t.replace('✅', '[OK]')
    # 2. Inline LaTeX math: \( ... \) -> $ ... $  (allow multiple lines between \(\) )
    t = re.sub(r'\\\(\s*([\s\S]*?)\\\)', lambda m: '$' + m.group(1).strip() + '$', t)
    # 3. Display LaTeX math: \[ ... \] -> $$ ... $$
    t = re.sub(r'\\\[\s*([\s\S]*?)\\\]', lambda m: '$$\n' + m.group(1).strip() + '\n$$', t)
    # 4. Pandoc treats $$...$$ on one line better; wrap with \n for safety (already done)
    # 5. Remove stray `\[` / `\]` from quote-block lines (rare)
    t = re.sub(r'\n> \[\s*\n', '\n> $$\n', t)
    t = re.sub(r'\n> \]\s*\n', '\n> \n', t)
    # 6. Fix ``` code fences (ensure no Pandoc confusion)
    open(dst, 'w', encoding='utf-8').write(t)
    print(f'cleaned: {dst} ({len(t)} chars)')
    return dst

cn_md = md_clean('riemann_thesis-standard.md', 'riemann_thesis_cn_clean.md')
en_md = md_clean('riemann_thesis_en.md',      'riemann_thesis_en_clean.md')

# Pandoc: --standalone produces self-contained docx (with embedded images/fonts), good for Word.
def pandoc_docx(in_md, out_docx):
    out = os.path.join(root, out_docx)
    subprocess.run([
        'pandoc.exe', in_md,
        '--standalone',
        '--from', 'markdown',
        '--to', 'docx',
        '--reference-doc=custom-reference.docx' if os.path.exists(os.path.join(root,'custom-reference.docx')) else '--toc',
        '-o', out
    ], cwd=root, check=True)
    print(f'wrote: {out} ({os.path.getsize(out)} bytes)')
    return out

cn_docx = pandoc_docx(cn_md, 'riemann_thesis_cn.docx')
en_docx = pandoc_docx(en_md, 'riemann_thesis_en.docx')

print('\nDONE: open these in Word -> Save as PDF (or Export to PDF):')
print('  ', cn_docx)
print('  ', en_docx)
