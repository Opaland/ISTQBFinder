from pypdf import PdfWriter

from qak import extraction
from conftest import FIXTURES


def test_pages_entetes_retires_et_sommaires_detectes():
    x = extraction.extraire(FIXTURES / "syllabus_v9.pdf")
    assert x.statut()[0] == "ok"
    assert x.nb_pages == 7
    # L'en-tête « Version 9.9 Page N of 7 date » et le pied de page sont retirés du texte…
    assert all("Page" not in p.texte and "Fictional" not in p.texte for p in x.pages)
    # … mais conservés pour les métadonnées.
    assert "Page 1 of 7" in x.brut_debut[0]
    assert [p.numero for p in x.pages if p.sommaire] == [2, 7]  # table des matières + index


def test_plan_ignore_liste_numerotee_et_objectifs_repetes():
    x = extraction.extraire(FIXTURES / "syllabus_v9.pdf")
    plan = [(t.numero, t.titre, t.page) for t in x.plan]
    assert ("1", "Fundamentals of Testing", 3) in plan
    assert not any(t.startswith("To national boards") for _, t, _ in plan)
    # « 1.1 Test Objectives » figure dans les objectifs p. 3 ET comme vrai titre p. 4 : seul le second compte.
    assert ("1.1", "Test Objectives", 4) in plan and ("1.1", "Test Objectives", 3) not in plan


def test_passages_ne_franchissent_pas_les_pages_et_portent_leur_section():
    x = extraction.extraire(FIXTURES / "syllabus_v9.pdf")
    ps = extraction.passages(x)
    ep = [p for p in ps if "divides data into partitions" in p.texte]
    assert len(ep) == 1 and ep[0].page == 5 and ep[0].section_num == "1.2"
    valides = [p for p in ps if "valid partition;" in p.texte][0]
    assert valides.section_num == "1.2.1" and valides.page == 5
    assert all(p.page in {q.numero for q in x.pages} for p in ps)


def test_page_imprimee_differente_conservee(tmp_path):
    f = tmp_path / "doc.txt"
    f.write_text("Page 10 de 12\nTexte de la première page assez long pour compter.\f"
                 "Page 11 de 12\nTexte de la seconde page assez long pour compter.", encoding="utf-8")
    x = extraction.extraire(f)
    assert [(p.numero, p.imprimee) for p in x.pages] == [(1, "10"), (2, "11")]


def test_markdown_plan_par_titres(tmp_path):
    f = tmp_path / "notes.md"
    f.write_text("# 1 Stratégie\nTexte de stratégie de test suffisamment long.\n## 1.1 Risques\nTexte sur les risques.",
                 encoding="utf-8")
    x = extraction.extraire(f)
    assert [(t.numero, t.titre) for t in x.plan] == [("1", "Stratégie"), ("1.1", "Risques")]
    assert x.plan_source == "markdown"


def test_pdf_sans_texte_signale_illisible(tmp_path):
    w = PdfWriter()
    for _ in range(4):
        w.add_blank_page(width=595, height=842)
    f = tmp_path / "scan.pdf"
    with open(f, "wb") as fh:
        w.write(fh)
    statut, message = extraction.extraire(f).statut()
    assert statut == "illisible" and "OCR" in message


def test_fichier_corrompu_et_format_inconnu(tmp_path):
    casse = tmp_path / "casse.pdf"
    casse.write_bytes(b"%PDF-1.4 pas vraiment un pdf")
    assert extraction.extraire(casse).statut()[0] == "echec"
    docx = tmp_path / "x.docx"
    docx.write_bytes(b"PK")
    assert "format non pris en charge" in extraction.extraire(docx).statut()[1]


def _pages(*textes):
    return [extraction.Page(i, None, t) for i, t in enumerate(textes, start=1)]


def test_plan_ignore_les_rangees_du_tableau_des_temps_de_formation():
    """#41 : CTEL-ITP — le tableau des temps de formation (annexe) reprend les titres des
    chapitres suivis de nombres ; il ne doit ni remplacer le vrai chapitre 10, ni couper la suite."""
    debut = [f"{n}. Chapter {n}\nTexte du chapitre." for n in range(1, 9)]
    pages = _pages(
        *debut,
        "9. Critical Success Factors 300 mins.\nTexte.\n9.1 Key Success Factors\nTexte.",
        "9.2 Setting a Culture for Improvement\nTexte du chapitre neuf.",
        "10. Adapting to Different Life Cycle Models 60 mins.\nKeywords:\n"
        "10.1 Adapting to Different Life Cycle Models\nTexte.",
        "11. References\n11.1 Standards\nTexte.",
        "12. Appendix A – Notice to Training Providers\n12.1 Training Times\n"
        "Nr. Chapter Course teaching\n1 Introduction 60 0 60\n2 The Context of Improvement 285 0 285\n"
        "9 Critical Success Factors 120 180 300\n10 Adapting to Different Life Cycle\nModels\n60 0 60\n"
        "10 S’Adapter à Différents Modèles de Cycle de Vie 60 0 60\n Total 2520 1065 3585",
    )
    plan = extraction._plan_depuis_texte(pages)[8:]
    assert [(t.numero, t.page) for t in plan] == [("9", 9), ("9.1", 9), ("9.2", 10), ("10", 11), ("10.1", 11),
                                                  ("11", 12), ("11.1", 12), ("12", 13), ("12.1", 13)]
    # Un vrai titre qui porte sa durée (« 300 mins. ») reste un titre.
    assert plan[0].titre == "Critical Success Factors 300 mins."


def test_plan_titres_completes_recolles_et_index():
    """#48 : titre coupé complété par la ligne suivante, mots coupés par une espace
    parasite recollés, intitulé « Index » d'une page d'index conservé."""
    corps = ("Les parties prenantes participent au management des tests. Le contrôle des tests "
             "et le leadership comptent. Learning objectives and knowledge.\n") * 3
    index = "\n".join(f"terme {k}, {k + 10}" for k in range(14))
    pages = _pages(
        "1 Introduction\n" + corps,
        "1.1 Importance des parties prenantes dans le management d es\ntests\n" + corps,
        "1.2 Le pilotage et le c ontrôle\n" + corps,
        "2 Appendix A – Learning Objectives/Cognitive Level of\nKnowledge\n" + corps,
        "2.1 Agile Test Le adership\n" + corps,
        "3 Index\n" + index,
    )
    pages[-1].sommaire = True
    plan = extraction._plan_depuis_texte(pages)
    assert [(t.numero, t.titre) for t in plan] == [
        ("1", "Introduction"),
        ("1.1", "Importance des parties prenantes dans le management des tests"),
        ("1.2", "Le pilotage et le contrôle"),
        ("2", "Appendix A – Learning Objectives/Cognitive Level of Knowledge"),
        ("2.1", "Agile Test Leadership"),
        ("3", "Index"),
    ]


def test_recollage_prudent():
    vocab = extraction._vocabulaire(_pages("go in to the into test and quel que l approche " * 3))
    # Deux vrais mots voisins ne sont jamais réunis, ni un mot et une élision.
    assert extraction._recoller("in to the test", vocab) == "in to the test"
    assert extraction._recoller("que l’approche", vocab) == "que l’approche"
    assert extraction._recoller("Test a nd", vocab) == "Test and"


def test_mots_coupes_recolles_dans_les_passages(tmp_path):
    # Issue #106 : « utilisabilit é » (espace parasite d'un PDF FR) est recollé dans le texte
    # des passages, pas seulement dans les titres ; deux vrais mots voisins restent séparés.
    f = tmp_path / "doc.txt"
    f.write_text("1 Utilisabilité\n" + "L'utilisabilité compte. " * 3
                 + "\nIl existe deux types d'évaluation de l'utilisabilit é et de la convivial ité.\n"
                 + "La convivialité aussi. " * 3 + "\nOn va in to the test, into it, in it, to it.\n",
                 encoding="utf-8")
    texte = " ".join(p.texte for p in extraction.passages(extraction.extraire(f)))
    assert "utilisabilité et de la convivialité." in texte
    assert "in to the test" in texte
