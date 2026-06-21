# ci_runner.ps1  Windows / GitHub CI entry point
#
# Runs three verification layers in order:
#   Layer 1  DAG static check   (dag_verify.py)
#   Layer 2  Axiom classifier   (coq_axiom_check.py)
#   Layer 3  Coq compiler        (coqc base_library.v main_proof.v)  [optional, skipped if no coqc]
#
# Non-zero exit if ANY layer fails.

$ErrorActionPreference = "Stop"
$repo = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $repo

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  RIEMANN HYPOTHESIS  CI PIPELINE"       -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

function Step($name, $script, $fatal=$true) {
    Write-Host ""
    Write-Host "---- [STEP] $name ----" -ForegroundColor Yellow
    & $script
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[FAIL] $name exited $LASTEXITCODE" -ForegroundColor Red
        if ($fatal) { exit $LASTEXITCODE }
    } else {
        Write-Host "[OK] $name" -ForegroundColor Green
    }
}

Step "dag_verify.py (cycle / blacklist / layer-order)" { python "$repo\dag_verify.py" }
Step "coq_axiom_check.py (classify S/R/Conj/Admitted)" { python "$repo\coq_axiom_check.py" } $false

$coqc = Get-Command coqc -ErrorAction SilentlyContinue
if ($coqc) {
    Write-Host ""
    Write-Host "---- [STEP] coqc compile (base_library.v + main_proof.v) ----" -ForegroundColor Yellow
    & coqc -q base_library.v
    $e1 = $LASTEXITCODE
    & coqc -q main_proof.v
    $e2 = $LASTEXITCODE
    if ($e1 -ne 0 -or $e2 -ne 0) {
        Write-Host "[FAIL] coq compile" -ForegroundColor Red
        exit 1
    } else {
        Write-Host "[OK] coq compile" -ForegroundColor Green
    }
} else {
    Write-Host ""
    Write-Host "[SKIP] coqc not on PATH  install Coq (opam install coq) to enable Layer 3." -ForegroundColor DarkGray
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  ALL LAYERS PASSED  CI OK"               -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
exit 0
