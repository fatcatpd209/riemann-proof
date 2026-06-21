arXiv-ready submission package

Contents:
  main.tex        -- entry point (includes preamble + content + appendix)
  preamble.tex    -- documentclass, packages, title, abstract
  content.tex     -- body of the paper (pandoc-generated from riemann_thesis_en.md)
  appendix.tex    -- Coq formalization & CI verification section + references
  main.bbl        -- note: references use thebibliography embedded in appendix.tex

Build (any TeX live with xelatex):
  xelatex main.tex
  xelatex main.tex  (second pass for cross-references)

Source PDF:  main.pdf

This paper is also available as a pre-compiled PDF in ../riemann_thesis_en.pdf
and a Chinese version at ../riemann_thesis_cn.pdf (517 KB, CJK-ready).

arXiv metadata suggestions:
  - Primary class: math.NT (Number Theory)
  - Secondary:     math.FA (Functional Analysis)
  - MSC 2020:      11M26, 46E35, 35P05
  - License:        Minimal rights required by arXiv.org
  - Title (final):  A Self-Consistent Variational Spectral Derivation of
                    the De Bruijn--Newman Constant Bound Λ  0,
                    with Equivalence to the Riemann Hypothesis