"""Essai #203 (jetable) : quelles formes de `command` MCP Claude Code démarre-t-il ?"""
import json, os, stat, sys
from pathlib import Path
R = Path(sys.argv[1]); RACINE = Path(__file__).resolve().parent.parent
(R / ".claude-plugin").mkdir(parents=True); (R / "bin").mkdir()
(R / "lanceur.py").write_text(
    "import os, sys\nsys.argv = [sys.argv[0]] + sys.argv[1:]\n"
    f"sys.path.insert(0, {str(RACINE)!r})\nfrom qak.cli import main\nsys.exit(main())\n", encoding="utf-8")
sh = '#!/bin/sh\necho "forme=sh $*" >> "${TMPDIR:-${TEMP:-/tmp}}/marques-essai.txt"\nexec python3 "$(dirname "$0")/../lanceur.py" "$@"\n'
(R / "bin" / "qa").write_text(sh, newline="\n")
(R / "bin" / "qa.cmd").write_text('@echo off\r\necho forme=cmd %*>> "%TEMP%\\marques-essai.txt"\r\npython "%~dp0..\\lanceur.py" %*\r\n', newline="")
(R / "bin" / "poly.cmd").write_text(':; exec python3 "$(dirname "$0")/../lanceur.py" "$@"\n@echo off\r\npython "%~dp0..\\lanceur.py" %*\r\n', newline="")
(R / "bin" / "polysh.cmd").write_text('#!/bin/sh\n:; exec python3 "$(dirname "$0")/../lanceur.py" "$@"\n@echo off\r\npython "%~dp0..\\lanceur.py" %*\r\n', newline="")
for f in (R / "bin").iterdir():
    f.chmod(f.stat().st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
P = "${CLAUDE_PLUGIN_ROOT}"
serveurs = {
 "z-sans-ext-seul": {"command": f"{P}/bin/qa", "args": ["mcp"]},
 "b-cmd": {"command": f"{P}/bin/qa.cmd", "args": ["mcp"]},
 "c-python": {"command": "python", "args": [f"{P}/lanceur.py", "mcp"]},
 "d-py": {"command": "py", "args": ["-3", f"{P}/lanceur.py", "mcp"]},
 "e-cmd-c": {"command": "cmd", "args": ["/c", f"{P}/bin/qa.cmd", "mcp"]},
 "g-python3": {"command": "python3", "args": [f"{P}/lanceur.py", "mcp"]},
 "h-poly": {"command": f"{P}/bin/poly.cmd", "args": ["mcp"]},
 "i-polysh": {"command": f"{P}/bin/polysh.cmd", "args": ["mcp"]},
 "j-env": {"command": "python3", "args": [f"{P}/lanceur.py", "mcp"], "env": {"X": "${CLAUDE_PLUGIN_DATA}"}},
}
(R / ".claude-plugin" / "plugin.json").write_text(json.dumps({"name": "essai", "version": "0.0.1", "description": "essai", "author": {"name": "x"}, "mcpServers": serveurs}, indent=1))
(R / ".claude-plugin" / "marketplace.json").write_text(json.dumps({"name": "essai-mkt", "owner": {"name": "x"}, "plugins": [{"name": "essai", "source": "./"}]}, indent=1))
