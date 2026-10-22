from qak import textes


def test_normaliser_retire_accents_apostrophes_et_ponctuation():
    assert textes.normaliser("Partitions d’Équivalence !") == "partitions d equivalence"


def test_concepts_reconnus_en_francais_et_au_pluriel():
    concepts, reste = textes.reperer_concepts("Les partitions d'équivalence et les valeurs limites")
    ids = [c for c, _ in concepts]
    assert ids == ["partition-equivalence", "valeurs-limites"]
    assert "partitions" not in reste and "equivalence" not in reste


def test_expression_longue_prioritaire_sur_terme_court():
    concepts, _ = textes.reperer_concepts("analyse statique du code")
    assert [c for c, _ in concepts] == ["analyse-statique"]


def test_signature_identique_en_francais_et_en_anglais():
    fr = textes.signature("Partitions d'équivalence")
    en = textes.signature("Equivalence partitioning")
    assert fr == en == {"#partition-equivalence"}


def test_mots_vides_et_generiques_ne_pesent_pas():
    _, reste = textes.reperer_concepts("Quelles techniques ISTQB pour la stratégie de test ?")
    assert "quelles" not in reste and "pour" not in reste


def test_jaccard_et_recouvrement():
    assert textes.jaccard({"a", "b"}, {"b", "c"}) == 1 / 3
    assert textes.recouvrement({"a"}, {"a", "b", "c"}) == 1.0
    assert textes.jaccard(set(), {"a"}) == 0.0


def test_tpi_ctp_step_et_modele_de_maturite_distincts():
    # Issue #45 : CTEL-ITP distingue TPI (§3.3.1) et les modèles de contenu STEP / CTP (§3.4).
    def ids(q):
        return [cid for cid, _ in textes.reperer_concepts(q)[0]]
    assert ids("critical testing processes") == ["ctp"] and ids("TPI Next") == ["tpi"]
    assert ids("systematic test and evaluation process") == ["step"]
    assert ids("TMMi") == ["tmmi"] and ids("modèle de maturité") == ["modele-maturite"]
    assert ids("Test Maturity Model integration") == ["tmmi"] and ids("TMM") == ["tmm"]
