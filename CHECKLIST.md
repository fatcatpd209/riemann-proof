# Riemann proof  submission checklist

## before every commit

- [ ] `python operate.py dag` passes
- [ ] `python operate.py axiom` passes (no Conj in main files)
- [ ] `python operate.py summary` shows only 1 S-Axiom
- [ ] `python operate.py scan 'Require Import' extension_lehmer main_proof` -> no hit
- [ ] `python operate.py scan '\bAdmitted\b' main_proof` -> no hit

## before submission

- [ ] push to GitHub Actions  CI green
- [ ] run `python operate.py checklist` and attach CHECKLIST.md to PR
- [ ] coqc compile of base_library.v + main_proof.v + phase2_layered.v
- [ ] DAG verify pass
- [ ] no Conjecture leaked into main layer
- [ ] cite thesis appendix E for Phase 6 (Coquelicot / Rellich / Gauss)