import re, os, shutil, subprocess

def md_fix(src, dst):
    t = open(src,'r',encoding='utf-8').read()
    t = t.replace('✅','[OK]')
    t = t.replace('\\(','\$').replace('\\)','\$').replace('\\[','$$').replace('\\]','$$')
    open(dst,'w',encoding='utf-8').write(t)

md_fix('riemann_thesis-standard.md','cn_clean.md')
md_fix('riemann_thesis_en.md','en_clean.md')

def pandoc(md, raw):
    subprocess.run(['pandoc.exe', md, '--standalone', '--from', 'markdown', '--to', 'latex', '-o', raw], cwd='.', check=True)

pandoc('cn_clean.md','cn_raw.tex')
pandoc('en_clean.md','en_raw.tex')

CN_HEADER = r"""\documentclass[11pt,a4paper]{ctexart}
\usepackage[margin=2.2cm]{geometry}
\usepackage{amsmath,amssymb,amsfonts,amsthm,mathtools}
\usepackage{bm}
\usepackage{mathrsfs}
\usepackage{booktabs,longtable,array}
\usepackage{float,color,caption}
\usepackage{fancyvrb}
\usepackage{xurl}
\usepackage{microtype}
\usepackage{setspace}
\usepackage{calc,etoolbox}
\usepackage{iftex}
\usepackage{hyperref}
\hypersetup{colorlinks=true,linkcolor=blue,citecolor=blue,urlcolor=blue,unicode=true,pdfborder={0 0 0}}
\linespread{1.18}
\frenchspacing
\emergencystretch=3em
\pretolerance=1000
\tolerance=2000
\hyphenpenalty=1000
\exhyphenpenalty=10000
\clubpenalty=10000
\widowpenalty=10000
\interdisplaylinepenalty=100
\setlength{\parindent}{2em}
\setlength{\parskip}{0.3em}
\DefineVerbatimEnvironment{Highlighting}{Verbatim}{commandchars=\\\{\},fontsize=\small,fontfamily=tt,baselinestretch=1.1,breaklines=true,breakanywhere=true}
\fvset{fontsize=\small,fontfamily=tt,baselinestretch=1.1,breaklines=true,breakanywhere=true}
\makeatletter
\gdef\@verbatim{\trivlist \item[]\if@minipage\else\vskip\parskip\fi
\let\@xobeysp\relax \leavevmode \start@boxvb
\VerbatimEnvironment
\VerbatimFontHook\VerbatimSizeHook\VerbatimBaselineStretchHook
\VerbatimLeftMarginHook\VerbatimRightMarginHook\VerbatimIndentHook
\VerbatimFillHook\VerbatimFillbreakHook
\VerbatimTabHook\VerbatimTabsHook
\VerbatimFontfamilyHook\VerbatimFontsizeHook
\VerbatimBaselinestretchHook
\VerbatimBreaklinesHook \VerbatimBreakanywhereHook
\FV@@@HashCommentStart \FV@@@HashCommentEnd
\FV@@@CommandChars \FV@@@EscapeChar \FV@@@CommentChar
\FV@@@XSpace \FV@@@Space \FV@@@BackSpace
\FV@@@Font \FV@@@Size \FV@@@BaselineStretch \FV@@@TabStop
\FV@@@Tab \FV@@@Tabs \FV@@@Fill \FV@@@Fillbreak
\FV@@@LeftMargin \FV@@@RightMargin \FV@@@Indent
\FV@@@Breaklines \FV@@@Breakanywhere
\FV@@@HashComment \FV@@@Comment
\FV@@@CommandChars \FV@@@EscapeChar
\FV@@@XSpaces \FV@@@Spaces \FV@@@BackSpaces \FV@@@TabStops}
\makeatother
\makeatletter
\pretolerance=2000 \tolerance=3000 \emergencystretch=3em
\makeatother
\apptocmd{\equation}{\emergencystretch=1em\pretolerance=2000\tolerance=3000}{}{}
\apptocmd{\align}{\emergencystretch=1em\pretolerance=2000\tolerance=3000}{}{}
\apptocmd{\gather}{\emergencystretch=1em\pretolerance=2000\tolerance=3000}{}{}
\apptocmd{alignat}{\emergencystretch=1em\pretolerance=2000\tolerance=3000}{}{}
\apptocmd{cases}{\emergencystretch=1em\pretolerance=2000\tolerance=3000}{}{}
\apptocmd{matrix}{\emergencystretch=1em\pretolerance=2000\tolerance=3000}{}{}
\apptocmd{pmatrix}{\emergencystretch=1em\pretolerance=2000\tolerance=3000}{}{}
\apptocmd{bmatrix}{\emergencystretch=1em\pretolerance=2000\tolerance=3000}{}{}
\apptocmd{Bmatrix}{\emergencystretch=1em\pretolerance=2000\tolerance=3000}{}{}
\apptocmd{vmatrix}{\emergencystretch=1em\pretolerance=2000\tolerance=3000}{}{}
\apptocmd{Vmatrix}{\emergencystretch=1em\pretolerance=2000\tolerance=3000}{}{}
\newcommand{\R}{\mathbb{R}}
\newcommand{\C}{\mathbb{C}}
\newcommand{\Z}{\mathbb{Z}}
\newcommand{\HH}{\mathbb{H}}
\newcommand{\LL}{\mathcal{L}}
\newcommand{\SSS}{\mathcal{S}}
\newcommand{\cE}{\mathcal{E}}
\newcommand{\Ld}{\lambda_{\mathrm{DBN}}}
\newcommand{\Ls}{\lambda_{\mathrm{spec}}}
\newcommand{\xixi}{\xi}
\newcommand{\XX}{\Xi}
\newtheorem{theorem}{定理}[section]
\newtheorem{lemma}[theorem]{引理}
\newtheorem{proposition}[theorem]{命题}
\newtheorem{corollary}[theorem]{推论}
\newtheorem{definition}{定义}[section]
\newtheorem{remark}{注}[section]
\newtheorem{axiom}{公理}[section]
"""

EN_HEADER = r"""\documentclass[11pt,a4paper]{article}
\usepackage[margin=2.2cm]{geometry}
\usepackage{amsmath,amssymb,amsfonts,amsthm,mathtools}
\usepackage{bm}
\usepackage{mathrsfs}
\usepackage{booktabs,longtable,array}
\usepackage{float,color,caption}
\usepackage{fancyvrb}
\usepackage{xurl}
\usepackage{microtype}
\usepackage{setspace}
\usepackage{calc,etoolbox}
\usepackage{iftex}
\usepackage{hyperref}
\hypersetup{colorlinks=true,linkcolor=blue,citecolor=blue,urlcolor=blue,unicode=true,pdfborder={0 0 0}}
\linespread{1.18}
\frenchspacing
\emergencystretch=3em
\pretolerance=1000
\tolerance=2000
\hyphenpenalty=1000
\exhyphenpenalty=10000
\clubpenalty=10000
\widowpenalty=10000
\interdisplaylinepenalty=100
\setlength{\parindent}{2em}
\setlength{\parskip}{0.3em}
\DefineVerbatimEnvironment{Highlighting}{Verbatim}{commandchars=\\\{\},fontsize=\small,fontfamily=tt,baselinestretch=1.1,breaklines=true,breakanywhere=true}
\fvset{fontsize=\small,fontfamily=tt,baselinestretch=1.1,breaklines=true,breakanywhere=true}
\makeatletter
\gdef\@verbatim{\trivlist \item[]\if@minipage\else\vskip\parskip\fi
\let\@xobeysp\relax \leavevmode \start@boxvb
\VerbatimEnvironment
\VerbatimFontHook\VerbatimSizeHook\VerbatimBaselineStretchHook
\VerbatimLeftMarginHook\VerbatimRightMarginHook\VerbatimIndentHook
\VerbatimFillHook\VerbatimFillbreakHook
\VerbatimTabHook\VerbatimTabsHook
\VerbatimFontfamilyHook\VerbatimFontsizeHook
\VerbatimBaselinestretchHook
\VerbatimBreaklinesHook \VerbatimBreakanywhereHook
\FV@@@HashCommentStart \FV@@@HashCommentEnd
\FV@@@CommandChars \FV@@@EscapeChar \FV@@@CommentChar
\FV@@@XSpace \FV@@@Space \FV@@@BackSpace
\FV@@@Font \FV@@@Size \FV@@@BaselineStretch \FV@@@TabStop
\FV@@@Tab \FV@@@Tabs \FV@@@Fill \FV@@@Fillbreak
\FV@@@LeftMargin \FV@@@RightMargin \FV@@@Indent
\FV@@@Breaklines \FV@@@Breakanywhere
\FV@@@HashComment \FV@@@Comment
\FV@@@CommandChars \FV@@@EscapeChar
\FV@@@XSpaces \FV@@@Spaces \FV@@@BackSpaces \FV@@@TabStops}
\makeatother
\makeatletter
\pretolerance=2000 \tolerance=3000 \emergencystretch=1em
\makeatother
\apptocmd{\equation}{\emergencystretch=1em\pretolerance=2000\tolerance=3000}{}{}
\apptocmd{\align}{\emergencystretch=1em\pretolerance=2000\tolerance=3000}{}{}
\apptocmd{\gather}{\emergencystretch=1em\pretolerance=2000\tolerance=3000}{}{}
\apptocmd{alignat}{\emergencystretch=1em\pretolerance=2000\tolerance=3000}{}{}
\apptocmd{cases}{\emergencystretch=1em\pretolerance=2000\tolerance=3000}{}{}
\newcommand{\R}{\mathbb{R}}
\newcommand{\C}{\mathbb{C}}
\newcommand{\Z}{\mathbb{Z}}
\newcommand{\HH}{\mathbb{H}}
\newcommand{\LL}{\mathcal{L}}
\newcommand{\SSS}{\mathcal{S}}
\newcommand{\cE}{\mathcal{E}}
\newcommand{\Ld}{\lambda_{\mathrm{DBN}}}
\newcommand{\Ls}{\lambda_{\mathrm{spec}}}
\newcommand{\xixi}{\xi}
\newcommand{\XX}{\Xi}
\newtheorem{theorem}{Theorem}[section]
\newtheorem{lemma}[theorem]{Lemma}
\newtheorem{proposition}[theorem]{Proposition}
\newtheorem{corollary}[theorem]{Corollary}
\newtheorem{definition}{Definition}[section]
\newtheorem{remark}{Remark}[section]
\newtheorem{axiom}{Axiom}[section]
"""

def build_tex(raw, header, out):
    t = open(raw,'r',encoding='utf-8').read()
    # strip pandoc preamble (everything up to \begin{document})
    m = re.match(r'.*?\\begin\{document\}', t, re.DOTALL)
    if not m:
        raise RuntimeError('cannot find \\begin{document}')
    body = t[m.end():]
    # drop trailing \end{document} if present
    body = re.sub(r'\\end\{document\}\s*$','',body,flags=re.DOTALL).rstrip() + '\n'
    # replace bare verbatim env with Highlighting (so our fvset applies with breaklines)
    body = re.sub(r'\\begin\{verbatim\}\s*\n', r'\\begin{Highlighting}\n', body)
    body = re.sub(r'\n\\end\{verbatim\}', r'\n\\end{Highlighting}', body)
    # Highlighting (pandoc output) -> keep, fvset already configured
    full = header + '\n' + body + '\n\\end{document}\n'
    open(out,'w',encoding='utf-8').write(full)

build_tex('cn_raw.tex', CN_HEADER, 'cn_final.tex')
build_tex('en_raw.tex', EN_HEADER, 'en_final.tex')
print('cn_final size:', len(open('cn_final.tex',encoding='utf-8').read()))
print('en_final size:', len(open('en_final.tex',encoding='utf-8').read()))

for name in ('cn_final','en_final'):
    subprocess.run(['xelatex.exe','-interaction=nonstopmode','-halt-on-error',f'{name}.tex'], cwd='.', check=False)
    subprocess.run(['xelatex.exe','-interaction=nonstopmode','-halt-on-error',f'{name}.tex'], cwd='.', check=False)

if os.path.exists('cn_final.pdf'):
    shutil.copy('cn_final.pdf','riemann_thesis_cn.pdf')
if os.path.exists('en_final.pdf'):
    shutil.copy('en_final.pdf','riemann_thesis_en.pdf')

for f in ('riemann_thesis_cn.pdf','riemann_thesis_en.pdf'):
    if os.path.exists(f):
        print(f, os.path.getsize(f),'bytes')
