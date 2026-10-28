"""Critères automatiques des essais de bout en bout (scripts/essais_agents.py, #91).

`controler()` est une fonction pure : on la vérifie sur des réponses écrites à la main,
sans lancer la CLI `claude`."""
import importlib.util
import json
import re

import pytest
from conftest import RACINE_CODE as RACINE

_spec = importlib.util.spec_from_file_location("essais_agents", RACINE / "scripts" / "essais_agents.py")
essais_agents = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(essais_agents)

BONNE = """Hypothèse de contexte : équipe Scrum, domaine non précisé.

**Méthode pas à pas**
1. Identifier les risques en planification de release — PO + équipe [CTFL-AT 2014 EN, §3.2.1, p. 32]
2. Évaluer probabilité × impact en planification d'itération [CTFL-AT 2014 EN, §3.2.1, p. 32]
3. Choisir techniques et profondeur par niveau de risque [CTAL-TM v3.0 FR, §1.3.5, p. 33]
4. Mettre les critères dans la DoD (interprétation)
5. Revoir les risques à la rétrospective [CTAL-TA v4.0 FR, §2.2, p. 28]

**Exemple de mise en œuvre** (fictif — interprétation)
Dans une équipe Scrum de 6 personnes…

| Domaine | Ce qui change |
|---|---|
| Santé / réglementé | pas de syllabus santé dans la bibliothèque |
| Web | … |
| Embarqué | … |
| Mobile | CT-MAT |
| API | tests de contrat |

**Confiance : 78/100** (élevée)

**Questions à choix**
1. Quel domaine ? a) santé b) web c) API
2. Quelle taille d'équipe ?
"""


def test_controler_reponse_mise_en_place_complete():
    criteres = {"methode": True, "etapes_sourcees": True, "exemple": True, "cadrage": True,
                "questions_choix": True, "hypotheses": True, "non_couvert": True, "confiance": True,
                "domaines": ["sant[ée]", "web", "embarqu", "mobile", "API"], "mentions": ["contrat"]}
    resultat = essais_agents.controler(BONNE, criteres)
    assert all(resultat.values()), [c for c, ok in resultat.items() if not ok]


@pytest.mark.parametrize("critere, alteration", [
    ("methode", lambda t: t.replace("3. ", "- ").replace("4. ", "- ")),
    ("etapes_sourcees", lambda t: t.replace("(interprétation)", "")),
    ("exemple", lambda t: t.replace("(fictif — interprétation)", "")),
    ("questions_choix", lambda t: t.split("**Questions à choix**")[0]),
    ("hypotheses", lambda t: t.replace("Hypothèse de contexte :", "Contexte")),
    ("non_couvert", lambda t: t.replace("pas de syllabus santé dans la bibliothèque", "IEC 62304")),
    ("confiance", lambda t: t.replace("**Confiance : 78/100**", "")),
    ("domaines:API", lambda t: t.replace("API", "")),
])
def test_controler_detecte_chaque_manque(critere, alteration):
    criteres = {"methode": True, "etapes_sourcees": True, "exemple": True, "questions_choix": True,
                "hypotheses": True, "non_couvert": True, "confiance": True, "domaines": ["API"]}
    resultat = essais_agents.controler(alteration(BONNE), criteres)
    assert resultat[critere] is False


def test_essais_par_domaine_presents():
    """#91 : les questions de mise en place couvrent les domaines demandés, avec critères."""
    essais = {e["id"]: e for e in json.loads((RACINE / "eval" / "essais.json").read_text(encoding="utf-8"))["essais"]}
    for ident in ("M1-rbt-agile", "M2-sante", "M3-web", "M4-embarque", "M5-mobile", "M6-api",
                  "S3-reglemente", "C1-ambigu"):
        assert ident in essais and essais[ident].get("criteres"), ident
    assert set(essais["M1-rbt-agile"]["criteres"]["domaines"]) >= {"web", "mobile", "API"}
    assert essais["C1-ambigu"]["criteres"]["questions_choix"] and "agent" not in essais["C1-ambigu"]
    # Tous les critères déclarés sont connus de controler().
    connus = {"methode", "etapes_sourcees", "exemple", "cadrage", "questions_choix", "hypotheses",
              "non_couvert", "confiance", "calcul_confiance", "niveau_coherent", "domaines", "mentions"}
    for e in essais.values():
        assert set(e.get("criteres", {})) <= connus, e["id"]


def test_citation_non_lue_fait_echouer_l_essai():
    """#127 : une citation dont la page n'a pas été lue n'est plus un simple indicateur."""
    lues = {("CTAL-TM", 29)}
    reponse = "Pistes [CTAL-TM v3.0 FR, §1.3.2, p. 29] et [CTAL-TAE v2.0 EN, §4.2.1, p. 32]."
    citations = essais_agents.verifier_citations(reponse, lues)
    bilan = {"citations": citations, "citations_non_lues": [c["citation"] for c in citations if not c["lue"]],
             "criteres_ko": []}
    motifs = essais_agents.motifs_echec(bilan)
    assert len(motifs) == 1 and "CTAL-TAE" in motifs[0]
    assert essais_agents.motifs_echec({"citations_non_lues": [], "criteres_ko": []}) == []
    assert essais_agents.motifs_echec({"erreur": "x"}) == ["erreur d'exécution"]


def test_consigne_controle_avant_d_envoyer():
    """#127 : liste de contrôle des références avant la réponse finale (skill et agents)."""
    from test_agents import AGENTS, SKILL, corps
    assert "Contrôle avant d'envoyer" in corps(SKILL) and "retire la" in corps(SKILL)
    for nom in ("thomas", "sylvie"):
        assert "contrôle avant" in corps(AGENTS / f"{nom}.md"), nom


# Extrait réel : eval/essais-resultats/2026-10-22/S1-rbt.md (Sylvie, relance sur a9ddcd7).
S1_RBT = """| **P2** Tester d'abord | Intention | Aligné | … | [CTAL-TM v3.0 FR, §1.3, p. 29 ; §1.3.1, p. 29 ; §1.3.4, p. 32] |

## Confiance : 72/100

- **Ce qui l'appuie :** j'ai lu le §1.3 de CTAL-TM v3.0 FR (sous-sections 1.3.1 à 1.3.4 et 1.3.6), version courante. Il est cohérent avec les passages de CTAL-TA v4.0 vus en recherche.
- **Ce qui la limite :** je n'ai pas lu la §1.3.5 (p. 33). Je n'ai pas non plus consulté le contexte agile de la release, ni CTAL-TA §2 ni CTFL §5.2. Le niveau dépend entièrement de ce que tu m'as décrit.

## Limites

- L'ISO/IEC/IEEE 29119 n'est pas dans la bibliothèque, donc toute conformité ISO est non vérifiable ici.

## Traçabilité

- **Document lu :** `CTAL-TM-3.0-fr`, ISTQB Advanced Level Test Management, v3.0 (2024-03-28)
- **Requête `chercher` :** `"risk-based testing" identification évaluation atténuation`. Le résultat CTAL-TA §2 (p. 26-27) ne figure qu'en extrait et n'est donc pas cité.
"""


def test_reference_declaree_non_lue_n_est_pas_une_citation():
    """#139 : « je n'ai pas lu la §1.3.5 (p. 33) » et « … n'est donc pas cité » dans les
    sections de bilan ne sont pas des citations non lues (faux positif sur S1-rbt)."""
    citations = essais_agents.verifier_citations(S1_RBT, {("CTAL-TM", 29), ("CTAL-TM", 32)})
    assert citations and all(c["lue"] for c in citations), citations
    assert not any("CTAL-TA" in c["citation"] or "33" in c["citation"] for c in citations)


@pytest.mark.parametrize("reponse", [
    # Dans la réponse elle-même, une négation n'excuse rien : contrôle strict.
    "## Pratiques\n\nLe §1.3.5, que je n'ai pas lu, impose ceci [CTAL-TM v3.0 FR, §1.3.5, p. 33].",
    # Dans une section de bilan, une vraie citation (sans déclaration de non-lecture) compte.
    "## Limites\n\nLe syllabus exclut ce cas [CTAL-TM v3.0 FR, §1.3.5, p. 33].",
    "## Traçabilité\n\n- Document lu : CTAL-TM v3.0 FR. Sections lues : §1.3.5 (p. 33).\n",
])
def test_controle_strict_hors_declaration_de_non_lecture(reponse):
    citations = essais_agents.verifier_citations(reponse, {("CTAL-TM", 29)})
    assert [c["lue"] for c in citations] == [False], citations


def test_citation_pp_est_controlee_et_ne_fusionne_pas():
    """#142 : « pp. N-M » est une citation comme une autre, et deux références voisines
    (S3-reglemente, 2026-10-22) restent deux citations rattachées à leur document."""
    reponse = ("matrice de risque qualitative [CTAL-TM v3.0 FR, §1.3.3, pp. 30-31 ; "
               "CTFL v4.0.1 EN, §5.2.3, p. 53].")
    citations = essais_agents.verifier_citations(reponse, {("CTAL-TM", 31)})
    assert [(c["citation"].split()[0], c["lue"]) for c in citations] == [("CTAL-TM", True), ("CTFL", False)]
    assert essais_agents.verifier_citations("[CTAL-TM v3.0 FR, §1.3.3, pp. 30-31]", set())[0]["lue"] is False
    # « §1.3 ; §1.3.1, p. 29 » : une seule citation, la seconde.
    assert len(essais_agents.verifier_citations("[CTAL-TM v3.0 FR, §1.3 ; §1.3.1, p. 29]", set())) == 1


def test_questions_choix_format_une_option_par_ligne():
    """#144 : le format prescrit (options numérotées sous la question, une par ligne) est
    reconnu ; les options écrites en ligne (« 1. … · 2. … ») ne le sont pas."""
    sous_liste = "**Questions à choix**\n- Votre cycle de vie ?\n  1. agile\n  2. cascade\n  3. mixte\n"
    en_ligne = "**Questions à choix**\n- Votre cycle de vie : 1. agile · 2. cascade · 3. mixte ?\n"
    assert essais_agents.controler(sous_liste, {"questions_choix": True}) == {"questions_choix": True}
    assert essais_agents.controler(en_ligne, {"questions_choix": True}) == {"questions_choix": False}


# Commandes d'écriture (AGENTS.md, « Aucune écriture sans accord explicite ») : aucune ne
# doit être pré-approuvée pendant les essais (#157).
ECRITURES = ["idee ajouter", "idee modifier", "idee statut", "idee retour", "idee lier", "idee retirer",
             "theme ajouter", "theme obsolete", "telecharger", "importer", "actualiser", "corriger", "retirer"]


def test_essais_n_autorisent_aucune_ecriture():
    """#157 : `--allowedTools` vient des règles `allow` de `.claude/settings.json`, sans
    règle générique `qa.py:*` ni commande d'écriture."""
    outils = essais_agents.outils_autorises()
    allow = json.loads((RACINE / ".claude" / "settings.json").read_text(encoding="utf-8"))["permissions"]["allow"]
    assert [o for o in outils if o.startswith("Bash(")] == [r for r in allow if r.startswith("Bash(")]
    assert not {"Write", "Edit", "NotebookEdit"} & set(outils)
    for py in ("python", "python3"):
        for commande in ECRITURES:
            assert not essais_agents.autorise(f"{py} qa.py {commande} QA-0001 --oui", outils), commande
        # Les lectures, elles, restent possibles sans invite (sinon l'essai ne mesure rien).
        for commande in ("chercher risque", "lire CTFL-4.0.1-en 40", "section CT-TAS-1.0-en 3.1.3",
                         "page CTAL-TM-3.0-fr 29", "idee chercher risque", "confiance --base 80"):
            assert essais_agents.autorise(f"{py} qa.py {commande}", outils), commande


def test_autorise_respecte_les_prefixes():
    regles = ["Bash(python qa.py idee chercher:*)", "Read"]
    assert essais_agents.autorise("python qa.py idee chercher x", regles)
    assert essais_agents.autorise("python qa.py idee chercher", regles)
    assert not essais_agents.autorise("python qa.py idee chercherx", regles)
    assert not essais_agents.autorise("python qa.py idee ajouter", regles)


def test_essais_sur_copie_temporaire_des_donnees(tmp_path):
    """#157 : les essais tournent sur une copie (QAK_RACINE) ; écrire dans la copie ne
    touche pas la source."""
    source = tmp_path / "depot"
    for rel, contenu in {"bibliotheque/index.db": "x", "bibliotheque/manifeste.json": "{}",
                         "connaissances/connaissances.jsonl": "", "connaissances/journal.jsonl": "",
                         "referentiel/taxonomie.json": "{}"}.items():
        (source / rel).parent.mkdir(parents=True, exist_ok=True)
        (source / rel).write_text(contenu, encoding="utf-8")
    (source / "bibliotheque" / "sources").mkdir()
    copie = essais_agents.racine_temporaire(source)
    try:
        assert copie != source and (copie / "bibliotheque" / "index.db").read_text() == "x"
        assert (copie / "bibliotheque" / "sources").is_dir()
        (copie / "connaissances" / "connaissances.jsonl").write_text('{"id": "QA-0001"}\n', encoding="utf-8")
        (copie / "referentiel" / "taxonomie.json").write_text('{"modifie": 1}', encoding="utf-8")
        assert (source / "connaissances" / "connaissances.jsonl").read_text() == ""
        assert (source / "referentiel" / "taxonomie.json").read_text() == "{}"
    finally:
        import shutil
        shutil.rmtree(copie)

# Extrait réel : eval/essais-resultats/2026-10-23/M5-mobile.md (Thomas, campagne sur a93d3fb).
M5_MOBILE = """**Sources retenues**
- CT-MAT 2019 FR (v2019, 2019-05-03) : §1.1, §1.6, §4.3.2, §4.4, §5.1, §5.3, §5.4 lus.
- CTAL-TAE v2.0 FR : §4.2.1, lu en partie (le reste est à la p. 35).
- CT-TAS v1.0 FR : §2.1.2 lu.

**Méthode pas à pas**
   - Les appareils réels doivent être allumés, chargés, connectés au réseau et avoir accès à l'application sous test. Packaging, logs et mises à jour sont aussi à prévoir [CTAL-TAE v2.0 FR, §4.2.1, p. 34].
"""


def test_lecture_partielle_declaree_dans_sources_retenues():
    """#181 : « lu en partie (le reste est à la p. 35) » dans « Sources retenues » est une
    déclaration, pas une citation ; la vraie citation (p. 34, lue) reste contrôlée."""
    citations = essais_agents.verifier_citations(M5_MOBILE, {("CTAL-TAE", 34)})
    assert [(c["citation"].split()[0], c["lue"]) for c in citations] == [("CTAL-TAE", True)], citations
    # Sans la page 34 lue, la citation du corps échoue toujours : seule la déclaration est exclue.
    assert [c["lue"] for c in essais_agents.verifier_citations(M5_MOBILE, set())] == [False]


@pytest.mark.parametrize("reponse", [
    # Dans le corps de la réponse, « lu en partie » n'excuse rien.
    "## Méthode\n\nLe §4.2.1, lu en partie (le reste est à la p. 35), impose ceci.",
    # Dans « Sources retenues », une référence sans déclaration de lecture partielle compte.
    "**Sources retenues**\n- CTAL-TAE v2.0 FR : §4.2.1 (p. 35) lu.\n",
])
def test_lecture_partielle_controle_strict_ailleurs(reponse):
    citations = essais_agents.verifier_citations("CTAL-TAE v2.0 FR. " + reponse, {("CTAL-TAE", 34)})
    assert [c["lue"] for c in citations] == [False], citations


@pytest.mark.parametrize("doc, passage, attendu", [
    ({"code": "CT-TAS", "version": "1.0", "langue": "en", "type": "syllabus"},
     {"doc_id": "CT-TAS-1.0-en", "section_num": "3.1.3", "page": 24}, "[CT-TAS v1.0 EN, §3.1.3, p. 24]"),
    ({"code": "CTFL-AT", "version": "2014", "langue": "fr", "type": "syllabus"},
     {"doc_id": "CTFL-AT-2014-fr", "section_num": "3.2.1", "page": 32}, "[CTFL-AT 2014 FR, §3.2.1, p. 32]"),
    ({"code": "CT-ATLaS", "version": "2.0", "langue": "fr", "type": "bok"},
     {"doc_id": "CT-ATLaS-BoK-2.0-fr", "section_num": "", "page": 5, "page_imprimee": "3"},
     "[CT-ATLaS BoK v2.0 FR, p. 5 (imprimée 3)]"),
])
def test_reference_a_recopier_format(doc, passage, attendu):
    """#172 : le sigle, la version, la langue, la section et la page viennent de l'outil."""
    from qak.cli import _ref_citation
    assert _ref_citation(doc, passage) == attendu


def test_lire_section_page_affichent_la_reference_a_recopier(capsys, racine_isolee):
    """#172 : chaque en-tête de `lire`/`section`/`page` est suivi de « Citer : [...] », et
    cette référence recopiée telle quelle passe le contrôle des essais."""
    from conftest import FIXTURES
    from qak.cli import main
    assert main(["importer", str(FIXTURES / "syllabus_v9.pdf")]) == 0
    capsys.readouterr()
    assert main(["chercher", "valeurs", "limites", "--json"]) == 0
    pid = json.loads(capsys.readouterr().out)["resultats"][0]["id"]
    for args in (["section", "CTFL", "2.1"], ["page", "CTFL", "3-6"], ["lire", str(pid)]):
        assert main(args) == 0
        sortie = capsys.readouterr().out
        lignes = sortie.splitlines()
        entetes = [i for i, l in enumerate(lignes) if l.startswith("── ")]
        assert entetes, args
        for i in entetes:
            page = lignes[i].split(" · p. ")[1].split()[0]
            assert lignes[i + 1].startswith("Citer : [CTFL v9.9 EN, ") and f"p. {page}]" in lignes[i + 1], lignes[i + 1]
        refs = [l.removeprefix("Citer : ") for l in lignes if l.startswith("Citer : ")]
        citations = essais_agents.verifier_citations(" ".join(refs), essais_agents.pages_lues(sortie))
        assert citations and all(c["lue"] for c in citations), citations
    assert main(["section", "CTFL", "2.1", "--json"]) == 0
    r = json.loads(capsys.readouterr().out)
    assert all(p["citer"].startswith("[CTFL v9.9 EN, §2.1") for p in r["passages"])


def test_consigne_recopier_la_reference():
    """#172 : le skill et les agents demandent de recopier la ligne « Citer : »."""
    from test_agents import AGENTS, SKILL, corps
    assert "Recopie la ligne `Citer :`" in corps(SKILL)
    for nom in ("thomas", "sylvie"):
        assert "ligne `Citer : [...]`" in corps(AGENTS / f"{nom}.md"), nom


@pytest.mark.parametrize("args", [["lire", "1"], ["page", "CTFL", "3"], ["section", "CTFL", "1"]])
def test_max_caracteres_negatif_refuse(capsys, racine_isolee, args):
    """`--max-caracteres -5` était accepté (sortie sans borne) : entier ≥ 0 exigé, 0 = sans limite."""
    from qak.cli import main
    with pytest.raises(SystemExit) as fin:  # argparse : rc=2, message en français (#164)
        main([*args, "--max-caracteres", "-5"])
    assert fin.value.code == 2 and "entier ≥ 0 attendu" in capsys.readouterr().err


def test_consigne_extrait_jamais_entre_crochets():
    """#182 (S2-automatisation, 2026-10-23) : une référence vue seulement en extrait ne
    s'écrit pas entre crochets ; elle est lue ou renvoyée sans crochets à « Où creuser »."""
    from test_agents import AGENTS, SKILL, corps
    for texte in (corps(SKILL), corps(AGENTS / "sylvie.md")):
        assert "Vu en extrait = jamais entre crochets" in texte and "Où creuser ensuite" in texte
    # Le contrôle des essais compte bien une telle référence comme citation non lue.
    reponse = "Pratique alignée [CTAL-TA v4.0 EN, §1.2.4, p. 17, vu en extrait seulement]."
    assert [c["lue"] for c in essais_agents.verifier_citations(reponse, set())] == [False]


# docs/essais-reponses.md : les tableaux d'une campagne qui désigne ses fichiers
# (« Fichiers : `eval/essais-resultats/<date>/` ») reprennent les en-têtes de ces
# fichiers d'essai, sur le modèle de test_exemples.py (#178).
ESSAIS_REPONSES = (RACINE / "docs" / "essais-reponses.md").read_text(encoding="utf-8")
RE_ENTETE_ESSAI = re.compile(
    r"\*\*Tours\*\* : (?P<tours>\d+) · \*\*coût\*\* : (?P<cout>[\d.]+) \$ · \*\*confiance annoncée\*\* : "
    r"(?P<confiance>\w+) · \*\*verdict\*\* : (?P<verdict>\S+) · \*\*citations\*\* : (?P<citations>\d+/\d+) lues"
    r" · \*\*Web\*\* : (?P<web>\d+)(?: · \*\*critères\*\* : (?P<criteres>\d+/\d+))?")


def campagnes_versionnees():
    """(titre, dossier, lignes du tableau) des sections qui désignent leurs fichiers."""
    for section in re.split(r"^(?=## )", ESSAIS_REPONSES, flags=re.M):
        m = re.search(r"Fichiers : `(eval/essais-resultats/[\d-]+)/`", section)
        if not m:
            continue
        lignes = [l for l in section.splitlines() if l.startswith("| ")]
        entetes = [c.strip() for c in lignes[0].strip("|").split("|")]
        rangees = [dict(zip(entetes, (c.strip() for c in l.strip("|").split("|")))) for l in lignes[2:]]
        yield section.splitlines()[0], m.group(1), rangees


def test_essais_reponses_designe_la_campagne_la_plus_recente():
    dossiers = sorted(p.name for p in (RACINE / "eval" / "essais-resultats").iterdir() if p.is_dir())
    designes = {d.rsplit("/", 1)[1] for _, d, _ in campagnes_versionnees()}
    assert dossiers[-1] in designes, f"campagne {dossiers[-1]} absente de docs/essais-reponses.md"
    assert "2026-10-23" in designes


@pytest.mark.parametrize("titre, dossier, rangees", list(campagnes_versionnees()), ids=lambda x: x if
                         isinstance(x, str) and x.startswith("eval/") else None)
def test_essais_reponses_d_accord_avec_les_fichiers(titre, dossier, rangees):
    assert rangees, titre
    for r in rangees:
        fichier = RACINE / dossier / f"{r['Essai']}.md"
        assert fichier.exists(), f"{titre} : {fichier} absent"
        e = RE_ENTETE_ESSAI.search(fichier.read_text(encoding="utf-8"))
        assert e, fichier
        attendu = {"Tours": e["tours"], "Coût": f"{e['cout'].replace('.', ',')} $", "Confiance": e["confiance"],
                   "Citations lues": e["citations"], "Web": e["web"], "Critères": e["criteres"] or "—"}
        assert {k: r[k] for k in attendu} == attendu, f"{titre} · {r['Essai']}"
        verdict = r["Verdict"].replace("*", "")
        assert verdict.startswith("ÉCHEC" if e["verdict"] == "ÉCHEC" else "réussi"), f"{titre} · {r['Essai']}"


def test_sylvie_calcule_sa_confiance():
    """#227 (étude par personas, P4b) : Sylvie annonçait 68, 72 puis 62 sans jamais lancer
    `qa.py confiance`. La consigne l'impose, et le critère `calcul_confiance` le contrôle."""
    from test_agents import AGENTS, corps
    texte = corps(AGENTS / "sylvie.md")
    assert "calcule-la toujours" in texte and "python qa.py confiance --autorite 0 --base" in texte
    assert "Calcul :" in texte
    sans_calcul = ("## Confiance : 68/100\n\n- J'ai lu directement les passages sur les revues.\n"
                   "- Ta description est brève.")
    avec_calcul = ("**Confiance : 72/100 (moyenne)**\nCalcul : base 70 × 0,6 = 42 ; 5 passages lus +20 ; "
                   "3 syllabus concordants +20 ; raisonnement −10 → 72")
    critere = {"confiance": True, "calcul_confiance": True}
    assert essais_agents.controler(sans_calcul, critere) == {"confiance": True, "calcul_confiance": False}
    assert essais_agents.controler(avec_calcul, critere) == {"confiance": True, "calcul_confiance": True}
    essais = {e["id"]: e for e in json.loads((RACINE / "eval" / "essais.json").read_text(encoding="utf-8"))["essais"]}
    assert essais["S4-recette"]["agent"] == "sylvie" and essais["S4-recette"]["criteres"]["calcul_confiance"]


@pytest.mark.parametrize("reponse, attendu", [
    # Réponses réelles de l'étude par personas (P4b, R2-P4b, relance du 2026-10-28).
    ("## Niveau atteint : 2 — Discipliné (provisoire, non démontré)\n\nLe niveau 2 n'est donc pas acquis, "
     "et je retiens **le niveau 1 — Initial**.", False),
    ("**Niveau atteint : 2 — Discipliné (Managed), non démontré ; je retiens le niveau 1 — Initial. "
     "Niveau visé : 2.**", False),
    ("## Niveau atteint : 2 — Discipliné (Managed), non démontré, donc je retiens 1 — Initial\n\n"
     "- **Niveau atteint : 1 — Initial.** Les pratiques sont déclarées, mais « non démontré ».", False),
    ("## Niveau atteint : 2 — Discipliné (provisoire), et seulement en partie", False),
    ("Rien sur le niveau.", False),
    # Corrects : la réserve éventuelle va dans « niveau visé » ou après la première phrase.
    ("## Niveau atteint : 1 — Initial (niveau visé : 2)", True),
    ("## Niveau atteint : 1 — Initial · niveau visé : 2 (partiellement)", True),
    ("- **Niveau atteint : 1 — Initial.** Rien ne prouve une stratégie écrite : « non démontré ».", True),
    ("## Niveau atteint : 2 — Discipliné\n\nTous les critères du niveau 2 sont démontrés.", True),
])
def test_titre_niveau_atteint_porte_le_niveau_retenu(reponse, attendu):
    """#228 : « Niveau atteint : 2 » en titre alors que le niveau retenu est 1 (2 passages sur 3)."""
    assert essais_agents.controler(reponse, {"niveau_coherent": True}) == {"niveau_coherent": attendu}


def test_consigne_niveau_atteint_retenu():
    """#228 : la consigne de Sylvie et la grille réservent le titre au niveau retenu."""
    from test_agents import AGENTS, corps
    assert "**N est le niveau retenu**" in corps(AGENTS / "sylvie.md")
    grille = (RACINE / "referentiel" / "grille-maturite.md").read_text(encoding="utf-8")
    assert "porte **toujours le niveau retenu**" in grille
    essais = {e["id"]: e for e in json.loads((RACINE / "eval" / "essais.json").read_text(encoding="utf-8"))["essais"]}
    assert essais["S4-recette"]["criteres"]["niveau_coherent"]
