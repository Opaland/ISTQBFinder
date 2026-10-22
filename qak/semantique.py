"""Recherche sémantique OPTIONNELLE (issue #107) : embeddings multilingues Hugging Face.

Désactivée par défaut. L'installation par défaut et la CI n'en dépendent pas :
    pip install -r requirements-semantique.txt
    python qa.py actualiser --semantique      # calcule bibliotheque/vecteurs.npz
    python qa.py chercher "…" --semantique     # recherche hybride BM25 + cosinus (RRF)

Le modèle ne sert qu'à CLASSER des passages de la bibliothèque : les citations restent
tirées des passages lus, jamais du modèle. Sans dépendances ou sans vecteurs, la recherche
reste lexicale et un avertissement le dit.
Modèle par défaut : intfloat/multilingual-e5-small (licence MIT, 118 M paramètres,
≈ 470 Mo) ; un autre modèle sentence-transformers via QAK_MODELE_SEMANTIQUE. Sans accès à
huggingface.co, télécharger le dossier du modèle ailleurs et pointer QAK_MODELE_SEMANTIQUE
vers ce dossier local.
"""
import os
import sqlite3
import time
from functools import lru_cache

from . import chemins

MODELE = "intfloat/multilingual-e5-small"
INSTALLATION = ("recherche sémantique indisponible : `pip install -r requirements-semantique.txt` "
                "puis `python qa.py actualiser --semantique`")


def nom_modele() -> str:
    return os.environ.get("QAK_MODELE_SEMANTIQUE") or MODELE


def fichier_vecteurs():
    return chemins.index_db().with_name("vecteurs.npz")


def dependances_presentes() -> bool:
    try:
        import numpy  # noqa: F401
        import sentence_transformers  # noqa: F401
    except ImportError:
        return False
    return True


def _prefixes(nom: str) -> tuple[str, str]:
    """Les modèles E5 attendent « query: » / « passage: » devant les textes."""
    return ("query: ", "passage: ") if "e5" in nom.lower() else ("", "")


@lru_cache(maxsize=1)
def _modele(nom: str):
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer(nom, device="cpu")


def _passages(cx: sqlite3.Connection) -> list[sqlite3.Row]:
    return cx.execute("SELECT p.id, p.section_titre, p.texte FROM passages p JOIN documents d ON d.doc_id = p.doc_id "
                      "WHERE d.statut_version = 'courant' AND p.sommaire = 0 ORDER BY p.id").fetchall()


def _empreinte(ids) -> str:
    return f"{len(ids)}:{min(ids, default=0)}:{max(ids, default=0)}:{sum(ids) % 1000003}"


def indexer(cx: sqlite3.Connection, lot: int = 64) -> dict:
    """Encode tous les passages courants et écrit bibliotheque/vecteurs.npz."""
    import numpy as np
    nom = nom_modele()
    _, prefixe = _prefixes(nom)
    rows = _passages(cx)
    debut = time.perf_counter()
    vecteurs = _modele(nom).encode([f"{prefixe}{r['section_titre'] or ''}\n{r['texte']}" for r in rows],
                                   batch_size=lot, normalize_embeddings=True, show_progress_bar=False)
    duree = time.perf_counter() - debut
    ids = np.array([r["id"] for r in rows], dtype=np.int64)
    np.savez(fichier_vecteurs(), ids=ids, vecteurs=vecteurs.astype(np.float16), modele=nom,
             empreinte=_empreinte(ids.tolist()))
    return {"passages": len(rows), "secondes": round(duree, 1), "modele": nom,
            "mo": round(fichier_vecteurs().stat().st_size / 1e6, 1)}


@lru_cache(maxsize=1)
def _charger(chemin: str, mtime: float):
    import numpy as np
    d = np.load(chemin)
    return d["ids"], d["vecteurs"].astype(np.float32), str(d["modele"]), str(d["empreinte"])


def etat(cx: sqlite3.Connection) -> str | None:
    """None si la recherche sémantique est utilisable, sinon la raison (française)."""
    if not dependances_presentes():
        return INSTALLATION
    f = fichier_vecteurs()
    if not f.exists():
        return "recherche sémantique : vecteurs absents — lancer `python qa.py actualiser --semantique`"
    ids, _, modele, empreinte = _charger(str(f), f.stat().st_mtime)
    if modele != nom_modele() or empreinte != _empreinte([r["id"] for r in _passages(cx)]):
        return "recherche sémantique : vecteurs périmés (index ou modèle changé) — relancer `actualiser --semantique`"
    return None


def classement(requete: str, k: int = 100) -> list[tuple[int, float]]:
    """Les k passages les plus proches de la requête : [(id, cosinus)], du plus proche au moins proche.
    À n'appeler qu'après `etat(cx) is None`."""
    import numpy as np
    f = fichier_vecteurs()
    ids, vecteurs, modele, _ = _charger(str(f), f.stat().st_mtime)
    prefixe, _ = _prefixes(modele)
    q = _modele(modele).encode([prefixe + requete], normalize_embeddings=True)[0].astype(np.float32)
    scores = vecteurs @ q
    meilleurs = np.argsort(-scores)[:k]
    return [(int(ids[i]), float(scores[i])) for i in meilleurs]
