"""Journal append-only des modifications de la base de connaissances et de la taxonomie
(connaissances/journal.jsonl, versionné) : qui a changé quoi, quand et pourquoi.

Le fichier est fusionné par Git en `merge=union` (.gitattributes) : deux postes qui ont
chacun ajouté des entrées n'entrent pas en conflit, les lignes des deux côtés sont gardées."""
import getpass
import json
import subprocess
from datetime import datetime
from functools import lru_cache
from pathlib import Path

from . import chemins

MARQUEURS_CONFLIT = ("<<<<<<<", "=======", ">>>>>>>", "|||||||")


@lru_cache(maxsize=1)
def auteur() -> str:
    """`git config user.name` du dépôt, sinon l'utilisateur du système."""
    try:
        r = subprocess.run(["git", "-C", str(chemins.racine()), "config", "user.name"],
                           capture_output=True, text=True, timeout=5)
        if r.returncode == 0 and r.stdout.strip():
            return r.stdout.strip()
    except (OSError, subprocess.SubprocessError):
        pass
    try:
        return getpass.getuser()
    except Exception:  # pas de compte identifiable (conteneur…)
        return "inconnu"


def noter(action: str, cible: str, details: dict | None = None, motif: str | None = None) -> dict:
    entree = {"horodatage": datetime.now().astimezone().isoformat(timespec="seconds"), "auteur": auteur(),
              "action": action, "cible": cible}
    if motif:
        entree["motif"] = motif
    if details:
        entree["details"] = details
    p = chemins.journal_jsonl()
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "a", encoding="utf-8") as f:
        f.write(json.dumps(entree, ensure_ascii=False) + "\n")
    return entree


def controler_conflits(p: Path, lignes: list[str], conseil: str) -> None:
    """Marqueurs de conflit Git laissés dans un JSONL : message lisible (fichier, ligne,
    quoi faire) au lieu d'un « Expecting value: line 1 column 1 »."""
    for n, ligne in enumerate(lignes, 1):
        if ligne.startswith(MARQUEURS_CONFLIT):
            raise ValueError(f"{p.name}, ligne {n} : marqueur de conflit Git « {ligne[:7]} » — fusion non "
                             f"terminée. {conseil} Supprimer les lignes <<<<<<< ======= >>>>>>>, puis `git add`.")


def lire(cible: str | None = None, limite: int = 30) -> list[dict]:
    p = chemins.journal_jsonl()
    if not p.exists():
        return []
    brut = p.read_text(encoding="utf-8-sig").splitlines()
    controler_conflits(p, brut, "Le journal est en ajout seul : garder les lignes des DEUX côtés.")
    lignes = []
    for n, l in enumerate(brut, 1):
        if not l.strip():
            continue
        try:
            lignes.append(json.loads(l))
        except json.JSONDecodeError as exc:
            raise ValueError(f"{p.name}, ligne {n} : JSON invalide ({exc.msg}). Corriger la ligne "
                             "(une entrée par ligne), puis relancer.") from exc
    if cible:
        lignes = [l for l in lignes if l["cible"] == cible or cible in json.dumps(l.get("details", {}))]
    return lignes[-limite:]
