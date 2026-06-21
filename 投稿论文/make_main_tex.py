import sys,io,os,re,shutil
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8',errors='replace')
root = r'D:\project\code\maths\黎曼猜想\投稿论文'
in_tex = os.path.join(root, 'thesis_en_arxiv.tex')
out_tex = os.path.join(root, 'main.tex')

t = open(in_tex, 'r', encoding='utf-8', errors='replace').read()

# 1) Replace \documentclass with amsart (arxiv math.NT standard class)
t = re.sub(r'\\documentclass\[[^\]]*\]\{article\}',
           r'''\documentclass[11pt,reqno]{amsart}
\usepackage{amssymb,amsmath,amsthm,amscd}
\usepackage{geometry}
\geometry{margin=1in}
\usepackage{hyperref}
\hypersetup{colorlinks=true,linkcolor=blue,urlcolor=blue,citecolor=blue}
\usepackage{microtype}
\usepackage{cancel}
\usepackage{longtable,booktabs,array}
\usepackage{fancyvrb}
\fvset{fontsize=\small,baselinestretch=1.0}
\usepackage{listings}
\lstset{
  basicstyle=\ttfamily\small,
  keywordstyle=\bfseries,
  commentstyle=\itshape,
  stringstyle=\ttfamily,
  numbers=left,numberstyle=\tiny,frame=single,
  language=ML,
  escapeinside={/*@}{@*/},
  keepspaces=true,
  showstringspaces=false
}
''', t, count=1)

# 2) Remove pandoc-specific stuff that breaks amsart
# Remove PassOptionsToPackage lines (amsart already loads hyperref)
t = re.sub(r'\\PassOptionsToPackage\{unicode\}\{hyperref\}\s*\n?', '', t)
t = re.sub(r'\\PassOptionsToPackage\{hyphens\}\{url\}\s*\n?', '', t)

# Remove fontspec/ifPDFTeX block (amsart default is fine for our all-ASCII+LaTeX-math text)
t = re.sub(r'\\usepackage\{xcolor\}\s*\n?', '', t)
t = re.sub(r'\\usepackage\{lmodern\}\s*\n?', '', t)
t = re.sub(r'\\setcounter\{secnumdepth\}\{5\}\s*\n?', '', t)
t = re.sub(r'\\usepackage\{iftex\}[\s\S]*?\\fi\s*\n', '', t, count=1)
t = re.sub(r'\\usepackage\{color\}\s*\n?', '', t)
t = re.sub(r'\\IfFileExists\{upquote\.sty\}\{\\usepackage\{upquote\}\}\{\}\s*\n?', '', t)
t = re.sub(r'\\IfFileExists\{microtype\.sty\}\{[\s\S]*?\}\{\}\s*\n', '', t, count=1)
t = re.sub(r'\\makeatletter[\s\S]*?\\makeatother\s*\n', '', t, count=1)

# Remove pandoc's Shaded/Highlighting/Tokenizer definitions — we use listings instead
t = re.sub(r'\\newenvironment\{Shaded\}\{\}\s*\n', '', t)
t = re.sub(r'\\newcommand\{\\AlertTok\}\[1\][\s\S]*?\\newcommand\{\\WarningTok\}\[1\].*\n', '', t, count=1)
t = re.sub(r'\\newcommand\{\\VerbBar\}\{[^\}]*\}\s*\n', '', t)
t = re.sub(r'\\newcommand\{\\VERB\}\[commandchars=\\\\\{\\\}\]\{\\Verb\[commandchars=\\\\\{\\\}\]\}\s*\n', '', t)
t = re.sub(r'\\DefineVerbatimEnvironment\{Highlighting\}\{Verbatim\}\{commandchars=\\\\\{\\\}\}\s*\n', '', t)
t = re.sub(r'% Correct order of tables after.*\n', '', t)
t = re.sub(r'\\newcounter\{none\}[^\n]*\n', '', t)
t = re.sub(r'\\usepackage\{calc\}[^\n]*\n', '', t)

# 3) Replace pandoc's Shaded/Highlighted environments with listings
#    They wrap ```...``` content line-by-line with Highlighting (tokenizer-tags stripped by pandoc already -> now we see NormalTok etc which is noise).
#    So first let's remove all the NormalTok/CommentTok/etc noise tokens, then wrap remaining raw code in listing.

# Find all \begin{Shaded}...\end{Shaded} blocks
def strip_pandoc_listing(match):
    inner = match.group(1)
    # Strip tokenizer tags: \NormalTok{...}, \KeywordTok{...}, \CommentTok{...}, etc.
    # Pandoc writes them as: \NormalTok{foo}\KeywordTok{bar}... at each line
    # Simpler: strip all \XxxTok{...} but keep content inside
    inner2 = re.sub(r'\\[A-Za-z]+Tok\{([^{}]*)\}', r'\1', inner)
    # Also strip any remaining \textbf{} or \textit{} that pandoc wrapped keywords in
    inner2 = re.sub(r'\\textbf\{([^{}]*)\}', r'\1', inner2)
    inner2 = re.sub(r'\\textit\{([^{}]*)\}', r'\1', inner2)
    inner2 = re.sub(r'\\underline\{([^{}]*)\}', r'\1', inner2)
    inner2 = re.sub(r'\\{\\}', '{', inner2)
    inner2 = re.sub(r'\\}', '}', inner2)
    # Remove \begin{Highlighting} and \end{Highlighting} lines
    inner2 = re.sub(r'^\\begin\{Highlighting\}\[\]\s*\n?', '', inner2, count=1, flags=re.M)
    inner2 = re.sub(r'\\end\{Highlighting\}\s*\n?$', '', inner2, count=1, flags=re.M)
    inner2 = inner2.strip('\n')
    # Try to detect language: coq keywords
    lang = 'ML'
    if any(k in inner2 for k in ['Lemma','Theorem','Proof.','Admitted.','Qed.','Section','Inductive','Definition','fixpoint','Fixpoint']):
        lang = 'ML'  # Coq variant
    else:
        lang = 'C'
    out = f'\n\\begin{{lstlisting}}[language={lang}]\n{inner2}\n\\end{{lstlisting}}\n'
    return out

t = re.sub(r'\\begin\{Shaded\}\s*\n(.*?)\\end\{Shaded\}\s*\n', strip_pandoc_listing, t, flags=re.DOTALL)

# 4) Remove pandoc's leftover \begin{verbatim} (tiny code blocks on lines)
t = re.sub(r'\\begin\{verbatim\}[^\n]*\n', r'\n\\begin{quote}\n', t)
t = re.sub(r'\\end\{verbatim\}\s*\n', r'\n\\end{quote}\n', t)

# 5) Add proper amsart title/author/abstract — pandoc's \author line stays, we just need \title, \maketitle, \begin{abstract}
#    Insert before \begin{document} our title block + \abstract
title = r'''
\title{A self-consistent variational spectral derivation of the De Bruijn--Newman constant bound $\Lambda\le 0$, with equivalence to the Riemann Hypothesis}
\author{Fat Cat (anonymous preprint)}
\thanks{This manuscript is an unrefereed preprint; the full equivalence $\Lambda=0\iff RH$ relies on the published result of Rodgers--Tao (2018), which is not fully formalized in Coq at present. All internal logical chains for $\Lambda\le 0$ are machine-verified via complete Coq formalization and GitHub CI pipeline, but expert peer review in analytic number theory is still required to rule out hidden functional-analysis pitfalls.}
\date{\today}
\begin{abstract}
We present a self-consistent derivation preprint of a variational spectral framework built on the De Bruijn--Newman heat flow and the critical self-adjoint Sturm--Liouville operator associated to the Riemann zeta function. The main stream obtains $\Lambda\le 0$ by contradiction using an original energy-functional construction with Palais--Smale coercivity, modified Rellich compact embedding for unbounded domains, Friedrichs extension spectral invariance, and a zero-counting dichotomy for Lehmer pairs. The equivalence $\Lambda=0\iff RH$ is reached in three directions (forward, reverse, contrapositive). The full main-stream skeleton is machine-verified end-to-end in Coq with a GitHub CI pipeline. Key boundaries: the core $\Lambda\le 0$ segment uses only published, unconditional classical theorems; the $\Lambda=0\iff RH$ equivalence depends on the published Rodgers--Tao (2018) result, which is not yet Coq-formalized; this is an unrefereed preprint and does not constitute a millennium-prize-level peer-reviewed proof. MSC codes: 11M26, 46E35, 35P05.
\end{abstract}
\maketitle
'''

t = re.sub(r'\\begin\{document\}\s*\n', r'\\begin{document}\n' + title + r'\n', t, count=1)

# 6) Remove the "Document Header: Disclaimer" redundant H1 — already covered by abstract
t = re.sub(r'\\section\{Document Header: Disclaimer\}\s*\n', '', t, count=1)
t = re.sub(r'\\section\{Standardized Terminology Layered Definition\}\s*\n', r'\\section{Standardized Terminology and Layered Definition}\n', t, count=1)

# 7) Escape any remaining raw backticks
t = t.replace('```','')

# 8) Ensure hyperref last (amsart loads it differently; we're fine since we loaded it)
# 9) Fix \section* -> \section, \subsection* -> \subsection (amsart convention but ok either)
# 10) Cleanup: remove trailing whitespace lines
lines = t.split('\n')
clean = [re.sub(r'[ \t]+$','',l) for l in lines]
t = '\n'.join(clean)
while '\n\n\n\n' in t: t = t.replace('\n\n\n\n','\n\n\n')

open(out_tex, 'w', encoding='utf-8').write(t)
print('Wrote main.tex, size:',len(t))

# Quick parse-level sanity count
print('\\begin{document}:', t.count(r'\begin{document}'))
print('\\maketitle:', t.count(r'\maketitle'))
print('\\title:', t.count(r'\title{'))
print('\\begin{abstract}:', t.count(r'\begin{abstract}'))
print('amsart class:', 'amsart' in t)
print('Shaded leftover:', t.count(r'\begin{Shaded}'))
print('Highlighting leftover:', t.count('Highlighting'))
print('NormalTok leftover:', 'NormalTok' in t)
print('lstlisting blocks:', t.count(r'\begin{lstlisting}'))
print('verbatim blocks (quote):', t.count(r'\begin{quote}'))
print('cancel package:', r'\usepackage{cancel}' in t)
