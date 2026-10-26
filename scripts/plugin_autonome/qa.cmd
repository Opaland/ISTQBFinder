@echo off
rem Lanceur Windows du plugin ISTQBFinder autonome (meme role que bin/qa) : Claude Code
rem resout la commande MCP ${CLAUDE_PLUGIN_ROOT}/bin/qa vers ce fichier, avec ou sans Git Bash.
rem Fins de ligne LF : ni etiquette ni goto ; aucun chemin developpe dans un bloc ( ).
setlocal
set "LANCEUR=%~dp0..\lanceur.py"
set "PY="
set "OPT="
python -c "import sys; sys.exit(sys.version_info < (3, 10))" >nul 2>nul && set "PY=python"
if not defined PY py -3 -c "import sys; sys.exit(sys.version_info < (3, 10))" >nul 2>nul && set "PY=py" && set "OPT=-3"
if not defined PY (
  echo ISTQBFinder : Python 3.10 ou plus introuvable dans le PATH ^(python, py^). L'installer depuis python.org, puis relancer. 1>&2
  exit /b 2
)
"%PY%" %OPT% "%LANCEUR%" %*
exit /b %ERRORLEVEL%
