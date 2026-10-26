"""#184 : export du plugin autonome (`scripts/exporter_plugin.py`), destiné au dépôt dédié
`Opaland/ISTQBFinder-plugin`, sans aucun syllabus (docs/plugin.md, § 6).

- Export dans un dossier temporaire : aucun PDF, aucun fichier de `bibliotheque/sources/`
  (empreintes comparées), fichiers requis présents, manifeste et marketplace valides.
- Lanceur (`lanceur.py`) : dossier de données recalculé comme Claude Code, `QAK_RACINE`.
- `claude plugin validate --strict` sur l'export quand la CLI est installée.
- Premier usage RÉEL (venv, un syllabus téléchargé depuis istqb.org, index, MCP) : lancé par
  le job CI `plugin-export` (QAK_ESSAI_PREMIER_USAGE=1) ; istqb.org injoignable → ignoré avec
  la raison, mauvaise réponse → échec (comme tests/test_sources_reelles.py)."""
import asyncio
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import types
from pathlib import Path

import pytest

from conftest import FIXTURES, RACINE_CODE
from test_permissions import ECRITURE

_spec = importlib.util.spec_from_file_location("exporter_plugin", RACINE_CODE / "scripts" / "exporter_plugin.py")
exp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(exp)


@pytest.fixture(scope="module")
def export(tmp_path_factory):
    cible = tmp_path_factory.mktemp("export") / "ISTQBFinder-plugin"
    assert exp.exporter(cible, version="0.0.0-essai") == []
    return cible


def _fichiers(dossier: Path) -> list[Path]:
    return sorted(f for f in dossier.rglob("*") if f.is_file() and ".git" not in f.relative_to(dossier).parts)


def test_aucun_pdf_ni_fichier_de_bibliotheque_sources(export):
    sources = RACINE_CODE / "bibliotheque" / "sources"
    interdits = {hashlib.sha256(f.read_bytes()).hexdigest() for f in sources.rglob("*") if f.is_file()}
    assert interdits, "bibliotheque/sources/ vide : le contrôle des empreintes ne prouverait rien"
    noms_sources = {f.name for f in sources.rglob("*") if f.is_file()}
    for f in _fichiers(export):
        donnees = f.read_bytes()
        assert f.suffix.lower() != ".pdf" and not donnees.startswith(b"%PDF"), f
        assert hashlib.sha256(donnees).hexdigest() not in interdits, f
        assert f.name not in noms_sources, f
        donnees.decode("utf-8")  # texte seulement
    rel = [f.relative_to(export).as_posix() for f in _fichiers(export)]
    assert not [r for r in rel if r.startswith(("bibliotheque/", "connaissances/", "tests/", "eval/", ".claude/"))]
    assert sum(f.stat().st_size for f in _fichiers(export)) < 1_000_000


def test_fichiers_requis_et_code_complet(export):
    for r in exp.REQUIS:
        assert (export / r).is_file(), r
    attendus = {f.relative_to(RACINE_CODE).as_posix() for d in exp.CODE_DOSSIERS
                for f in (RACINE_CODE / d).rglob("*") if f.is_file() and "__pycache__" not in f.parts}
    assert attendus <= {f.relative_to(export).as_posix() for f in _fichiers(export)}
    assert (export / "LICENSE").read_text(encoding="utf-8").startswith("MIT License")
    notice = (export / "NOTICE.md").read_text(encoding="utf-8")
    assert "istqb.org" in notice and "aucun syllabus" in notice.lower()
    lisez_moi = (export / "README.md").read_text(encoding="utf-8")
    for passage in ("claude plugin marketplace add Opaland/ISTQBFinder-plugin",
                    "claude plugin install istqbfinder@istqbfinder", "/istqbfinder:installer",
                    "qa importer --prive", "une base par installation", "--keep-data", "QAK_RACINE"):
        assert passage in lisez_moi, passage
    if os.name != "nt":
        assert os.access(export / "bin" / "qa", os.X_OK)


def test_manifeste_et_marketplace(export):
    m = json.loads((export / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    assert m["name"] == "istqbfinder" and m["version"] == "0.0.0-essai" and m["license"] == "MIT"
    assert m["mcpServers"] == {"istqbfinder": {"command": "${CLAUDE_PLUGIN_ROOT}/bin/qa", "args": ["mcp"]}}
    assert m["repository"] == "https://github.com/Opaland/ISTQBFinder-plugin"
    assert re.fullmatch(r"[0-9a-f]{40}|inconnu", m["metadata"]["commit"])
    marche = json.loads((export / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
    assert marche["name"] == "istqbfinder" and marche["plugins"] == [
        {"name": "istqbfinder", "source": "./", "description": exp.DESCRIPTION}]


def test_skills_et_agents_autonomes_sans_ecriture_preapprouvee(export):
    for f in [*export.glob("skills/*/SKILL.md"), *export.glob("agents/*.md")]:
        texte = f.read_text(encoding="utf-8")
        assert "${CLAUDE_PLUGIN_ROOT}/.." not in texte and "relatifs au clone" not in texte, f
        if f.name == "SKILL.md" and f.parent.name != "installer":
            assert "Version plugin autonome" in texte and "/istqbfinder:installer" in texte, f
        ligne = next((l for l in texte.splitlines() if l.startswith("allowed-tools:")), "")
        commandes = re.findall(r"Bash\(qa (.*?):?\*?\)", ligne)
        assert not [c for c in commandes if c.startswith(("installer", "telecharger"))
                    or any(c.startswith(e) for e in ECRITURE)], f
    sylvie = (export / "agents" / "sylvie.md").read_text(encoding="utf-8")
    assert "`${CLAUDE_PLUGIN_ROOT}/referentiel/grille-maturite.md`" in sylvie
    installer = (export / "skills" / "installer" / "SKILL.md").read_text(encoding="utf-8")
    assert "disable-model-invocation: true" in installer and "qa installer $ARGUMENTS" in installer


def test_export_remplace_un_export_precedent_et_garde_git(export, tmp_path):
    cible = tmp_path / "clone-du-plugin"
    (cible / ".git").mkdir(parents=True)
    (cible / ".git" / "HEAD").write_text("ref: refs/heads/main\n", encoding="utf-8")
    assert exp.exporter(cible, version="1") == []
    (cible / "obsolete.txt").write_text("ancien fichier", encoding="utf-8")
    assert exp.exporter(cible, version="2") == []
    assert not (cible / "obsolete.txt").exists() and (cible / ".git" / "HEAD").exists()
    etranger = tmp_path / "etranger"
    etranger.mkdir()
    (etranger / "precieux.txt").write_text("à garder", encoding="utf-8")
    with pytest.raises(SystemExit, match="ni vide ni un export"):
        exp.exporter(etranger)
    assert (etranger / "precieux.txt").exists()


def test_verifier_refuse_un_pdf_ou_un_document_de_la_bibliotheque(tmp_path):
    cible = tmp_path / "export"
    assert exp.exporter(cible, version="1") == []
    shutil.copy2(FIXTURES / "syllabus_v9.pdf", cible / "skills" / "glisse.pdf")
    source = next((RACINE_CODE / "bibliotheque" / "sources").glob("*.pdf"))
    shutil.copy2(source, cible / "renomme.txt")
    problemes = exp.verifier(cible)
    assert "PDF interdit : skills/glisse.pdf" in problemes
    assert "fichier de bibliotheque/ interdit : renomme.txt" in problemes
    (cible / "README.md").unlink()
    assert "fichier requis absent : README.md" in exp.verifier(cible)


def _lanceur(export: Path):
    spec = importlib.util.spec_from_file_location("lanceur_plugin", export / "lanceur.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_lanceur_dossier_de_donnees_comme_claude_code(export, tmp_path, monkeypatch):
    """`${CLAUDE_PLUGIN_DATA}` = `<config>/plugins/data/<id>/`, `<id>` = `plugin@marketplace` où
    tout caractère autre que lettre, chiffre, `_`, `-` devient `-` (doc officielle) : l'outil
    Bash, qui ne reçoit pas la variable, retombe sur le même dossier que le serveur MCP."""
    lanceur = _lanceur(export)
    monkeypatch.delenv("CLAUDE_PLUGIN_DATA", raising=False)
    monkeypatch.delenv("QAK_RACINE", raising=False)
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(tmp_path / "config"))
    assert lanceur.marketplace() == "istqbfinder"  # chargé en place : marketplace.json à la racine
    assert lanceur.dossier_plugin() == tmp_path / "config" / "plugins" / "data" / "istqbfinder-istqbfinder"
    assert lanceur.racine_donnees() == lanceur.dossier_plugin() / "donnees"
    monkeypatch.setattr(lanceur, "PLUGIN", tmp_path / ".claude" / "plugins" / "cache" / "ma.place" / "istqbfinder" / "1.0")
    assert lanceur.identifiant() == "istqbfinder-ma-place"  # copié dans le cache d'une marketplace GitHub
    monkeypatch.setenv("CLAUDE_PLUGIN_DATA", str(tmp_path / "donne-par-claude"))
    assert lanceur.dossier_plugin() == tmp_path / "donne-par-claude"
    monkeypatch.setenv("QAK_RACINE", str(tmp_path / "clone"))
    assert lanceur.racine_donnees() == tmp_path / "clone"
    assert lanceur.python_venv().parent.parent == tmp_path / "donne-par-claude" / "venv"


def test_lanceur_refuse_un_python_trop_ancien_et_parle_sur_stderr(export, monkeypatch, capsys):
    lanceur = _lanceur(export)
    monkeypatch.setattr(lanceur, "sys", types.SimpleNamespace(version_info=(3, 9, 0), version="3.9.0 (essai)",
                                                              executable="python-ancien", stderr=sys.stderr))
    assert lanceur.main(["chercher", "x"]) == 2
    sortie = capsys.readouterr()
    assert sortie.out == "" and "Python 3.10 ou plus requis" in sortie.err


@pytest.mark.skipif(not shutil.which("claude"), reason="CLI `claude` absente : `claude plugin validate` non lancé")
def test_claude_plugin_validate_strict_sur_l_export(export):
    r = subprocess.run([shutil.which("claude"), "plugin", "validate", "--strict", str(export)],
                       capture_output=True, text=True, timeout=120, encoding="utf-8")
    assert r.returncode == 0, r.stdout + r.stderr
    assert "Validation passed" in r.stdout


def _istqb_injoignable() -> str | None:
    import urllib.error
    from qak import catalogue
    try:
        catalogue._ouvrir(catalogue.documents(["CTFL"])[0]["telechargement"], "HEAD", delai=20).close()
        return None
    except (urllib.error.URLError, OSError) as exc:
        return f"istqb.org injoignable : {exc}"


@pytest.mark.skipif(os.environ.get("QAK_ESSAI_PREMIER_USAGE") != "1",
                    reason="premier usage réel (venv, téléchargement istqb.org) : job CI plugin-export, "
                           "ou QAK_ESSAI_PREMIER_USAGE=1")
def test_premier_usage_reel_un_syllabus(tmp_path):
    raison = _istqb_injoignable()
    if raison:
        pytest.skip(raison)
    plugin = tmp_path / "plugin"
    assert exp.exporter(plugin, version="0.0.0-essai") == []
    avant = {f.relative_to(plugin).as_posix(): f.read_bytes() for f in _fichiers(plugin)}
    config = tmp_path / "config"
    env = {k: v for k, v in os.environ.items() if k not in ("QAK_RACINE", "CLAUDE_PLUGIN_DATA")}
    env["CLAUDE_CONFIG_DIR"] = str(config)
    qa = [str(plugin / "bin" / ("qa.cmd" if os.name == "nt" else "qa"))]

    r = subprocess.run(qa + ["installer", "CTFL"], capture_output=True, text=True, env=env, cwd=tmp_path,
                       timeout=900, encoding="utf-8", errors="replace")
    if r.returncode and "installation des dépendances impossible" in r.stderr:
        pytest.skip(f"PyPI injoignable : {r.stderr[-300:]}")
    assert r.returncode == 0, r.stdout + r.stderr
    assert re.search(r"CTFL\s+importe\s+CTFL-[\d.]+-en", r.stdout), r.stdout
    assert "Diagnostic : OK" in r.stdout and "qa importer --prive" in r.stderr

    donnees = config / "plugins" / "data" / "istqbfinder-istqbfinder"
    pdf = list((donnees / "donnees" / "bibliotheque" / "sources").glob("*.pdf"))
    assert len(pdf) == 1 and pdf[0].read_bytes().startswith(b"%PDF")
    assert (donnees / "donnees" / "bibliotheque" / "index.db").exists()
    assert (donnees / "venv").is_dir()
    # Rien n'a été écrit dans le dossier du plugin (ni PDF, ni index, ni __pycache__).
    assert {f.relative_to(plugin).as_posix(): f.read_bytes() for f in _fichiers(plugin)} == avant
    assert not list(plugin.rglob("__pycache__"))

    r = subprocess.run(qa + ["chercher", "partitions d'équivalence"], capture_output=True, text=True, env=env,
                       cwd=tmp_path, timeout=120, encoding="utf-8", errors="replace")
    assert r.returncode == 0 and "CTFL-" in r.stdout, r.stdout + r.stderr

    # Serveur MCP tel que Claude Code le lance (CLAUDE_PLUGIN_DATA fourni) : même dossier de données.
    pytest.importorskip("mcp", reason="SDK `mcp` absent du Python des tests : dialogue MCP non essayé")
    from mcp import Client, StdioServerParameters

    async def dialogue():
        params = StdioServerParameters(command=qa[0], args=["mcp"], cwd=str(tmp_path),
                                       env={**env, "CLAUDE_PLUGIN_DATA": str(donnees)})
        async with Client(params) as c:
            texte = (await c.call_tool("chercher", {"requete": "partitions d'équivalence"})).content[0].text
            assert "CTFL-" in texte, texte

    asyncio.run(asyncio.wait_for(dialogue(), 120))


def test_verrou_libere_si_le_processus_meurt(export, tmp_path):
    """Un serveur MCP arrêté par Claude Code en pleine préparation ne laisse pas de verrou
    (constaté avec un verrou en dossier : `qa installer` attendait 15 minutes)."""
    verrou = tmp_path / "venv.verrou"
    code = ("import sys, time; sys.path.insert(0, sys.argv[1]); import lanceur; "
            "v = lanceur.Verrou(__import__('pathlib').Path(sys.argv[2])); v.__enter__(); "
            "print('tenu', flush=True); time.sleep(60)")
    p = subprocess.Popen([sys.executable, "-B", "-c", code, str(export), str(verrou)], stdout=subprocess.PIPE, text=True)
    try:
        assert p.stdout.readline().strip() == "tenu"
        lanceur = _lanceur(export)
        lanceur.ATTENTE_VERROU = 2
        with pytest.raises(SystemExit, match="préparation toujours en cours"):
            with lanceur.Verrou(verrou):
                pass
    finally:
        p.kill()
        p.wait(10)
    lanceur.ATTENTE_VERROU = 5
    with lanceur.Verrou(verrou):  # libéré par le système à la mort du processus
        pass
