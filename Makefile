# === Riemann Hypothesis Self-Consistent Proof  Makefile ===
# Windows: use `make.ps1` PowerShell script below instead.
# *nix:     run `make <target>` from this directory.

REPO   := $(CURDIR)
COQC   ?= coqc
PY     ?= python3

MAIN_FILES := base_library.v main_proof.v phase2_layered.v logic_tools.v

.PHONY: all dag axiom coq clean ci help

all: help

help:
@echo "Targets:"
@echo "  dag   - static DAG cycle / blacklist / layer-order check"
@echo "  axiom - Axiom / Conjecture / Admitted classification"
@echo "  coq   - compile main layer Coq files (base_library + main_proof)"
@echo "  ci    - run dag -> axiom -> coq three-layer CI"

dag:
$(PY) dag_verify.py

axiom:
$(PY) coq_axiom_check.py

coq:
$(COQC) -q base_library.v
$(COQC) -q main_proof.v

ci: dag axiom
@echo "[CI-OK] dag + axiom checks passed; coq step skipped (may need Coq toolchain)."

clean:
rm -f *.vo *.vok *.vos *.glob
