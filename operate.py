#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Riemann proof  one-click operator script.

Commands:
  python operate.py run          full CI pipeline (same as end_to_end.ps1)
  python operate.py dag          DAG static analysis only
  python operate.py axiom        Axiom classification only
  python operate.py coq          coqc compile only (if coqc present)
  python operate.py list         show all .v files + Require graph
  python operate.py scan TEXT    grep TEXT across every .v file (context 2 lines)
  python operate.py summary      one-page stats of whole codebase
  python operate.py checklist    write CHECKLIST.md (submit/readme artifact)
  python operate.py --help       show this help
"""

import os, re, sys, subprocess, json
from pathlib import Path

REPO = Path(__file__).resolve().parent

V_FILES = sorted(p for p in REPO.rglob('*.v') if not p.name.startswith('_'))


def banner(t):
    print()
    print("=" * 72)
    print(f"  {t}")
    print("=" * 72)


def run_dag():
    banner("STAGE 1  dag_verify.py (cycle / blacklist / layer)")
    r = subprocess.run([sys.executable, str(REPO/'dag_verify.py')])
    return r.returncode


def run_axiom():
    banner("STAGE 2  coq_axiom_check.py (S/R/Conj/Admitted)")
    r = subprocess.run([sys.executable, str(REPO/'coq_axiom_check.py')])
    return r.returncode


def run_coq():
    banner("STAGE 3 — coqc compile (base_library / main_proof / phase2_layered / logic_tools)")
    try:
        r = subprocess.run(['where' if os.name=='nt' else 'which', 'coqc'],
                           capture_output=True, text=True)
        if r.returncode != 0:
            print("  [SKIP] coqc not installed. Install via coq.inria.fr or `opam install coq`")
            return 0
    except Exception:
        print("  [SKIP] coqc not installed")
        return 0
    files = ['logic_tools.v', 'base_library.v', 'main_proof.v', 'phase2_layered.v']
    ok = True
    for f in files:
        p = REPO / f
        if not p.exists():
            print(f"  [SKIP]   {f} missing")
            continue
        r = subprocess.run(['coqc', '-q', f], cwd=str(REPO))
        if r.returncode == 0:
            print(f"  [OK]     {f} -> compiled")
        else:
            print(f"  [FAIL]   {f} exited {r.returncode}")
            ok = False
    return 0 if ok else 1


def show_list():
    banner(f"ALL .v FILES ({len(V_FILES)})")
    require_re = re.compile(r'^\s*(?:From\s+\S+\s+)?Require(?:\s+Export)?\s+([^\s.]+)', re.MULTILINE)
    for p in V_FILES:
        src = p.read_text(encoding='utf-8-sig', errors='replace')
        reqs = sorted(set(require_re.findall(src)))
        depth = len(p.relative_to(REPO).parts) - 1
        pad = "  " * depth
        rel = p.relative_to(REPO)
        print(f"  {pad}{rel}  (requires: {', '.join(reqs) if reqs else '-'})")


def scan(text):
    banner(f"SCAN: {text}")
    hits = 0
    for p in V_FILES:
        lines = p.read_text(encoding='utf-8-sig', errors='replace').splitlines()
        for i, ln in enumerate(lines):
            if text in ln:
                hits += 1
                rel = p.relative_to(REPO)
                print(f"  {rel}:{i+1}: {ln.strip()}")
    if hits == 0:
        print("  no hits")
    else:
        print(f"\n  {hits} hit(s) across {len(V_FILES)} files")


def run_summary():
    banner("CODEBASE SUMMARY")
    axiom_re = re.compile(r'^\s*Axiom\s+(\w+)', re.MULTILINE)
    conj_re  = re.compile(r'^\s*Conjecture\s+(\w+)', re.MULTILINE)
    hyp_re   = re.compile(r'^\s*Hypothesis\s+(\w+)', re.MULTILINE)
    admit_re = re.compile(r'\bAdmitted\b')
    lemma_re = re.compile(r'^\s*(?:Lemma|Theorem|Definition)\s+(\w+)', re.MULTILINE)

    total_axiom = total_conj = total_hyp = total_admit = total_lemma = 0
    per_file = []
    for p in V_FILES:
        s = p.read_text(encoding='utf-8-sig', errors='replace')
        a = len(axiom_re.findall(s)); c = len(conj_re.findall(s))
        h = len(hyp_re.findall(s));  m = len(admit_re.findall(s))
        l = len(lemma_re.findall(s))
        total_axiom += a; total_conj += c; total_hyp += h
        total_admit += m; total_lemma += l
        per_file.append((str(p.relative_to(REPO)), a, c, h, m, l))

    print(f"  files .v        : {len(V_FILES)}")
    print(f"  Axiom           : {total_axiom}")
    print(f"  Conjecture      : {total_conj}")
    print(f"  Hypothesis      : {total_hyp}")
    print(f"  Admitted        : {total_admit}")
    print(f"  Lemma/Theorem/Def: {total_lemma}")
    print(f"  lines thesis md : {sum(1 for _ in open(REPO/'riemann_thesis-standard.md','r',encoding='utf-8-sig',errors='replace'))}")
    print()
    print("  per file (top 10 by Admitted):")
    for rel, a, c, h, m, l in sorted(per_file, key=lambda x: -x[4])[:10]:
        print(f"    {rel:<48} axiom={a:<3} conj={c:<2} hyp={h:<2} admit={m:<3} lemma={l:<3}")


def run_checklist():
    banner("WRITING CHECKLIST.md")
    out = REPO / 'CHECKLIST.md'
    md = []
    md += ["# Riemann proof  submission checklist", ""]
    md += ["## before every commit", ""]
    md += ["- [ ] `python operate.py dag` passes"]
    md += ["- [ ] `python operate.py axiom` passes (no Conj in main files)"]
    md += ["- [ ] `python operate.py summary` shows only 1 S-Axiom"]
    md += ["- [ ] `python operate.py scan 'Require Import' extension_lehmer main_proof` -> no hit"]
    md += ["- [ ] `python operate.py scan '\\bAdmitted\\b' main_proof` -> no hit"]
    md += ["", "## before submission", ""]
    md += ["- [ ] push to GitHub Actions  CI green"]
    md += ["- [ ] run `python operate.py checklist` and attach CHECKLIST.md to PR"]
    md += ["- [ ] coqc compile of base_library.v + main_proof.v + phase2_layered.v"]
    md += ["- [ ] DAG verify pass"]
    md += ["- [ ] no Conjecture leaked into main layer"]
    md += ["- [ ] cite thesis appendix E for Phase 6 (Coquelicot / Rellich / Gauss)"]
    out.write_text("\n".join(md), encoding='utf-8')
    print(f"  written -> {out}")
    return 0


def run_all():
    dag = run_dag(); print()
    ax  = run_axiom(); print()
    ok_coq = run_coq()
    banner("FINAL VERDICT")
    if dag == 0 and ax == 0 and ok_coq == 0:
        print("  ALL ENABLED STAGES PASSED")
        return 0
    print("  SOME STAGES FAILED")
    return 1


def main(argv):
    if not argv or argv[0] in ('-h','--help','help','?'):
        print(__doc__)
        return 0
    cmd = argv[0]
    if cmd == 'run':   return run_all()
    if cmd == 'dag':   return run_dag()
    if cmd == 'axiom': return run_axiom()
    if cmd == 'coq':   return run_coq()
    if cmd == 'list':  show_list(); return 0
    if cmd == 'summary': run_summary(); return 0
    if cmd == 'checklist': return run_checklist()
    if cmd == 'scan':
        if len(argv) < 2: print(__doc__); return 2
        scan(argv[1]); return 0
    print(__doc__); return 2


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
