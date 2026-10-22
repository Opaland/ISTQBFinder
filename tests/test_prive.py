"""#116 : documents internes dans bibliotheque/prive/ — indexés localement, jamais versionnés."""
import shutil
import subprocess

import pytest

from qak import bibliotheque, chemins, recherche
from qak.cli import main
from conftest import FIXTURES

TEXTE = ("# 1 Bilan de campagne\n\nLe registre des risques du projet interne a été revu chaque semaine avec "
         "les responsables métier zygomorphe.\n")


def _git(racine, *args):
    return subprocess.run(["git", "-C", str(racine), "-c", "user.name=t", "-c", "user.email=t@t", *args],
                          capture_output=True, text=True, check=True).stdout


@pytest.fixture
def depot(racine_isolee):
    """La racine de test devient un dépôt Git muni du .gitignore du projet."""
    if not shutil.which("git"):
        pytest.skip("git absent")
    shutil.copy(chemins.CODE / ".gitignore", racine_isolee / ".gitignore")
    _git(racine_isolee, "init", "-q")
    _git(racine_isolee, "add", ".gitignore")
    _git(racine_isolee, "commit", "-qm", "init")
    return racine_isolee


def test_import_prive_n_ecrit_rien_de_suivi_par_git(depot, tmp_path_factory):
    externe = tmp_path_factory.mktemp("externe") / "bilan-client.md"
    externe.write_text(TEXTE, encoding="utf-8")
    assert main(["importer", str(externe), "--prive"]) == 0
    assert _git(depot, "status", "--porcelain", "--untracked-files=all") == ""
    assert (chemins.prive() / "bilan-client.md").is_file()
    assert not chemins.sources().exists() or not any(chemins.sources().iterdir())
    assert "bilan" not in (chemins.manifeste().read_text(encoding="utf-8") if chemins.manifeste().exists() else "")
    entree = next(iter(bibliotheque.lire_manifeste(prive=True)["documents"].values()))
    assert entree["prive"] is True
    assert recherche.chercher("zygomorphe")["resultats"]                    # indexé localement
    assert bibliotheque.controle_index()["perimes"] == set()


def test_fichier_depose_dans_prive_indexe_par_actualiser(depot):
    chemins.prive().mkdir(parents=True)
    (chemins.prive() / "note.md").write_text(TEXTE, encoding="utf-8")
    r = bibliotheque.actualiser()
    assert any("(privé)" in x for x in r["importes"]), r
    assert bibliotheque.actualiser()["importes"] == []                    # stable
    # `actualiser` (ré)écrit le manifeste versionné, mais sans rien du document interne.
    suivis = _git(depot, "status", "--porcelain", "--untracked-files=all").split()
    assert set(suivis) <= {"??", "bibliotheque/manifeste.json"}
    assert bibliotheque.lire_manifeste()["documents"] == {}


def test_import_prive_refuse_un_fichier_de_sources(racine_isolee):
    chemins.sources().mkdir(parents=True)
    f = chemins.sources() / "interne.md"
    f.write_text(TEXTE, encoding="utf-8")
    with pytest.raises(ValueError, match="VERSIONNÉ"):
        bibliotheque.importer(f, prive=True)


def test_corriger_puis_retirer_un_document_prive(depot, tmp_path_factory, capsys):
    """#130 : `corriger` et `retirer` ignoraient bibliotheque/prive/ (« Document inconnu »)."""
    bibliotheque.importer(FIXTURES / "syllabus_v9.pdf")
    externe = tmp_path_factory.mktemp("externe") / "bilan-client.md"
    externe.write_text(TEXTE, encoding="utf-8")
    doc_id = bibliotheque.importer(externe, prive=True)["doc_id"]
    public_avant = chemins.manifeste().read_bytes()
    assert main(["corriger", doc_id, "--titre", "Bilan anonymisé", "--langue", "fr"]) == 0
    entree = next(iter(bibliotheque.lire_manifeste(prive=True)["documents"].values()))
    assert entree["titre"] == "Bilan anonymisé" and "titre" in entree["champs_forces"]
    assert {d["doc_id"]: d["titre"] for d in bibliotheque.inventaire()}[doc_id] == "Bilan anonymisé"
    assert main(["retirer", doc_id, "--supprimer-fichier"]) == 0
    assert "supprimé" in capsys.readouterr().out
    assert bibliotheque.lire_manifeste(prive=True)["documents"] == {}
    assert not (chemins.prive() / "bilan-client.md").exists()
    assert not recherche.chercher("zygomorphe")["resultats"]
    assert doc_id not in {d["doc_id"] for d in bibliotheque.inventaire()}
    assert chemins.manifeste().read_bytes() == public_avant              # manifeste versionné inchangé
    assert bibliotheque.actualiser()["importes"] == []                    # pas de réimport
    # --supprimer-fichier refusé pour un document public (versionné)
    public = next(iter(bibliotheque.lire_manifeste()["documents"].values()))["doc_id"]
    with pytest.raises(ValueError, match="privés"):
        bibliotheque.retirer(public, supprimer_fichier=True)
