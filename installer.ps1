# Installation d'ISTQBFinder sous Windows (PowerShell 5.1 ou 7). Idempotent : relançable
# sans risque (venv réutilisé, indexation incrémentale).
#
#   powershell -ExecutionPolicy Bypass -File installer.ps1
#   powershell -ExecutionPolicy Bypass -File installer.ps1 -Assistant gemini   # claude|copilot|gemini|tous
#
# Procédure détaillée par assistant : docs\installation.md
param(
    [ValidateSet("", "claude", "copilot", "gemini", "tous")]
    [string]$Assistant = ""
)
$ErrorActionPreference = "Stop"
Set-Location -Path $PSScriptRoot
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONUTF8 = "1"

function Etape([string]$texte) { Write-Host "`n== $texte" }
function Echec([string]$texte) { Write-Host "`nKO : $texte" -ForegroundColor Red; exit 1 }
function VersionOk([string[]]$commande) {
    try {
        $exe = $commande[0]; $reste = @($commande | Select-Object -Skip 1)
        & $exe @reste -c "import sys; sys.exit(sys.version_info < (3, 10))" 2>$null | Out-Null
        return ($LASTEXITCODE -eq 0)
    } catch { return $false }
}

Etape "1/5 Python >= 3.10"
$py = $null
foreach ($candidat in @(@("py", "-3"), @("python"), @("python3"))) {
    if ((Get-Command $candidat[0] -ErrorAction SilentlyContinue) -and (VersionOk $candidat)) { $py = $candidat; break }
}
if (-not $py) {
    Echec "Python 3.10 ou plus récent introuvable. Installez-le depuis https://www.python.org/downloads/ (cocher « Add python.exe to PATH ») ou « winget install Python.Python.3.12 », puis relancez."
}
$pyExe = $py[0]; $pyArgs = @($py | Select-Object -Skip 1)
Write-Host ("OK : " + (& $pyExe @pyArgs --version))

Etape "2/5 Environnement virtuel .venv"
$vpy = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
if ((Test-Path $vpy) -and (VersionOk @($vpy))) {
    Write-Host "OK : .venv existant réutilisé"
} else {
    & $pyExe @pyArgs -m venv .venv
    if ($LASTEXITCODE -ne 0) { Echec "création du venv impossible." }
    Write-Host "OK : .venv créé"
}

Etape "3/5 Dépendances (requirements.txt)"
& $vpy -m pip install --disable-pip-version-check -q -r requirements.txt
if ($LASTEXITCODE -ne 0) { Echec "installation des dépendances impossible (réseau ? proxy ?). Relancez une fois le problème réglé." }
Write-Host "OK : dépendances installées"

Etape "4/5 Indexation de la bibliothèque (environ 3 min la première fois, quelques secondes ensuite)"
& $vpy qa.py actualiser
if ($LASTEXITCODE -ne 0) { Echec "indexation en échec : voir le message ci-dessus." }

Etape "5/5 Diagnostic"
if ($Assistant) { & $vpy qa.py diagnostic --assistant $Assistant } else { & $vpy qa.py diagnostic }
if ($LASTEXITCODE -ne 0) { Echec "diagnostic en échec : corrigez les lignes KO ci-dessus puis relancez installer.ps1." }

Write-Host @"

Installation terminée. Lancez votre assistant depuis ce dossier, venv activé
(les commandes « python qa.py … » utilisent alors le bon Python) :

    .\.venv\Scripts\Activate.ps1
    claude          # Claude Code    (ou : code .   pour VS Code + Copilot ; gemini   pour Gemini CLI)

Procédure par assistant : docs\installation.md
"@
