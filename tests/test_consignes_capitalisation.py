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


def test_consigne_d_erreurs_conforme_a_idee_ajouter(monkeypatch, capsys):
    """#256 : capitalisation.md décrit les erreurs de `idee ajouter` telles qu'elles sont
    (toutes listées en une fois ; `pages` entier converti, pas refusé). Le texte et le
    comportement sont vérifiés ensemble : changer l'un sans l'autre fait échouer ce test."""
    consigne = " ".join((RACINE_CODE / ".claude" / "skills" / "qa-knowledge" / "reference"
                         / "capitalisation.md").read_text(encoding="utf-8").split())
    assert "une à la fois" not in consigne and "jamais `29`" not in consigne
    assert "listant toutes en une fois" in consigne
    assert "un entier (`29`) est accepté et converti en texte" in consigne

    base = {"titre": "Identifier les risques qualité", "resume": "r", "probleme": "p", "principe": "x"}
    fautive = {**base, "theme": "rbt", "references": [{"type": "istqb", "document": "X", "page": "3"}]}
    monkeypatch.setattr("sys.stdin", io.StringIO(json.dumps(fautive)))
    assert main(["idee", "ajouter"]) == 2
    err = capsys.readouterr().err
    assert "toutes listées" in err and "theme_principal" in err and "doc_id" in err and "pages" in err, err

    entier = {**base, "theme_principal": "rbt", "references": [{"type": "web", "url": "https://exemple.org", "pages": 29}]}
    monkeypatch.setattr("sys.stdin", io.StringIO(json.dumps(entier)))
    assert main(["idee", "ajouter"]) == 0, capsys.readouterr()
    assert "Idée créée" in capsys.readouterr().out


# Toute consigne qui chiffre la longueur d'un extrait : « au moins 6 mots significatifs ».
LONGUEUR_EXTRAIT = re.compile(r"au moins (\d+) mots\s+significatifs")


def test_gabarit_et_consignes_annoncent_la_longueur_reelle_de_l_extrait(monkeypatch, capsys):
    """#263 : `idee modele` annonçait un extrait de « quelques mots » alors que `idee ajouter`
    exige MOTS_EXTRAIT_MIN mots significatifs ; les agents suivaient le gabarit à la lettre et
    leur JSON était refusé. Le gabarit, chaque consigne qui chiffre la règle et la validation
    sont vérifiés ensemble : changer l'un sans les autres fait échouer ce test."""
    from qak.connaissances import MOTS_EXTRAIT_MIN
    gabarit = MODELE_IDEE["references"][0]["extrait"]
    assert "quelques mots" not in gabarit
    assert [int(n) for n in LONGUEUR_EXTRAIT.findall(gabarit)] == [MOTS_EXTRAIT_MIN], gabarit
    assert "phrase entière" in gabarit and "mot pour mot" in gabarit

    chiffres = {}
    for chemin in CONSIGNES:
        texte = " ".join(chemin.read_text(encoding="utf-8").split())
        # Les bilans d'essais (docs/essais-*.md) citent l'ancien gabarit : historique, pas consigne.
        if not chemin.name.startswith("essais"):
            assert "quelques mots" not in texte, f"{chemin.name} : « quelques mots » contredit la règle de l'extrait"
        for n in LONGUEUR_EXTRAIT.findall(texte):
            chiffres.setdefault(int(n), []).append(chemin.relative_to(RACINE_CODE).as_posix())
    assert set(chiffres) == {MOTS_EXTRAIT_MIN}, chiffres
    thomas = " ".join((RACINE_CODE / ".claude" / "agents" / "thomas.md").read_text(encoding="utf-8").split())
    assert f"au moins {MOTS_EXTRAIT_MIN} mots significatifs" in thomas

    # La validation applique bien ce chiffre : MOTS_EXTRAIT_MIN - 1 mots refusés, au seuil
    # le contrôle de longueur passe (l'extrait est ensuite cherché dans la page).
    from qak.connaissances import extrait_trop_court
    mots_ok = " ".join(f"mot{i}" for i in range(MOTS_EXTRAIT_MIN))
    assert extrait_trop_court(mots_ok) is None
    assert f"minimum {MOTS_EXTRAIT_MIN}" in extrait_trop_court(mots_ok.rsplit(" ", 1)[0])

    # `idee doublons --extrait` signale le même défaut avant que le JSON soit proposé.
    monkeypatch.setattr("sys.stdin", io.StringIO(""))
    assert main(["idee", "doublons", "--titre", "Approche GQM pour les métriques", "--theme", "rbt",
                 "--doc", "CTAL-TM-3.0-fr", "--pages", "29", "--extrait", "L'approche GQM"]) == 0
    assert "Extrait trop court" in capsys.readouterr().out
    assert main(["idee", "doublons", "--titre", "Approche GQM pour les métriques", "--theme", "rbt",
                 "--doc", "CTAL-TM-3.0-fr", "--pages", "29", "--extrait", mots_ok]) == 0
    assert "Extrait trop court" not in capsys.readouterr().out
