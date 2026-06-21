import os, subprocess, shutil, re
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH

root = r'd:\project\code\maths\黎曼猜想'

def read_md_utf8(p):
    with open(p,'rb') as f: b = f.read()
    if b.startswith(b'\xef\xbb\xbf'): b = b[3:]
    return b.decode('utf-8')

def pandoc_via_stdin(md_text, out_html):
    proc = subprocess.run(
        ['pandoc','--standalone','--from','markdown','--to','html5','--mathml'],
        input=md_text,
        text=True,
        capture_output=True,
        cwd=root,
        env={**os.environ, 'PYTHONUTF8':'1'},
    )
    if proc.returncode != 0:
        print('pandoc stderr:', proc.stderr)
        raise SystemExit(proc.returncode)
    with open(out_html,'w',encoding='utf-8-sig') as f:  # utf-8-sig adds BOM for Word
        f.write(proc.stdout)

def word_html_to_docx(html_path, docx_path):
    word = None
    try:
        word = __import__('win32com.client', fromlist=['Dispatch']).Dispatch('Word.Application')
    except ImportError:
        import win32com.client
        word = win32com.client.Dispatch('Word.Application')
    word.Visible = False
    doc = word.Documents.Open(html_path, ReadOnly=True)
    doc.SaveAs(docx_path, FileFormat=16)  # wdFormatXMLDocument
    doc.Close()
    word.Quit()

