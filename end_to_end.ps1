param(
    [switch]$SkipCoq, [switch]$OnlyCoq, [switch]$NoReport
)
$ErrorActionPreference = 'Continue'
$repo  = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $repo
$ts = Get-Date -Format 'yyyyMMdd-HHmmss'
$outDir = Join-Path $repo ("ci_out_" + $ts)
New-Item -ItemType Directory -Force -Path $outDir | Out-Null

function Banner($t) { Write-Host ""; Write-Host ("="*72) -ForegroundColor Cyan; Write-Host "  $t" -ForegroundColor Cyan; Write-Host ("="*72) -ForegroundColor Cyan }
function Ok($s)   { Write-Host "  [OK]   $s" -ForegroundColor Green }
function Skip2($s){ Write-Host "  [SKIP] $s" -ForegroundColor DarkGray }
function Fail($s) { Write-Host "  [FAIL] $s" -ForegroundColor Red }

$results = @()

function Run-Py($name, $script, $log) {
    Write-Host ""
    Write-Host "---- $name ----" -ForegroundColor Yellow
    & $script *> $log
    $code = $LASTEXITCODE
    Write-Host "  exit = $code"
    return $code
}

Banner "RIEMANN PROOF - end-to-end pipeline  ($ts)"

# stage 1
if (-not $OnlyCoq) {
    $log1 = Join-Path $outDir '01_dag.log'
    $code = Run-Py 'STAGE 1 - dag_verify.py' { python (Join-Path $repo 'dag_verify.py') } $log1
    if ($code -eq 0) { Ok "dag_verify.py PASS" } else { Fail "dag_verify.py FAIL (exit $code)" }
    $results += @{ n='dag_verify'; code=$code; log=$log1 }
}

# stage 2
if (-not $OnlyCoq) {
    $log2 = Join-Path $outDir '02_axiom.log'
    $code = Run-Py 'STAGE 2 - coq_axiom_check.py' { python (Join-Path $repo 'coq_axiom_check.py') } $log2
    if ($code -eq 0) { Ok "coq_axiom_check.py PASS" } else { Fail "coq_axiom_check.py FAIL" }
    $results += @{ n='axiom_check'; code=$code; log=$log2 }
}

# stage 3  coqc (only if available AND not skipped)
$coqc = Get-Command coqc -ErrorAction SilentlyContinue
if ($coqc -and -not $SkipCoq) {
    Write-Host ""; Write-Host "---- STAGE 3 - coqc compile ----" -ForegroundColor Yellow
    $log3 = Join-Path $outDir '03_coqc.log'
    $e3 = 0
    $files = @('base_library.v','logic_tools.v','main_proof.v','phase2_layered.v')
    foreach ($f in $files) {
        if (-not (Test-Path (Join-Path $repo $f))) { Skip2 "$f missing"; continue }
        Write-Host "  coqc -q $f"
        & coqc -q $f *>> $log3
        if ($LASTEXITCODE -eq 0) { Ok "  $f OK" } else { Fail "  $f failed"; $e3 = 1 }
    }
    if ($e3 -eq 0) { Ok "all main files compile" }
    $results += @{ n='coqc_compile'; code=$e3; log=$log3 }
} elseif ($SkipCoq) { Skip2 'coqc stage disabled by -SkipCoq' }
else { Skip2 'coqc not installed  run opam install coq (Linux/Mac/WSL) or coq.inria.fr installer (Windows)' }

# verdict
$allOk = ($results | Where-Object { $_.code -ne 0 }).Count -eq 0

Banner "VERDICT"
if ($allOk) {
    Ok "ALL ENABLED STAGES PASSED."
    Ok "Report folder: $outDir"
} else {
    Fail "SOME STAGES FAILED  see $outDir"
}

# report
if (-not $NoReport) {
    $md = Join-Path $outDir 'report.md'
    $html = Join-Path $outDir 'report.html'
    $lines = @(
        "# Riemann proof - CI report ($ts)",
        "",
        "| stage | name | exit |",
        "|-------|------|------|"
    )
    $i = 1
    foreach ($r in $results) {
        $status = if ($r.code -eq 0) { 'PASS' } else { 'FAIL' }
        $lines += "| $i | $($r.n) | $status |"
        $i++
    }
    $lines += ""
    if ($allOk) { $lines += "**ALL ENABLED STAGES PASSED.**" } else { $lines += "**SOME STAGES FAILED.**" }
    $lines += ""
    $lines += "Logs: " + $outDir
    Set-Content -Path $md -Value $lines -Encoding UTF8

    $htmlBody = @"
<!doctype html><html><head><meta charset='utf-8'>
<title>Riemann proof CI</title>
<style>
body{font-family:-apple-system,'Segoe UI',sans-serif;margin:40px 60px;color:#222}
h1{color:#2a4} table{border-collapse:collapse} th,td{border:1px solid #ccc;padding:8px 12px}
.pass{color:#084} .fail{color:#c22} .skip{color:#666}
</style></head><body>
<h1>Riemann proof - CI report</h1>
<p><em>generated $ts</em></p>
<p class="$(@{true='pass';false='fail'}[$allOk])"><b>$(if($allOk){'ALL PASSED'}else{'SOME FAILED'})</b></p>
<table><tr><th>#</th><th>name</th><th>exit</th></tr>
"@
    $i = 1
    foreach ($r in $results) {
        $cls = if ($r.code -eq 0) { 'pass' } else { 'fail' }
        $status = if ($r.code -eq 0) { 'PASS' } else { 'FAIL' }
        $htmlBody += "<tr><td>$i</td><td>$($r.n)</td><td class='$cls'><b>$status</b></td></tr>`n"
        $i++
    }
    $htmlBody += "</table><h2>How to run</h2><pre>powershell -ExecutionPolicy Bypass -File .\end_to_end.ps1</pre>"
    $htmlBody += "<h2>Logs</h2><p>$outDir</p></body></html>"
    Set-Content -Path $html -Value $htmlBody -Encoding UTF8

    $json = @{ timestamp=$ts; repo=$repo; verdict= $(if($allOk){'PASS'}else{'FAIL'}); stages=$results } | ConvertTo-Json -Depth 4
    Set-Content -Path (Join-Path $outDir 'summary.json') -Value $json -Encoding UTF8

    Ok "report.md / report.html / summary.json written to $outDir"
}

exit $(if ($allOk) { 0 } else { 1 })
