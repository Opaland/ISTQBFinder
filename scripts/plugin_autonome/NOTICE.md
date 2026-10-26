# NOTICE — code et documents tiers

## Ce que contient ce dépôt

Ce dépôt contient le code et la documentation d'ISTQBFinder : la CLI `qa.py` et `qak/`, les
skills, les agents, le lanceur, `catalogue/` et `referentiel/`. La licence MIT (`LICENSE`)
couvre **ce code et cette documentation seulement**.

Il ne contient **aucun syllabus ni aucun autre document de l'ISTQB®**, ni aucune traduction.
Aucun PDF n'y est versionné. Un contrôle de l'export (`scripts/exporter_plugin.py` du dépôt
source) refuse tout PDF et tout fichier de `bibliotheque/sources/`.

## Les documents téléchargés au premier usage

`qa installer` (ou `/istqbfinder:installer`) télécharge les syllabus anglais **depuis
istqb.org uniquement**. La liste des domaines autorisés vient de `catalogue/istqb.json`, et
elle est contrôlée aussi après redirection. Les PDF vont dans le dossier de données de
l'utilisateur (`qa emplacements`), jamais dans ce dépôt.

- Ces documents restent la propriété de l'International Software Testing Qualifications
  Board (© ISTQB®). Ils ne relèvent pas de la licence MIT.
- L'utilisateur les télécharge lui-même, à la source, pour son propre usage. Il est tenu
  par la notice de copyright de chaque syllabus. Les notices récentes n'autorisent que la
  copie d'**extraits**, à usage non commercial et avec citation de la source (par exemple
  CTFL v4.0.1, p. 2).
- L'autorisation que le mainteneur d'ISTQBFinder a obtenue de l'ISTQB®, du CFTL et de la
  TMMi Foundation vaut pour le dépôt source. Elle ne s'étend ni à ce dépôt ni aux copies
  téléchargées par les utilisateurs.
- Toute citation tirée d'un syllabus mentionne le syllabus, sa version et ses pages. La CLI
  la fournit sur la ligne « Citer : ».

## Traductions françaises et autres documents

Les traductions françaises (le plus souvent du CFTL) et les documents TMMi ne sont **pas**
téléchargés. Seul istqb.org est autorisé. L'utilisateur qui en dispose les dépose
lui-même dans son dossier de données (`qa importer --prive <fichier>`), sous sa
responsabilité et selon les droits de leurs auteurs.

Source : https://github.com/Opaland/ISTQBFinder (commit `{commit}`).
