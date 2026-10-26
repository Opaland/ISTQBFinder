---
name: installer
description: Premier usage du plugin ISTQBFinder — prépare l'environnement Python dans le dossier de données du plugin, télécharge les syllabus ISTQB anglais depuis istqb.org (tous, ou les codes donnés), les indexe et contrôle l'installation. Lancé par l'utilisateur.
argument-hint: "[codes, ex. CTFL CTAL-TM — vide : tous les syllabus anglais]"
disable-model-invocation: true
allowed-tools: Bash(qa emplacements:*), Bash(qa inventaire:*), Bash(qa manquants:*), Bash(qa diagnostic:*)
---

# Premier usage d'ISTQBFinder (plugin)

L'utilisateur a lancé cette commande lui-même : c'est son accord pour le téléchargement.
Rends compte en français, sans rien faire d'autre que ce qui suit.

1. `qa emplacements` : montre où vont le venv et les données (jamais dans le dossier du
   plugin).
2. `qa installer $ARGUMENTS` : crée le venv au besoin (une minute environ), télécharge
   **depuis istqb.org uniquement** (domaines de `catalogue/istqb.json`) les syllabus
   anglais demandés, ou tous si aucun code n'est donné (quelques minutes), puis indexe et
   lance le diagnostic. Laisse la commande aller au bout (délai long : 15 minutes).
3. `qa manquants` : résume « N syllabus en anglais ; aucun en français ».
4. Rappelle les deux points suivants :
   - **Traductions françaises** : elles ne sont pas téléchargées, car seul istqb.org est
     autorisé. L'utilisateur peut déposer ses PDF à la main avec `qa importer --prive
     <fichier.pdf>`, avec son accord, ou se servir d'un clone d'ISTQBFinder (variable
     `QAK_RACINE`, README du plugin).
   - **Base d'idées** : elle est vide au départ. C'est celle du dossier de données (une base
     par installation), que la désinstallation supprime sauf `--keep-data`.

Si une étape échoue (réseau, Python absent, `python3-venv` manquant), recopie le message
du lanceur tel quel. Ne contourne rien : aucun autre domaine de téléchargement.
