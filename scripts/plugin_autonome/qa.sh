#!/bin/sh
# Lanceur du plugin ISTQBFinder autonome (Linux, macOS ; Windows : bin/qa.cmd) : `qa <commande>`.
# bin/ est dans le PATH de l'outil Bash ; le serveur MCP du plugin est `qa mcp`. Tout le
# travail (venv, dossier de données, QAK_RACINE) est fait par lanceur.py, en Python.
LANCEUR="$(cd "$(dirname "$0")/.." && pwd)/lanceur.py"
# Python 3.10 ou plus seulement (l'alias « python3 » du Microsoft Store, sans Python, échoue ici).
for PY in python3 python; do
  if "$PY" -c "import sys; sys.exit(sys.version_info < (3, 10))" >/dev/null 2>&1; then
    exec "$PY" "$LANCEUR" "$@"
  fi
done
echo "ISTQBFinder : Python 3.10 ou plus introuvable dans le PATH (python3, python). L'installer, puis relancer." >&2
exit 2
