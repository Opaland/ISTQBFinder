# Essais de bout en bout des agents (Thomas, Sylvie)

Questions posées en conditions réelles (`claude -p --agent …`) par `scripts/essais_agents.py`
sur `eval/essais.json`. Réponses complètes et commandes exécutées :
`eval/essais-resultats/<date>/<id>.md`. Le harnais vérifie automatiquement que chaque
citation « §x, p. N » correspond à une page **lue** pendant la conversation ; le jugement
de fond ci-dessous est humain.

## Campagne du 2026-10-22 (main après #17)

| Essai | Agent | Tours | Coût | Confiance annoncée | Citations lues | Web | Verdict |
|---|---|---|---|---|---|---|---|
| T1 couverture des tests | Thomas | 6 | 0,16 $ | 90 | 8/9 | 0 | Bon : pistes CTFL §4.2-4.4, TTA §2.8, CT-AI §3.4.3 ; 1 citation non lue (CTAL-AT §3.1) |
| T2 RBT en équipe agile | Thomas | 5 | 0,15 $ | 82 | 3/3 | 0 | Bon |
| T3 maintenance Playwright | Thomas | 6 | 0,14 $ | **95** | 4/4 | **0** | Principes ISTQB justes et lus, liens Playwright signalés comme interprétation ; **mais** Web non fait alors que justifié, confiance gonflée → #49, #18 |
| T4 processus de qualification | Thomas | 5 | 0,13 $ | 70 | 4/5 | 0 | Bon : hypothèse de lecture explicitée, IDEAL, TMMi/TPI, rétrospectives ; 1 citation non lue |
| T5 priorisation des tests | Thomas | 4 | 0,11 $ | 90 | 3/3 | 0 | Très bon : tableau comparatif CTFL §5.1.5 / CTAL-TM §1.3.4-1.3.5 |
| T6 thèmes pauvres de la base | Thomas | 5 | 0,08 $ | 80 | — | 0 | Juste : constate que la base d'idées est vide, propose les thèmes riches en syllabus |
| S1 démarche RBT (cas d'usage) | Sylvie | 9 | 0,17 $ | 82 | 9/10 | 0 | Très utile : 4 pratiques, verdicts sourcés (CTAL-TM §1.3.2-1.3.6, CTFL §5.2.3-5.2.4), 8 manques, niveau 1 justifié, chemin vers le niveau 2 ; défauts : vocabulaire « Conforme », confiance non reproductible, section lue partiellement → #30, #18, #22 |
| S2 100 % automatisé Playwright | Sylvie | 7 | 0,16 $ | 72 | 6/6 | 0 | Bon : écart sur « 100 % » et « supprimer le manuel », Playwright « Hors ISTQB » |

**Synthèse** : 8 réponses utiles, au format demandé (pistes par syllabus, tableaux, « où
creuser », « à capitaliser » sans enregistrement), coût moyen ≈ 0,14 $. 37 citations sur
40 correspondent à une page lue ; les 3 autres renvoient à des passages vus seulement en
extrait de recherche (règle « lire avant de citer » imparfaitement suivie). Aucune
recherche Web, y compris quand elle était justifiée (T3). Les scores de confiance ne sont
pas reproductibles. Défauts suivis dans les issues #18, #22, #30, #49.

## Relancer

```bash
python qa.py actualiser                       # index à jour
python scripts/essais_agents.py               # tous les essais (≈ 1,20 $, ≈ 15 min)
python scripts/essais_agents.py S1-rbt        # un seul
```
