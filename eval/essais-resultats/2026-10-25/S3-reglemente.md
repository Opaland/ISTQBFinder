# S3-reglemente — sylvie

**Question** : Pour le logiciel de notre dispositif médical, je prévois : une matrice de traçabilité exigences → tests tenue dans un tableur, une analyse de risques faite une seule fois en début de projet, et des tests système manuels avant chaque release. Est-ce aligné ISTQB ? Quel niveau de maturité ?

**Tours** : 4 · **coût** : 0.133 $ · **confiance annoncée** : 62 · **verdict** : réussi · **citations** : 11/11 lues · **Web** : 0 · **critères** : 5/5

## Réponse

**Avis indicatif d'alignement sur les syllabus ISTQB locaux ; ni attestation de conformité, ni évaluation ISTQB/TMMi/ISO.**

Ta démarche est partiellement alignée. La matrice de traçabilité va dans le sens de l'ISTQB. L'analyse de risques faite une seule fois s'en écarte nettement. Les tests système manuels sont acceptables, mais le syllabus invite à automatiser la régression. Les trois points sont des intentions : le niveau atteint est plafonné à 1.

## Pratiques décrites

- **P1** : matrice de traçabilité exigences → tests dans un tableur. *Intention.*
- **P2** : analyse de risques réalisée une seule fois, en début de projet. *Intention.*
- **P3** : tests système manuels avant chaque release. *Intention.*

| Pratique | Intention / en place | Verdict | Ce que dit l'ISTQB | Source |
|---|---|---|---|---|
| P1 Matrice exigences → tests (tableur) | Intention | Partiellement aligné | La traçabilité doit être établie et maintenue tout au long du processus de test, entre éléments de la base de test, testware, résultats et défauts. Relier les cas de test aux exigences permet de vérifier la couverture. Relier les résultats aux risques permet d'évaluer le risque résiduel. Elle sert aussi à l'analyse d'impact des changements et aux audits. Le syllabus n'impose pas d'outil, donc le tableur n'est pas un écart. Il manque le lien vers les risques, les résultats et les défauts, ainsi que la maintenance de la matrice. | [CTFL v4.0.1 EN, §1.4.4, pp. 20-21] |
| P2 Analyse de risques unique en début de projet | Intention | Écart (sur le « une seule fois ») ; l'analyse en elle-même n'est pas évaluable | Le suivi des tests doit inclure le suivi des risques : évolution des risques connus, analyse des nouveaux risques, ajustement du registre. Le test basé sur les risques comprend l'identification, l'évaluation, puis le contrôle (suivi et atténuation). L'analyse doit inclure diverses parties prenantes. Le niveau de risque combine probabilité et impact. | [CTAL-TM v3.0 FR, §1.3.1, p. 29] ; [CTAL-TM v3.0 FR, §1.3.2, pp. 29-30] ; [CTAL-TM v3.0 FR, §1.3.3, pp. 30-31] |
| P3 Tests système manuels avant chaque release | Intention | Partiellement aligné | Le niveau de risque devrait guider la priorisation, l'étendue des tests de régression, l'indépendance et les revues des cas de test. Les résultats peuvent être rapportés en risque résiduel pour décider de la livraison. Les suites de régression sont exécutées de nombreuses fois et croissent à chaque release : elles sont de bonnes candidates à l'automatisation. Une analyse d'impact est conseillée pour fixer l'étendue de la régression. Rien n'indique chez toi un lien avec les risques, une analyse d'impact ou une automatisation. | [CTAL-TM v3.0 FR, §1.3.4, pp. 32-33] ; [CTFL v4.0.1 EN, §2.2.3, pp. 30-31] |

## Ce qui manque

- **Suivi des risques pendant le projet**, avec mise à jour du registre et analyse des nouveaux risques [CTAL-TM v3.0 FR, §1.3.1, p. 29].
- **Implication de parties prenantes variées** dans l'identification des risques, avec une liste de participants convenue avec le chef de projet. La démarche ne dit pas qui participe [CTAL-TM v3.0 FR, §1.3.2, p. 30].
- **Évaluation explicite** (probabilité × impact, matrice de risque) [CTAL-TM v3.0 FR, §1.3.3, p. 31].
- **Atténuation des risques par les tests**. L'effort et la rigueur des tests sont proportionnels au niveau de risque : les risques élevés sont testés plus tôt et avec des techniques plus rigoureuses. La priorisation des tests s'appuie sur ces niveaux [CTAL-TM v3.0 FR, §1.3.4, pp. 32-33].
- **Rapport de livraison en risque résiduel** [CTAL-TM v3.0 FR, §1.3.4, p. 32].
- **Traçabilité vers les risques et les résultats de test**, au-delà du lien exigences → tests [CTFL v4.0.1 EN, §1.4.4, p. 21].
- **Analyse d'impact et réflexion sur l'automatisation de la régression** [CTFL v4.0.1 EN, §2.2.3, p. 31].
- **Politique et stratégie de test, planification, supervision et contrôle, environnement de test.** Ce sont les domaines du niveau 2 de la grille du dépôt. Tu n'en décris aucun.
- **Cadre réglementaire du dispositif médical.** Aucun syllabus de la bibliothèque ne le couvre (voir Limites).

## Niveau atteint : 1 — Initial · niveau visé : 2 (partiellement)

- **Pourquoi 1** : les trois pratiques sont des intentions. Aucune n'est en place, donc le niveau est plafonné à 1, comme le prévoit la grille du dépôt.
- **Pourquoi le niveau visé n'est pas plus haut** : le niveau 2 suppose une démarche rattachée à une stratégie écrite, planifiée, supervisée et contrôlée, avec l'environnement de test nécessaire (grille du dépôt, cohérente avec le TMMi niveau 2). Ton analyse de risques ponctuelle ne permet pas la supervision et le contrôle. Ce critère ne serait donc pas rempli même si tout était appliqué.
- **Pour passer au niveau 2** :
  1. Écrire la stratégie de test et la planifier.
  2. Rendre le registre de risques vivant : suivi, réévaluation à chaque jalon ou release.
  3. Lier risques, tests et résultats dans la matrice.
  4. Piloter l'étendue des tests système par le risque résiduel.
  5. Mettre en place l'environnement de test.
- Les niveaux 3 à 5 sont une adaptation du dépôt, pas une reprise du TMMi.

## Questions à choix

**Quel est le principal objectif de ce suivi ?**
1. Préparer un audit ou une certification réglementaire
2. Améliorer d'abord l'efficacité des tests, sans enjeu d'audit
3. Les deux

**Quelles suites veux-tu ?**
1. Une liste de contrôle RBT prête à l'emploi (au format JSON de `idee modele`)
2. Un approfondissement sur la traçabilité et la régression (lire CTAL-TM §1.3.6, CTAL-TA §2)
3. Une recherche plus large sur le cadre réglementaire des dispositifs médicaux (Thomas, Web)

## Confiance : 62/100

- **Ce qui la soutient** : j'ai lu CTAL-TM §1.3 jusqu'à §1.3.4 et le début de §1.3.5, ainsi que CTFL §1.4.4 et §2.2.3. Les sources sont récentes et la couverture lexicale est élevée sur le risque et la traçabilité.
- **Ce qui la limite** : les trois pratiques ne sont que des intentions, sans détail sur le contexte. Je n'ai pas lu de passage sur le test système en tant que niveau de test, donc P3 reste partiellement évalué. Je n'ai pas lu la suite de §1.3.5 ni §1.3.6.

## Limites

- Aucun syllabus de la bibliothèque ne couvre le cadre réglementaire d'un dispositif médical (par exemple IEC 62304 ou ISO 14971).
- Les exigences de ce cadre sur la traçabilité, la gestion des risques et les tests de release sont donc non vérifiables ici.
- Le syllabus signale seulement que certaines normes de sûreté, comme l'IEC 61508, prescrivent techniques et couverture selon le niveau d'intégrité. Le Test Manager doit s'assurer que ces normes sont respectées [CTAL-TM v3.0 FR, §1.3.4, p. 32].
- L'ISO/IEC/IEEE 29119 n'est pas dans la bibliothèque : toute conformité ISO est non vérifiable.
- Ton niveau réglementaire d'intégrité (classe de sécurité du logiciel) n'est pas connu. Il peut rendre insuffisant ce qui est « aligné » ISTQB.

## Où creuser ensuite

- à lire : CTAL-TM v3.0 FR §1.3.5 (techniques lourdes, adaptées aux systèmes critiques pour la sécurité) et §1.3.6 (métriques et difficultés du RBT).
- à lire : CTAL-TA v4.0 FR §2 (Analyste de test et risques produit).
- à lire : le syllabus sur le test système (niveaux de test) et CT-AcT 2019 FR §5.2.3 (traçabilité en test d'acceptation), pour affiner P3.

## Traçabilité

- **Date de l'avis** : 2026-10-25
- **Documents lus** :
  - `CTAL-TM-3.0-fr`, v3.0, publié le 2024-03-28. Sections lues : §1.3 à §1.3.5 (début), pp. 29-33.
  - `CTFL-4.0.1-en`, v4.0.1, publié le 2024-09-15. Sections lues : §1.4.4 (pp. 20-21) et §2.2.3 (pp. 30-31).
  - `referentiel/grille-maturite.md`, lue mais non citée comme source ISTQB.
- **Requêtes `chercher`** :
  - `"risk-based testing identification évaluation atténuation"`
  - `"traceability requirements test cases coverage"`
  - `"system testing manual regression release"`

**Avis indicatif d'alignement sur les syllabus ISTQB locaux ; ni attestation de conformité, ni évaluation ISTQB/TMMi/ISO.**

## Commandes exécutées

- `Read {"file_path": "/tmp/claude-0/-home-user/da9346e2-ce5e-5882-830a-19be129b35c4/scratchpad/wt-K178/referentiel/grille-matur`
- `python qa.py chercher "risk-based testing identification évaluation atténuation"; python qa.py chercher "traceability requirements test cases coverage"; python qa.py chercher "system testing manual re`
- `python qa.py section CTAL-TM-3.0-fr 1.3; python qa.py section CTFL-4.0.1-en 1.4.4; python qa.py section CTFL-4.0.1-en 2.2.3`
