import json

import pytest

from qak import chemins, connaissances, journal, taxonomie
from qak.connaissances import ErreurValidation

IDEE = {
    "titre": "Matrice probabilité × impact pour prioriser les tests",
    "resume": "Noter probabilité et impact de chaque risque produit pour ordonner les tests.",
    "probleme": "Effort de test réparti uniformément alors que les risques sont inégaux.",
    "principe": "Niveau de risque = probabilité × impact ; profondeur et ordre de test en découlent.",
    "theme_principal": "rbt",
}


def test_ajout_minimal_valeurs_par_defaut_et_miroir_jsonl():
    r = connaissances.ajouter(dict(IDEE))
    assert r["etat"] == "cree" and r["id"] == "QA-0001"
    i = connaissances.voir("QA-0001")
    assert (i["statut"], i["maturite"]) == ("a_explorer", "hypothese")
    lignes = chemins.connaissances_jsonl().read_text(encoding="utf-8").splitlines()
    assert json.loads(lignes[0])["titre"] == IDEE["titre"]
    assert journal.lire("QA-0001")[0]["action"] == "idee_creee"


def test_champs_obligatoires_et_valeurs_controlees():
    with pytest.raises(ErreurValidation, match="principe"):
        connaissances.ajouter({k: v for k, v in IDEE.items() if k != "principe"})
    with pytest.raises(ErreurValidation, match="statut invalide"):
        connaissances.ajouter({**IDEE, "statut": "termine"})
    with pytest.raises(ErreurValidation, match="validée"):
        connaissances.ajouter({**IDEE, "statut": "validee"})
    with pytest.raises(KeyError, match="Thème inconnu"):
        connaissances.ajouter({**IDEE, "theme_principal": "inexistant"})
    with pytest.raises(ErreurValidation, match="URL"):
        connaissances.ajouter({**IDEE, "references": [{"type": "web", "titre": "sans lien"}]})


def test_doublon_reformule_bloque_puis_force_avec_motif():
    connaissances.ajouter(dict(IDEE))
    reformule = {**IDEE, "titre": "Prioriser les tests avec une matrice impact / probabilité",
                 "resume": "Ordonner les tests selon probabilité et impact des risques produit."}
    r = connaissances.ajouter(reformule)
    assert r["etat"] == "refuse" and r["doublons"][0]["id"] == "QA-0001"
    with pytest.raises(ErreurValidation, match="motif"):
        connaissances.ajouter(reformule, forcer=True)
    assert connaissances.ajouter(reformule, forcer=True, motif="variante orientée agile")["etat"] == "cree"


def test_doublon_detecte_entre_francais_et_anglais():
    connaissances.ajouter({**IDEE, "titre": "Partitions d'équivalence pour réduire le nombre de cas de test",
                           "theme_principal": "boite-noire"})
    sim = connaissances.doublons({"titre": "Equivalence partitioning", "resume": "reduce the number of test cases",
                                  "principe": "", "probleme": ""})
    assert sim and sim[0]["id"] == "QA-0001"


def test_idee_differente_non_signalee():
    connaissances.ajouter(dict(IDEE))
    autre = {**IDEE, "titre": "Charte de session exploratoire", "resume": "Cadrer une session exploratoire de 90 min.",
             "probleme": "Tests exploratoires non traçables.", "principe": "Charte, timebox, debriefing.",
             "theme_principal": "exploratoire"}
    assert connaissances.doublons(autre) == []


def test_modifier_ajoute_les_references_sans_perdre_les_anciennes():
    connaissances.ajouter({**IDEE, "references": [{"type": "web", "url": "https://exemple.org/a", "titre": "A"}]})
    connaissances.modifier("QA-0001", {"references": [{"type": "web", "url": "https://exemple.org/b", "titre": "B"}],
                                       "themes_secondaires": ["priorisation"]})
    i = connaissances.voir("QA-0001")
    assert [r["url"] for r in i["references"]] == ["https://exemple.org/a", "https://exemple.org/b"]
    assert all(r.get("consulte_le") for r in i["references"])
    assert i["themes_secondaires"] == ["priorisation"]
    assert connaissances.modifier("QA-0001", {"titre": IDEE["titre"]})["etat"] == "inchange"
    with pytest.raises(ErreurValidation, match="idee statut"):
        connaissances.modifier("QA-0001", {"statut": "validee"})


def test_regles_de_statut():
    connaissances.ajouter(dict(IDEE))
    with pytest.raises(ErreurValidation, match="motif"):
        connaissances.changer_statut("QA-0001", "validee", None)
    with pytest.raises(ErreurValidation, match="retour"):
        connaissances.changer_statut("QA-0001", "experimentee", "essai")
    connaissances.ajouter_retour("QA-0001", "Release 3.2", "2 défauts critiques trouvés plus tôt")
    assert connaissances.changer_statut("QA-0001", "experimentee", "appliqué en 3.2")["apres"] == "experimentee"
    assert [e["action"] for e in journal.lire("QA-0001")] == ["idee_creee", "retour_ajoute", "statut_change"]


def test_relations_dans_les_deux_sens():
    connaissances.ajouter(dict(IDEE))
    connaissances.ajouter({**IDEE, "titre": "Charte exploratoire", "resume": "Session de 90 min cadrée.",
                           "probleme": "Exploratoire non tracé.", "principe": "Charte et debriefing.",
                           "theme_principal": "exploratoire"})
    connaissances.lier("QA-0002", "QA-0001", "complementaire", "les risques orientent les chartes")
    assert connaissances.voir("QA-0002")["relations"][0]["cible"] == "QA-0001"
    assert connaissances.voir("QA-0001")["relations_entrantes"][0]["source"] == "QA-0002"
    with pytest.raises(ErreurValidation):
        connaissances.lier("QA-0001", "QA-0001", "variante")
    with pytest.raises(KeyError):
        connaissances.lier("QA-0001", "QA-9999", "variante")


def test_base_reconstruite_depuis_le_jsonl_apres_git_pull():
    connaissances.ajouter(dict(IDEE))
    # Simule un `git pull` qui apporte une idée saisie sur un autre poste.
    p = chemins.connaissances_jsonl()
    autre = json.loads(p.read_text(encoding="utf-8").splitlines()[0])
    autre.update(id="QA-0002", titre="Idée venue d'un autre poste")
    p.write_text(p.read_text(encoding="utf-8") + json.dumps(autre, ensure_ascii=False) + "\n", encoding="utf-8")
    assert [i["id"] for i in connaissances.lister()] == ["QA-0001", "QA-0002"]
    # Base supprimée : reconstruite à l'identique depuis le miroir versionné.
    chemins.base_db().unlink()
    assert connaissances.voir("QA-0002")["titre"] == "Idée venue d'un autre poste"


def test_recherche_et_liste_par_theme_avec_sous_themes():
    connaissances.ajouter(dict(IDEE))
    assert connaissances.chercher("risk prioritization")[0]["id"] == "QA-0001"  # requête anglaise, idée française
    assert [i["id"] for i in connaissances.lister(theme="test-management")] == ["QA-0001"]  # rbt ⊂ test-management
    assert connaissances.lister(theme="exploratoire") == []


def test_theme_obsolete_resolu_vers_son_remplacant():
    taxonomie.rendre_obsolete("priorisation", "rbt", "fusion des thèmes")
    r = connaissances.ajouter({**IDEE, "theme_principal": "priorisation"})
    assert any("obsolète" in w for w in r["avertissements"])
    assert connaissances.voir(r["id"])["theme_principal"] == "rbt"


def test_references_istqb_verifiees_contre_la_bibliotheque(bibliotheque_test):
    ok = {**IDEE, "references": [{"type": "istqb", "doc_id": "CTFL", "pages": "6",
                                  "extrait": "Risk level is determined by risk likelihood and risk impact"}]}
    r = connaissances.ajouter(ok)
    ref = connaissances.voir(r["id"])["references"][0]
    assert (ref["doc_id"], ref["version"]) == (bibliotheque_test, "9.9")  # complété depuis l'index
    with pytest.raises(ErreurValidation, match="inexistante"):
        connaissances.valider({**IDEE, "references": [{"type": "istqb", "doc_id": "CTFL", "pages": "40"}]})
    with pytest.raises(ErreurValidation, match="n'apparaît pas"):
        connaissances.valider({**IDEE, "references": [{"type": "istqb", "doc_id": "CTFL", "pages": "6",
                                                       "extrait": "mutation testing guarantees complete coverage of every product risk"}]})
    with pytest.raises(ErreurValidation, match="ni section"):
        connaissances.valider({**IDEE, "references": [{"type": "istqb", "doc_id": "CTFL"}]})
    _, avert = connaissances.valider({**IDEE, "references": [{"type": "istqb", "doc_id": "CTAL-TM", "pages": "3"}]})
    assert "absent de la bibliothèque" in avert[0]
    assert connaissances.verifier_references()[0]["problemes"] == []


def test_couverture_signale_les_themes_vides():
    connaissances.ajouter(dict(IDEE))
    rows = {r["code"]: r for r in connaissances.couverture()}
    assert rows["rbt"]["idees"] == 1 and rows["rbt"]["etat"] == "pauvre"
    assert rows["exploratoire"]["etat"] == "vide" and rows["exploratoire"]["passages"] is None


def test_modifier_refuse_les_champs_geres_par_l_outil_et_inconnus():
    """#51 : un champ « id » dans `idee modifier` écrasait silencieusement une autre idée."""
    connaissances.ajouter(dict(IDEE))
    connaissances.ajouter({**IDEE, "titre": "Charte de session exploratoire", "resume": "Cadrer une session.",
                           "probleme": "Exploratoire non tracé.", "principe": "Charte et debriefing.",
                           "theme_principal": "exploratoire",
                           "references": [{"type": "web", "url": "https://exemple.org/c", "titre": "C"}]})
    avant = chemins.connaissances_jsonl().read_text(encoding="utf-8")
    for champ, valeur in (("id", "QA-0002"), ("cree_le", "1999-01-01"), ("maj_le", "1999-01-01"),
                          ("relations", [{"cible": "QA-0002", "type": "variante"}]),
                          ("retours", [{"contexte": "x", "resultat": "y"}])):
        with pytest.raises(ErreurValidation, match=champ):
            connaissances.modifier("QA-0001", {champ: valeur, "titre": "Titre modifié"})
    with pytest.raises(ErreurValidation, match="inconnu.*couleur"):
        connaissances.modifier("QA-0001", {"couleur": "bleu"})
    with pytest.raises(ErreurValidation, match="id"):
        connaissances.ajouter({**IDEE, "id": "QA-0002"})
    assert chemins.connaissances_jsonl().read_text(encoding="utf-8") == avant
    assert connaissances.voir("QA-0002")["references"][0]["url"] == "https://exemple.org/c"

@pytest.mark.parametrize("donnees, message", [
    ([], "objet JSON"),
    (None, "objet JSON"),
    ({**IDEE, "theme_principal": 123}, "theme_principal : texte attendu"),
    ({**IDEE, "titre": 42}, "titre : texte attendu"),
    ({**IDEE, "themes_secondaires": "metriques"}, "themes_secondaires : liste"),
    ({**IDEE, "references": {"type": "web"}}, "references : liste d'objets"),
    ({**IDEE, "references": ["https://exemple.org"]}, "references : liste d'objets"),
    ({**IDEE, "references": [{"type": "web", "url": ["https://exemple.org"]}]}, "references.url"),
])
def test_types_invalides_message_francais(donnees, message):
    """#55 : un JSON de mauvais type provoquait une trace Python (AttributeError)."""
    with pytest.raises(ErreurValidation, match=message):
        connaissances.ajouter(donnees)


def test_type_invalide_cli_code_retour_2(capsys, monkeypatch):
    import io
    from qak import cli
    monkeypatch.setattr("sys.stdin", io.StringIO("[]"))
    assert cli.main(["idee", "ajouter"]) == 2
    assert "objet JSON" in capsys.readouterr().err

def _ref_ctfl(**champs):
    return {**IDEE, "references": [{"type": "istqb", "doc_id": "CTFL", **champs}]}


EXTRAIT_P6 = "Risk level is determined by risk likelihood and risk impact"


@pytest.mark.parametrize("champs, message", [
    # mots en vrac, sens inversé, citation inventée : plus de « sac de mots » à 70 %
    ({"pages": "6", "extrait": "risk impact and risk likelihood determined by risk level"}, "mot pour mot"),
    ({"pages": "6", "extrait": "Risk level is never determined by risk likelihood and risk impact"}, "mot pour mot"),
    ({"pages": "6", "extrait": "Risk level is determined by risk likelihood and team velocity"}, "mot pour mot"),
    ({"pages": "6", "extrait": "!!! ..."}, "trop court"),
    ({"pages": "6", "extrait": "risk level is determined"}, "trop court"),
    # section incohérente avec la page citée, joker LIKE, formats de page douteux
    ({"pages": "6", "section": "1.2", "extrait": EXTRAIT_P6}, "ne figure pas aux pages 6"),
    ({"section": "%"}, "numéro attendu"),
    ({"section": "1_2"}, "numéro attendu"),
    ({"pages": "-5"}, "format attendu"),
    ({"pages": "0"}, "à partir de 1"),
    ({"pages": "6-4"}, "plages croissantes"),
    ({"pages": "p. 6"}, "format attendu"),
])
def test_reference_istqb_stricte(bibliotheque_test, champs, message):
    """#28 : section/page incohérentes, extraits en vrac ou inventés, joker « % », page « -5 »."""
    with pytest.raises(ErreurValidation, match=message):
        connaissances.valider(_ref_ctfl(**champs))


def test_reference_istqb_tolere_les_espaces_parasites_des_pdf(bibliotheque_test):
    """Les PDF FR coupent des mots (« êtr e », « perme ttant ») : recollés avant comparaison,
    sans tolérer de changement d'ordre ; la citation peut enjamber un retour à la ligne."""
    connaissances.valider(_ref_ctfl(pages="6", section="2.1", extrait="Risk lev el is determ ined by risk "
                                                                      "likeli hood and risk impact."))
    connaissances.valider(_ref_ctfl(pages=5, extrait="divides data into partitions such that all "
                                                     "elements of a given partition"))


def test_section_joker_ne_designe_plus_tout_le_document(bibliotheque_test):
    from qak import recherche
    assert recherche.lire_section("CTFL", "%")["passages"] == []
    assert recherche.lire_section("CTFL", "1.2")["passages"]


CHARTE = {**IDEE, "titre": "Charte de session exploratoire", "resume": "Cadrer une session de 90 min.",
          "probleme": "Exploratoire non tracé.", "principe": "Charte, timebox, debriefing.",
          "theme_principal": "exploratoire"}


def _reecrire_jsonl(transformer):
    p = chemins.connaissances_jsonl()
    idees = [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]
    idees = [x for x in (transformer(i) for i in idees) if x]
    p.write_text("".join(json.dumps(i, ensure_ascii=False) + "\n" for i in idees), encoding="utf-8")


def test_jsonl_modifie_a_la_main_trace_et_signale():
    """#33 : principe modifié, statut forcé à « expérimentée » sans retour et idée supprimée
    à la main étaient acceptés sans trace ; la relation devenait orpheline (« ? »)."""
    q1 = connaissances.ajouter(dict(IDEE))["id"]
    q2 = connaissances.ajouter(dict(CHARTE))["id"]
    connaissances.lier(q1, q2, "complementaire")
    connaissances.avertissements()

    def editer(i):
        if i["id"] == q2:
            return None
        return {**i, "principe": "Principe réécrit à la main.", "statut": "experimentee"}
    _reecrire_jsonl(editer)
    connaissances.lister()
    avert = connaissances.avertissements()
    assert any("modifié hors de l'outil" in w for w in avert)
    assert any("expérimentée » sans retour" in w for w in avert)
    assert any("orpheline" in w and q2 in w for w in avert)
    e = journal.lire()[-1]
    assert e["action"] == "modification_externe"
    assert e["details"]["supprimees"] == [q2]
    assert set(e["details"]["modifiees"][q1]) == {"principe", "statut"}
    assert e["details"]["modifiees"][q1]["statut"] == {"avant": "a_explorer", "apres": "experimentee"}
    assert connaissances.avertissements() == []  # signalé une fois, à la reconstruction


def test_git_pull_d_ajouts_faits_avec_l_outil_non_signale():
    """Une idée ajoutée avec l'outil sur un autre poste arrive avec sa ligne de journal :
    pas de « modification externe »."""
    connaissances.ajouter(dict(IDEE))
    p, jnl = chemins.connaissances_jsonl(), chemins.journal_jsonl()
    jsonl_avant, journal_avant = p.read_text(encoding="utf-8"), jnl.read_text(encoding="utf-8")
    q2 = connaissances.ajouter(dict(CHARTE))["id"]
    jsonl_apres, journal_apres = p.read_text(encoding="utf-8"), jnl.read_text(encoding="utf-8")
    p.write_text(jsonl_avant, encoding="utf-8")   # retour à l'état d'avant…
    connaissances.lister()
    jnl.write_text(journal_apres, encoding="utf-8")  # …puis `git pull` du JSONL et du journal
    p.write_text(jsonl_apres, encoding="utf-8")
    connaissances.avertissements()
    assert q2 in [i["id"] for i in connaissances.lister()]
    assert connaissances.avertissements() == []
    assert all(e["action"] != "modification_externe" for e in journal.lire())


def test_ligne_jsonl_invalide_message_clair():
    connaissances.ajouter(dict(IDEE))
    p = chemins.connaissances_jsonl()
    p.write_text(p.read_text(encoding="utf-8") + "{pas du json\n", encoding="utf-8")
    with pytest.raises(ErreurValidation, match=r"ligne 2 : JSON invalide"):
        connaissances.lister()
    p.write_text('{"id": "QA-0009", "titre": "sans le reste"}\n', encoding="utf-8")
    with pytest.raises(ErreurValidation, match=r"ligne 1 : champ\(s\) obligatoire\(s\) absent\(s\) : resume"):
        connaissances.lister()


def test_retirer_une_idee_proprement():
    q1 = connaissances.ajouter(dict(IDEE))["id"]
    q2 = connaissances.ajouter(dict(CHARTE))["id"]
    connaissances.lier(q1, q2, "complementaire")
    with pytest.raises(ErreurValidation, match="10 caractères"):
        connaissances.retirer(q2, "doublon")
    r = connaissances.retirer(q2, "fusionnée dans une idée plus complète")
    assert r["relations_entrantes_retirees"] == [{"source": q1, "type": "complementaire"}]
    assert [i["id"] for i in connaissances.lister()] == [q1]
    assert connaissances.voir(q1)["relations"] == []
    e = [x for x in journal.lire(q2) if x["action"] == "idee_retiree"][0]
    assert e["details"]["idee"]["titre"] == CHARTE["titre"] and e["motif"].startswith("fusionnée")
    chemins.base_db().unlink()  # reconstruction : rien d'inexpliqué
    connaissances.lister()
    assert connaissances.avertissements() == []
    with pytest.raises(KeyError):
        connaissances.retirer(q2, "déjà retirée auparavant")
