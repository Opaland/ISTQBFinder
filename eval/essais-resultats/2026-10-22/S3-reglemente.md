# S3-reglemente — sylvie

**Question** : Pour le logiciel de notre dispositif médical, je prévois : une matrice de traçabilité exigences → tests tenue dans un tableur, une analyse de risques faite une seule fois en début de projet, et des tests système manuels avant chaque release. Est-ce aligné ISTQB ? Quel niveau de maturité ?

**Tours** : 8 · **coût** : 0.159 $ · **confiance annoncée** : 72 · **verdict** : réussi · **citations** : 5/5 lues · **Web** : 0 · **critères** : 5/5

## Réponse

**Avis indicatif d'alignement sur les syllabus ISTQB locaux ; ni attestation de conformité, ni évaluation ISTQB/TMMi/ISO.**

Ta démarche est partiellement alignée. La matrice de traçabilité va dans le sens de l'ISTQB. L'analyse de risques faite une seule fois s'écarte de ce que décrit le syllabus. Les tests système manuels avant chaque release sont alignés en principe, mais incomplets. Tu n'as pas dit que ces pratiques existent déjà, donc je les traite comme des intentions.

## Pratiques décrites
- **P1.** Matrice de traçabilité exigences → tests, tenue dans un tableur. *Intention.*
- **P2.** Analyse de risques faite une seule fois, en début de projet. *Intention.*
- **P3.** Tests système manuels avant chaque release. *Intention.*

| Pratique | Intention / en place | Verdict | Ce que dit l'ISTQB | Source |
|---|---|---|---|---|
| P1 | Intention | Partiellement aligné | La traçabilité doit être établie **et maintenue** tout au long du processus de test. Elle relie la base de test, les testwares, les résultats et les défauts. Elle sert à vérifier la couverture des exigences, à analyser l'impact des changements et à faciliter les audits. Elle relie aussi les résultats de test aux risques, pour évaluer le risque résiduel. Ta matrice ne couvre que exigences → tests : il manque les résultats, les défauts et les risques. Le tableur n'est pas un problème en soi, car le syllabus ne prescrit pas d'outil. | [CTFL v4.0.1 EN, §1.4.4, pp. 20-21] |
| P2 | Intention | **Écart** | L'analyse des risques n'est pas un acte unique. Le suivi des tests inclut le suivi des risques : évolution des risques connus, analyse des nouveaux risques, ajustement du registre des risques. Le contrôle des risques comprend l'atténuation **et** le suivi. Ce suivi sert à vérifier l'efficacité des mesures, à affiner l'évaluation et à repérer les risques émergents. | [CTAL-TM v3.0 FR, §1.3.1, p. 29] ; [CTFL v4.0.1 EN, §5.2.4, p. 53] |
| P3 | Intention | Partiellement aligné | Le test de régression confirme l'absence d'effets indésirables d'un changement. Il est précédé d'une analyse d'impact pour en déterminer l'étendue. Ces suites s'exécutent de nombreuses fois et grossissent à chaque release : elles sont de **fortes candidates à l'automatisation**. Le niveau de risque devrait aussi fixer l'étendue des régressions. Des tests uniquement manuels, sans priorisation par le risque, ne suivent pas ces pratiques. | [CTFL v4.0.1 EN, §2.2.3, pp. 30-31] ; [CTAL-TM v3.0 FR, §1.3.4, p. 32] |

Le test basé sur les risques de la Test Management (TM) décrit quatre activités : identifier, évaluer, suivre et atténuer les risques [CTAL-TM v3.0 FR, §1.3, p. 29]. Ta démarche ne couvre pas la première à la quatrième de façon continue.

## Ce qui manque
- **Identification avec les parties prenantes.** Le syllabus demande d'impliquer un large éventail de parties prenantes, avec une liste convenue avec le chef de projet, via ateliers, entretiens ou checklists. Tu ne mentionnes pas qui participe [CTAL-TM v3.0 FR, §1.3.2, pp. 29-30].
- **Évaluation probabilité × impact.** Elle repose sur une matrice de risque ou un calcul, et sur la catégorisation des risques [CTAL-TM v3.0 FR, §1.3.3, pp. 30-31 ; CTFL v4.0.1 EN, §5.2.3, pp. 52-53]. Ton dispositif médical est un cas où le facteur d'impact « besoins en matière de sûreté » (CTAL-TM, §1.3.3) compte beaucoup.
- **Lien risques → tests.** Les résultats de l'analyse doivent déterminer la portée, les niveaux et types de test, les techniques, la couverture visée, l'effort et la priorité d'exécution [CTFL v4.0.1 EN, §5.2.3, p. 53 ; CTAL-TM v3.0 FR, §1.3.1, p. 29].
- **Suivi des risques et mise à jour du registre pendant le projet** [CTAL-TM v3.0 FR, §1.3.1, p. 29].
- **Traçabilité vers les risques et les résultats.** Elle permet d'évaluer le risque résiduel [CTFL v4.0.1 EN, §1.4.4, p. 21].
- **Analyse d'impact et stratégie de régression.** Il faut une étendue de régression fondée sur l'impact et le risque, et une réflexion sur l'automatisation [CTFL v4.0.1 EN, §2.2.3, p. 31].
- **Exigences réglementaires.** Le syllabus note que certaines normes de sûreté prescrivent techniques de test et couverture selon le niveau d'intégrité. Le Test Manager doit s'assurer qu'elles sont respectées [CTAL-TM v3.0 FR, §1.3.4, p. 32]. Je ne sais pas quelle réglementation s'applique à ton dispositif.
- **Stratégie de test écrite et supervision.** Tu ne mentionnes ni politique ou stratégie de test, ni planification, ni suivi et contrôle, ni environnement de test. Ce sont les domaines du niveau 2 de la grille.

## Niveau
**Niveau atteint : 1 — Initial · niveau visé : 1-2 (au mieux).**

Aucune pratique n'est déclarée en place, donc le niveau est plafonné à 1 (grille du dépôt). Si tes trois intentions étaient appliquées telles quelles, tu resterais au niveau 1 : il manque la stratégie écrite et le contrôle continu des risques.

**Pour passer au niveau 2 (Discipliné)**, selon la grille :
- Écrire une stratégie de test rattachée à une politique.
- Faire une analyse de risques complète avec les parties prenantes, puis la remettre à jour pendant le projet.
- En déduire profondeur et priorité des tests, y compris la régression.
- Superviser et contrôler le projet, avec un environnement de test défini.
- Tenir la traçabilité à jour.

Les niveaux 3 à 5 sont une adaptation du dépôt, pas une reprise du TMMi (l'échelle s'en inspire seulement, voir `referentiel/grille-maturite.md`). Ils ne sont pas évalués ici.

## Confiance : 72/100
- J'ai lu les passages de référence : CTAL-TM §1.3 à 1.3.4, CTFL §1.4.4, §2.2.3, §5.2.3 et §5.2.4.
- Ta description est brève : aucune preuve de terrain, pas de contexte réglementaire, pas de cycle de vie précisé.
- Je n'ai pas lu les syllabus sur le test système ni sur l'outillage de traçabilité.

## Limites
- Les normes du dispositif médical (ex. IEC 62304, ISO 14971, ISO 13485) et l'ISO/IEC/IEEE 29119 ne sont pas dans la bibliothèque. Toute conformité réglementaire ou ISO est **non vérifiable** ici. Les exigences réglementaires d'un logiciel médical peuvent imposer davantage que l'ISTQB, par exemple sur la gestion des risques et la documentation. Thomas pourrait chercher plus largement sur le Web.
- L'ISTQB décrit des pratiques, pas une norme : il ne s'agit pas de conformité.

## Questions à choix
1. Quelle réglementation s'applique à ton dispositif ?
   1. Règlement européen sur les dispositifs médicaux (MDR / IEC 62304)
   2. FDA (États-Unis)
   3. Je ne sais pas encore
2. Quelle suite veux-tu ?
   1. Une checklist détaillée de test basé sur les risques, à conserver
   2. Une recherche Web par Thomas sur les exigences réglementaires
   3. Rien de plus pour l'instant

## Traçabilité
- **Date de l'avis :** 2026-10-22.
- **Documents lus :**
  - `CTAL-TM-3.0-fr`, v3.0 (2024-03-28). §1.3 à 1.3.4, pp. 29-32 (§1.3.4 lu en partie, sa fin non lue).
  - `CTFL-4.0.1-en`, v4.0.1 (2024-09-15). §1.4.4, pp. 20-21 ; §2.2.3, pp. 30-31 ; §5.2.3, pp. 52-53 ; §5.2.4, p. 53 (début lu).
- **Requêtes `chercher` :**
  - « risk-based testing identification évaluation atténuation »
  - « traceability requirements test cases coverage »
  - « risk analysis regular review risk register product risk »
  - « regression testing automation manual repeated release system testing »
- **Référentiel de grille :** `referentiel/grille-maturite.md`.

**Avis indicatif d'alignement sur les syllabus ISTQB locaux ; ni attestation de conformité, ni évaluation ISTQB/TMMi/ISO.**

## Commandes exécutées

- `Read {"file_path": "/tmp/claude-0/-home-user/da9346e2-ce5e-5882-830a-19be129b35c4/scratchpad/wt-127/referentiel/grille-maturi`
- `python qa.py chercher "risk-based testing identification évaluation atténuation" 2>&1 | head -60`
- `python qa.py chercher "traceability requirements test cases coverage" 2>&1 | head -50`
- `python qa.py chercher "risk analysis regular review risk register product risk" 2>&1 | head -50`
- `python qa.py section CTAL-TM-3.0-fr 1.3 2>&1 | head -120; echo ======; python qa.py section CTFL-4.0.1-en 1.4.4 2>&1 | head -40; echo =====; python qa.py section CTFL-4.0.1-en 5.2.4 2>&1 | head -40`
- `python qa.py chercher "regression testing automation manual repeated release system testing" 2>&1 | head -30; python qa.py section CTAL-TM-3.0-fr 1.3.4 2>&1 | head -40; python qa.py section CTFL-4.0.1`
- `python qa.py section CTFL-4.0.1-en 2.2.3 2>&1 | head -25`
