# S1-rbt — sylvie

**Question** : J'ai vu qu'on pouvait mettre en place une stratégie de test basée sur les risques. Je pense faire ceci : un atelier en début de release avec le PO pour lister les fonctionnalités risquées, on teste ces fonctionnalités en premier et plus en profondeur, et on ne fait que du smoke test sur le reste. Est-ce que je suis aligné ISTQB ? Quel est le niveau de maturité de ma démarche ?

**Tours** : 6 · **coût** : 0.117 $ · **confiance annoncée** : 78 · **verdict** : réussi · **citations** : 6/6 lues · **Web** : 0

## Réponse

**Avis indicatif d'alignement sur les syllabus ISTQB locaux ; ni attestation de conformité, ni évaluation ISTQB/TMMi/ISO.**

Ta démarche suit l'esprit du test basé sur les risques (RBT), mais elle est incomplète. Trois étapes sont à compléter : les parties prenantes de l'atelier, l'évaluation du niveau de risque, et le suivi des risques pendant la release. Le « smoke test seulement » sur le reste ne correspond pas à ce que décrit le syllabus. Rien n'est encore en place, donc le niveau est plafonné à 1.

## Pratiques décrites

- **P1** : atelier de début de release avec le PO pour lister les fonctionnalités risquées (*intention*).
- **P2** : tester d'abord les fonctionnalités risquées (*intention*).
- **P3** : tester ces fonctionnalités plus en profondeur (*intention*).
- **P4** : ne faire que du smoke test sur le reste (*intention*).

## Verdict par pratique

| Pratique | Statut | Verdict | Ce que dit l'ISTQB | Source |
|---|---|---|---|---|
| P1 Atelier avec le PO | Intention | Partiellement aligné | Les « ateliers sur les risques » font partie des techniques d'identification. Il faut impliquer l'échantillon le plus large possible de parties prenantes, avec une liste complète et convenue avec le chef de projet. Une identification qui ignore des parties prenantes clés « peut s'avérer très problématique ». Le PO seul est probablement insuffisant (dev, ops, support, sécurité, etc.). Le syllabus demande aussi d'évaluer les risques, pas seulement de les lister. | [CTAL-TM v3.0 FR, §1.3.2, pp. 29-30] ; [§1.3.3, pp. 30-31] |
| P2 Tester d'abord le risqué | Intention | Aligné | Pour les risques élevés, les tests « doivent commencer tôt ». À l'exécution, la priorisation suit les niveaux de risque, ce qui assure une couverture précoce des zones critiques. Une exécution « profondeur d'abord » convient quand il faut atténuer les risques les plus élevés au plus vite. | [CTAL-TM v3.0 FR, §1.3, p. 29] ; [§1.3.4, pp. 32-33] |
| P3 Tests plus profonds | Intention | Partiellement aligné | Le temps et l'effort doivent être proportionnels au niveau de risque, avec des techniques plus rigoureuses pour les risques élevés. Le syllabus demande aussi d'analyser des facteurs contextuels : éléments du test, caractéristiques de qualité, niveaux et types de test, cycle de vie, équipe, exigences réglementaires. Ta démarche ne dit pas comment le niveau de risque est établi, ni comment il fixe la profondeur et les techniques. | [CTAL-TM v3.0 FR, §1.3.4, p. 32] |
| P4 Smoke test seul sur le reste | Intention | Partiellement aligné | Les risques plus faibles peuvent commencer plus tard et utiliser des techniques moins rigoureuses. Le niveau de risque doit aussi influencer l'étendue des tests de régression. L'approche « largeur d'abord » donne au moins un test à chaque risque. Tout le reste en smoke test n'est pas une approche que le syllabus décrit. Il faut décider explicitement, pour chaque risque, de tester moins, de contourner, de transférer ou d'accepter. | [CTAL-TM v3.0 FR, §1.3.4, pp. 32-33] |

Je n'ai pas lu de passage qui définisse le « smoke test ». Je ne me prononce donc pas sur le terme lui-même, seulement sur son usage comme seule couverture des risques faibles.

## Ce qui manque

- **Évaluation du niveau de risque.** Chaque risque est évalué par sa probabilité et son impact, qualitativement dans la plupart des cas, avec une matrice de risque. Les facteurs de probabilité et d'impact sont listés [CTAL-TM v3.0 FR, §1.3.3, pp. 30-31].
- **Suivi des risques pendant la release.** Le suivi des tests doit inclure celui des risques : nouveaux risques et ajustement du registre. L'analyse est « continue et itérative », à ne pas faire une seule fois en début de projet [CTAL-TM v3.0 FR, §1.3.1, p. 29 ; §1.3.6, p. 34].
- **Reporting en risque résiduel et décision de fin de test.** Si le temps s'épuise, le RBT permet de recommander au management de prolonger les tests ou d'accepter le risque restant. Cela suppose d'avoir tracé ce qui a été couvert et ce qui ne l'a pas été [CTAL-TM v3.0 FR, §1.3.4, pp. 32-33].
- **Mesure du bénéfice en rétrospective.** Par exemple : les parties prenantes étaient-elles représentées ? Les défauts prioritaires ont-ils été trouvés tôt ? Les tests ignorés avaient-ils un risque plus faible que les tests exécutés ? [CTAL-TM v3.0 FR, §1.3.6, p. 34]
- **Rattachement à une stratégie de test écrite.** C'est un critère du niveau 2 de la grille du dépôt, qui n'est pas dans le passage lu.

## Niveau atteint : 1 — Initial · niveau visé : 2 — Discipliné

- **Pourquoi 1 :** toutes les pratiques sont des intentions. Seules les pratiques en place comptent (grille du dépôt).
- **Pourquoi pas 2 même une fois appliquée :** le niveau 2 de la grille suppose une stratégie écrite, des risques identifiés avec les parties prenantes, évalués en probabilité et impact, et traduits en priorité et profondeur. Il suppose aussi un suivi des risques pendant le projet. Aujourd'hui, seule l'identification est esquissée, et incomplète.
- **Pour passer au niveau 2 :**
  1. Élargir l'atelier.
  2. Évaluer les risques avec une matrice, et conserver un registre des risques.
  3. Relier chaque niveau de risque à une profondeur et des techniques de test.
  4. Revoir le registre pendant la release.
  5. Rapporter le risque résiduel.
  6. Écrire la stratégie.
- Les niveaux 3 à 5 sont une adaptation du dépôt : standardisation, indicateurs, amélioration continue. Ils ne sont pas démontrés ici.

## Questions à choix

1. Dans quel contexte appliques-tu cette démarche ?
   - a) Agile itératif, avec des releases régulières.
   - b) Cycle séquentiel.
   - c) Domaine réglementé (santé, ferroviaire, finance, etc.).

   Je n'ai pas lu les syllabus agiles pour cet avis. Pour un domaine réglementé, aucun syllabus de la bibliothèque ne couvre la réglementation.
2. Quelle suite veux-tu ?
   - a) Une liste de contrôle RBT prête à l'emploi (JSON).
   - b) Un modèle de matrice de risque et de registre.
   - c) Une recherche plus large avec Thomas, par exemple sur la place des smoke tests et de la régression en agile.

## Confiance : 78/100

- J'ai lu §1.3 à §1.3.4 et §1.3.6 de CTAL-TM v3.0 FR, un syllabus courant et explicite sur le sujet.
- La description de ta démarche est courte, et je n'ai pas lu §1.3.5 (techniques RBT).
- Je n'ai pas lu les syllabus CTFL ni CTAL-AT. Le contexte agile n'est donc pas vérifié.

## Limites

- Aucun syllabus de la bibliothèque ne couvre le cadre réglementaire éventuel de ton produit. Les pratiques qui en dépendent sont « Non vérifiable ».
- L'ISO/IEC/IEEE 29119 n'est pas dans la bibliothèque, donc toute conformité ISO est non vérifiable.
- Ce n'est pas une évaluation TMMi.

## Traçabilité

- **Date de l'avis :** 2026-10-22.
- **Document lu :** `CTAL-TM-3.0-fr`, ISTQB Advanced Level Test Management, v3.0, publié le 2024-03-28.
- **Sections et pages lues :**
  - §1.3 (introduction), p. 29
  - §1.3.1, p. 29
  - §1.3.2, pp. 29-30
  - §1.3.3, pp. 30-31 (sortie tronquée juste après le passage sur la matrice de risque)
  - §1.3.4, pp. 32-33
  - §1.3.6, p. 34
- **Grille :** `referentiel/grille-maturite.md`. Je ne cite aucune page de ses références.
- **Requêtes `chercher` :**
  1. `"risk-based testing identification évaluation atténuation"`
  2. `"risk-based testing" CTFL`
  3. `"test basé sur les risques smoke test régression agile release"`

  Je n'ai pas cité les passages vus uniquement en extrait.

**Avis indicatif d'alignement sur les syllabus ISTQB locaux ; ni attestation de conformité, ni évaluation ISTQB/TMMi/ISO.**

## Commandes exécutées

- `Read {"file_path": "/tmp/claude-0/-home-user/da9346e2-ce5e-5882-830a-19be129b35c4/scratchpad/wt-G/referentiel/grille-maturite`
- `python qa.py chercher "risk-based testing identification évaluation atténuation" 2>&1 | head -80`
- `python qa.py section CTAL-TM-3.0-fr 1.3 --max-caracteres 9000 2>&1`
- `python qa.py chercher "risk-based testing" CTFL 2>&1 | head -30; python qa.py chercher "test basé sur les risques smoke test régression agile release" 2>&1 | head -40`
- `python qa.py section CTAL-TM-3.0-fr 1.3.4 2>&1; python qa.py section CTAL-TM-3.0-fr 1.3.6 2>&1`
