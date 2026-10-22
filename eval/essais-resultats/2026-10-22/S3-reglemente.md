# S3-reglemente — sylvie

**Question** : Pour le logiciel de notre dispositif médical, je prévois : une matrice de traçabilité exigences → tests tenue dans un tableur, une analyse de risques faite une seule fois en début de projet, et des tests système manuels avant chaque release. Est-ce aligné ISTQB ? Quel niveau de maturité ?

**Tours** : 6 · **coût** : 0.151 $ · **confiance annoncée** : 72 · **citations** : 6/7 lues · **Web** : 0 · **critères** : 5/5

## Réponse

**Avis indicatif d'alignement sur les syllabus ISTQB locaux ; ni attestation de conformité, ni évaluation ISTQB/TMMi/ISO.**

Ta démarche est partiellement alignée. La traçabilité et les tests système sont compatibles avec l'ISTQB, mais une analyse de risques faite une seule fois s'écarte nettement de ce que décrivent les syllabus. Tout est à l'état d'intention : le niveau atteint est donc plafonné à 1.

## Pratiques décrites

| # | Pratique | Intention / en place |
|---|---|---|
| P1 | Matrice de traçabilité exigences → tests, dans un tableur | intention |
| P2 | Analyse de risques une seule fois, en début de projet | intention |
| P3 | Tests système manuels avant chaque release | intention |

## Verdicts

| Pratique | Verdict | Ce que dit l'ISTQB | Source |
|---|---|---|---|
| P1 | Partiellement aligné | Il faut établir et maintenir la traçabilité tout au long du processus de test. Elle doit couvrir la base de test, les éléments de testware (conditions, **risques**, cas de test), les résultats et les anomalies. Tracer les cas de test vers les exigences permet de vérifier la couverture. Tracer les résultats vers les risques permet d'évaluer le risque résiduel. Une bonne traçabilité aide aussi à mesurer l'impact des changements et à faciliter les audits. Ta matrice ne couvre que exigences → tests : les risques, les résultats et les anomalies n'y figurent pas. Le syllabus mentionne des outils de gestion du testware qui facilitent la traçabilité, mais n'interdit pas le tableur. | [CTFL v4.0.1 EN, §1.4.4, pp. 20-21] ; [CTAL-TA v4.0 EN, §1.3.7, pp. 22-23] |
| P2 | **Écart** | Le test basé sur les risques comprend l'analyse des risques (identification + évaluation) et leur contrôle (atténuation + suivi). Les risques et leur niveau « ne sont pas statiques et changent dans le temps », d'où un suivi régulier, par exemple à chaque itération. Le suivi du test doit inclure le suivi des risques : analyse des nouveaux risques et mise à jour du registre. Une analyse unique contredit ce suivi continu. | [CTAL-TA v4.0 EN, §2.1, p. 25] ; [CTAL-TM v3.0 EN, §1.3.1, p. 28] ; [CTFL v4.0.1 EN, §5.2.4, p. 53] |
| P3 | Partiellement aligné | Le test système vise le comportement global du système, fonctionnel de bout en bout et non fonctionnel. Il peut être confié à une équipe indépendante. Le test manuel n'est pas contredit. Mais les suites de non-régression sont exécutées à chaque release et grossissent avec elles, ce qui en fait de bonnes candidates à l'automatisation. Manquent aussi dans ta description : le lien avec les risques pour fixer la profondeur des tests, et les autres niveaux de test. | [CTFL v4.0.1 EN, §2.2.1, p. 29] ; [CTFL v4.0.1 EN, §2.2.3, p. 31] |

Pour P3, le passage sur l'automatisation de la non-régression est un extrait de recherche (#11512). Je ne l'ai pas lu en section complète.

## Ce qui manque

- **Évaluation des risques.** Il faut évaluer probabilité et impact, puis combiner les deux en un niveau de risque avec une matrice ou un produit. Les facteurs d'impact cités incluent les besoins de sécurité (*safety*), les sanctions légales et la responsabilité civile [CTAL-TM v3.0 EN, §1.3.3, pp. 29-30]. C'est très pertinent pour un dispositif médical, mais ta description ne dit pas si c'est prévu.
- **Parties prenantes.** L'analyse doit associer le plus grand éventail possible de parties prenantes, avec une liste convenue avec le chef de projet [CTAL-TM v3.0 EN, §1.3.2, pp. 28-29].
- **Atténuation par le test.** Le temps et l'effort de test doivent être proportionnels au niveau de risque. Les risques élevés se testent plus tôt et avec des techniques plus rigoureuses [CTAL-TM v3.0 EN, §1.3.4, p. 30 ; CTFL v4.0.1 EN, §5.2.3, p. 53].
- **Suivi des risques.** Il faut un registre des risques mis à jour pendant le projet. La fréquence se fixe par itération ou selon le responsable du risque produit [CTAL-TA v4.0 EN, §2.1, p. 25].
- **Traçabilité risques ↔ tests ↔ résultats.** Elle permet d'évaluer le risque résiduel [CTFL v4.0.1 EN, §1.4.4, p. 21].
- **Supervision.** Ta description ne mentionne ni stratégie ou planification de test écrite, ni supervision et contrôle, ni environnement de test. Ce sont les critères du niveau 2 de la grille [`referentiel/grille-maturite.md`].
- **Exigences réglementaires.** Les syllabus lus ne détaillent aucune exigence propre aux dispositifs médicaux (voir Limites).

## Niveau atteint : 1 — Initial · niveau visé : 2 (Discipliné)

Aucune pratique n'est déclarée « en place » : le niveau est plafonné à 1. Si tout était appliqué tel que décrit, tu serais encore sous le niveau 2. L'analyse de risques unique ne produit pas de suivi, et la stratégie écrite, la supervision et l'environnement de test ne sont pas démontrés.

**Pour atteindre le niveau 2** (ces critères sont tous à démontrer) :
- une stratégie de test écrite, rattachée aux risques ;
- une analyse de risques complète (parties prenantes, probabilité × impact) qui détermine la priorité et la profondeur des tests ;
- une traçabilité étendue aux risques et aux résultats ;
- un suivi des risques et des tests pendant le projet, avec mise à jour du registre ;
- un environnement de test défini.

Les niveaux 3 à 5 sont une adaptation du dépôt, non issue des syllabus.

## Confiance : 72/100

- **Pour :** les passages sur la traçabilité et le test basé sur les risques sont lus dans trois syllabus qui concordent (CTFL, CTAL-TM, CTAL-TA).
- **Contre :** la description est courte et aucune preuve de terrain n'est fournie. Je n'ai pas lu le plan complet du CTFL §2.2.3 ni la suite de CTAL-TM §1.3.4.

## Limites

- **Dispositif médical :** je n'ai trouvé aucune exigence réglementaire détaillée dans les syllabus lus. Les normes habituelles du domaine (par ex. ISO 14971, IEC 62304) ne sont pas dans la bibliothèque. Je ne peux donc rien conclure sur ta conformité réglementaire, qui reste non vérifiable ici.
- **Hors périmètre :** un audit réglementaire exigerait une analyse de risques tenue à jour sur tout le cycle de vie. Les syllabus lus vont dans ce sens, mais cela relève d'un autre référentiel que ceux que j'ai lus.
- **Suite possible :** Thomas peut faire une recherche plus large sur les exigences propres aux dispositifs médicaux.

## Questions à choix

1. Quel cadre réglementaire s'applique à ton dispositif ?
   - UE (MDR) / IEC 62304
   - FDA (États-Unis)
   - Pas encore déterminé
2. Que préfères-tu comme suite ?
   - Approfondir l'analyse de risques (liste de contrôle RBT détaillée)
   - Évaluer plus finement l'automatisation de la non-régression
   - Demander à Thomas une recherche sur la réglementation des dispositifs médicaux
3. Parmi P1-P3, une pratique est-elle déjà appliquée (avec une preuve : document, outil, réunion) ? Si oui, le niveau pourra être réévalué.

## Piste à conserver (non enregistrée)

```json
{
  "titre": "Liste de contrôle RBT alignée ISTQB",
  "contenu": "1) Identifier les risques avec un échantillon large de parties prenantes (liste convenue avec le chef de projet) ; 2) catégoriser ; 3) évaluer probabilité et impact (matrice ou produit) en tenant compte de la sécurité et du juridique ; 4) en déduire priorité, profondeur de test et techniques ; 5) tracer risques ↔ tests ↔ résultats ; 6) suivre les risques et mettre à jour le registre régulièrement.",
  "sources": ["CTAL-TM v3.0 EN §1.3.1-1.3.4", "CTFL v4.0.1 EN §1.4.4, §5.2", "CTAL-TA v4.0 EN §2.1"]
}
```

Je ne l'ai pas validé avec `python qa.py idee modele`. Les champs exacts sont à vérifier avant tout enregistrement.

## Traçabilité

- **Date de l'avis :** 2026-10-22.
- **Documents lus :**
  - `CTFL-4.0.1-en`, v4.0.1 (2024-09-15) : §1.4.4 (pp. 20-21), §5.2-5.2.4 (pp. 51-53), §2.2.1 (pp. 28-29). Le §2.2.3 (p. 31) n'est lu que via un extrait de recherche.
  - `CTAL-TM-3.0-en`, v3.0 (2024-05-03) : §1.3-1.3.4 (pp. 28-30).
  - `CTAL-TA-4.0-en`, v4.0 (2025-05-02) : §2.1 (p. 25) ; §1.3.7 (pp. 22-23) via extrait de recherche.
  - `referentiel/grille-maturite.md`.
- **Requêtes `chercher` :**
  - `"risk-based testing" identification évaluation atténuation`
  - `"traceability requirements test cases"`
  - `"risk management regular reassessment product risks"`
  - `"medical device regulatory safety-critical"`
  - `"regression testing automation change impact release"`
- **Commandes `section` :** CTFL 1.4.4, 5.2, 2.2.1 ; CTAL-TA 2.1 ; CTAL-TM 1.3. La section CTFL 2.3.4 est introuvable.

**Avis indicatif d'alignement sur les syllabus ISTQB locaux ; ni attestation de conformité, ni évaluation ISTQB/TMMi/ISO.**

## Commandes exécutées

- `Read {"file_path": "/tmp/claude-0/-home-user/da9346e2-ce5e-5882-830a-19be129b35c4/scratchpad/wt-90/referentiel/grille-maturit`
- `python qa.py chercher "risk-based testing identification évaluation atténuation" 2>&1 | head -60; python qa.py chercher "traceability requirements test cases" 2>&1 | head -50; python qa.py chercher "r`
- `python qa.py section CTFL-4.0.1-en 1.4.4 2>&1 | head -40; echo ======; python qa.py section CTFL-4.0.1-en 5.2 2>&1 | head -120; echo ======; python qa.py section CTAL-TA-4.0-en 2.1 2>&1 | head -60`
- `python qa.py section CTAL-TM-3.0-en 1.3 2>&1 | head -120; echo =====; python qa.py chercher "medical device regulatory safety-critical" 2>&1 | head -30`
- `python qa.py section CTFL-4.0.1-en 2.2.1 2>&1 | head -40; echo ====; python qa.py chercher "regression testing automation change impact release" 2>&1 | head -25; echo ===; python qa.py section CTFL-4.`
