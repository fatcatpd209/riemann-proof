@echo off
setlocal
REM ============ arXiv/Zenodo/GitHub ONE-SHOT SUBMIT =============
REM Usage: run once from PowerShell:
REM   .\submit_all.ps1
REM First set env vars:
REM   $env:GITHUB_PAT="ghp_xxx"
REM   $env:ZENODO_TOKEN="xxx"
REM ==============================================================

echo === Step 1: GitHub Release ===
python "%~dp0release_github.py"
if errorlevel 1 ( echo GITHUB FAILED & exit /b 1 )

echo === Step 2: Zenodo Upload ===
python "%~dp0zenodo_upload.py"
if errorlevel 1 ( echo ZENODO FAILED & exit /b 2 )

echo === Step 3: arXiv browser automation (open your browser tab!) ===
echo Open this tab and make sure you're LOGGED IN as fatcatpd209:
echo   https://arxiv.org/submit
echo When the tab loads, CONTINUE in this terminal.
pause

echo All done. Now paste the Zenodo DOI into your arXiv abstract manually.
endlocal
