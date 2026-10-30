# M2-sante — thomas

**Question** : Je suis Test Manager sur le logiciel d'un dispositif médical. Comment mettre en place la traçabilité des exigences vers les tests et un test basé sur les risques ?

**Tours** : 11 · **coût** : 0.319 $ · **confiance annoncée** : 63 · **verdict** : réussi · **citations** : 10/10 lues · **Web** : 1 · **critères** : 8/8 · **fidélité** (juge LLM, indicatif) : 0.73 sur 6 lignes citées, 0 contradiction(s)

## Réponse

**Sources retenues**
- Base d'idées : rien de capitalisé sur le sujet (deux requêtes `idee chercher`).
- CTFL v4.0.1 EN §1.4.4, CTAL-TM v3.0 EN §1.3 à §1.3.5, CTAL-TA v4.0 EN §2.1, CTAL-TTA v4.0 EN §2.8.2, CTEL-TM 2011 EN §8.3.4 (ancien) et CT-AuT v2.1.1 EN §2.1.2.6 (analogie automobile) ont été lus.
- Il n'y a **aucun syllabus dispositif médical** dans la bibliothèque. IEC 62304 et ISO 14971 ne sont connues que par une recherche Web. Cette recherche n'a rendu que des résumés d'éditeurs d'outils, pas les normes.
- Je n'ai pas lu CTAL-TM §1.3.6 (métriques de succès et difficultés du RBT) ni la suite de §1.3.4 (p. 31).

Les syllabus donnent la méthode générique : tracer, évaluer le risque, puis proportionner l'effort de test au niveau de risque. La partie réglementaire (classes de sécurité logicielle, preuves attendues) n'est pas dans la bibliothèque.

Hypothèse de contexte : logiciel (SaMD ou embarqué) soumis à IEC 62304 et ISO 14971, cycle plutôt séquentiel ou hybride, audits réglementaires à prévoir.

## Méthode pas à pas

1. **Définir le modèle de traçabilité.** Les éléments à relier sont la base de test, les conditions de test, les risques, les cas de test, les résultats et les anomalies [CTFL v4.0.1 EN, §1.4.4, p. 20]. Livrable : un schéma de la chaîne, par exemple besoin utilisateur → exigence → risque/mesure de maîtrise → cas de test → résultat → anomalie. Le schéma serait à valider par qualité et réglementaire. La notion de traçabilité bidirectionnelle (verticale vers le code, horizontale vers les tests) est détaillée dans le syllabus automobile [CT-AuT v2.1.1 EN, §2.1.2.6, p. 23].
2. **Justifier l'effort par l'usage.** La traçabilité sert à évaluer la couverture, à mesurer l'impact des changements, à faciliter les audits et à renseigner les rapports [CTFL v4.0.1 EN, §1.4.4, p. 21]. En contexte réglementé, le Test Manager y consacre un temps significatif : matrices de traçabilité, documents versionnés, modifications vérifiées et signées [CTEL-TM 2011 EN, §8.3.4, p. 66]. Ce syllabus date de 2011, à lire avec prudence.
3. **Faire l'analyse de risque avec les bons acteurs.** L'analyse comprend l'identification puis l'évaluation, avec des parties prenantes variées. Le Test Manager la modère [CTAL-TM v3.0 EN, §1.3.1, p. 28 ; §1.3.2, p. 28-29]. Livrable : un registre des risques. En dispositif médical, il est en pratique alimenté par l'analyse ISO 14971 (interprétation).
4. **Évaluer le niveau de risque.** On combine probabilité et impact, avec une matrice ordinale si les données ne sont pas statistiques. Parmi les facteurs d'impact figurent la criticité, les sanctions légales et les besoins de sécurité [CTAL-TM v3.0 EN, §1.3.3, p. 30]. L'AT affine par élément testé (composant, interface, fonction) [CTAL-TA v4.0 EN, §2.1, p. 25].
5. **Choisir une technique lourde.** En systèmes critiques, on emploie des techniques formelles : analyse de dangers, FMEA, arbre de fautes [CTAL-TM v3.0 EN, §1.3.5, p. 31-32].
6. **Proportionner les tests au risque.** Un risque élevé appelle des tests plus précoces et des techniques plus rigoureuses ; un risque faible, l'inverse [CTAL-TM v3.0 EN, §1.3.4, p. 30]. Pour chaque risque, l'AT propose niveaux, types, techniques, indépendance et rigueur des tests [CTAL-TA v4.0 EN, §2.1, p. 25]. Livrable : une stratégie de test par niveau de risque.
7. **Fixer la couverture structurelle par niveau d'intégrité.** Une norme sectorielle part d'une analyse de dangers, attribue des niveaux d'intégrité, puis définit la couverture attendue par niveau [CTAL-TTA v4.0 EN, §2.8.2, p. 19]. Les tableaux du syllabus portent sur IEC 61508. Ils diffèrent pour ISO 26262 et DO-178C, donc ne s'appliquent pas tels quels à IEC 62304.
8. **Boucler : risques résiduels et suivi.** On relie résultats et risques pour évaluer le risque résiduel [CTFL v4.0.1 EN, §1.4.4, p. 21]. Le suivi des tests inclut le suivi des risques et la mise à jour du registre [CTAL-TM v3.0 EN, §1.3.1, p. 28].

## Exemple de mise en œuvre (fictif, interprétation)
Pour une application de dosage de 8 personnes : un atelier de risques (clinique, qualité, dev, test) alimente un registre. Chaque risque porte un identifiant, qui est repris dans les exigences et les cas de test. Les risques de classe élevée reçoivent des tests de conception plus poussés et une couverture structurelle élevée, les risques faibles des tests plus légers. Un outil d'exigences ou de test génère la matrice dans les deux sens. Chaque nouvelle version déclenche une revue d'impact par la traçabilité.

## Adaptation par domaine

| Domaine | Ce qui change | Où lire |
|---|---|---|
| Santé / réglementé (le vôtre) | Classes IEC 62304 et lien ISO 14971 : voir le Web. Le syllabus apporte le principe : technique lourde, couverture par niveau d'intégrité, documents versionnés. | CTAL-TM §1.3.5, CTAL-TTA §2.8.2, CTEL-TM §8.3.4 |
| Web | Principes transposables, pas de syllabus dédié. | CTFL §1.4.4 |
| Embarqué | Matériel/logiciel et HiL, surtout via l'automobile. | CT-AuT §2.1.2.6 |
| Mobile | CT-MAT 2019 (non lu). | à lire : CT-MAT §1.8 |
| API | Hors sujet ici. | — |

Côté Web : la classification IEC 62304 dépend de la gravité du dommage potentiel (A = aucun, B = non grave, C = décès ou blessure grave) et découle de l'analyse ISO 14971. Les activités de vérification doivent être proportionnées à la classe. Ces points viennent de résumés non officiels, à confirmer dans les normes [Web — « Software Safety Classifications », jamb.readthedocs.io, consulté le 2026-10-30] [Web — « What You need to know about IEC 62304 », securitycompass.com, consulté le 2026-10-30].

## Par quoi je commencerais
1. **Schéma de traçabilité plus identifiants de risque dans les exigences et les tests** : impact fort, effort faible.
2. **Matrice risque → niveau de rigueur de test**, validée avec qualité et réglementaire : impact fort, effort moyen.
3. **Revue d'impact à chaque changement via la matrice** : impact moyen, effort moyen (outillage).

## Où creuser ensuite
- `section CTAL-TM-3.0-en 1.3.6` (métriques et difficultés du RBT).
- `section CTAL-TM-3.0-en 1.3.4` (suite en p. 31).
- `section CTAL-TA-4.0-en 2.2` (contrôle des risques).
- `section CT-MBT-1.1-fr 2.3.3` (traçabilité avec un modèle).

**Confiance : 63/100 (moyenne)** : base 88 × 0,6 = 53 ; 6 passages lus +20 ; 2 syllabus concordants +10 ; Web −10 ; raisonnement sans source −10. Le score est limité par l'absence de syllabus médical et par un Web qui ne s'appuie que sur des résumés secondaires.

**Questions à choix**
1. Quelle est la classe de sécurité logicielle visée ?
   1. A
   2. B
   3. C
2. Quelle suite voulez-vous ?
   1. Approfondir les techniques de risque (FMEA, analyse de dangers)
   2. Comparer les syllabus sur la traçabilité
   3. Capitaliser ces pistes

## À capitaliser ?
Pas de doublon trouvé. Les deux premières références ci-dessous sont des passages lus, avec extraits copiés mot pour mot. La référence Web est secondaire.

```json
{
 "titre": "Traçabilité exigences-risques-tests en dispositif médical",
 "resume": "Chaîner exigence, risque, test, résultat et anomalie, et proportionner la rigueur de test au niveau de risque.",
 "probleme": "Prouver en audit que chaque exigence et chaque risque est couvert par des tests adaptés.",
 "principe": "Tracer bidirectionnellement ; dériver la profondeur de test du niveau de risque ; fixer la couverture par niveau d'intégrité.",
 "theme_principal": "rbt",
 "themes_secondaires": ["exigences", "reglementee"],
 "domaine_application": "Logiciel de dispositif médical soumis à IEC 62304 / ISO 14971",
 "prerequis": "Analyse de risque ISO 14971 disponible ; outil de gestion d'exigences et de tests.",
 "benefices": "Preuve d'audit, analyse d'impact des changements, risque résiduel mesurable.",
 "limites": "Aucun syllabus ISTQB médical dans la bibliothèque ; classes IEC 62304 à confirmer dans la norme.",
 "maturite": "documentee",
 "statut": "a_evaluer",
 "provenance": "Recherche du 2026-10-30 : « traçabilité des exigences vers les tests et RBT, dispositif médical »",
 "references": [
  {"type": "istqb", "doc_id": "CTFL-4.0.1-en", "pages": "21", "section": "1.4.4", "extrait": "Traceability of test results to risks can be used to evaluate the level of residual risk"},
  {"type": "istqb", "doc_id": "CTAL-TM-3.0-en", "pages": "30", "section": "1.3.4", "extrait": "Testing for higher risk levels should start early and use more rigorous test techniques"},
  {"type": "web", "titre": "Software Safety Classifications", "url": "https://jamb.readthedocs.io/en/latest/iec-62304/safety-classifications.html", "note": "Résumé non officiel des classes IEC 62304 ; à confirmer dans la norme."}
 ]
}
```

Rien n'est enregistré. La conversation principale lancera `idee ajouter` après votre accord.

Sources :
- [Software Safety Classifications](https://jamb.readthedocs.io/en/latest/iec-62304/safety-classifications.html)
- [What You need to know about IEC 62304](https://www.securitycompass.com/blog/iec-62304-medical-software-lifecycle/)

## Commandes exécutées

- `Read {"file_path": "/tmp/claude-0/-home-user/da9346e2-ce5e-5882-830a-19be129b35c4/scratchpad/wt-campagne/.claude/skills/qa-kn`
- `python qa.py idee chercher traçabilité exigences risques dispositif médical; python qa.py idee chercher requirements traceability risk-based testing`
- `python qa.py chercher traceability requirements tests; python qa.py chercher risk-based testing risk analysis; python qa.py chercher traçabilité exigences tests; python qa.py chercher medical device s`
- `python qa.py section CTFL-4.0.1-en 1.4.4 --max-caracteres 4000; python qa.py section CTAL-TM-3.0-en 1.3 --max-caracteres 9000`
- `python qa.py section CTEL-TM-2011-en 8.3.4 --max-caracteres 5000; python qa.py section CTAL-TA-4.0-en 2.1 --max-caracteres 6000`
- `python qa.py section CTAL-TM-3.0-en 1.3.5 --max-caracteres 5000; python qa.py section CTAL-TTA-4.0-en 2.8.2 --max-caracteres 4000; python qa.py section CT-AuT-2.1.1-en 2.1.2.6 --max-caracteres 3000`
- `WebSearch {"query": "IEC 62304 software safety classification A B C traceability risk management ISO 14971 verification", "mode": `
- `python qa.py confiance --help | head -30; python qa.py idee modele | head -40; python qa.py idee doublons --titre "Traçabilité exigences-risques-tests en dispositif médical" --resume "Chaîner exigence`
- `python qa.py themes | head -40; python qa.py confiance --base 88 --lus 6 --concordants 2 --web 1 --raisonnement 1`
- `python qa.py idee doublons --titre "Traçabilité exigences-risques-tests en dispositif médical" --resume "Chaîner exigence, risque, test, résultat ; rigueur de test proportionnée au niveau de risque" -`
