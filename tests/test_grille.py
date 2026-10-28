"""Issue #30 : grille de maturité alignée sur sa source (CTEL-ITP 2011 §3.3.2) et
vocabulaire d'alignement, pas de conformité, chez Sylvie."""
from conftest import RACINE_CODE

GRILLE = (RACINE_CODE / "referentiel" / "grille-maturite.md").read_text(encoding="utf-8")
SYLVIE = (RACINE_CODE / ".claude" / "agents" / "sylvie.md").read_text(encoding="utf-8")
MENTION = "ni attestation de conformité, ni évaluation ISTQB/TMMi/ISO"
VERDICTS = ("Aligné", "Partiellement aligné", "Écart", "Hors ISTQB", "Non vérifiable")


def ligne_niveau(n: int) -> str:
    return next(l for l in GRILLE.splitlines() if l.startswith(f"| {n} |"))


def test_libelles_exacts_en_et_fr_cftl():
    for n, fr, en in [(1, "Initial", "Initial"), (2, "Discipliné", "Managed"), (3, "Ajusté", "Defined"),
                      (4, "Géré quantitativement", "Management and measurement"),
                      (5, "En optimisation", "Optimization")]:
        assert f"| {fr} · {en} |" in ligne_niveau(n)


def test_politique_et_strategie_au_niveau_2():
    assert "stratégie" in ligne_niveau(2) and "politique" in ligne_niveau(2)
    assert "stratégie" not in ligne_niveau(3) and "politique" not in ligne_niveau(3)
    # Le fondement renvoie à sa source, sans crochets ni page (#246).
    assert "environnement de test (à lire : CTEL-ITP 2011 EN et FR §3.3.2)" in " ".join(GRILLE.split())


def test_grille_renvoie_sans_citation_recopiable():
    """#246 (récidive de #140) : Sylvie recopiait `[CTEL-ITP 2011 EN, §3.3.2, p. 26]` depuis
    la grille sans l'avoir lu (3 avis sur 7). La grille ne contient plus aucune référence
    au format d'une citation : le contrôle des essais n'y trouve rien à recopier."""
    from test_essais import essais_agents
    assert "[" not in GRILLE and essais_agents.verifier_citations(GRILLE, set()) == []
    assert "à lire : CTEL-ITP 2011 EN §3.1.2" in " ".join(GRILLE.split())
    assert "section CTEL-ITP-2011-en 3.3.2" in GRILLE
    assert "une référence de la grille ne se cite qu'après" in " ".join(SYLVIE.split())
    # La recopie réelle (étude P4b, relances #227 et #232) reste un échec du contrôle.
    recopie = "Niveau 1 (grille du dépôt, fondée sur [CTEL-ITP 2011 EN, §3.3.2, p. 26])."
    assert [c["lue"] for c in essais_agents.verifier_citations(recopie, set())] == [False]


def test_echelle_inspiree_et_non_evaluation_tmmi():
    assert "inspirée du TMMi" in GRILLE
    assert "reprennent ceux du modèle TMMi" not in GRILLE


def test_intention_plafonne_le_niveau():
    for texte in (GRILLE, SYLVIE):
        assert "intention" in texte and "en place (preuve : …)" in texte
        assert "plafonné à 1" in texte and "niveau visé" in texte


def test_verdicts_d_alignement():
    for texte in (GRILLE, SYLVIE):
        for v in VERDICTS:
            assert v in texte, v
        assert "Partiellement conforme" not in texte and "| Conforme |" not in texte


def test_sylvie_mentions_obligatoires_et_tracabilite():
    assert "certifiée" not in SYLVIE
    assert "experte des syllabus ISTQB" in SYLVIE
    assert SYLVIE.count(MENTION) >= 2  # rôle + en-tête de réponse
    assert "**En tête**" in SYLVIE and "**En pied**" in SYLVIE
    assert "**Traçabilité**" in SYLVIE and "doc_id" in SYLVIE
    assert MENTION in GRILLE
