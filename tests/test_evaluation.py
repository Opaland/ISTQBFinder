"""Évaluation de la recherche (issue #56) : mesure, filtres de jeu et seuil de la CI."""
import json

import pytest

from qak import evaluation
from qak.cli import main

JEU = {"cas": [
    {"requete": "equivalence partitioning", "attendus": [{"code": "CTFL", "section": "1.2"}], "controle": True},
    {"requete": "risk level", "attendus": [{"code": "CTFL", "section": "2.1"}]},
    {"requete": "blockchain quantique", "attendus": [{"code": "CTFL", "section": "9"}], "controle": True},
    {"requete": "gestion des tests", "attendus": [{"code": "CTAL-TM", "section": "1"}]},  # document absent
]}


@pytest.fixture
def jeu(tmp_path):
    chemin = tmp_path / "jeu.json"
    chemin.write_text(json.dumps(JEU), encoding="utf-8")
    return chemin


def test_evaluer_rappel_mrr_et_jeux(bibliotheque_test, jeu):
    r = evaluation.evaluer(5, jeu=jeu)
    assert (r["trouves"], r["total"], r["ignorees"]) == (2, 3, 1)
    assert r["rappel"] == pytest.approx(2 / 3) and r["mrr"] == pytest.approx(2 / 3)
    assert [d["rang"] for d in r["details"]] == [1, 1, None]
    controle = evaluation.evaluer(5, controle=True, jeu=jeu)
    assert [d["requete"] for d in controle["details"]] == ["equivalence partitioning", "blockchain quantique"]
    assert [d["requete"] for d in evaluation.evaluer(5, controle=False, jeu=jeu)["details"]] == ["risk level"]
    with pytest.raises(ValueError):
        evaluation.evaluer(0, jeu=jeu)


def test_evaluer_min_rappel_fait_echouer(capsys, racine_isolee):
    # Bibliothèque vide : 0 question évaluée → aucun seuil n'est atteint (rc=2), sans seuil rc=0.
    assert main(["evaluer"]) == 0
    assert main(["evaluer", "--min-rappel", "0.80"]) == 2
    assert "aucune question évaluée" in capsys.readouterr().err


def test_evaluer_min_rappel_sous_le_seuil(capsys, bibliotheque_test, jeu, monkeypatch):
    vrai = evaluation.evaluer
    monkeypatch.setattr(evaluation, "evaluer", lambda k, controle=None, **_: vrai(k, controle, jeu=jeu))
    assert main(["evaluer", "--min-rappel", "0.6"]) == 0  # 2/3
    capsys.readouterr()
    assert main(["evaluer", "--min-rappel", "0.7"]) == 2
    assert "sous le seuil" in capsys.readouterr().err


@pytest.mark.parametrize("args", [["evaluer", "-k", "0"], ["chercher", "risque", "-n", "0"],
                                  ["evaluer", "--min-rappel", "1.5"]])
def test_k_n_et_seuil_valides(args, capsys):
    with pytest.raises(SystemExit) as e:
        main(args)
    assert e.value.code == 2


def test_jeu_eloigne_separe(bibliotheque_test, tmp_path):
    # Issue #107 : les questions « loin du vocabulaire ISTQB » forment un jeu à part, exclu du
    # contrôle et du réglage (elles mesurent une piste, pas le moteur livré).
    chemin = tmp_path / "jeu2.json"
    chemin.write_text(json.dumps({"cas": JEU["cas"] + [
        {"requete": "risk level", "attendus": [{"code": "CTFL", "section": "2.1"}], "eloigne": True}]}),
        encoding="utf-8")
    assert evaluation.evaluer(5, jeu=chemin)["total"] == 3
    assert evaluation.evaluer(5, controle=True, jeu=chemin)["total"] == 2
    assert [d["requete"] for d in evaluation.evaluer(5, jeu=chemin, eloigne=True)["details"]] == ["risk level"]


def test_jeu_examens_bien_forme():
    # Issue #150 : vérité terrain = objectif d'apprentissage du corrigé officiel (FL-4.2.1 → CTFL §4.2.1),
    # ramené à une section existante qui en est un préfixe ; jeu à part (ni contrôle, ni éloigné).
    from qak import chemins
    fichier = evaluation.fichier_jeu("examens")
    assert fichier == chemins.CODE / "eval" / "examens.json" and evaluation.fichier_jeu("controle") is None
    cas = json.loads(fichier.read_text(encoding="utf-8"))["cas"]
    assert len(cas) >= 100
    prefixes = {"CTFL": "FL", "CTAL-TM": "TM", "CTAL-TA": "TA"}
    for c in cas:
        (a,) = c["attendus"]
        prefixe, numero = c["objectif"].split("-")
        assert prefixes[a["code"]] == prefixe and evaluation._dans_section(numero, a["section"]), c
        assert c["source"] and not c.get("controle") and not c.get("eloigne")
        assert len(c["requete"]) <= 140, c["requete"]  # requête reformulée, pas l'énoncé recopié


def test_evaluer_jeu_examens_lit_son_fichier(capsys, racine_isolee):
    assert main(["evaluer", "--jeu", "examens"]) == 0
    nombre = len(json.loads(evaluation.fichier_jeu("examens").read_text(encoding="utf-8"))["cas"])
    assert f"ignorées (document absent) : {nombre}" in capsys.readouterr().out
