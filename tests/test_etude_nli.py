"""Choix du passage de l'étude NLI / du juge (scripts/etude_nli.py, #243).

Le passage d'une paire est pris dans l'index réel des syllabus versionnés (importés dans la
racine isolée du garde-fou, sans réseau) : pour CTFL §4.1 p. 39 et CT-AI §3.4.3 p. 37,
l'ancien choix (le morceau qui partage le plus de mots avec l'affirmation française)
retenait un morceau sans la phrase qui soutient l'affirmation."""
import importlib.util
import json

import pytest

from conftest import RACINE_CODE as RACINE
from qak import bibliotheque

_spec = importlib.util.spec_from_file_location("etude_nli", RACINE / "scripts" / "etude_nli.py")
etude_nli = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(etude_nli)

MANIFESTE = json.loads((RACINE / "bibliotheque" / "manifeste.json").read_text(encoding="utf-8"))["documents"]
JEU = json.loads((RACINE / "eval" / "nli" / "paires.json").read_text(encoding="utf-8"))["paires"]


def _importer(doc_id):
    e = next(e for e in MANIFESTE.values() if e["doc_id"] == doc_id)
    r = bibliotheque.importer(RACINE / "bibliotheque" / "sources" / e["fichier"],
                              meta_forcee={**{k: e[k] for k in e.get("champs_forces", [])}, "doc_id": doc_id})
    assert r["etat"] in ("importe", "doublon"), r


@pytest.mark.parametrize("doc_id, page, section, phrase", [
    ("CTFL-4.0.1-en", 39, "4.1", "Experience-based test techniques can detect defects that may be missed"),
    ("CT-AI-2.0-en", 37, "3.4.3", "structural coverage alone does not guarantee that a neural network will generalize"),
])
def test_passage_contient_la_phrase_utile(doc_id, page, section, phrase):
    _importer(doc_id)
    p = next(p for p in JEU if (p["doc_id"], p["page"], p["section"]) == (doc_id, page, section)
             and p["etiquette"] == "soutenue")
    texte = " ".join(etude_nli.passage(bibliotheque.connecter(), p, p["affirmation"]).split())
    assert phrase in texte, texte[:300]
    assert len(texte) <= etude_nli.LIMITE_CARACTERES


def test_fenetre_pure():
    morceaux = ["Intro sans rapport. " * 20, "Neuron coverage does not guarantee generalization.", "Fin. " * 300]
    choisi = etude_nli.fenetre(morceaux, "La couverture des neurones ne garantit pas la généralisation.", limite=600)
    assert "Neuron coverage" in choisi and "Fin." not in choisi
    # Tout tient dans la limite : la section entière.
    assert etude_nli.fenetre(["a b", "c d"], "rien", limite=100) == "a b\nc d"
    # Un morceau seul plus long que la limite reste candidat (jamais de passage vide).
    assert etude_nli.fenetre(["x " * 500], "x", limite=10).startswith("x")
