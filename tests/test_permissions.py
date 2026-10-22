"""Issue #19 : les commandes qui écrivent (base d'idées, bibliothèque, taxonomie) ne sont
jamais pré-approuvées ; l'utilisateur confirme chaque écriture."""
import json
import re

from conftest import RACINE_CODE

ECRITURE = ("idee ajouter", "idee modifier", "idee statut", "idee retour", "idee lier", "theme ajouter",
            "theme obsolete", "telecharger", "importer", "actualiser", "corriger", "retirer")


def _ecrit(regle: str) -> bool:
    m = re.match(r"Bash\(python3? qa\.py ?(.*?):?\*?\)$", regle)
    if not m:
        return False
    cmd = m.group(1).rstrip(":*").strip()
    return cmd == "" or any(cmd.startswith(e) or e.startswith(cmd) and len(cmd) < len(e) for e in ECRITURE)


def test_settings_n_autorise_que_la_lecture():
    s = json.loads((RACINE_CODE / ".claude" / "settings.json").read_text(encoding="utf-8"))
    assert not [r for r in s["permissions"]["allow"] if _ecrit(r)]
    demandees = " ".join(s["permissions"]["ask"])
    assert all(f"qa.py {e}:" in demandees for e in ECRITURE)


def test_skills_ne_preapprouvent_pas_les_ecritures():
    for f in (RACINE_CODE / ".claude" / "skills").glob("*/SKILL.md"):
        ligne = next(l for l in f.read_text(encoding="utf-8").splitlines() if l.startswith("allowed-tools:"))
        regles = re.findall(r"Bash\([^)]*\)", ligne)
        assert not [r for r in regles if _ecrit(r)], f.parent.name
