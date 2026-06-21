param(
    [switch]$Clean,
    [switch]$Verbose,
    [string]$Coqc = "D:\Rocq-Platform~9.0~2025.08\bin\coqc.exe"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Continue"

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Push-Location $root

if (-not (Test-Path $Coqc)) {
    Write-Host "[FATAL] coqc not found: $Coqc" -ForegroundColor Red
    Pop-Location
    exit 1
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  RiemannProof Local Coq/Rocq Verification" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
& $Coqc --version 2>&1 | ForEach-Object { Write-Host "  $_" -ForegroundColor DarkGray }
Write-Host "  Working dir : $root" -ForegroundColor DarkGray
Write-Host "  Time        : $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor DarkGray
Write-Host "------------------------------------------------------------" -ForegroundColor Cyan

$modules = @(
    "riemann_coq.v",
    "logic_tools.v",
    "base_library.v",
    "main_proof.v",
    "phase2_layered.v",
    "extension_lehmer.v",
    "riemann_hypothesis_formal.v",
    "riemann_coq_analysis.v"
)

if ($Clean) {
    Write-Host "[CLEAN] removing *.vo *.vok *.glob .coq-work" -ForegroundColor Yellow
    Get-ChildItem -Path $root -Filter "*.vo" -File | Remove-Item -Force -ErrorAction SilentlyContinue
    Get-ChildItem -Path $root -Filter "*.vok" -File | Remove-Item -Force -ErrorAction SilentlyContinue
    Get-ChildItem -Path $root -Filter "*.glob" -File | Remove-Item -Force -ErrorAction SilentlyContinue
}

$results = @()
$pass = 0
$fail = 0

foreach ($m in $modules) {
    $vo = [System.IO.Path]::GetFileNameWithoutExtension($m) + ".vo"
    $sw = [System.Diagnostics.Stopwatch]::StartNew()

    $stdout = & $Coqc -q -I . $m 2>&1
    $code  = $LASTEXITCODE
    $sw.Stop()

    $ok = ($code -eq 0) -and (Test-Path (Join-Path $root $vo))

    if ($ok) { $pass++ } else { $fail++ }

    $line = if ($ok) { "[ OK ]" } else { "[FAIL]" }
    $color = if ($ok) { "Green" } else { "Red" }
    Write-Host ("  {0}  {1,-42}  {2,6:N1}s" -f $line, $m, $sw.Elapsed.TotalSeconds) -ForegroundColor $color

    if (-not $ok) {
        foreach ($l in $stdout) { Write-Host "       $l" -ForegroundColor DarkYellow }
    }
    elseif ($Verbose) {
        foreach ($l in $stdout) { Write-Host "       $l" -ForegroundColor DarkGray }
    }

    $results += [pscustomobject]@{
        Module  = $m
        VoFile  = $vo
        OK      = $ok
        Exit    = $code
        Sec     = [math]::Round($sw.Elapsed.TotalSeconds, 2)
    }
}

Write-Host "------------------------------------------------------------" -ForegroundColor Cyan
Write-Host ("  Total: {0}  Pass: {1}  Fail: {2}" -f ($pass + $fail), $pass, $fail) -ForegroundColor $(if ($fail -eq 0) { 'Green' } else { 'Red' })
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

$manifest = Join-Path $root "_verify_manifest.json"
$results | ConvertTo-Json | Set-Content -Path $manifest -Encoding UTF8
Write-Host "  Manifest written: $manifest" -ForegroundColor DarkGray

Pop-Location

if ($fail -gt 0) { exit 1 }
exit 0
