#!/usr/bin/env python3
"""Produit le paquet `.mcpb` (extension Claude Desktop) du serveur MCP en lecture seule (#200).

    python scripts/produire_mcpb.py <sortie.mcpb> [--version X.Y.Z]
    python scripts/produire_mcpb.py --essayer <clone>     # commande du manifeste, tools/list

Le paquet ne contient que `mcpb/manifest.json` : ni code, ni syllabus. L'extension lance le
Python du venv d'un clone installé (`user_config.clone`), avec `qa.py mcp`. Les PDF ne
peuvent pas être redistribués hors du dépôt (NOTICE.md, #149).

`verifier()` contrôle le manifeste (aucune référence à un PDF ni à `bibliotheque/`, commande
du venv du clone sous Linux/macOS et sous Windows, outils identiques à ceux du serveur) puis
le paquet écrit (seul `manifest.json`, aucun PDF) ; la production échoue sinon. Le format est
validé en CI par `npx @anthropic-ai/mcpb validate` (job `mcpb`). Aucune publication ici.

`--essayer` fait ce que ferait Claude Desktop sans lui : remplace `${user_config.clone}` dans
la commande de la plateforme courante, lance le serveur et lui demande `tools/list` par
JSON-RPC sur stdio. Ce n'est pas un essai dans Claude Desktop.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import zipfile
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
MANIFESTE = RACINE / "mcpb" / "manifest.json"
CONTENU = ("manifest.json",)
SEMVER = re.compile(r"^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.+-]+)?$")
INTERDIT = re.compile(r"\.pdf\b|bibliotheque", re.IGNORECASE)
COMMANDES = {
    "": ("${user_config.clone}/.venv/bin/python", ["${user_config.clone}/qa.py", "mcp"]),
    "win32": ("${user_config.clone}\\.venv\\Scripts\\python.exe", ["${user_config.clone}\\qa.py", "mcp"]),
}


def outils_du_serveur() -> list[str]:
    sys.path.insert(0, str(RACINE))
    from qak import serveur_mcp
    return [f.__name__ for f in serveur_mcp.OUTILS]


def verifier(manifeste: dict) -> list[str]:
    """Erreurs du manifeste, en français ; vide s'il est conforme."""
    erreurs = []
    texte = json.dumps(manifeste, ensure_ascii=False)
    if INTERDIT.search(texte):
        erreurs.append(f"le manifeste référence un PDF ou la bibliothèque : « {INTERDIT.search(texte)[0]} ».")
    if not SEMVER.match(str(manifeste.get("version", ""))):
        erreurs.append(f"version « {manifeste.get('version')} » non conforme à semver (X.Y.Z).")
    clone = manifeste.get("user_config", {}).get("clone", {})
    if clone.get("type") != "directory" or not clone.get("required"):
        erreurs.append("user_config.clone doit être un dossier (type directory) obligatoire.")
    config = manifeste.get("server", {}).get("mcp_config", {})
    for plateforme, (commande, args) in COMMANDES.items():
        vue = config.get("platform_overrides", {}).get(plateforme, {}) if plateforme else config
        if (vue.get("command"), vue.get("args")) != (commande, args):
            erreurs.append(f"commande {plateforme or 'par défaut'} : {commande} {' '.join(args)} attendu.")
    noms = [t.get("name") for t in manifeste.get("tools", [])]
    if noms != outils_du_serveur():
        erreurs.append(f"outils déclarés {noms} différents de ceux du serveur {outils_du_serveur()}.")
    return erreurs


def verifier_paquet(paquet: Path) -> list[str]:
    with zipfile.ZipFile(paquet) as z:
        noms = z.namelist()
    erreurs = [f"fichier inattendu dans le paquet : {n}" for n in noms if n not in CONTENU]
    return erreurs + [f"PDF dans le paquet : {n}" for n in noms if n.lower().endswith(".pdf")]


def produire(sortie: Path, version: str | None = None) -> Path:
    manifeste = json.loads(MANIFESTE.read_text(encoding="utf-8"))
    if version:
        manifeste["version"] = version
    if erreurs := verifier(manifeste):
        raise SystemExit("Manifeste refusé :\n- " + "\n- ".join(erreurs))
    sortie.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(sortie, "w", zipfile.ZIP_DEFLATED) as z:
        info = zipfile.ZipInfo("manifest.json", date_time=(1980, 1, 1, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        z.writestr(info, json.dumps(manifeste, ensure_ascii=False, indent=2) + "\n")
    if erreurs := verifier_paquet(sortie):
        sortie.unlink()
        raise SystemExit("Paquet refusé :\n- " + "\n- ".join(erreurs))
    return sortie


def commande(manifeste: dict, clone: Path, plateforme: str = sys.platform) -> list[str]:
    """Commande lancée par l'hôte sur `plateforme`, `${user_config.clone}` remplacé."""
    config = manifeste["server"]["mcp_config"]
    vue = {**config, **config.get("platform_overrides", {}).get(plateforme, {})}
    return [x.replace("${user_config.clone}", str(clone)) for x in [vue["command"], *vue["args"]]]


def essayer(clone: Path) -> list[str]:
    """Outils annoncés par le serveur lancé avec la commande du manifeste (initialize, tools/list)."""
    manifeste = json.loads(MANIFESTE.read_text(encoding="utf-8"))
    argv = commande(manifeste, clone.resolve())
    if not Path(argv[0]).is_file():
        raise SystemExit(f"Python du venv introuvable : {argv[0]}. Lancez installer.sh dans le clone, "
                         "puis .venv/bin/python -m pip install -r requirements-mcp.txt.")
    messages = [
        {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
            "protocolVersion": "2025-06-18", "capabilities": {},
            "clientInfo": {"name": "produire_mcpb", "version": "1"}}},
        {"jsonrpc": "2.0", "method": "notifications/initialized"},
        {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
    ]
    entree = "".join(json.dumps(m) + "\n" for m in messages)
    with subprocess.Popen(argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          text=True, encoding="utf-8", env={**os.environ, "PYTHONIOENCODING": "utf-8"}) as proc:
        proc.stdin.write(entree)
        proc.stdin.flush()
        for ligne in proc.stdout:
            reponse = json.loads(ligne)
            if reponse.get("id") == 2:
                proc.stdin.close()
                proc.wait(30)
                return [t["name"] for t in reponse["result"]["tools"]]
        raise SystemExit(f"Le serveur n'a pas répondu à tools/list : {proc.stderr.read().strip()[-500:]}")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Produit le paquet .mcpb du serveur MCP (#200), sans PDF.")
    p.add_argument("sortie", type=Path, nargs="?", help="fichier .mcpb à écrire")
    p.add_argument("--version", help="version semver du paquet (défaut : celle de mcpb/manifest.json)")
    p.add_argument("--essayer", type=Path, metavar="CLONE",
                   help="lance le serveur avec la commande du manifeste pour ce clone et liste ses outils")
    a = p.parse_args(argv)
    if a.essayer:
        noms = essayer(a.essayer)
        if noms != outils_du_serveur():
            print(f"KO : outils annoncés {noms}, attendus {outils_du_serveur()}")
            return 1
        print(f"OK : {' '.join(commande(json.loads(MANIFESTE.read_text(encoding='utf-8')), a.essayer.resolve()))}"
              f" -> {len(noms)} outils ({', '.join(noms)})")
        return 0
    if not a.sortie:
        p.error("indiquez le fichier .mcpb à écrire, ou --essayer CLONE")
    paquet = produire(a.sortie, a.version)
    print(f"OK : {paquet} ({paquet.stat().st_size} octets, manifest.json seul, aucun PDF)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
