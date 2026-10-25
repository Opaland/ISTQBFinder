# M7-shift-left — thomas

**Question** : Je veux mettre en place une démarche shift left testing, comment faire ? Qu'est-ce que cela impose ?

**Tours** : 8 · **coût** : 0.162 $ · **confiance annoncée** : 90 · **verdict** : réussi · **citations** : 9/9 lues · **Web** : 0 · **critères** : 7/7

## Réponse

**Sources retenues**
- Syllabus lus : CTFL v4.0.1 EN (§2.1.4, 2.1.5, 3.1.2), CTAL-AT v2.0 EN (§4, 4.2), CT-TAS v1.0 EN (§3.1.3), CT-QDO v1.0 EN (§2.1.3).
- Les traductions FR de CT-TAS existent, mais je n'ai cité que les passages EN lus.
- Base d'idées : aucune idée capitalisée sur le sujet.
- Web : non utilisé. Aucun outil ni actualité n'était nommé.

Les syllabus décrivent le shift left comme un déplacement des activités de test vers le début du cycle de vie. Ce n'est pas un projet d'outillage, c'est un changement de pratiques et d'adhésion. Le meilleur socle est CTFL §2.1.5. CTAL-AT §4 détaille le côté exigences. CT-TAS et CT-QDO détaillent le côté automatisation et pipeline.

Hypothèse de contexte : équipe agile ou DevOps livrant une application web, sans contrainte réglementaire forte. Je n'ai ni la taille de l'équipe ni l'outillage.

## Méthode pas à pas

1. **Obtenir l'adhésion des parties prenantes d'abord**
   - Qui : QA Lead, sponsors, développeurs, PO. Quand : avant tout changement. Livrable : accord sur l'objectif et le budget.
   - L'ISTQB précise que le shift left « might result in extra training, effort and/or costs earlier » et que les parties prenantes doivent y adhérer [CTFL v4.0.1 EN, §2.1.5, p. 27].
2. **Cadrer le périmètre**
   - Qui : QA Lead. Livrable : état des lieux de ce qui est testé et à quel moment.
   - Le shift left ne dit pas de négliger les tests tardifs [CTFL v4.0.1 EN, §2.1.5, p. 27].
   - Pour l'automatisation, CT-TAS propose d'identifier la distribution actuelle, de choisir la distribution cible, puis de planifier une feuille de route [CT-TAS v1.0 EN, §3.1.3, p. 24].
3. **Améliorer la base de test (exigences et stories)**
   - Qui : testeurs, PO, développeurs, en affinage du backlog. Livrables : critères d'acceptation, user stories testables.
   - Revoir les spécifications avec un regard de testeur (ambiguïtés, incomplétudes, incohérences) [CTFL v4.0.1 EN, §2.1.5, p. 27].
   - CTAL-AT §4.1 liste les pratiques : example mapping, storyboarding et testboarding, user story slicing, et prise en compte des biais cognitifs [CTAL-AT v2.0 EN, §4, p. 31].
   - Les activités d'ingénierie des exigences (élicitation, analyse, spécification, validation) soutiennent toutes le shift left [CTAL-AT v2.0 EN, §4.2, p. 36].
4. **Développer le test statique**
   - Qui : toute l'équipe. Livrables : revues systématiques, analyse statique dans la chaîne.
   - Le test statique détecte des défauts dès les premières phases. Il est recommandé d'y impliquer des parties prenantes variées [CTFL v4.0.1 EN, §3.1.2, p. 33].
   - L'analyse statique du code se fait avant les tests dynamiques, ou en processus automatisé [CTFL v4.0.1 EN, §2.1.5, p. 27].
5. **Tester avant ou pendant le code, et automatiser en bas de la pyramide**
   - Qui : développeurs et testeurs. Livrables : tests de composants, pipeline CI/CD.
   - Écrire les cas de test avant le code, utiliser la CI (idéalement la CD) avec des tests de composants automatisés [CTFL v4.0.1 EN, §2.1.5, p. 27].
   - En cas de déséquilibre, aller du bas vers le haut. Une faible couverture de code signale un manque de tests de composants. TDD et ateliers sur les techniques de test améliorent leur qualité [CT-TAS v1.0 EN, §3.1.3, p. 24].
   - Les tests de composants avec doubles de test (mocks, stubs) et les tests de contrat donnent un retour plus tôt que des tests UI ou API lents et instables [CT-TAS v1.0 EN, §3.1.3, p. 25].
6. **Tester les caractéristiques non fonctionnelles dès le niveau composant**
   - Qui : développeurs, spécialistes performance et sécurité. Ces tests sont d'habitude tardifs, car ils attendent un système complet et un environnement représentatif [CTFL v4.0.1 EN, §2.1.5, p. 27].
7. **Installer le test continu et la responsabilité partagée**
   - Principes : tester tôt et souvent, collaboration pluridisciplinaire (« quality is everyone's responsibility »), automatisation, adaptation continue [CT-QDO v1.0 EN, §2.1.3, p. 24].
   - Boucler par des rétrospectives : les améliorations recommandées doivent être suivies [CTFL v4.0.1 EN, §2.1.6, p. 28].
   - Le shift right complète le dispositif : monitoring, retours des utilisateurs, canary releases [CT-TAS v1.0 EN, §3.1.3, p. 25].

**Ce que ça impose** (synthèse des étapes ci-dessus)
- **Adhésion** : un budget et une formation avancés, pour des gains attendus plus tard (étape 1).
- **Collaboration** : les testeurs entrent dans les discussions d'exigences, et les développeurs portent des tests (étapes 3, 5, 7).
- **Compétences** : techniques de test, TDD, outillage CI/CD (étape 5).
- **Infrastructure** : un pipeline et des environnements stables. CTFL §2.1.4 note que la CI/CD facilite des environnements de test stables, mais aussi que le pipeline doit être défini et établi, et que l'automatisation demande des ressources [CTFL v4.0.1 EN, §2.1.4, p. 27].
- **Maintien du test manuel et tardif** : l'exploratoire et l'utilisabilité restent nécessaires, même en DevOps [CT-QDO v1.0 EN, §2.1.2, p. 24].
- **Outils d'IA** : CTAL-AT les mentionne pour détecter les ambiguïtés et suggérer des scénarios. Il demande de les évaluer de façon critique et de ne pas remplacer l'analyse collaborative [CTAL-AT v2.0 EN, §4, p. 32].

## Exemple de mise en œuvre (fictif, interprétation)
« Dans une équipe Scrum de 6 personnes qui livre une appli web toutes les 2 semaines, je ferais ceci :
- Sprint 0 : état des lieux et accord du PO et du management (étapes 1-2).
- Affinage : un example mapping de 25 minutes par story à risque (étape 3).
- Chaque merge request : analyse statique et tests de composants dans le pipeline (étapes 4-5).
- Rétrospective : 2 indicateurs suivis, par exemple la part des défauts trouvés avant le développement et le taux de retours en production (étape 7). »

## Adaptation par domaine

| Domaine | Ce qui change | Où lire |
|---|---|---|
| Santé / réglementé | Traçabilité et revues formelles renforcées. Pas de syllabus dispositif médical (IEC 62304 absent). | CTAL-TTA v4.0 §2.8.2, CTAL-AT v2.0 §3.1.2 (non lus ici) |
| Web | Cas de référence des passages lus : CI/CD, tests de composants, contrats. Pas de syllabus web dédié. | CT-TAS §3.1.3, CT-QDO |
| Embarqué | Le matériel retarde les tests, donc simulation et HiL. Surtout couvert par l'automobile. | CT-AuT v2.1.1 (non lu) |
| Mobile | Tests précoces sur émulateurs, puis appareils réels. | CT-MAT 2019 (non lu) |
| API | Tests de contrat et doubles de test, call graph des API. | [CT-TAS v1.0 EN, §3.1.3, p. 25] |

Les lignes « non lu » sont des repères d'après l'index, pas des citations. Je les ai notées sans les avoir ouvertes.

**Par quoi je commencerais**
1. Revue des stories et example mapping (impact fort, effort faible).
2. Analyse statique et tests de composants dans la CI (impact fort, effort moyen).
3. Tests non fonctionnels précoces (impact moyen, effort fort).

**Où creuser ensuite**
- `section CTAL-AT-2.0-en 4.1.3` (example mapping) et `4.1.5` (user story slicing)
- `section CT-TAS-1.0-en 3.1` (distribution de l'automatisation)
- `section CT-QDO-1.0-en 2.1`
- `section CTFL-4.0.1-en 3.2` (processus de revue)

**Confiance : 90/100** (élevée). Calcul : base 100 × 0,6 = 60 ; 6 passages lus +20 ; 3 syllabus concordants +20 ; raisonnement sans source −10. Les étapes d'ordonnancement, l'exemple et les limites par domaine sont de l'interprétation.

## Questions à choix

**Quel est ton cycle de vie ?**
1. Agile / Scrum
2. DevOps / livraison continue
3. Séquentiel (V-model)

**Sur quoi veux-tu que j'approfondisse ?**
1. Exigences : example mapping, user story slicing (CTAL-AT §4.1)
2. Automatisation et pipeline : pyramide, tests de contrat (CT-TAS, CT-QDO)
3. Indicateurs de validation et business case (hors syllabus lus, je chercherais)

**Veux-tu capitaliser ?**
1. Oui, enregistrer l'idée proposée ci-dessous
2. Non, pas maintenant

## À capitaliser ?

Vérification des doublons : aucune idée similaire.

```json
{
 "titre": "Mise en place du shift left : adhésion, base de test, statique, automatisation basse",
 "resume": "Déplacer les activités de test vers le début du cycle de vie : revue des spécifications, tests avant le code, CI/CD, analyse statique, non-fonctionnel dès le niveau composant, avec adhésion des parties prenantes.",
 "probleme": "Défauts détectés tard, coût de reprise élevé, retours lents.",
 "principe": "Obtenir l'adhésion, améliorer la base de test, développer le test statique, automatiser les tests de composants et de contrat, avancer le non-fonctionnel, puis boucler par rétrospective. Ne pas négliger les tests tardifs.",
 "theme_principal": "shift-left",
 "themes_secondaires": ["statique"],
 "domaine_application": "Équipes agiles ou DevOps ; transposable à d'autres cycles de vie.",
 "prerequis": "Adhésion des parties prenantes, pipeline CI/CD défini, compétences en test chez les développeurs.",
 "benefices": "Moins de reprises et de défauts en aval, retours plus rapides.",
 "limites": "Coûts et formation en amont ; le test manuel et tardif reste nécessaire.",
 "maturite": "documentee",
 "statut": "a_evaluer",
 "provenance": "Recherche du 2026-10-25 : « mise en place d'une démarche shift left testing »",
 "references": [
  {"type": "istqb", "doc_id": "CTFL-4.0.1-en", "pages": "27", "section": "2.1.5", "extrait": "Shift left might result in extra training, effort and/or costs earlier in the process"},
  {"type": "istqb", "doc_id": "CT-TAS-1.0-en", "pages": "25", "section": "3.1.3", "extrait": "contract testing has been increasingly prominent"},
  {"type": "istqb", "doc_id": "CTAL-AT-2.0-en", "pages": "36", "section": "4.2", "extrait": "Shift left moves quality activities earlier in the software development lifecycle"}
 ]
}
```

## Commandes exécutées

- `Read {"file_path": "/tmp/claude-0/-home-user/da9346e2-ce5e-5882-830a-19be129b35c4/scratchpad/wt-K178/.claude/skills/qa-knowle`
- `python qa.py idee chercher shift left testing; python qa.py chercher shift left; python qa.py chercher "shift-left early testing static testing"; python qa.py chercher "tester tôt dès le début du cycl`
- `python qa.py lire 4784 --contexte 1 --max-caracteres 4000; python qa.py section CTAL-AT-2.0-en 4.2 --max-caracteres 7000`
- `python qa.py lire 3621 --contexte 1 --max-caracteres 4500; python qa.py lire 972 --contexte 1 --max-caracteres 4500`
- `python qa.py section CTAL-AT-2.0-en 4 --max-caracteres 3500; python qa.py lire 4798 --contexte 0 --max-caracteres 3000; python qa.py idee doublons --titre "Mise en place du shift left" --resume "Démar`
- `python qa.py confiance --base 100 --lus 5 --syllabus-concordants 3 2>&1 | tail -5; python qa.py confiance --help | head -20; python qa.py idee modele | head -30`
- `python qa.py confiance --base 100 --lus 6 --concordants 3 --raisonnement 1`
