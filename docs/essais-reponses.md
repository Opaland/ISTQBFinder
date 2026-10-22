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

## Campagne du 2026-10-22 (bis) : mise en place par domaine et mode conversationnel (#90, #91, #92)

Nouveaux essais `M*` (mise en place par domaine), `S3` (audit en domaine réglementé) et
`C1` (question volontairement ambiguë, skill seul en `claude -p`). Chaque essai porte des
`criteres` contrôlés par `controler()` dans `scripts/essais_agents.py` : méthode en ≥ 4
étapes, chaque étape sourcée (« § ») ou marquée interprétation, exemple fictif, domaines
du tableau, questions de cadrage / à choix, hypothèses explicites, couverture absente
signalée, mentions attendues, confiance.

| Essai | Agent | Tours | Coût | Confiance | Citations lues | Web | Critères | Verdict |
|---|---|---|---|---|---|---|---|---|
| M1 RBT en agile (sans domaine) | Thomas | 7 | 0,17 $ | 80 | 11/11 | 0 | 11/11 | Bon : 7 étapes sourcées (CTFL-AT §3.2.1, CTFL §5.1.2, CTAL-AT §3.1.1, CTAL-TA §2.1.1-2.2, CTAL-TM §1.3.6), exemple Scrum fictif, tableau des 5 domaines (repères signalés « non lus »), questions à choix. Remplace l'exemple 1 de `exemples-conversations.md` |
| M2 dispositif médical | Thomas | 6 | 0,16 $ | 55 | 9/9 | 1 | 7/7 | Bon et honnête : traçabilité (CTFL §1.4.4, CT-FT §3.3) + RBT (CTAL-TM §1.3) ; dit qu'aucun syllabus ne couvre IEC 62304 / ISO 14971, Web (sources secondaires) signalé et confiance abaissée |
| M3 web e-commerce | Thomas | 11 | 0,20 $ | 66 | 5/5 | 1 | 6/6 | Bon : CT-TAS §1.1, §3.1.1, §4.1, CTAL-AT §1.4, §3.1.2 ; « pas de syllabus web dédié, principes transposés » ; Web marginal et signalé |
| M4 embarqué / intégration matériel | Thomas | 10 | 0,18 $ | 68 | 5/5 | 0 | 7/7 | Bon : CT-AuT (niveaux ISO 26262 / ASPICE, XiL/HiL), CTEL-TM 2011 §8.3.3 (labo d'intégration, prototypes), CTAL-TTA §4.1 ; aucun syllabus industriel |
| M5 mobile iOS / Android | Thomas | 14 | 0,20 $ | 68 | 12/13 | 0 | 6/6 | Très bon : CT-MAT 2019 dédié (§1.1, §1.6, §1.8, §4-5) ; 1 citation non lue (CTAL-TAE §4.2.1 EN) |
| M6 API REST multi-équipes | Thomas | 19 | 0,22 $ | 80 | 11/11 | 0 | 7/7 | Bon : contrat versionné en CI (CT-QDO §3.2.2), alignement des équipes (CTAL-TM §1.4.2), performance (CT-PT §3.2) ; choix consommateur/fournisseur marqué interprétation |
| S3 audit, dispositif médical | Sylvie | 6 | 0,15 $ | 72 | 6/7 | 0 | 5/5 | Utile : analyse de risques unique = **Écart** (CTAL-TA §2.1, CTAL-TM §1.3.1), traçabilité incomplète, niveau 1 ; normes du domaine « non vérifiables ici » ; questions à choix ; 1 citation non lue (CTFL §2.2.3) |
| C1 « Comment on gère les risques ? » | skill | 4 | 0,12 $ | 82 | 1/1 | 0 | 3/3 | Conforme à #92 en `-p` : « **Hypothèse :** risques produit/qualité » en tête, ne bloque pas, « Questions à choix » (criticité a/b/c, besoin a-d) en fin |

**Avant correctif** (premier passage, conservé en `*-avant-correctif.md`) : M1 (6/11) et M4
(4/7) étaient traités comme des questions de connaissance (pistes, pas de méthode ni
d'exemple) parce que « comment l'ISTQB propose-t-il d'intégrer… » et « comment organiser… »
n'étaient pas reconnus comme des questions de mise en place ; C1 (1/3) posait des
questions ouvertes sans hypothèse ni options. Corrigé dans cette PR (détection élargie
dans `strategie.md`, `SKILL.md`, `thomas.md` ; hypothèse en tête et questions de cadrage
**à choix**), puis relancé.

**Citations non lues (#127)** : M5 (CTAL-TAE §4.2.1 EN) et S3 (CTFL §2.2.3) citaient une
page vue seulement en extrait de recherche. Correctif : « contrôle avant d'envoyer »
(chaque référence doit avoir son `lire`/`section`/`page`, sinon lue ou retirée) dans le
skill, Thomas et Sylvie ; `essais_agents.py` marque désormais l'essai **en échec** (code
retour 1) dès qu'une citation n'a pas été lue. Relance : M5 10/10 citations lues (0,20 $),
S3 5/5 (0,16 $), tous critères satisfaits ; les fichiers M5 et S3 sont ceux de la relance.

### Couverture de la bibliothèque par domaine

| Domaine | Couvert par | Non couvert (dit par l'assistant) |
|---|---|---|
| Santé / réglementé | principes : CTAL-TM v3.0 §1.3, CTFL v4.0.1 §1.4.4, CTAL-TTA v4.0 §2.8.2 (niveaux d'intégrité), CTEL-TM 2011 §8.3.4, CT-FT (conformité, finance) | **aucun syllabus santé / dispositif médical** ; IEC 62304, ISO 14971 absents → Web ou import du texte des normes |
| Web | CT-TAS v1.0, CTAL-AT v2.0, CT-PT 2018 §3.2, CT-MAT §2.2.4 (web apps) | **aucun syllabus web dédié** : principes transposés |
| Embarqué / intégré | CT-AuT v2.1.1 (automobile, EN), CTEL-TM 2011 §8.3.3 (EN, ancien), CTAL-TTA §4.1 | rien d'industriel, ferroviaire ou aéronautique (DO-178C seulement cité) ; anglais seulement |
| Mobile | CT-MAT 2019 (FR + EN), dédié | version 2019 : aucun outil actuel |
| API | CTAL-TTA v4.0 §2.7, CT-QDO v1.0 §3.2.2 (contrat, EN seulement), CTAL-TAE v2.0 §5.1.3, CT-PT | **aucun syllabus API dédié** |

Ces manques ne figurent pas dans `manquants` : ce n'est pas un syllabus ISTQB absent
(les 26 codes du catalogue sont présents en anglais), mais un domaine que l'ISTQB ne
couvre pas. Pour aller plus loin : importer un document non ISTQB (`/ajouter-syllabus`
avec le fichier, cité comme « non ISTQB ») ou recherche Web justifiée.

**Coût** : 11 essais (8 + 3 relances) ≈ 2,06 $, soit ≈ 0,19 $ par essai.
Relancer : `python scripts/essais_agents.py M S3-reglemente C1-ambigu` (préfixe accepté).

## Relancer

```bash
python qa.py actualiser                       # index à jour
python scripts/essais_agents.py               # tous les essais (16, ≈ 2,80 $, ≈ 30 min)
python scripts/essais_agents.py S1-rbt        # un seul
python scripts/essais_agents.py M             # par préfixe : tous les essais M…
```
