"""Outils partagés par les scripts de scripts/ (#197)."""
import shutil
import tempfile
from pathlib import Path

DOSSIERS = ("bibliotheque", "connaissances", "referentiel")


def racine_temporaire(source: Path, fichiers: tuple[str, ...], prefixe: str) -> Path:
    """Racine de données jetable pour `QAK_RACINE` : copie de `fichiers` (chemins relatifs
    à `source`, ignorés s'ils n'existent pas), PDF de `bibliotheque/sources` liés (copiés
    si le lien est impossible : seul le contrôle « index à jour » les lit). Une écriture
    dans la copie n'atteint jamais le dépôt ; à supprimer par l'appelant."""
    tmp = Path(tempfile.mkdtemp(prefix=prefixe))
    for dossier in DOSSIERS:
        (tmp / dossier).mkdir()
    for rel in fichiers:
        if (source / rel).exists():
            shutil.copy2(source / rel, tmp / rel)
    try:
        (tmp / "bibliotheque" / "sources").symlink_to(source / "bibliotheque" / "sources")
    except OSError:
        shutil.copytree(source / "bibliotheque" / "sources", tmp / "bibliotheque" / "sources")
    return tmp
