#!/usr/bin/env bash
# Installation d'ISTQBFinder sous Linux / macOS. Idempotent : relançable sans risque
# (venv réutilisé, indexation incrémentale).
#
#   ./installer.sh                         # Python, venv, dépendances, index, diagnostic
#   ./installer.sh --assistant gemini      # + vérifie l'intégration claude|copilot|gemini|tous
#
# Procédure détaillée par assistant : docs/installation.md
set -euo pipefail

cd "$(dirname "$0")"

ASSISTANT=""
while [ $# -gt 0 ]; do
    case "$1" in
        --assistant) ASSISTANT="${2:-}"; shift 2 || { echo "KO : --assistant attend claude, copilot, gemini ou tous." >&2; exit 2; } ;;
        --assistant=*) ASSISTANT="${1#*=}"; shift ;;
        -h|--help) sed -n '2,8p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
        *) echo "KO : option inconnue « $1 » (voir ./installer.sh --help)." >&2; exit 2 ;;
    esac
done
case "$ASSISTANT" in
    ""|claude|copilot|gemini|tous) ;;
    *) echo "KO : --assistant attend claude, copilot, gemini ou tous (reçu : « $ASSISTANT »)." >&2; exit 2 ;;
esac

etape() { printf '\n== %s\n' "$1"; }
echec() { printf '\nKO : %s\n' "$1" >&2; exit 1; }

etape "1/5 Python ≥ 3.10"
PY=""
for candidat in python3 python; do
    if command -v "$candidat" >/dev/null 2>&1 \
        && "$candidat" -c 'import sys; sys.exit(sys.version_info < (3, 10))' 2>/dev/null; then
        PY="$candidat"; break
    fi
done
[ -n "$PY" ] || echec "Python 3.10 ou plus récent introuvable. Installez-le (https://www.python.org/downloads/ ; Debian/Ubuntu : sudo apt install python3 python3-venv ; macOS : brew install python), puis relancez."
echo "OK : $("$PY" --version) ($(command -v "$PY"))"

etape "2/5 Environnement virtuel .venv"
if [ -x .venv/bin/python ] && .venv/bin/python -c 'import sys; sys.exit(sys.version_info < (3, 10))' 2>/dev/null; then
    echo "OK : .venv existant réutilisé"
else
    "$PY" -m venv .venv || echec "création du venv impossible (Debian/Ubuntu : sudo apt install python3-venv), puis relancez."
    echo "OK : .venv créé"
fi
VPY=.venv/bin/python

etape "3/5 Dépendances (requirements.txt)"
"$VPY" -m pip install --disable-pip-version-check -q -r requirements.txt \
    || echec "installation des dépendances impossible (réseau ? proxy ?). Relancez une fois le problème réglé."
echo "OK : dépendances installées"

etape "4/5 Indexation de la bibliothèque (≈ 3 min la première fois, quelques secondes ensuite)"
"$VPY" qa.py actualiser || echec "indexation en échec : voir le message ci-dessus."

etape "5/5 Diagnostic"
if [ -n "$ASSISTANT" ]; then
    "$VPY" qa.py diagnostic --assistant "$ASSISTANT" || echec "diagnostic en échec : corrigez les lignes KO ci-dessus puis relancez ./installer.sh."
else
    "$VPY" qa.py diagnostic || echec "diagnostic en échec : corrigez les lignes KO ci-dessus puis relancez ./installer.sh."
fi

cat <<'FIN'

Installation terminée. Lancez votre assistant depuis ce dossier, venv activé
(les commandes `python qa.py …` utilisent alors le bon Python) :

    source .venv/bin/activate
    claude          # Claude Code    (ou : code .   pour VS Code + Copilot ; gemini   pour Gemini CLI)

Procédure par assistant : docs/installation.md
FIN
