# T2-rbt-agile — thomas

**Question** : Recherche des idées pour intégrer le risk-based testing dans une équipe produit agile.

**Tours** : 14 · **coût** : 0.272 $ · **confiance annoncée** : 91 · **verdict** : réussi · **citations** : 7/7 lues · **Web** : 0 · **fidélité** (juge LLM, indicatif) : 0.79 sur 7 lignes citées, 0 contradiction(s)

## Réponse

Sources retenues : base d'idées (aucune idée capitalisée), puis cinq passages lus dans quatre syllabus, EN et FR. J'ai lu CTAL-TM v3.0 EN §1.3.3, CTAL-TM v3.0 FR §1.3.6, CTAL-AT v2.0 EN §3.1.1, CTFL v4.0.1 EN §5.1.2 et CTFL-AT 2014 EN §3.2.1. Ce dernier est en retrait de l'ISTQB et remplacé par CTAL-AT. Pas de Web : la question ne nomme aucun outil. Je n'ai pas lu en entier CTAL-AT sur le risque, CTAL-TA §2 ni CTFL §5.2.3-5.2.4.

Le risk-based testing (RBT) s'intègre dans l'agile en l'insérant dans les deux cérémonies de planification. L'analyse de risque devient une activité d'équipe répétée, pas un document initial.

Hypothèse de contexte : équipe Scrum de 5 à 9 personnes, produit web, sans contrainte réglementaire forte, livraison toutes les 2 semaines.

**Pistes par syllabus**
- **CTFL v4.0.1 — §5.1.2 Planification**
  - En release planning, les testeurs participent à l'analyse des risques projet et qualité, et la stratégie de test de la release en découle. [CTFL v4.0.1 EN, §5.1.2, p. 48]
  - En iteration planning, ils font l'analyse détaillée des risques des user stories. [CTFL v4.0.1 EN, §5.1.2, p. 48]
  - *À creuser : §5.2.3-5.2.4 (analyse puis contrôle des risques).*
- **CTAL-AT v2.0 — §3.1.1 Planification des tests en agile**
  - Le testeur anime des sessions de *risk-storming* avec les représentants métier et les développeurs, pour identifier les risques et prioriser les tests. [CTAL-AT v2.0 EN, §3.1.1, p. 24]
  - Les quadrants de test aident à choisir types, niveaux et techniques de test. [CTAL-AT v2.0 EN, §3.1.1, p. 25]
  - La planification de release évalue les risques qualité sur tout le périmètre et fixe la stratégie de test fonctionnelle et non fonctionnelle. [CTAL-AT v2.0 EN, §3.1.1, p. 25]
- **CTFL-AT 2014 (ancien, mais très concret) — §3.2.1**
  - Procédure en 6 étapes pour l'iteration planning :
    1. réunir l'équipe, testeur compris ;
    2. lister les items du backlog ;
    3. identifier les risques de chaque item ;
    4. évaluer chaque risque (impact × probabilité) ;
    5. proportionner l'effort de test au niveau de risque ;
    6. choisir les techniques de test. [CTFL-AT 2014 EN, §3.2.1, p. 32]
  - Les tâches à risque élevé démarrent plus tôt et reçoivent plus d'effort de test. [CTFL-AT 2014 EN, §3.2.1, p. 32]
  - Il faut réajuster l'analyse périodiquement : nouveaux risques, niveaux réévalués, efficacité de la mitigation. [CTFL-AT 2014 EN, §3.2.1, p. 32]
  - Un risque peut être traité avant l'exécution, par exemple par une revue approfondie des user stories. [CTFL-AT 2014 EN, §3.2.1, p. 32]
- **CTAL-TM v3.0 — §1.3 Test basé sur les risques**
  - Facteurs de **probabilité** : complexité technique, équipes distribuées, pression sur les délais, forte instabilité de la base de test. Facteurs d'**impact** : fréquence d'usage, criticité métier, réputation, pertes financières. [CTAL-TM v3.0 EN, §1.3.3, p. 29-30]
  - Sans données statistiques fiables, l'évaluation reste qualitative : échelles ordinales combinées dans une matrice de risque. [CTAL-TM v3.0 EN, §1.3.3, p. 30]
  - Mesure en rétrospective, par exemple : les tests ignorés avaient-ils un risque plus faible que les tests exécutés ? Les défauts critiques ont-ils été trouvés tôt ? [CTAL-TM v3.0 FR, §1.3.6, p. 34]
  - Pièges listés : difficulté à estimer, complaisance du « déjà vu », risques importants non identifiés, parties prenantes qui changent. L'analyse doit rester continue et itérative. [CTAL-TM v3.0 FR, §1.3.6, p. 34]
  - *À creuser : §1.3.2, §1.3.4 et §1.3.5 (identification, mitigation, techniques).*

**Ce que j'en retiens** (interprétation)
- Deux niveaux suffisent : un registre de risques léger en release planning, et un passage de 15 à 30 minutes par story en iteration planning.
- Pour que ça tienne dans un sprint, utilise une échelle ordinale simple (3 niveaux) et rattache le niveau de risque aux critères d'acceptation ou à la Definition of Done.
- Les pièges de CTAL-TM (complaisance, parties prenantes qui changent) justifient une revue du registre à chaque rétrospective.

**Par quoi je commencerais**
1. Risk-storming en iteration planning, avec l'échelle 3 niveaux : impact fort, effort faible.
2. Indicateurs de rétrospective tirés de CTAL-TM §1.3.6 : impact moyen à fort, effort faible.
3. Registre de risques de release et lien avec la stratégie de test : impact fort, effort moyen.

**Où creuser ensuite**
- `section CTAL-TM-3.0-en 1.3.4` et `1.3.5` (mitigation et techniques de RBT).
- `section CTFL-4.0.1-en 5.2.3` et `5.2.4` (analyse et contrôle des risques).
- `section CTAL-TA-4.0-en 2` (rôle du Test Analyst dans le RBT).
- À lire : CTAL-AT v2.0 EN, sections sur les risques qualité (non lues).

**Confiance : 91/100** (élevée). Calcul de l'outil : base 85 × 0,6 = 51 ; 5 passages lus +20 ; syllabus concordants +20. Ce score est sans doute un peu généreux : deux des cinq passages sont des extraits de §3.1.1 et §5.1.2, et la source la plus détaillée (CTFL-AT) date de 2014. Je n'ai pas lu CTAL-AT sur le risque en profondeur.

**Questions à choix**
1. Quel est ton contexte ?
   1. Produit web ou SaaS, sans réglementation
   2. Domaine réglementé (santé, finance)
   3. Autre (mobile, embarqué, API)
2. Quelle suite veux-tu ?
   1. Approfondir la mitigation et les techniques (CTAL-TM §1.3.4-1.3.5)
   2. Détailler une démarche pas à pas avec exemple et adaptation par domaine
   3. Capitaliser la piste proposée ci-dessous

**À capitaliser ?** (pas de doublon trouvé ; thème `rbt`)
```json
{
  "titre": "RBT agile : risk-storming à chaque planification",
  "resume": "Analyser les risques qualité en release planning puis en iteration planning, avec toute l'équipe, et les réviser en continu.",
  "principe": "Le niveau de risque (impact × probabilité) pilote l'ordre et l'effort de test des user stories.",
  "themes": ["rbt"],
  "references": [
    {"document": "CTAL-AT-2.0-en", "page": 24, "extrait": "Testers can contribute by facilitating risk-storming sessions with business representatives and developers"},
    {"document": "CTFL-4.0.1-en", "page": 48, "extrait": "Testers involved in iteration planning participate in the detailed risk analysis of user stories"}
  ]
}
```
Je n'ai pas vérifié les champs de ce JSON avec `idee modele`. La conversation principale doit le faire avant `idee ajouter`.

## Commandes exécutées

- `Read {"file_path": "/tmp/claude-0/-home-user/da9346e2-ce5e-5882-830a-19be129b35c4/scratchpad/wt-campagne/.claude/skills/qa-kn`
- `python qa.py idee chercher risk-based testing agile 2>&1 | head -60`
- `python qa.py chercher risk-based testing agile 2>&1 | head -80`
- `python qa.py chercher "risk-based testing" CTAL-AT agile iteration risk 2>&1 | head -40; python qa.py chercher "product risk" "risk-based testing" CTFL 5.2 2>&1 | head -30`
- `python qa.py section CTAL-TM-3.0-fr 1.3.6 --max-caracteres 5000 2>&1; python qa.py section CTFL-AT-2014-en 3.2.1 --max-caracteres 6000 2>&1`
- `python qa.py inventaire 2>&1 | grep -iE "CTFL-4|CTFL-AT|CTAL-AT|CTAL-TM" | head; python qa.py section CTAL-TM-3.0-en 1.3 --max-caracteres 200 2>&1 | head -30`
- `python qa.py chercher "risk" "agile" "CTAL-AT" "release planning" "iteration" 2>&1 | grep -E "CTAL-AT|CTFL-4" | head`
- `python qa.py chercher "risk" "agile" "CTAL-AT" "release planning" "iteration" 2>&1 | grep -A3 -E "^\[(2|6|7)\]"; python qa.py section CTFL-4.0.1-en 5.2 --max-caracteres 200 2>&1 | tail -12`
- `python qa.py section CTAL-TM-3.0-en 1.3.3 --max-caracteres 5000 2>&1`
- `python qa.py section CTAL-AT-2.0-en 3.1.1 --max-caracteres 6000 2>&1; python qa.py section CTFL-4.0.1-en 5.1.2 --max-caracteres 3500 2>&1`
- `python qa.py idee doublons --titre "RBT agile : risk-storming à chaque planification" --resume "Analyser les risques qualité en release planning puis en iteration planning, avec toute l'équipe, et les`
- `python qa.py themes 2>&1 | grep -iE "risk|risq" | head -5; python qa.py confiance --base 85 --lus 5 --concordants 4 2>&1 | tail -6`
- `python qa.py confiance --base 85 --lus 5 --concordants 3 2>&1 | tail -5; python qa.py idee doublons --titre "RBT agile : risk-storming à chaque planification" --resume "Analyser les risques qualité en`
