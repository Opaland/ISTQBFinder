@echo off
rem Fichier généré par scripts/generer_integrations.py : ne pas modifier, relancer le script.
rem Lanceur Windows du plugin ISTQBFinder (#203) : meme role que bin/qa (sh), sans Git Bash.
setlocal
set "RACINE=%~dp0..\.."
if not exist "%RACINE%\qa.py" (
  echo ISTQBFinder : qa.py introuvable deux dossiers au-dessus de bin\. Le plugin se charge en place depuis un clone installe : claude plugin marketplace add ^<clone^>/plugin, puis claude plugin install istqbfinder@istqbfinder-local. 1>&2
  exit /b 2
)
set "PY="
set "OPT="
if exist "%RACINE%\.venv\Scripts\python.exe" set "PY=%RACINE%\.venv\Scripts\python.exe"
if not defined PY python -c "import sys; sys.exit(sys.version_info < (3, 10))" >nul 2>nul && set "PY=python"
if not defined PY py -3 -c "import sys; sys.exit(sys.version_info < (3, 10))" >nul 2>nul && set "PY=py" && set "OPT=-3"
if not defined PY (
  echo ISTQBFinder : ni venv .venv dans le clone ni Python 3.10+ dans le PATH. Lancer installer.ps1 dans le clone. 1>&2
  exit /b 2
)
"%PY%" %OPT% "%RACINE%\qa.py" %*
exit /b %ERRORLEVEL%
