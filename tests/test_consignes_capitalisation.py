"""Les exemples d'idée en JSON des consignes passent `idee ajouter` (#230).

Un agent recopie le JSON des consignes : un exemple au mauvais format (`theme` au lieu de
`theme_principal`, `page` entier, `document` au lieu de `doc_id`) se propage dans ses
propositions « À capitaliser ». Chaque exemple est donc passé à la vraie commande
`idee ajouter`, dans la racine isolée du garde-fou (rien n'est écrit dans connaissances/),
après import des syllabus réels qu'il cite : références, pages, sections et extraits sont
vérifiés comme pour l'utilisateur.
"""
import io
import json
import re

import pytest

from conftest import RACINE_CODE
from qak import bibliotheque
from qak.cli import MODELE_IDEE, main

# Sources des consignes (les copies générées de plugin/ et .gemini/ en dérivent).
CONSIGNES = sorted([*(RACINE_CODE / ".claude").rglob("*.md"), RACINE_CODE / "AGENTS.md",
                    RACINE_CODE / "README.md", *(RACINE_CODE / "docs").glob("*.md")])
BLOC = re.compile(r"```json\s*\n(.*?)\n\s*```|<<'JSON'\s*\n(.*?)\n\s*JSON\s*$", re.S | re.M)
# Clés qu'une référence peut porter : celles du gabarit, plus les compléments documentés.
CLES_REFERENCE = {k for r in MODELE_IDEE["references"] for k in r} | {"version", "consulte_le"}


def _exemples():
    for chemin in CONSIGNES:
        for m in BLOC.finditer(chemin.read_text(encoding="utf-8")):
            texte = m.group(1) or m.group(2)
            try:
                donnees = json.loads(texte)
            except json.JSONDecodeError:
                continue  # gabarit à trous (« <le JSON ci-dessous> ») : pas un exemple
            if isinstance(donnees, dict) and "titre" in donnees:
                ligne = chemin.read_text(encoding="utf-8")[:m.start()].count("\n") + 1
                yield pytest.param(donnees, id=f"{chemin.relative_to(RACINE_CODE).as_posix()}:{ligne}")


EXEMPLES = list(_exemples())


def test_les_consignes_contiennent_des_exemples():
    assert len(EXEMPLES) >= 2, "plus aucun exemple d'idée trouvé : le motif de BLOC est-il à jour ?"


def _importer_documents_cites(idee):
    manifeste = json.loads((RACINE_CODE / "bibliotheque" / "manifeste.json").read_text(encoding="utf-8"))["documents"]
    for ref in idee.get("references", []):
        if ref.get("type") != "istqb":
            continue
        entree = next((e for e in manifeste.values() if e["doc_id"] == ref.get("doc_id")), None)
        assert entree, f"{ref.get('doc_id')} : doc_id absent du manifeste (donner le doc_id exact)"
        forces = {k: entree[k] for k in entree.get("champs_forces", [])}
        r = bibliotheque.importer(RACINE_CODE / "bibliotheque" / "sources" / entree["fichier"],
                                  meta_forcee={**forces, "doc_id": entree["doc_id"]})
        assert r["etat"] in ("importe", "doublon") and r["doc_id"] == entree["doc_id"], r


@pytest.mark.parametrize("idee", EXEMPLES)
def test_exemple_d_idee_accepte_par_idee_ajouter(idee, monkeypatch, capsys):
    inconnues = [k for k in idee if k not in MODELE_IDEE]
    assert not inconnues, f"champ(s) absent(s) de `idee modele` : {inconnues}"
    for ref in idee.get("references", []):
        assert set(ref) <= CLES_REFERENCE, f"clé(s) de référence inconnue(s) : {set(ref) - CLES_REFERENCE}"
    _importer_documents_cites(idee)
    monkeypatch.setattr("sys.stdin", io.StringIO(json.dumps(idee, ensure_ascii=False)))
    code = main(["idee", "ajouter"])
    sortie = capsys.readouterr()
    assert code == 0 and "Idée créée" in sortie.out, sortie.err or sortie.out
    assert "non vérifiable" not in sortie.out, sortie.out
