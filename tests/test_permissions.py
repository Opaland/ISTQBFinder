"""Issue #19 : les commandes qui écrivent (base d'idées, bibliothèque, taxonomie) ne sont
jamais pré-approuvées ; l'utilisateur confirme chaque écriture."""
import json
import re

from conftest import RACINE_CODE

ECRITURE = ("idee ajouter", "idee modifier", "idee statut", "idee retour", "idee lier", "idee retirer",
            "theme ajouter", "theme obsolete", "telecharger", "importer", "actualiser", "corriger", "retirer")


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


def _commandes_documentees(texte: str) -> list[str]:
    """Lignes `python qa.py …` des blocs de code et des `code` en ligne d'un document."""
    blocs = re.findall(r"```(?:bash|text)?\n(.*?)```", texte, re.S)
    lignes = [l.lstrip("$ ").strip() for b in blocs for l in b.splitlines()]
    lignes += re.findall(r"`(python3? qa\.py [^`]+)`", texte)
    # « python qa.py <commande> » est un gabarit, pas une commande.
    return [l for l in lignes if re.match(r"python3? qa\.py [^<]", l)]


def test_exemples_de_lecture_couverts_par_l_allowlist_et_sans_json():
    """#128 : chaque commande en lecture seule de capitalisation.md (et des procédures de
    Thomas et du skill) est couverte par une règle `allow` de settings.json, et ne contient
    ni heredoc ni accolade suivie d'un guillemet : Claude Code bloque ces formes en
    `claude -p` (« Contains brace with quote character »), même autorisées."""
    s = json.loads((RACINE_CODE / ".claude" / "settings.json").read_text(encoding="utf-8"))
    prefixes = [re.match(r"Bash\((.*?):\*\)$", r).group(1) for r in s["permissions"]["allow"]
                if re.match(r"Bash\(.*:\*\)$", r)]
    sources = [RACINE_CODE / ".claude" / "skills" / "qa-knowledge" / "reference" / "capitalisation.md",
               RACINE_CODE / ".claude" / "skills" / "qa-knowledge" / "SKILL.md",
               RACINE_CODE / ".claude" / "agents" / "thomas.md"]
    vues = []
    for f in sources:
        for cmd in _commandes_documentees(f.read_text(encoding="utf-8")):
            if any(cmd.split("qa.py ", 1)[1].startswith(e) for e in ECRITURE):
                continue  # écritures : demandées à l'utilisateur (règles `ask`)
            vues.append(cmd)
            assert any(cmd.startswith(p) for p in prefixes), f"{f.name} : {cmd} hors allowlist"
            assert "<<" not in cmd and not re.search(r"\{\s*[\"']", cmd), f"{f.name} : {cmd} bloqué en -p"
    assert any("idee doublons --titre" in c for c in vues)


def test_confiance_et_diagnostic_preapprouves():
    """#146 : `confiance` (appelé à chaque réponse) et `diagnostic` n'écrivent rien ; ils sont
    pré-approuvés dans settings.json et dans le skill qui calcule la confiance."""
    s = json.loads((RACINE_CODE / ".claude" / "settings.json").read_text(encoding="utf-8"))
    skill = (RACINE_CODE / ".claude" / "skills" / "qa-knowledge" / "SKILL.md").read_text(encoding="utf-8")
    for cmd in ("confiance", "diagnostic"):
        assert f"Bash(python qa.py {cmd}:*)" in s["permissions"]["allow"]
        assert f"Bash(python qa.py {cmd}:*)" in skill
        assert not _ecrit(f"Bash(python qa.py {cmd}:*)")
