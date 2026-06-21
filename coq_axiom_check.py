#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, re, sys

REPO = os.path.dirname(os.path.abspath(__file__))
AXIOM_RE = re.compile(r'^\s*Axiom\s+(\w+)\s*:', re.MULTILINE)
CONJ_RE  = re.compile(r'^\s*Conjecture\s+(\w+)\s*:', re.MULTILINE)
HYP_RE   = re.compile(r'^\s*Hypothesis\s+(\w+)\s*:', re.MULTILINE)
ADMIT_RE = re.compile(r'\bAdmitted\b')

EXTERNAL_MAP = {
    'Rodgers_Tao_2018':    ('R-Axiom', 'Rodgers&Tao2018 无条件 L>=0, S=S_RT 已对齐'),
    'S_boundedbelow_spec': ('S-Axiom', '下确界存在, Coquelicot 实分析可消去'),
}

def read(p):
    with open(p, 'r', encoding='utf-8-sig', errors='replace') as f:
        return f.read()

def scan(p):
    s = read(p)
    return {
        'axioms': AXIOM_RE.findall(s),
        'conjs':  CONJ_RE.findall(s),
        'hyps':   HYP_RE.findall(s),
        'admits': ADMIT_RE.findall(s),
    }

def main():
    files = []
    for r, _, fs in os.walk(REPO):
        for f in fs:
            if f.endswith('.v') and not f.startswith('_'):
                files.append(os.path.join(r, f))

    interesting = []
    for p in files:
        r = scan(p)
        if r['axioms'] or r['conjs'] or r['hyps'] or r['admits']:
            r['path'] = p
            interesting.append(r)

    print("=" * 80)
    print(" COQ AXIOM / CONJECTURE / HYPOTHESIS / ADMITTED CLASSIFICATION")
    print("=" * 80)

    s_axiom, r_axiom, conj, hyp = [], [], [], []
    for r in sorted(interesting, key=lambda x: x['path']):
        stem = os.path.basename(r['path'])
        print(f"\n--- {stem}  axioms={len(r['axioms'])} conj={len(r['conjs'])} hyp={len(r['hyps'])} admits={len(r['admits'])} ---")
        for a in r['axioms']:
            tag, info = EXTERNAL_MAP.get(a, ('R-Axiom', '未分类'))
            (s_axiom if tag == 'S-Axiom' else r_axiom).append((a, info, stem))
            print(f"  AXIOM   {a:<28} [{tag}] {info}")
        for c in r['conjs']:
            conj.append((c, stem))
            print(f"  CONJ    {c:<28} OPEN CONJECTURE (main禁止引用)")
        for h in r['hyps']:
            hyp.append((h, stem))
            print(f"  HYP     {h:<28} module interface")
        if r['admits']:
            print(f"  ADMITTED x {len(r['admits']):<3}  (需 Qed)")

    print("\n" + "=" * 80)
    print(" LAYER 0 AXIOM SUMMARY")
    print("=" * 80)
    print(f"  S-Axiom (可消去): {len(s_axiom)}")
    for a, info, stem in s_axiom:
        print(f"    - {a:<28} [{stem}] {info}")
    print(f"  R-Axiom (长期保留): {len(r_axiom)}")
    for a, info, stem in r_axiom:
        print(f"    - {a:<28} [{stem}] {info}")
    print(f"  Conjecture (开放): {len(conj)}")
    for c, stem in conj:
        print(f"    - {c:<28} [{stem}]")

    print("\n" + "=" * 80)
    print(" PHASE 6 消去优先级")
    print("=" * 80)
    print("  [HIGH]  Evans 1998 Sobolev -> Coquelicot.Sobolev")
    print("  [HIGH]  Rellich 无界域     -> Unbounded_Rellich + exp_decay_bound")
    print("  [MID]   高斯/振荡积分       -> cos_integral_shift + R_sqrt_pi_le_3")
    print("  [LOW]   Titchmarsh 零点单阶 -> Hadamard + Riemann-von-Mangoldt")
    print("  [KEEP]  Rodgers_Tao_2018   (前沿论文, 长期)")
    print("  [KEEP]  CSV 1994 Lehmer     (拓展, 长期)")
    print("  [KEEP]  Polya / Csordas-Smith (开放, 不进主干)")

    fatal = []
    for c, stem in conj:
        if stem in ('main_proof.v', 'base_library.v', 'logic_tools.v', 'phase2_layered.v'):
            fatal.append(f"FATAL: conjecture {c} leaked into {stem}")

    print("\n" + "=" * 80)
    if fatal:
        print(" [FAIL]")
        for f in fatal: print(f"  {f}")
        sys.exit(1)
    print(" [PASS] no conjecture leaked into main files")
    print("=" * 80)
    sys.exit(0)

if __name__ == '__main__':
    main()
