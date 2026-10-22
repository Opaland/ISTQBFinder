# Sorties CLI des exemples — 2026-10-22

Généré par `python scripts/rejouer_exemples.py` dans une racine temporaire (QAK_RACINE) : sortie brute, non retouchée. Référencé par `docs/exemples-conversations.md` (§3 à §5).

## §3 — préparer la capitalisation

```text
$ python qa.py section CTAL-TM-3.0-fr 1.3.3

── CTAL-TM-3.0-fr · ISTQB Advanced Level Test Management · v3.0 (2024-03-28) · p. 30 · §1.3.3 Évaluation des risques qualité (passage #4565)
1.3.3 Évaluation des risques qualité
Une fois les risques identifiés, ils peuvent être évalués. Cette évaluation des risques qualité comprend la
catégorisation des risques par type (risque produit ou risque projet) et par caractéristiques de qualité
impactées.
La détermination du niveau de risque implique généralement une évaluation, pour chaque élément de
risque, de la probabilité du risque et de l'impact du risque en cas de survenance. Les facteurs qui
influencent la probabilité du risque qualité sont les suivants :
• Complexité de la technologie, des outils ou de l'architecture du système
• Maturité de l'organisation

── CTAL-TM-3.0-fr · ISTQB Advanced Level Test Management · v3.0 (2024-03-28) · p. 31 · §1.3.3 Évaluation des risques qualité (passage #4566)
• Problèmes de personnel liés aux compétences, à la disponibilité, à la motivation ou au travail
autonome, y compris la connaissance du SDLC utilisé
• Conflit au sein de l'équipe
• Problèmes contractuels avec les fournisseurs
• Equipes géographiquement dispersées
• Faiblesse du leadership managérial ou technique
• Pression liée au temps, aux ressources, au budget et au management
• Absence d'activités d'assurance qualité à un stade précoce
• Taux élevés de changement de la base de test, du produit ou du personnel
Les facteurs influençant l'impact du risque sont les suivants :
• Fréquence d'utilisation de la fonctionnalité affectée
• Criticité de la fonctionnalité affectée
• Criticité de l'objectif métier concerné
• Atteinte à la réputation
• Perte de revenus pour le métier
• Pertes financières, écologiques ou sociales potentielles, ou responsabilité (juridique)
• Sanctions civiles ou pénales
• Problèmes d'interface et d'intégrité
• Absence de solutions de rechange raisonnables
• Besoins en matière de sûreté
Le Test Manager combine la probabilité du risque et l'impact du risque pour déterminer le niveau de
risque.
Si l'analyse des risques est basée sur des données étendues et statistiquement valables, une évaluation
quantitative est appropriée. Par exemple, la probabilité du risque peut être exprimée en pourcentage et
l'impact du risque en montant. Dans ce cas, le niveau de risque peut être calculé comme le produit de
ces deux facteurs. En général, cependant, la probabilité du risque et l'impact du risque ne peuvent être
déterminés que qualitativement sur des échelles ordinales, par exemple très élevé, élevé, moyen, faible
ou très faible. Les valeurs de probabilité du risque et d'impact du risque sont ensuite combinées dans une
matrice de risque pour créer un niveau de risque global. Ce niveau de risque global doit être interprété
comme une évaluation qualitative et relative sur une échelle ordinale.
À moins que l'analyse des risques ne soit basée sur des données exhaustives et statistiquement
valables, l'analyse des risques sera qualitative, basée sur les perceptions subjectives des parties
prenantes de la probabilité du risque et de son impact.
[code retour 0]
```

```text
$ python qa.py theme proposer "prioriser les tests selon probabilité et impact des risques"
  rbt                        Test management › Risk-Based Testing  (score 0.447)
  priorisation               Test management › Priorisation des tests  (score 0.365)
  mbt                        Analyse et conception des tests › Test basé sur les modèles  (score 0.224)
[code retour 0]
```

```text
$ python qa.py idee doublons --titre "Matrice probabilité × impact pour prioriser les tests" --resume "Évaluer chaque risque qualité selon sa probabilité et son impact, puis en dériver l'effort et l'ordre de test." --theme rbt
Aucune idée similaire.
Thèmes suggérés : priorisation, rbt, test-de-ia
[code retour 0]
```

```text
$ python qa.py idee ajouter
(entrée standard : {"titre": "Matrice probabilité × impact pour prioriser les tests", "resume": "Évaluer chaque risque qualité selon sa probabilité et son impact, puis en dériver l'effort et l'ordre de test.", "probleme": "Effort de test réparti uniformément alors que les risques produit sont inégaux.", "principe": "Lister les risques qualité, noter probabilité et impact, calculer le niveau de risque, allouer profondeur et ordre de test.", "theme_principal": "rbt", "themes_secondaires": ["priorisation"], "maturite": "documentee", "provenance": "Exemple rejoué par scripts/rejouer_exemples.py", "references": [{"type": "istqb", "doc_id": "CTAL-TM-3.0-fr", "pages": "30", "section": "1.3.3", "extrait": "pour chaque élément de risque, de la probabilité du risque et de l'impact du risque"}]})
Idée créée : QA-20261022-484e
[code retour 0]
```

## §3 — ce que l'outil refuse

### Référence vers une page inexistante

```text
$ python qa.py idee ajouter
(entrée standard : {"titre": "Variante page 300", "resume": "Évaluer chaque risque qualité selon sa probabilité et son impact, puis en dériver l'effort et l'ordre de test.", "probleme": "Effort de test réparti uniformément alors que les risques produit sont inégaux.", "principe": "Lister les risques qualité, noter probabilité et impact, calculer le niveau de risque, allouer profondeur et ordre de test.", "theme_principal": "rbt", "themes_secondaires": ["priorisation"], "maturite": "documentee", "provenance": "Exemple rejoué par scripts/rejouer_exemples.py", "references": [{"type": "istqb", "doc_id": "CTAL-TM-3.0-fr", "pages": "300", "section": "1.3.3", "extrait": "pour chaque élément de risque, de la probabilité du risque et de l'impact du risque"}]})
Erreur : Page 300 inexistante dans CTAL-TM-3.0-fr (95 pages).
[code retour 2]
```

### Extrait reformulé

```text
$ python qa.py idee ajouter
(entrée standard : {"titre": "Variante extrait reformulé", "resume": "Évaluer chaque risque qualité selon sa probabilité et son impact, puis en dériver l'effort et l'ordre de test.", "probleme": "Effort de test réparti uniformément alors que les risques produit sont inégaux.", "principe": "Lister les risques qualité, noter probabilité et impact, calculer le niveau de risque, allouer profondeur et ordre de test.", "theme_principal": "rbt", "themes_secondaires": ["priorisation"], "maturite": "documentee", "provenance": "Exemple rejoué par scripts/rejouer_exemples.py", "references": [{"type": "istqb", "doc_id": "CTAL-TM-3.0-fr", "pages": "30", "section": "1.3.3", "extrait": "pour chaque élément de risque, de l'impact du risque en cas de survenance et de la probabilité du risque"}]})
Erreur : L'extrait cité n'apparaît pas mot pour mot aux pages 30 de CTAL-TM-3.0-fr : recopier une suite continue du passage lu (`lire` / `page`), sans reformuler ni couper au milieu.
[code retour 2]
```

### Même idée reformulée

```text
$ python qa.py idee ajouter
(entrée standard : {"titre": "Matrice impact × probabilité pour prioriser les tests", "resume": "Évaluer chaque risque qualité selon sa probabilité et son impact, puis en dériver l'effort et l'ordre de test.", "probleme": "Effort de test réparti uniformément alors que les risques produit sont inégaux.", "principe": "Lister les risques qualité, noter probabilité et impact, calculer le niveau de risque, allouer profondeur et ordre de test.", "theme_principal": "rbt", "themes_secondaires": ["priorisation"], "maturite": "documentee", "provenance": "Exemple rejoué par scripts/rejouer_exemples.py", "references": [{"type": "istqb", "doc_id": "CTAL-TM-3.0-fr", "pages": "30", "section": "1.3.3", "extrait": "pour chaque élément de risque, de la probabilité du risque et de l'impact du risque"}]})
REFUSÉ — Doublon probable : compléter l'idée existante (`idee modifier`) ou la lier (`idee lier`) plutôt que d'en créer une nouvelle.
  DOUBLON PROBABLE QA-20261022-484e « Matrice probabilité × impact pour prioriser les tests » (similarité 1.0, a_explorer)
[code retour 2]
```

### Statut validée sans motif

```text
$ python qa.py idee statut QA-20261022-484e validee
Erreur : Le statut « validee » exige un motif d'au moins 10 caractères (--motif) : sur quoi repose la décision ?
[code retour 2]
```

### Expérimentée sans retour d'expérience

```text
$ python qa.py idee statut QA-20261022-484e experimentee --motif "appliquée sur une release"
Erreur : « expérimentée » exige au moins un retour d'expérience (`idee retour`).
[code retour 2]
```

## §4 — retrouver et faire évoluer

```text
$ python qa.py idee chercher probabilité impact
QA-20261022-484e  [a_explorer/documentee] Matrice probabilité × impact pour prioriser les tests (rbt)
        Évaluer chaque risque qualité selon sa «probabilité» et son «impact», puis en dériver l'effort et l'ordre de test …
[code retour 0]
```

```text
$ python qa.py idee lister --theme rbt
QA-20261022-484e  rbt                    a_explorer   documentee Matrice probabilité × impact pour prioriser les tests
[code retour 0]
```

```text
$ python qa.py idee retour QA-20261022-484e --contexte "Release web, équipe produit de 6 personnes" --resultat "2 défauts critiques trouvés avant la recette" --enseignement "atelier d'1 h suffisant"
QA-20261022-484e : retour d'expérience enregistré (1 au total)
[code retour 0]
```

```text
$ python qa.py idee statut QA-20261022-484e experimentee --motif "appliquée sur une release"
QA-20261022-484e : a_explorer → experimentee
[code retour 0]
```

## §5 — couverture

```text
$ python qa.py couverture
thème                                    idées passages  état
Stratégie et gouvernance QA                  0      624  vide
Test management                              0      781  vide
  Risk-Based Testing                         1      373  pauvre
  Estimation et planification                0     1099  vide
  Métriques et reporting                     0     1164  vide
  Gestion des anomalies                      0      384  vide
  Priorisation des tests                     1       82  pauvre
Analyse et conception des tests              0     1118  vide
  Techniques boîte noire                     0      272  vide
  Techniques boîte blanche et couvertu       0      150  vide
  Techniques basées sur l'expérience         0      222  vide
  Tests exploratoires                        0      332  vide
  Test basé sur les modèles                  0      280  vide
  Couverture des tests                       0      461  vide
Tests statiques et revues                    0      702  vide
Exigences et critères d'acceptation          0     1901  vide
Tests fonctionnels                           0      225  vide
Niveaux et types de test                     0     1006  vide
Tests non fonctionnels                       0      794  vide
  Tests de performance                       0      449  vide
  Tests de sécurité                          0      465  vide
  Utilisabilité et accessibilité             0      718  vide
Automatisation des tests                     0     1019  vide
  Stratégie et ROI de l'automatisation       0      110  vide
  Maintenabilité des tests automatisés       0      180  vide
  Test d'API et de services                  0      158  vide
CI/CD et qualité des pipelines               0      583  vide
Shift-left et shift-right                    0       83  vide
  Shift-left                                 0      207  vide
  Shift-right et test en production          0      501  vide
Maturité et amélioration continue            0      517  vide
  TMMi et référentiels qualité               0      494  vide
IA et ingénierie des tests                   0      231  vide
  Tester des systèmes d'IA                   0      366  vide
  L'IA au service du test                    0      111  vide
Qualité logicielle réglementée               0      301  vide
Domaines métier spécifiques                  0      617  vide
Outils, méthodes et organisation des é       0     1748  vide
  Test en contexte agile et à l'échell       0     1132  vide
  Compétences et animation d'équipe          0      590  vide
Environnements et données de test            0      602  vide

Thèmes pauvres en idées mais documentés dans les syllabus (pistes d'exploration) : exigences (1901 passages), organisation (1748 passages), metriques (1164 passages), agile (1132 passages), conception (1118 passages)
[code retour 0]
```
