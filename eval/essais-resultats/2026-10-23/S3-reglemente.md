# S3-reglemente — sylvie

**Question** : Pour le logiciel de notre dispositif médical, je prévois : une matrice de traçabilité exigences → tests tenue dans un tableur, une analyse de risques faite une seule fois en début de projet, et des tests système manuels avant chaque release. Est-ce aligné ISTQB ? Quel niveau de maturité ?

**Tours** : 6 · **coût** : 0.138 $ · **confiance annoncée** : 62 · **verdict** : réussi · **citations** : 9/9 lues · **Web** : 0 · **critères** : 5/5

## Réponse

**Avis indicatif d'alignement sur les syllabus ISTQB locaux ; ni attestation de conformité, ni évaluation ISTQB/TMMi/ISO.**

**Synthèse.** Votre démarche est partiellement alignée. La matrice de traçabilité va dans le sens des syllabus. L'analyse de risques réalisée une seule fois contredit explicitement le CTAL-TM. Les tests système manuels avant release ne sont pas évaluables en l'état. Pour le cadre réglementaire d'un dispositif médical, aucun syllabus de la bibliothèque n'est applicable.

**Pratiques décrites** (les trois sont formulées au futur, donc ce sont des intentions) :
- P1 : matrice de traçabilité exigences → tests dans un tableur. Intention.
- P2 : analyse de risques faite une seule fois en début de projet. Intention.
- P3 : tests système manuels avant chaque release. Intention.

| Pratique | Intention / en place | Verdict | Ce que dit l'ISTQB | Source |
|---|---|---|---|---|
| P1 Matrice exigences → tests (tableur) | Intention | Partiellement aligné | La traçabilité entre la base de test et le testware (conditions de test, risques, cas de test), les résultats et les anomalies soutient la supervision et le contrôle. Elle permet d'évaluer la couverture. Elle permet aussi d'analyser l'impact des changements et de faciliter les audits. Votre matrice ne couvre que exigences → tests. Les liens vers les résultats, les anomalies et les risques ne sont pas décrits. Le syllabus ne parle pas du choix du tableur comme outil. | [CTFL v4.0.1 EN, §1.4.4, pp. 20-21] |
| P2 Analyse de risques unique en début de projet | Intention | **Écart** | « L'analyse des risques est donc une activité continue et itérative qui ne doit pas être réalisée une seule fois au début du projet. » Le suivi des tests doit inclure le suivi des risques : nouveaux risques et ajustement du registre. Les parties prenantes changent et de nouveaux risques apparaissent. | [CTAL-TM v3.0 FR, §1.3.6, p. 34] ; [CTAL-TM v3.0 FR, §1.3.1, p. 29] |
| P3 Tests système manuels avant chaque release | Intention | Partiellement aligné | Les syllabus lus sur le test basé sur les risques ne traitent pas de « manuel » ou « automatisé » comme critère de conformité. Ils demandent que les tests soient choisis et priorisés selon le niveau de risque. Ils demandent aussi d'adapter l'étendue des tests de régression et le niveau d'indépendance au niveau de risque, et de rapporter l'avancement en risque résiduel. Votre description ne dit pas comment les tests sont choisis, priorisés ni rapportés. Elle ne dit pas non plus si le manuel exclusivement est adapté à des releases fréquentes. Le syllabus n'en dit rien dans les passages lus. | [CTAL-TM v3.0 FR, §1.3.4, pp. 32-33] |
| Exigences réglementaires du dispositif médical | Non décrit | Non vérifiable | Le CTAL-TM cite seulement, à titre d'exemple, qu'une norme de sûreté (IEC 61508) peut prescrire techniques et couverture selon le niveau d'intégrité. Le Test Manager doit s'assurer qu'elle est respectée. | [CTAL-TM v3.0 FR, §1.3.4, p. 32] |

**Ce qui manque** (étapes du processus de test basé sur les risques absentes de la démarche) :
- **Identification des risques avec les parties prenantes.** Entretiens, ateliers, brainstorming ou checklists. La liste des participants doit être convenue avec le chef de projet. Rien n'indique qui participe à l'analyse. [CTAL-TM v3.0 FR, §1.3.2, pp. 29-30]
- **Évaluation probabilité × impact.** Elle s'appuie sur une catégorisation des risques et sur une matrice de risque. Pour un dispositif médical, les facteurs d'impact incluent les besoins en matière de sûreté. [CTAL-TM v3.0 FR, §1.3.3, pp. 30-31]
- **Atténuation traduite en plan de test.** Le niveau de risque détermine la profondeur et les techniques de test, l'ordre d'exécution et la décision de livraison. [CTAL-TM v3.0 FR, §1.3.4, pp. 32-33]
- **Suivi et réévaluation des risques pendant le projet.** Cela inclut un registre des risques à jour. [CTAL-TM v3.0 FR, §1.3.1, p. 29]
- **Traçabilité tests ↔ risques et résultats.** Elle permet d'évaluer le risque résiduel. [CTFL v4.0.1 EN, §1.4.4, p. 21]
- **Rétrospective sur le test basé sur les risques.** Elle mesure notamment si les parties prenantes concernées ont participé à l'analyse. [CTAL-TM v3.0 FR, §1.3.6, p. 34]
- **Politique ou stratégie de test écrite.** Les syllabus lus ne la détaillent pas. Elle est le critère du niveau 2 de la grille du dépôt, sans passage de syllabus lu pour l'étayer.

**Niveau atteint : 1 — Initial · niveau visé : 1 à 2 au mieux.**
- Aucune pratique n'est « en place » avec preuve, donc le niveau est plafonné à 1 (grille du dépôt).
- Même si les trois pratiques étaient appliquées, le niveau 2 serait hors d'atteinte. Il exige une démarche rattachée à une stratégie écrite, supervisée et contrôlée, suivant les étapes du syllabus. Or l'analyse de risques unique contredit ces étapes (grille du dépôt).
- Pour passer au niveau 2 :
  1. Rédiger une stratégie de test.
  2. Réaliser l'analyse de risques avec les parties prenantes et la réviser à chaque jalon ou release.
  3. En déduire la priorité et la profondeur des tests.
  4. Suivre les tests et les risques pendant le projet.
  5. Prévoir l'environnement de test.
- Les niveaux 3 à 5 sont une adaptation du dépôt, pas une reprise du TMMi.

**Questions à choix**

Quel est le cadre réglementaire du logiciel ?
1. Règlement européen sur les dispositifs médicaux (MDR/IVDR) et IEC 62304.
2. Réglementation FDA (États-Unis).
3. Je ne sais pas encore.

Que souhaitez-vous faire ensuite ?
1. Une recherche plus large sur la réglementation avec Thomas (le Web n'est pas utilisé ici).
2. Une liste de contrôle du test basé sur les risques, au format JSON.
3. Rien de plus pour l'instant.

**Confiance : 62/100.** Les passages cités ont été lus : CTAL-TM §1.3 (sauf la fin de §1.3.5), §1.3.6 et CTFL §1.4.4. La couverture lexicale des recherches est correcte pour les risques et la traçabilité, mais faible pour les tests manuels avant release. Je n'ai lu aucun passage sur les spécificités des dispositifs médicaux. Les verdicts sur P3 et sur la réglementation sont donc fragiles. Comme les trois pratiques sont des intentions, le niveau atteint reste plafonné.

**Limites.**
- Aucun syllabus de la bibliothèque ne couvre le cadre réglementaire d'un dispositif médical (IEC 62304, ISO 14971, MDR, FDA). Toute conformité à ces textes est non vérifiable ici.
- L'ISO/IEC/IEEE 29119 n'est pas dans la bibliothèque.
- La suite de §1.3.5 (techniques lourdes, dont l'analyse des dangers) n'est pas lue. Elle pourrait être pertinente pour un système critique.
- Je n'ai rien enregistré.

**Traçabilité**
- Date de l'avis : 2026-10-23.
- Documents lus :
  - CTAL-TM-3.0-fr, v3.0 (2024-03-28) : §1.3 à §1.3.4 (pp. 29-33, lus en partie, §1.3.5 tronquée), §1.3.6 (p. 34).
  - CTFL-4.0.1-en, v4.0.1 (2024-09-15) : §1.4.4 (pp. 20-21).
  - Grille : `referentiel/grille-maturite.md`.
- Requêtes `chercher` :
  - « risk-based testing identification évaluation atténuation »
  - « traceability requirements test cases coverage »
  - « test system manuel regression avant release risques réévaluation »
  - « medical device regulatory safety-critical »
- Les autres résultats de ces requêtes n'ont été vus qu'en extrait ; ils ne sont pas cités.

**Avis indicatif d'alignement sur les syllabus ISTQB locaux ; ni attestation de conformité, ni évaluation ISTQB/TMMi/ISO.**

## Commandes exécutées

- `Read {"file_path": "/tmp/claude-0/-home-user/da9346e2-ce5e-5882-830a-19be129b35c4/scratchpad/final2/referentiel/grille-maturi`
- `python qa.py chercher "risk-based testing identification évaluation atténuation" 2>&1 | head -60; python qa.py chercher "traceability requirements test cases coverage" 2>&1 | head -50`
- `python qa.py section CTAL-TM-3.0-fr 1.3 2>&1; python qa.py section CTFL-4.0.1-en 1.4.4 2>&1`
- `python qa.py chercher "test system manuel regression avant release risques réévaluation" 2>&1 | head -40; python qa.py chercher "medical device regulatory safety-critical" 2>&1 | head -30`
- `python qa.py section CTAL-TM-3.0-fr 1.3.6 2>&1`
