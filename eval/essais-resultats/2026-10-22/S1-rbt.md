# S1-rbt — sylvie

**Question** : J'ai vu qu'on pouvait mettre en place une stratégie de test basée sur les risques. Je pense faire ceci : un atelier en début de release avec le PO pour lister les fonctionnalités risquées, on teste ces fonctionnalités en premier et plus en profondeur, et on ne fait que du smoke test sur le reste. Est-ce que je suis aligné ISTQB ? Quel est le niveau de maturité de ma démarche ?

**Tours** : 9 · **coût** : 0.171 $ · **confiance annoncée** : 82 · **citations** : 9/10 lues · **Web** : 0

## Réponse

Ta démarche va dans le bon sens, mais elle est incomplète. Elle couvre l'identification des risques et la priorisation. L'évaluation structurée, l'atténuation proportionnée au niveau de risque et le suivi ne sont pas décrits. Je la place au niveau 1 de maturité.

## Ta démarche, reformulée
- **P1** : un atelier en début de release avec le PO pour lister les fonctionnalités risquées.
- **P2** : tester ces fonctionnalités en premier.
- **P3** : les tester plus en profondeur.
- **P4** : ne faire que du smoke test sur le reste.

## Verdicts par pratique

| Pratique | Verdict | Ce que dit l'ISTQB | Source |
|---|---|---|---|
| P1 – Atelier avec le PO | **Partiellement conforme** | Les ateliers sur les risques sont une technique reconnue d'identification. Il faut impliquer « l'échantillon le plus large possible de parties prenantes », dont la liste est convenue avec le chef de projet. Ne pas tenir compte des parties prenantes clés est « très problématique ». Le PO seul ne suffit donc pas (dev, ops/support, sécurité, métier…). | CTAL-TM 3.0 fr, §1.3.2, p. 29-30 |
| P1 – « Lister » les fonctionnalités risquées | **Partiellement conforme** | Après l'identification vient l'évaluation. Elle catégorise les risques, estime la probabilité et l'impact de chacun, puis détermine le niveau de risque (matrice qualitative ou produit quantitatif). Une simple liste ne donne pas de niveau de risque. | CTAL-TM 3.0 fr, §1.3.3, p. 30-31 ; CTFL 4.0.1 en, §5.2.3, p. 52-53 |
| P2 – Tester les risques en premier | **Conforme** | La priorisation des tests s'appuie sur les niveaux de risque. À l'exécution, elle assure une couverture précoce des zones les plus critiques. L'approche « profondeur d'abord » convient quand il faut atténuer les risques les plus élevés au plus tôt. | CTAL-TM 3.0 fr, §1.3.4, p. 32-33 |
| P3 – Tester plus en profondeur | **Partiellement conforme** | Le principe est exact : effort et rigueur proportionnels au niveau de risque. Mais le syllabus attend des choix explicites : techniques et couverture, niveaux et types de test, testeurs les plus expérimentés, indépendance, étendue de la régression, revues. « Plus en profondeur » ne dit pas comment. | CTAL-TM 3.0 fr, §1.3.4, p. 32 ; CTFL 4.0.1 en, §5.2.4, p. 53 |
| P4 – Smoke test seul sur le reste | **Partiellement conforme** | Les risques plus faibles peuvent être testés plus tard avec des techniques moins rigoureuses. Mais « le reste » n'est pas évalué dans ta démarche. L'acceptation du risque est une réponse légitime, à condition d'être décidée sur la base d'une analyse. L'approche « largeur d'abord » donne au moins un test par risque. Je n'ai pas lu de passage qui définisse le smoke test, donc je ne juge pas sa pertinence. | CTAL-TM 3.0 fr, §1.3.4, p. 32-33 |

## Ce qui manque
- **Évaluation probabilité × impact**, avec une échelle ou une matrice, et un niveau de risque par élément de test (CTAL-TM §1.3.3 ; CTFL §5.2.3).
- **Découpage par élément de test**. Le risque n'est pas uniforme dans l'objet de test (CTAL-TM §1.3.2 et §1.3.4 ; CTAL-TA 4.0 fr §2.1.1, p. 27).
- **Parties prenantes élargies** et liste convenue avec le chef de projet (CTAL-TM §1.3.2).
- **Traduction du niveau de risque en actions de test** : techniques, couverture, types de test, testeurs, indépendance, régression (CTAL-TM §1.3.4 ; CTFL §5.2.3, qui liste aussi l'estimation de l'effort).
- **Suivi des risques** pendant la release : registre mis à jour, nouveaux risques, efficacité de l'atténuation (CTAL-TM §1.3.1 ; CTFL §5.2.4).
- **Rapport en termes de risque résiduel** et recommandation au management quand le temps manque : prolonger les tests ou accepter le risque (CTAL-TM §1.3.4, p. 33).
- **Analyse itérative**, pas une seule fois en début de release. Les parties prenantes et les risques évoluent (CTAL-TM §1.3.6, p. 34).
- **Rétrospective avec métriques de succès** : défauts critiques détectés tôt, tests ignorés de risque inférieur aux tests exécutés, incidents en production (CTAL-TM §1.3.6).

## Niveau de maturité : 1 — Initial
Selon la grille du dépôt, un niveau n'est atteint que si tous ses critères le sont. Tes pratiques décrivent une intention structurée avec un seul atelier. Elles n'ont ni évaluation, ni suivi, ni rôles explicites. Le niveau 2 (Géré) exige des risques évalués et traduits en priorité et profondeur de test, puis suivis pendant le projet. Tout critère non mentionné est « non démontré », pas « acquis ». Si tu as déjà certains de ces éléments, dis-le-moi et je réviserai.

**Pour passer au niveau 2** :
1. Évaluer chaque risque (probabilité × impact) avec un barème partagé.
2. Relier chaque niveau de risque à une profondeur de test précise.
3. Tenir un registre des risques, revu pendant la release.
4. Rapporter l'avancement en risque résiduel.

Ce niveau n'est pas une évaluation TMMi officielle, qui exige un évaluateur accrédité et des preuves de terrain.

## Confiance : 82/100
- **Ce qui la soutient** : j'ai lu les passages de trois syllabus récents (CTAL-TM 3.0, CTFL 4.0.1, CTAL-TA 4.0), et ils concordent.
- **Ce qui la limite** : ta description est courte, donc plusieurs éléments sont « non démontrés » plutôt que absents. La fin de CTFL §5.2.4 (p. 53-54) n'est lue que partiellement. Je n'ai lu aucune définition du smoke test.

**Limites** : l'ISO/IEC/IEEE 29119 n'est pas dans la bibliothèque, donc toute conformité ISO est non vérifiable ici. L'ISTQB n'est pas une norme : je parle d'alignement sur ses pratiques.

## Piste à capitaliser
Je te propose de conserver la liste de contrôle RBT (identification → évaluation → atténuation → suivi → rapport en risque résiduel → rétrospective), avec les sources ci-dessus. Je ne l'enregistre pas sans ton accord. Si tu veux comparer avec les pratiques hors ISTQB, comme le smoke test ou les workshops agiles, Thomas pourra faire une recherche plus large.

## Commandes exécutées

- `python qa.py chercher "risk-based testing identification évaluation atténuation" 2>&1 | head -60`
- `Read {"file_path": "/home/user/istqbfinder/referentiel/grille-maturite.md"}`
- `python qa.py inventaire 2>&1 | head -40`
- `for s in 1.3.1 1.3.2 1.3.3 1.3.4 1.3.5 1.3.6; do echo "=== TM-fr §$s"; python qa.py section CTAL-TM-3.0-fr $s 2>&1 | head -60; done`
- `python qa.py section CTFL-4.0.1-en 5.2 2>&1 | head -60; echo ======; python qa.py section CTAL-TA-4.0-fr 2.1 2>&1 | head -60`
- `python qa.py section CTFL-4.0.1-en 5.2.3 2>&1 | tail -25; echo; python qa.py section CTFL-4.0.1-en 5.2.4 2>&1 | head -30`
- `python qa.py section CTAL-TM-3.0-fr 1.3 2>&1 | head -120`
- `python qa.py section CTAL-TM-3.0-fr 1.3.4 2>&1 | head -70; python qa.py section CTAL-TM-3.0-fr 1.3.5 2>&1 | head -50; python qa.py section CTAL-TM-3.0-fr 1.3.6 2>&1 | head -60`
