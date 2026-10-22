import json
import re
from urllib.parse import urlparse

from qak import bibliotheque, chemins, textes


def test_thesaurus_un_terme_un_seul_concept():
    vus = {}
    for cid, termes in textes.thesaurus():
        for t in termes:
            n = textes.normaliser(t)
            assert n not in vus, f"« {t} » dans {vus.get(n)} et {cid}"
            vus[n] = cid


def test_catalogue_officiel_coherent():
    cat = bibliotheque.catalogue()
    codes = [d["code"] for d in cat["documents"]]
    assert len(codes) == len(set(codes)) >= 25
    for d in cat["documents"]:
        assert urlparse(d["telechargement"]).hostname == "istqb.org"
        assert urlparse(d["page_officielle"]).hostname == "istqb.org"
        assert d["niveau"] in ("fondation", "avance", "expert", "specialiste")
        for m in d["motifs"]:
            re.compile(m)
    assert cat["domaines_autorises"] == ["istqb.org"]


def test_jeu_d_evaluation_bien_forme():
    cas = json.loads((chemins.CODE / "eval" / "requetes.json").read_text(encoding="utf-8"))["cas"]
    codes = {d["code"] for d in bibliotheque.catalogue()["documents"]}
    assert len(cas) >= 40 and sum(bool(c.get("controle")) for c in cas) >= 10
    assert all(a["code"] in codes for c in cas for a in c["attendus"])


def test_catalogue_niveaux_agiles_et_syllabus_en_retrait():
    """#44 : relevé istqb.org/certifications du 2026-10-22 — CT-ATLaS, CTFL-AT et CTAL-ATT sont
    « Specialist » ; CTFL-AT et CTAL-ATT sont « Retiring », remplacés par CTAL-AT (Core Advanced)."""
    from qak import bibliotheque, catalogue
    cat = {d["code"]: d for d in bibliotheque.catalogue()["documents"]}
    assert {c: cat[c]["niveau"] for c in ("CT-ATLaS", "CTFL-AT", "CTAL-ATT", "CTAL-AT")} == {
        "CT-ATLaS": "specialiste", "CTFL-AT": "specialiste", "CTAL-ATT": "specialiste", "CTAL-AT": "avance"}
    for code in ("CTFL-AT", "CTAL-ATT"):
        assert cat[code]["statut_officiel"] == "retiring" and cat[code]["successeur"] in cat
        assert "successeur : CTAL-AT" in catalogue.statut_officiel(code)
    assert catalogue.statut_officiel("CTAL-AT") == "" and catalogue.statut_officiel(None) == ""
    # Le manifeste versionné suit le catalogue.
    manifeste = json.loads((chemins.CODE / "bibliotheque" / "manifeste.json").read_text(encoding="utf-8"))
    assert any(e.get("code") == "CTFL-AT" for e in manifeste["documents"].values())
    for e in manifeste["documents"].values():
        if e.get("code") in cat:
            assert e["niveau"] == cat[e["code"]]["niveau"], e["doc_id"]


def test_niveau_corrige_dans_le_manifeste_reporte_dans_l_index(bibliotheque_test, capsys):
    from qak import bibliotheque
    from qak.cli import main
    manif = bibliotheque.lire_manifeste()
    next(iter(manif["documents"].values()))["niveau"] = "expert"
    bibliotheque.ecrire_manifeste(manif)
    bibliotheque.actualiser()
    assert bibliotheque.inventaire()[0]["niveau"] == "expert"
