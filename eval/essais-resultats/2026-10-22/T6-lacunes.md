# T6-lacunes — thomas

**Question** : Identifie les thèmes QA sur lesquels notre base de connaissances est encore pauvre.

**Tours** : 4 · **coût** : 0.08 $ · **confiance annoncée** : 70 · **verdict** : réussi · **citations** : 0/0 lues · **Web** : 0

## Réponse

Ta base d'idées est vide : `idee lister` répond « Aucune idée » et les 40 thèmes de la taxonomie affichent 0 idée. Elle est donc pauvre partout. Ce qui varie, c'est la quantité de matière que les syllabus offrent déjà pour la remplir.

**Sources retenues** : `python qa.py idee lister`, `themes` et `couverture`, ainsi que `inventaire` (42 fichiers, 26 codes en EN et 14 en FR). Je n'ai lu aucun passage de syllabus, donc je ne cite aucune référence ISTQB. Le Web n'était pas nécessaire.

Hypothèse de contexte : « pauvre » veut dire peu d'idées capitalisées, pas peu de syllabus.

**Thèmes à remplir en premier** (beaucoup de matière dans les syllabus, aucune idée capitalisée)
- Exigences et critères d'acceptation : 1 901 passages.
- Outils, méthodes et organisation des équipes : 1 748 passages, dont agile (1 132) et compétences d'équipe (590).
- Métriques et reporting : 1 164 passages.
- Estimation et planification : 1 099 passages.
- Analyse et conception des tests : 1 118 passages, dont couverture (461) et boîte noire (272).
- Niveaux et types de test : 1 006 passages.
- Automatisation : 1 019 passages.

**Thèmes pauvres en idées ET en syllabus** (angles morts probables)
- Priorisation des tests : 82 passages.
- Shift-left et shift-right (thème parent) : 83 passages.
- Stratégie et ROI de l'automatisation : 110 passages.
- L'IA au service du test : 111 passages. CT-GenAI v1.1 est pourtant récent.
- Boîte blanche : 150 passages.
- Test d'API : 158 passages. Les tests de contrat sont couverts seulement en anglais (CT-QDO).
- Maintenabilité de l'automatisation : 180 passages.
- Shift-left : 207 passages.
- Qualité logicielle réglementée : 301 passages. La bibliothèque n'a aucun syllabus santé ni dispositif médical, donc la norme IEC 62304 demanderait le Web.

**Limites de la bibliothèque**
- Plusieurs syllabus sont anciens ou remplacés : CT-SEC 2016, CTEL 2011, CTFL-AT 2014, CTAL-ATT et CTAL-TA 2019. Prudence pour y fonder des idées.
- Il n'y a pas de syllabus web dédié ni de syllabus API dédié.

**Par quoi je commencerais** (interprétation)
1. **Métriques et reporting**, ou **Risk-Based Testing** (373 passages) : impact fort pour un Test Manager, effort faible. CTAL-TM v3.0 existe en FR et en EN.
2. **Priorisation et shift-left/right** : impact moyen à fort, effort faible, car il y a peu de passages à lire.
3. **Exigences et critères d'acceptation** : impact fort, effort moyen à fort, vu le volume. À découper par sous-thème.

**Où creuser ensuite** : `python qa.py chercher --theme metriques`, puis `chercher --theme rbt`. Je lirais ensuite les sections correspondantes de CTAL-TM v3.0.

**Confiance : 70/100** (correcte). Les chiffres viennent directement de l'outil (inventaire, thèmes, liste vide). Je n'ai lu aucun passage, donc je n'ai pas vérifié la qualité du contenu derrière les nombres de passages. Ce nombre mesure l'occurrence de mots-clés, pas la pertinence. Je n'ai pas lancé `qa.py confiance`.

**Questions à choix**
1. Par quel thème commencer ?
   1. Métriques et reporting
   2. Risk-Based Testing et priorisation
   3. Exigences et critères d'acceptation
2. Quelle suite donner ?
   1. Approfondir un thème : je lis les meilleurs passages et je propose des idées prêtes à capitaliser.
   2. Comparer deux thèmes pauvres.
   3. `/ajouter-syllabus <code>` pour combler un angle mort (syllabus web, API ou santé).

**À capitaliser ?** Rien pour l'instant : je n'ai pas lu de passage qui puisse servir d'extrait.

## Commandes exécutées

- `python qa.py inventaire; python qa.py themes; python qa.py couverture 2>&1 | head -80`
- `Read {"file_path": "/tmp/claude-0/-home-user/da9346e2-ce5e-5882-830a-19be129b35c4/scratchpad/wt-G/.claude/skills/qa-knowledge`
- `python qa.py idee lister 2>&1 | tail -5; python qa.py confiance --help 2>&1 | head -20`
