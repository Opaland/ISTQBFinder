#!/usr/bin/env python3
"""Lanceur du plugin ISTQBFinder autonome : `qa <commande>` (#184).

Copié tel quel à la racine du plugin par `scripts/exporter_plugin.py` (dépôt ISTQBFinder) ;
appelé par `bin/qa` (Linux, macOS) et `bin/qa.cmd` (Windows) avec le Python du système,
bibliothèque standard seulement.

- Dossier du plugin (`${CLAUDE_PLUGIN_ROOT}`) : le code, en lecture seule. Rien n'y est écrit
  (pas même `__pycache__`).
- Dossier de données du plugin : `${CLAUDE_PLUGIN_DATA}`, que Claude Code transmet au serveur
  MCP. L'outil Bash ne le reçoit pas : le lanceur le recalcule comme Claude Code,
  `<config>/plugins/data/<id>/`, `<id>` = `istqbfinder@<marketplace>` où tout caractère autre
  que lettre, chiffre, `_` ou `-` devient `-`. On y trouve :
  - `venv/` : environnement Python (pypdf, SDK MCP), créé au premier usage ;
  - `donnees/` : bibliothèque, index, base d'idées, journal (`QAK_RACINE`).
- `QAK_RACINE`, s'il est défini, remplace `donnees/` (par exemple un clone d'ISTQBFinder,
  avec ses traductions françaises et sa base d'idées).

Commandes propres au lanceur :
- `qa installer [codes…]` : premier usage. Venv, téléchargement des syllabus anglais depuis
  istqb.org (tous, ou les codes donnés ; domaines de `catalogue/istqb.json` seulement),
  indexation, diagnostic.
- `qa emplacements` : où sont le code, le venv et les données.
Toute autre commande est passée à `qa.py` (venv créé au besoin). Pour `qa mcp` (serveur lancé
par Claude Code, qui l'abandonne après 30 s), la création du venv part dans un processus
détaché ; un verrou de fichier tenu par le processus évite deux préparations simultanées.
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

NOM_PLUGIN = "istqbfinder"
PLUGIN = Path(__file__).resolve().parent
DEPENDANCES = ("requirements.txt", "requirements-mcp.txt")
MARQUE_VENV = "istqbfinder-dependances.txt"
ATTENTE_VERROU = 15 * 60   # secondes : préparation en cours dans un autre processus
ATTENTE_MCP = 20           # secondes : Claude Code abandonne un serveur MCP muet après 30 s (MCP_TIMEOUT)


def dire(message: str) -> None:
    """Toujours sur stderr : stdout appartient à qa.py (et au protocole MCP)."""
    print(f"ISTQBFinder : {message}", file=sys.stderr, flush=True)


def marketplace() -> str:
    """Nom de la marketplace d'où vient le plugin. Installé depuis GitHub, le plugin est copié
    dans `<config>/plugins/cache/<marketplace>/<plugin>/<version>/` ; chargé en place (marketplace
    ajoutée depuis un dossier), il porte sa marketplace à sa racine."""
    p = PLUGIN.parts
    if len(p) >= 5 and p[-5] == "plugins" and p[-4] == "cache" and p[-2] == NOM_PLUGIN:
        return p[-3]
    try:
        return json.loads((PLUGIN / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))["name"]
    except (OSError, ValueError, KeyError):
        return NOM_PLUGIN


def identifiant() -> str:
    return re.sub(r"[^A-Za-z0-9_-]", "-", f"{NOM_PLUGIN}@{marketplace()}")


def dossier_plugin() -> Path:
    if os.environ.get("CLAUDE_PLUGIN_DATA"):
        return Path(os.environ["CLAUDE_PLUGIN_DATA"])
    config = Path(os.environ.get("CLAUDE_CONFIG_DIR") or Path.home() / ".claude")
    return config / "plugins" / "data" / identifiant()


def racine_donnees() -> Path:
    return Path(os.environ.get("QAK_RACINE") or dossier_plugin() / "donnees")


def python_venv() -> Path:
    venv = dossier_plugin() / "venv"
    return venv / "Scripts" / "python.exe" if os.name == "nt" else venv / "bin" / "python"


def empreinte() -> str:
    """Change quand une mise à jour du plugin modifie les dépendances : le venv est alors complété."""
    h = hashlib.sha256(f"{sys.version_info[0]}.{sys.version_info[1]}".encode())
    for nom in DEPENDANCES:
        h.update((PLUGIN / nom).read_bytes())
    return h.hexdigest()


class Verrou:
    """Verrou de fichier tenu par le PROCESSUS (fcntl / msvcrt) : libéré par le système si ce
    processus meurt, par exemple quand Claude Code arrête un serveur MCP trop lent."""

    def __init__(self, chemin: Path):
        self.chemin, self.f = chemin, None

    def __enter__(self):
        self.f = open(self.chemin, "a+b")
        debut = time.monotonic()
        while True:
            try:
                if os.name == "nt":
                    import msvcrt
                    self.f.seek(0)
                    msvcrt.locking(self.f.fileno(), msvcrt.LK_NBLCK, 1)
                else:
                    import fcntl
                    fcntl.flock(self.f.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                return self
            except OSError:
                if time.monotonic() - debut > ATTENTE_VERROU:
                    self.f.close()
                    raise SystemExit(f"ISTQBFinder : préparation toujours en cours ailleurs ({self.chemin}).")
                time.sleep(1)

    def __exit__(self, *exc):
        if os.name == "nt":
            import msvcrt
            self.f.seek(0)
            try:
                msvcrt.locking(self.f.fileno(), msvcrt.LK_UNLCK, 1)
            except OSError:
                pass
        self.f.close()


def venv_pret() -> bool:
    marque = python_venv().parent.parent / MARQUE_VENV
    try:
        return python_venv().exists() and marque.read_text(encoding="utf-8").strip() == empreinte()
    except OSError:
        return False


def preparer_venv() -> Path:
    """Crée ou complète le venv du dossier de données ; renvoie son Python."""
    py = python_venv()
    if venv_pret():
        return py
    dossier = dossier_plugin()
    dossier.mkdir(parents=True, exist_ok=True)
    with Verrou(dossier / "venv.verrou"):
        if venv_pret():
            return py  # préparé par un autre processus pendant l'attente
        dire(f"préparation de l'environnement Python dans {py.parent.parent} (premier usage, une minute environ)…")
        if not py.exists():
            r = subprocess.run([sys.executable, "-m", "venv", str(py.parent.parent)], stdout=sys.stderr.fileno())
            if r.returncode or not py.exists():
                shutil.rmtree(py.parent.parent, ignore_errors=True)
                raise SystemExit("ISTQBFinder : création du venv impossible. Sous Debian ou Ubuntu, installer "
                                 "le paquet python3-venv, puis relancer.")
        cmd = [str(py), "-m", "pip", "install", "--disable-pip-version-check", "--quiet"]
        for nom in DEPENDANCES:
            cmd += ["-r", str(PLUGIN / nom)]
        if subprocess.run(cmd, stdout=sys.stderr.fileno()).returncode:
            raise SystemExit("ISTQBFinder : installation des dépendances impossible (pip, accès à PyPI ?). "
                             "Relancer `qa installer` une fois le réseau rétabli.")
        (py.parent.parent / MARQUE_VENV).write_text(empreinte() + "\n", encoding="utf-8")
        dire("environnement Python prêt.")
        return py


def preparer_pour_mcp() -> Path:
    """Serveur MCP lancé avant tout premier usage : la préparation (pip, souvent plus de 30 s)
    part dans un processus détaché, qui survit à l'arrêt du serveur par Claude Code. On l'attend
    ATTENTE_MCP secondes ; au-delà, on s'arrête avec un message (reconnecter dans /mcp)."""
    if venv_pret():
        return python_venv()
    dossier = dossier_plugin()
    dossier.mkdir(parents=True, exist_ok=True)
    journal = dossier / "preparation.log"
    options = ({"creationflags": subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP}
               if os.name == "nt" else {"start_new_session": True})
    with open(journal, "ab") as sortie:
        subprocess.Popen([sys.executable, str(Path(__file__).resolve()), "_preparer"], stdin=subprocess.DEVNULL,
                         stdout=sortie, stderr=sortie, env=os.environ.copy(), **options)
    limite = time.monotonic() + ATTENTE_MCP
    while time.monotonic() < limite:
        if venv_pret():
            return python_venv()
        time.sleep(1)
    raise SystemExit(f"ISTQBFinder : premier usage, environnement Python en préparation (journal : {journal}). "
                     "Reconnecter le serveur dans /mcp d'ici une minute, ou lancer /istqbfinder:installer.")


def environnement() -> dict:
    racine = racine_donnees()
    racine.mkdir(parents=True, exist_ok=True)
    return {**os.environ, "QAK_RACINE": str(racine), "PYTHONDONTWRITEBYTECODE": "1"}


def qa(py: Path, args: list[str]) -> int:
    """`qa.py <args>` avec le Python du venv, sans rendre la main."""
    return subprocess.call([str(py), str(PLUGIN / "qa.py"), *args], env=environnement())


def executer(py: Path, args: list[str]):
    cmd = [str(py), str(PLUGIN / "qa.py"), *args]
    if os.name == "nt":  # execv sous Windows crée un nouveau processus : on garde la main
        sys.exit(subprocess.call(cmd, env=environnement()))
    os.execve(str(py), cmd, environnement())


def emplacements() -> int:
    print(f"Plugin (code, lecture seule) : {PLUGIN}")
    print(f"Dossier de données du plugin : {dossier_plugin()}")
    print(f"Python du venv               : {python_venv()}{'' if python_venv().exists() else ' (absent : qa installer)'}")
    origine = "variable QAK_RACINE" if os.environ.get("QAK_RACINE") else "défaut"
    print(f"{'Données (' + origine + ')':<29}: {racine_donnees()}")
    print(f"  bibliothèque               : {racine_donnees() / 'bibliotheque'}")
    print(f"  base d'idées               : {racine_donnees() / 'connaissances' / 'connaissances.jsonl'}")
    return 0


def installer(codes: list[str]) -> int:
    """Premier usage : venv, syllabus anglais depuis istqb.org, index, diagnostic."""
    py = preparer_venv()
    dire(f"données dans {racine_donnees()}")
    dire("téléchargement des syllabus anglais depuis istqb.org (catalogue/istqb.json)…")
    rc = qa(py, ["telecharger", *codes] if codes else ["telecharger", "--tous"])
    if rc:
        dire("au moins un téléchargement a échoué (voir ci-dessus) ; relancer `qa installer` plus tard : "
             "un document déjà présent est reconnu (doublon) et n'est pas importé deux fois.")
    rc = qa(py, ["actualiser"]) or rc
    qa(py, ["diagnostic"])
    dire("traductions françaises : non téléchargées (istqb.org seulement). Les déposer à la main : "
         "`qa importer --prive <fichier.pdf>`.")
    return rc


def main(args: list[str]) -> int:
    if sys.version_info < (3, 10):
        dire(f"Python 3.10 ou plus requis ({sys.executable} est en {sys.version.split()[0]}).")
        return 2
    if args[:1] == ["emplacements"]:
        return emplacements()
    if args[:1] == ["installer"]:
        if any(a in ("-h", "--help") for a in args[1:]):
            print("usage : qa installer [codes ...]\n\nPremier usage : venv, syllabus anglais depuis istqb.org "
                  "(tous, ou les codes donnés, ex. CTFL CTAL-TM), indexation, diagnostic.")
            return 0
        return installer(args[1:])
    if args[:1] == ["_preparer"]:  # interne : préparation détachée lancée par preparer_pour_mcp()
        preparer_venv()
        return 0
    executer(preparer_pour_mcp() if args[:1] == ["mcp"] else preparer_venv(), args)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
