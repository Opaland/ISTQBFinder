# S5-hil — sylvie

**Question** : Pour notre calculateur automobile, nos tests HiL sont lancés manuellement avant chaque jalon, la traçabilité exigences-tests est faite à la main dans Excel et la couverture de code n'est pas mesurée. Est-ce suffisant au regard de l'ISTQB ? Quel niveau ?

**Tours** : 11 · **coût** : 0.258 $ · **confiance annoncée** : 52 · **verdict** : réussi · **citations** : 14/14 lues · **Web** : 0 · **critères** : 5/5 · **fidélité** (juge LLM, indicatif) : 0.79 sur 4 lignes citées, 0 contradiction(s)

## Réponse

Avis indicatif d'alignement sur les syllabus ISTQB locaux ; ni attestation de conformité, ni évaluation ISTQB/TMMi/ISO.

Ta démarche est partiellement alignée : la traçabilité existe, mais elle est manuelle, et la couverture de code n'est pas mesurée. Le lancement manuel des tests HiL est aussi à documenter. Je n'ai ni le niveau ASIL de tes exigences ni ta stratégie de test, donc je ne peux pas dire si c'est suffisant.

**Pratiques décrites**
- P1 : tests HiL lancés manuellement avant chaque jalon.
- P2 : traçabilité exigences-tests faite à la main dans Excel.
- P3 : couverture de code non mesurée.

Tu les décris comme existantes (« sont lancés », « est faite »). Aucune preuve n'est citée : pas de stratégie écrite, de rapport, d'historique Excel ni de revue. Je les marque donc « en place (preuve : déclaration seule) ».

| Pratique | Intention / en place | Verdict | Ce que dit l'ISTQB | Source |
|---|---|---|---|---|
| P1 HiL manuel avant chaque jalon | en place (déclaré, sans preuve) | Partiellement aligné | Le HiL est un environnement reconnu, utilisable pour les tests composant, intégration et système. Le syllabus ne dit rien du déclenchement manuel. Il demande des critères de régression dans la stratégie de test, par exemple fondés sur les risques et une analyse d'impact. Il admet aussi de rejouer tous les tests automatisés à chaque livraison. Un lancement avant jalon seulement n'est pas décrit comme critère. | [CT-AuT v2.1.1 EN, §3.2.3.2, p. 37] ; [CT-AuT v2.1.1 EN, §2.1.2.3, p. 22] |
| P2 Traçabilité manuelle sous Excel | en place (déclaré, sans preuve) | Partiellement aligné | ASPICE exige une traçabilité bidirectionnelle (analyse d'impact, évaluation de la couverture, suivi du statut) et une traçabilité horizontale entre exigences, spécifications de test et résultats. Elle doit aussi lier demandes de changement et rapports de défauts. Le syllabus juge utile une chaîne d'outils cohérente quand les liens sont nombreux. Un outil n'est pas imposé : Excel est donc admissible. Rien n'indique que les liens couvrent les résultats et les défauts, ni qu'ils sont bidirectionnels. | [CT-AuT v2.1.1 EN, §2.1.2.6, p. 23] ; [CT-TAS v1.0 EN, §6.2.1, p. 48] |
| P3 Couverture de code non mesurée | en place (déclaré) | Écart si le calculateur a des exigences ASIL. Non vérifiable sinon. | Pour un système lié à la sécurité, une norme réglementaire fixe normalement les niveaux de couverture requis. Ils dépendent du niveau d'intégrité. Le syllabus TTA illustre ces niveaux avec l'IEC 61508 (instructions, branches, MC/DC), et précise que l'ISO 26262 les fixe différemment. En ISO 26262, une méthode « highly recommended » doit être appliquée. Une méthode « recommended » doit l'être, ou être écartée avec une justification. | [CTAL-TTA v4.0 EN, §2.8.2, p. 20] ; [CT-AuT v2.1.1 EN, §2.2.5, p. 28] |

Je n'ai pas lu les tables ISO 26262 : aucun syllabus de la bibliothèque ne donne les seuils de couverture par ASIL. Le verdict « Écart » repose sur le principe général, pas sur un seuil chiffré.

**Ce qui manque**
- Une stratégie de test écrite qui fixe les environnements par niveau de test et les critères de régression. [CT-AuT v2.1.1 EN, §2.1.2.3, p. 22]
- Le niveau ASIL des exigences (analyse de dangers et d'évaluation des risques, HARA), et ce qu'il impose en techniques, types de test et étendue. Le syllabus rappelle que l'ASIL est lié à un objectif de sécurité précis, pas au produit entier. [CT-AuT v2.1.1 EN, §2.2.4.1, p. 26] ; [CT-AuT v2.1.1 EN, §2.2.4.2, p. 27]
- Une vérification des unités logicielles (cas de test unitaires, analyse statique type MISRA-C, revues) et des critères de régression associés. Tu ne mentionnes rien sur le niveau unitaire. [CT-AuT v2.1.1 EN, §2.1.2.5, p. 23]
- Une mesure de couverture. Le syllabus CT-TAS cite les outils de couverture de code (couverture par la suite de tests de composant, lacunes) et la matrice de traçabilité (fonctionnalités non couvertes par un test). Tu n'as ni l'un ni l'autre sous forme outillée. [CT-TAS v1.0 EN, §6.2.1, p. 48]
- La justification écrite de tout écart aux méthodes recommandées. [CT-AuT v2.1.1 EN, §2.2.5, p. 28]

**Niveau atteint : 1 — Initial** · niveau visé : 2 — Discipliné

- **Pourquoi 1 :** le niveau 2 de la grille du dépôt exige une politique ou stratégie de test écrite, une planification, une supervision et contrôle des tests, et un environnement de test. Aucun de ces éléments n'est démontré dans ta description. Un critère non mentionné est « non démontré », pas « acquis ». Les pratiques que tu cites sont réelles mais ponctuelles et manuelles, donc dépendantes des personnes.
- **Pour passer au niveau 2 :**
  1. rédiger la stratégie de test, avec les critères de régression et le choix des environnements XiL par niveau ;
  2. rattacher les tests aux niveaux ASIL ;
  3. suivre les tests HiL pendant le projet, pas seulement avant le jalon ;
  4. couvrir les résultats et les défauts dans la traçabilité ;
  5. mesurer la couverture, ou justifier par écrit pourquoi elle ne l'est pas.
- Les niveaux 3 à 5 sont une adaptation du dépôt : indicateurs quantitatifs pour décider (niveau 4), amélioration continue à partir des mesures (niveau 5).

**Confiance : 52/100 (moyenne)**
Calcul : base 36 × 0,6 = 22 ; 15 passages lus +20 ; 3 syllabus concordants +20 ; raisonnement sans source −10 → 52.
- La couverture lexicale de la recherche sur la couverture de code est faible (36/100), et le niveau repose sur ton résumé en trois phrases.
- Le jugement sur l'ASIL est un raisonnement, pas un passage lu.

**Limites**
- Aucun syllabus de la bibliothèque ne reproduit les tables de méthodes ni les seuils de couverture de l'ISO 26262. La conformité à l'ISO 26262, à l'ASPICE ou à l'IEC 61508 est donc non vérifiable ici. Les seuils de couverture de l'IEC 61508 cités plus haut sont une illustration du syllabus.
- Je ne sais pas si ton calculateur est lié à la sécurité, ni à quel ASIL.
- Les syllabus ne disent rien de l'automatisation des tests HiL ni de l'outil Excel lui-même.
- Je n'ai pas lu de version FR du syllabus automobile.

**Questions à choix**

Quel est le niveau de criticité du calculateur ?
1. ASIL C ou D, sur au moins un objectif de sécurité
2. ASIL A ou B seulement
3. QM, sans exigence de sécurité fonctionnelle

Quelle suite veux-tu ?
1. Approfondir les sections ASPICE et ISO 26262 (tables de méthodes)
2. Détailler la liste de contrôle d'une stratégie de test niveau 2
3. Chercher plus largement avec Thomas (le chercheur) sur la couverture MC/DC et l'ISO 26262

**Où creuser ensuite**
- À lire : CT-AuT v2.1.1 EN §2.1.2.1 à 2.1.2.4 (processus de test et testware ASPICE), §4.2.4 (tests fondés sur les exigences), §4.2.5 (sélection selon le contexte).
- À lire : CTAL-TTA v4.0 EN §2.8.1 (systèmes non liés à la sécurité).
- À lire : CT-TAS v1.0 EN, sections sur l'automatisation pour le déclenchement automatique des tests.

**Traçabilité**
- Date de l'avis : 2026-10-30.
- Documents lus :
  - CT-AuT-2.1.1-en, v2.1.1 (2025-12-21) : §2.1.2.3 (p. 22), §2.1.2.5 (p. 22-23), §2.1.2.6 (p. 23), §2.2.4 (p. 26-27), §2.2.5 (p. 27-28), §3.2.3 (p. 37), §4.2.1 (p. 44-45).
  - CTAL-TTA-4.0-en, v4.0 (2021-06-30) : §2.8.2 (p. 19-20).
  - CT-TAS-1.0-en, v1.0 (2024-05-03) : §6.2.1 (p. 47-48).
- Référence de la grille : grille du dépôt (`referentiel/grille-maturite.md`), sans page citée.
- Requêtes `chercher` lancées :
  - « traceability requirements tests coverage test automation »
  - « code coverage structural coverage safety-critical automotive »
- Autres commandes : `plan CT-AuT-2.1.1-en`, `confiance`.

Avis indicatif d'alignement sur les syllabus ISTQB locaux ; ni attestation de conformité, ni évaluation ISTQB/TMMi/ISO.

## Commandes exécutées

- `Read {"file_path": "/tmp/claude-0/-home-user/da9346e2-ce5e-5882-830a-19be129b35c4/scratchpad/wt-campagne/referentiel/grille-m`
- `python qa.py chercher "traceability requirements tests coverage test automation" 2>&1 | head -80`
- `python qa.py chercher "code coverage structural coverage safety-critical automotive" 2>&1 | head -80`
- `python qa.py plan CT-AuT-2.1.1-en 2>&1`
- `python qa.py section CTAL-TTA-4.0-en 2.8.2 2>&1`
- `python qa.py section CT-TAS-1.0-en 6.2.1 --max-caracteres 4000 2>&1`
- `python qa.py section CT-AuT-2.1.1-en 2.1.2.6 2>&1; python qa.py section CT-AuT-2.1.1-en 2.2.4 2>&1; python qa.py section CT-AuT-2.1.1-en 3.2.3 2>&1`
- `python qa.py section CT-AuT-2.1.1-en 2.1.2.3 2>&1; python qa.py section CT-AuT-2.1.1-en 2.1.2.5 2>&1`
- `python qa.py section CT-AuT-2.1.1-en 4.2.1 2>&1; python qa.py section CT-AuT-2.1.1-en 2.2.5 2>&1`
- `python qa.py confiance --autorite 0 --base 36 --lus 15 --concordants 3 --ancien 0 --contradiction 0 --web 0 --raisonnement 1 --non-couvert 0 2>&1`
