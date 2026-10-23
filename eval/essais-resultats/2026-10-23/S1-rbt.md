# S1-rbt — sylvie

**Question** : J'ai vu qu'on pouvait mettre en place une stratégie de test basée sur les risques. Je pense faire ceci : un atelier en début de release avec le PO pour lister les fonctionnalités risquées, on teste ces fonctionnalités en premier et plus en profondeur, et on ne fait que du smoke test sur le reste. Est-ce que je suis aligné ISTQB ? Quel est le niveau de maturité de ma démarche ?

**Tours** : 10 · **coût** : 0.189 $ · **confiance annoncée** : 70 · **verdict** : réussi · **citations** : 10/10 lues · **Web** : 0

## Réponse

Avis indicatif d'alignement sur les syllabus ISTQB locaux ; ni attestation de conformité, ni évaluation ISTQB/TMMi/ISO.

Ton idée suit l'esprit du test basé sur les risques, mais elle reste partielle : il manque l'évaluation des risques, leur suivi et leur réévaluation. Comme rien n'est encore appliqué, le niveau est plafonné à 1.

## Pratiques décrites

| # | Pratique | Statut |
|---|---|---|
| P1 | Atelier en début de release avec le PO | intention |
| P2 | Lister les fonctionnalités risquées | intention |
| P3 | Tester ces fonctionnalités en premier et plus en profondeur | intention |
| P4 | Smoke test seulement sur le reste | intention |

| Pratique | Intention / en place | Verdict | Ce que dit l'ISTQB | Source |
|---|---|---|---|---|
| P1 Atelier avec le PO | intention | Partiellement aligné | Les ateliers sur les risques font partie des techniques d'identification. Il faut impliquer l'échantillon le plus large possible de parties prenantes, avec une liste convenue avec le chef de projet. Ne pas tenir compte des parties prenantes clés peut être « très problématique ». En agile, le testeur anime des sessions de « risk-storming » avec des représentants métier **et** des développeurs. Le PO seul est un cercle étroit. L'analyse n'est pas à faire « une seule fois au début du projet » : les parties prenantes et les risques changent. | [CTAL-TM v3.0 FR, §1.3.2, pp. 29-30] ; [CTAL-TM v3.0 FR, §1.3.6, p. 34] ; [CTAL-AT v2.0 EN, §3.1.1, pp. 24-25] |
| P2 Lister les fonctionnalités risquées | intention | Partiellement aligné | Après l'identification vient l'évaluation. Le niveau de risque combine probabilité et impact, avec une échelle ordinale et une matrice de risque. Les facteurs de probabilité et d'impact sont listés (criticité, fréquence d'usage, complexité, etc.). Une liste « risqué / pas risqué » ne donne pas de niveaux. | [CTAL-TM v3.0 FR, §1.3.3, pp. 30-31] |
| P3 Tester d'abord et plus en profondeur | intention | Aligné sur le principe | Plus le niveau de risque est élevé, plus les tests commencent tôt et plus l'effort est intense. Les tests à risque élevé utilisent des techniques plus rigoureuses. La priorisation guide la séquence d'exécution, y compris en « profondeur d'abord ». | [CTAL-TM v3.0 FR, §1.3, p. 29] ; [§1.3.4, pp. 32-33] |
| P4 Smoke test seulement sur le reste | intention | Partiellement aligné | Les risques faibles peuvent commencer plus tard avec des techniques moins rigoureuses, ce qui va dans ton sens. L'approche « largeur d'abord » prévoit au moins un test par risque. L'acceptation du risque est une réponse d'atténuation admise, à condition d'être explicite. En rétrospective, on vérifie que les tests ignorés avaient un risque inférieur à celui des tests exécutés. | [CTAL-TM v3.0 FR, §1.3.4, pp. 32-33] ; [§1.3.6, p. 34] |

Je n'ai lu aucun passage qui décrive « smoke test seulement sur les risques faibles » comme tactique du test basé sur les risques. Le smoke test lui-même n'est donc pas évalué comme technique.

## Ce qui manque

- **Évaluation probabilité × impact** de chaque risque, avec une échelle et des critères définis [CTAL-TM v3.0 FR, §1.3.3, pp. 30-31].
- **Parties prenantes élargies**, avec une liste complète convenue : développeurs, métier, exploitation, etc. [CTAL-TM v3.0 FR, §1.3.2, p. 30].
- **Traduction du niveau de risque** en choix de techniques, de profondeur et de niveaux ou types de test, par élément de test [CTAL-TM v3.0 FR, §1.3.4, p. 32].
- **Suivi des risques et registre des risques**, avec analyse des nouveaux risques et ajustement du registre [CTAL-TM v3.0 FR, §1.3.1, p. 29].
- **Réévaluation continue** pendant la release, pas seulement au début [CTAL-TM v3.0 FR, §1.3.6, p. 34].
- **Reporting en risque résiduel** et recommandation au management (prolonger les tests ou accepter le risque) si le temps manque [CTAL-TM v3.0 FR, §1.3.4, pp. 32-33].
- **Décision explicite** d'accepter, transférer ou atténuer les risques non testés en profondeur [CTAL-TM v3.0 FR, §1.3.4, p. 32].
- **Mesure du bénéfice** en rétrospective : parties prenantes impliquées, défauts critiques trouvés tôt, tests ignorés à risque inférieur [CTAL-TM v3.0 FR, §1.3.6, p. 34].
- **Inscription dans la stratégie de test de la release** : objectifs, niveaux, types et techniques de test pour atténuer les risques [CTAL-AT v2.0 EN, §3.1.1, p. 25].

## Niveau atteint : 1 — Initial · niveau visé : 2

- **Pourquoi 1 :** aucune pratique n'est en place, seulement des intentions. Selon la grille du dépôt, le niveau est alors plafonné à 1.
- **Pourquoi le niveau visé est 2 :** ta démarche décrit seulement l'identification et la priorisation. Il faudrait ajouter l'évaluation, la stratégie écrite, la supervision et l'environnement de test pour atteindre le niveau 2 (Discipliné).
- **Pour passer au niveau 2 :** applique l'atelier élargi sur une release. Évalue les risques (probabilité × impact) et consigne-les dans un registre. Traduis-les en priorité et en profondeur dans une stratégie ou un plan de test écrit. Suis les risques et les tests pendant la release.
- **Niveaux 3 à 5 :** ils relèvent d'une adaptation du dépôt (grille du dépôt) : standardisation, indicateurs, amélioration continue. Ils sont hors de portée à ce stade.

## Questions à choix

**Quel est ton contexte de livraison ?**
1. Agile, itérations courtes (Scrum ou équivalent)
2. Releases séquentielles ou en cascade
3. Contexte réglementé (santé, ferroviaire, banque…)

**Que veux-tu approfondir ?**
1. Une liste de contrôle RBT prête à l'emploi (atelier, matrice, registre)
2. Les différences entre « profondeur d'abord » et « largeur d'abord » pour ton cas
3. Une recherche plus large (Web) sur l'usage du smoke test dans une démarche RBT (par Thomas)

## Confiance : 70/100

- **Base :** la couverture lexicale de la recherche est de 84/100.
- **Lectures :** 12 passages ou sections lus, avec 2 syllabus courants concordants (CTAL-TM v3.0 et CTAL-AT v2.0).
- **Pénalité :** −10 parce que ma lecture de « smoke seulement » relève de mon raisonnement, pas d'un passage lu.

## Limites

- Je n'ai pas lu la version française du CTAL-AT : la citation est en anglais.
- Aucun syllabus de la bibliothèque ne couvre ton contexte métier ni un éventuel cadre réglementaire. Si ton produit en dépend, les pratiques liées sont non vérifiables ici.
- L'ISO/IEC/IEEE 29119 n'est pas dans la bibliothèque : toute conformité ISO est non vérifiable.
- Le niveau juge la démarche décrite, pas ton organisation.

## Traçabilité

- **Date de l'avis :** 2026-10-23.
- **Documents lus :**
  - `CTAL-TM-3.0-fr`, v3.0, publié le 2024-03-28 : §1.3 à §1.3.6, pp. 29-34 (lus en entier).
  - `CTAL-AT-2.0-en`, v2.0, publié le 2026-04-17 : §3.1.1, pp. 24-25.
- **Grille du dépôt :** `referentiel/grille-maturite.md` (lue).
- **Requêtes `chercher` :**
  - `"risk-based testing" identification évaluation atténuation`
  - `"test basé sur les risques niveau de risque probabilité impact"`
  - `"smoke test"` (extraits non cités)
  - `"analyse des risques produit PO product owner parties prenantes itération release"`
- **Score de confiance :** `confiance --base 84 --lus 12 --concordants 2 --raisonnement 1`.

Avis indicatif d'alignement sur les syllabus ISTQB locaux ; ni attestation de conformité, ni évaluation ISTQB/TMMi/ISO.

## Commandes exécutées

- `Read {"file_path": "/tmp/claude-0/-home-user/da9346e2-ce5e-5882-830a-19be129b35c4/scratchpad/final2/referentiel/grille-maturi`
- `python qa.py chercher "risk-based testing" identification évaluation atténuation`
- `python qa.py chercher "test basé sur les risques niveau de risque probabilité impact"`
- `python qa.py section CTAL-TM-3.0-fr 1.3 --max-caracteres 20000`
- `python qa.py chercher "smoke test"`
- `python qa.py chercher "analyse des risques produit PO product owner parties prenantes itération release"`
- `python qa.py section CTAL-AT-2.0-en 3.1.1 --max-caracteres 5000`
- `python qa.py confiance --help`
- `python qa.py confiance --base 84 --lus 12 --concordants 2 --raisonnement 1`
