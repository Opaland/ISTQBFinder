"""Interface en ligne de commande unique, appelée par le skill Claude Code.

    python qa.py <commande> [options]     (depuis la racine du dépôt)

Sorties en texte français compact ; `--json` sur les commandes de lecture pour un
traitement automatique."""
import argparse
import json
import re
import sys
import sqlite3
from pathlib import Path

from . import bibliotheque, catalogue, connaissances, journal, recherche, taxonomie
from .connaissances import ErreurValidation

MODELE_IDEE = {
    "titre": "Titre court et explicite",
    "resume": "Description synthétique en 1-3 phrases",
    "probleme": "Problème ou situation auquel l'idée répond",
    "principe": "Principe / technique / mode opératoire",
    "theme_principal": "code de thème (voir `themes`)",
    "themes_secondaires": ["code", "code"],
    "domaine_application": "Contexte où l'idée s'applique (type de produit, équipe, cycle)",
    "prerequis": "Conditions nécessaires",
    "benefices": "Bénéfices attendus",
    "limites": "Limites, risques, contre-indications",
    "maturite": "hypothese | documentee | pratiquee | eprouvee",
    "statut": "a_explorer | a_evaluer (validee/experimentee : via `idee statut`)",
    "provenance": "Recherche du AAAA-MM-JJ : « question posée » / saisie utilisateur",
    "references": [
        {"type": "istqb", "doc_id": "CTAL-TA-4.0-fr", "pages": "31-32", "section": "3.1.1",
         "extrait": "quelques mots copiés du passage lu (vérifiés automatiquement)"},
        {"type": "web", "titre": "Titre de la page", "url": "https://…", "note": "ce que la source apporte"},
    ],
}


def _ecrire(texte: str = "") -> None:
    sys.stdout.write(texte + "\n")


def _json(obj) -> None:
    _ecrire(json.dumps(obj, ensure_ascii=False, indent=1, default=str))


def _ref_page(r: dict) -> str:
    imp = r.get("page_imprimee")
    return f"p. {r['page']}" + (f" (imprimée {imp})" if imp else "")


def _ref_doc(r: dict) -> str:
    etat = "" if r.get("statut_version", "courant") == "courant" else f" [{r['statut_version'].upper()}]"
    retrait = catalogue.statut_officiel(r.get("code"))
    return (f"{r['doc_id']} · {r.get('titre', '')} · v{r.get('version') or '?'} ({r.get('date_publication') or 'date ?'})"
            f"{etat}" + (f" ⚠ {retrait}" if retrait else ""))


def lire_entree_standard() -> str:
    """Entrée standard lue en octets et décodée en UTF-8 : sous Windows, `sys.stdin` suit la
    page de code de la console (cp1252) et corrompait les accents (« Ã‰valuer »). Le BOM
    éventuel (Bloc-notes, PowerShell) est retiré."""
    tampon = getattr(sys.stdin, "buffer", None)
    if tampon is None:  # flux texte déjà décodé (tests, redirection Python)
        return sys.stdin.read().lstrip("\ufeff")
    try:
        return tampon.read().decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise ErreurValidation("Entrée standard illisible : enregistrer le JSON en UTF-8 "
                               f"(octet invalide en position {exc.start}).") from exc


def _lire_donnees(source: str) -> dict:
    brut = lire_entree_standard() if source == "-" else Path(source).read_text(encoding="utf-8-sig")
    try:
        return json.loads(brut)
    except json.JSONDecodeError as exc:
        raise ErreurValidation(f"JSON invalide ({exc.msg}, ligne {exc.lineno}).") from exc


# ---------------------------------------------------------------- bibliothèque

def cmd_catalogue(a):
    docs = catalogue.documents(niveau=a.niveau)
    presents = {}
    if bibliotheque.chemins.index_db().exists():
        for d in bibliotheque.inventaire():
            presents.setdefault(d["code"], []).append(f"{d['langue']} v{d['version']}"
                                                      + ("" if d["statut_version"] == "courant" else "*"))
    cat = bibliotheque.catalogue()
    _ecrire(f"Catalogue ISTQB officiel — relevé le {cat['verifie_le']} ({len(docs)} syllabus)")
    for d in docs:
        ligne = f"  {d['code']:10} {d['niveau']:11} {d['titre'][:58]:58} v{d['version_constatee']:10}"
        ligne += f" local : {', '.join(presents.get(d['code'], [])) or '—'}"
        if catalogue.statut_officiel(d["code"]):
            ligne += f" ⚠ {catalogue.statut_officiel(d['code'])}"
        if a.verifier:
            v = catalogue.verifier(d)
            ligne += f" | {v['etat']}" + (f" ⚠ NOUVEAU FICHIER : {v['fichier']}" if v["nouveau_fichier"] else "")
        _ecrire(ligne)
    _ecrire(f"\n{cat['conditions']}")
    if not a.verifier:
        _ecrire("(--verifier interroge istqb.org pour détecter les nouvelles versions)")


def cmd_telecharger(a):
    if not (a.codes or a.tous or a.niveau):
        raise ErreurValidation("Préciser des codes (ex. CTFL CTAL-TM), --niveau ou --tous.")
    rc = 0
    for d in catalogue.documents(None if a.tous or a.niveau else a.codes, a.niveau):
        r = catalogue.telecharger(d)
        _ecrire(f"{d['code']:10} {r['etat']:8} {r.get('doc_id', '')} — {r['message']}")
        for n in r.get("versions", []):
            _ecrire(f"           version : {n}")
        rc = 2 if r["etat"] == "echec" else rc
    return rc


def cmd_importer(a):
    meta = {"code": a.code, "titre": a.titre, "niveau": a.niveau, "domaine": a.domaine, "version": a.version,
            "langue": a.langue, "date_publication": a.date, "source_officielle": a.source, "type": a.type}
    rc = 0
    for f in a.fichiers:
        p = Path(f)
        fichiers = sorted(x for x in p.iterdir() if x.suffix.lower() in bibliotheque.EXTENSIONS) if p.is_dir() else [p]
        if not fichiers:
            _ecrire(f"{p} : aucun fichier PDF / .txt / .md")
            rc = 2
        for x in fichiers:
            if not x.exists():
                _ecrire(f"{x} : introuvable")
                rc = 2
                continue
            r = bibliotheque.importer(x, meta, remplacer=a.remplacer, motif=a.motif, prive=a.prive)
            if r["etat"] in ("echec", "refuse"):
                rc = 2
            _ecrire(f"{x.name} → {r['etat']} {r.get('doc_id', '')} — {r['message']}")
            if r.get("meta"):
                m = r["meta"]
                _ecrire(f"    détecté : code={m['code']} type={m['type']} version={m['version']} "
                        f"langue={m['langue']} date={m['date_publication']} — corriger avec `corriger` si faux")
            for n in r.get("versions", []):
                _ecrire(f"    version : {n}")
    return rc


def cmd_actualiser(a):
    r = bibliotheque.actualiser(forcer=a.forcer)
    _ecrire(f"Inchangés : {r['inchanges']} · importés : {len(r['importes'])} · réindexés : {len(r['reindexes'])}")
    for cle, titre in (("importes", "Importés"), ("a_confirmer", "MODIFIÉS SUR PLACE (à confirmer)"), ("reindexes", "Réindexés"), ("doublons", "Doublons ignorés"),
                       ("absents", "Sources disparues (passages retirés de l'index)"), ("echecs", "ÉCHECS"),
                       ("versions", "Versions remplacées")):
        if r[cle]:
            _ecrire(f"{titre} :")
            for x in r[cle]:
                _ecrire(f"  - {x}")
    return 2 if r["echecs"] else 0


def cmd_inventaire(a):
    docs = bibliotheque.inventaire()
    if a.json:
        return _json(docs)
    if not docs:
        return _ecrire("Bibliothèque vide. `telecharger --tous` (syllabus EN officiels) ou `importer <fichiers>`.")
    alertes = []
    _ecrire(f"{'document':24} {'type':8} {'niveau':11} {'date':10} {'pages':>5} {'passages':>8}  extraction / version")
    for d in docs:
        ver = {"courant": "", "remplace": f" → remplacé par {d['remplace_par']}",
               "a_confirmer": " (modifié sur place : à confirmer)"}.get(d["statut_version"], " (source absente)")
        retrait = catalogue.statut_officiel(d["code"])
        _ecrire(f"{d['doc_id']:24} {d['type'] or '?':8} {d['niveau'] or '?':11} {d['date_publication'] or '?':10} "
                f"{d['nb_pages'] or 0:>5} {d['nb_passages']:>8}  {d['statut_extraction']}{ver}"
                + (f" ⚠ {retrait}" if retrait else ""))
        if d["statut_extraction"] != "ok" or not d["code"] or not d["nb_titres"]:
            alertes.append(f"{d['doc_id']} : {d['statut_extraction']} — {d['message_extraction']}"
                           + ("" if d["code"] else " — code ISTQB non reconnu")
                           + ("" if d["nb_titres"] else " — aucune section détectée"))
    langues = {}
    for d in docs:
        if d["statut_version"] == "courant":
            langues.setdefault(d["langue"], set()).add(d["code"])
    _ecrire(f"\n{len(docs)} fichiers · versions courantes : "
            + ", ".join(f"{len(v)} codes en {k}" for k, v in sorted(langues.items())))
    manquants = [d["code"] for d in bibliotheque.catalogue()["documents"]
                 if not any(d["code"] in v for v in langues.values())]
    if manquants:
        _ecrire(f"Absents du catalogue officiel : {', '.join(manquants)}")
    perime = bibliotheque.avertissement_index()
    if perime:
        alertes.insert(0, perime)
    if alertes:
        _ecrire("\nÀ surveiller :")
        for x in alertes:
            _ecrire(f"  - {x}")


def cmd_manquants(a):
    r = bibliotheque.manquants()
    if a.json:
        return _json(r)
    _ecrire(f"{'code':10} {'niveau':11} {'anglais':22} {'français':22} titre")
    for l in r["catalogue"]:
        if a.langue and l[a.langue]:
            continue
        _ecrire(f"{l['code']:10} {l['niveau']:11} {l['en'] or '— MANQUANT':22} {l['fr'] or '— manquant':22} "
                f"{l['titre'][:45]}" + (f"  [remplacés : {', '.join(l['remplaces'])}]" if l["remplaces"] else "")
                + (f"  ⚠ {', '.join(l['a_surveiller'])}" if l["a_surveiller"] else "")
                + (f"  ⚠ {catalogue.statut_officiel(l['code'])}" if l["statut_officiel"] else ""))
    _ecrire(f"\nCatalogue officiel : {len(r['catalogue'])} syllabus · manquants en anglais : "
            f"{len(r['absents_en'])} · sans traduction française locale : {len(r['absents_fr'])}")
    if r["absents_en"]:
        _ecrire(f"Récupérer les officiels : python qa.py telecharger {' '.join(r['absents_en'])}")
    if r["absents_fr"]:
        _ecrire("Traductions françaises : non téléchargeables automatiquement — déposer le PDF (CFTL) dans "
                "bibliotheque/sources/ puis `python qa.py actualiser` (skill /ajouter-syllabus).")
    if r["hors_catalogue"]:
        _ecrire(f"Documents locaux hors catalogue : {', '.join(r['hors_catalogue'])}")


def cmd_corriger(a):
    if not any(getattr(a, k) for k in ("code", "titre", "niveau", "domaine", "version", "langue", "date", "source",
                                       "type")):
        raise ErreurValidation("Rien à corriger : préciser au moins un champ (--version, --date AAAA-MM-JJ, "
                               "--langue fr|en, --niveau…).")
    champs = {"code": a.code, "titre": a.titre, "niveau": a.niveau, "domaine": a.domaine, "version": a.version,
              "langue": a.langue, "date_publication": a.date, "source_officielle": a.source, "type": a.type}
    e = bibliotheque.modifier_metadonnees(a.doc_id, **champs)
    _ecrire(f"{e['doc_id']} mis à jour (champs forcés : {', '.join(e['champs_forces'])}). "
            "L'identifiant reste inchangé ; relancer `inventaire` pour vérifier les versions.")


def cmd_retirer(a):
    e = bibliotheque.retirer(a.doc_id, a.supprimer_fichier)
    dossier = "bibliotheque/prive" if e["prive"] else "bibliotheque/sources"
    if e["fichier_supprime"]:
        _ecrire(f"{a.doc_id} retiré de la bibliothèque privée ; fichier {dossier}/{e['fichier']} supprimé.")
    else:
        _ecrire(f"{a.doc_id} retiré de la bibliothèque. Fichier conservé : {dossier}/{e['fichier']} "
                "(le déplacer hors du dossier, sinon `actualiser` le réimportera"
                + (" ; ou `--supprimer-fichier`)." if e["prive"] else ")."))


def cmd_chercher(a):
    r = recherche.chercher(" ".join(a.requete), n=a.n, docs=a.doc, niveau=a.niveau, langue=a.langue,
                           section=a.section, theme=a.theme, toutes_versions=a.toutes_versions,
                           inclure_sommaires=a.sommaires, par_doc=a.par_doc)
    perime = bibliotheque.avertissement_index()
    if perime:
        r["avertissements"] = [perime, *r.get("avertissements", [])]
    if a.json:
        return _json(r)
    _ecrire(f"Notions : {', '.join(r['groupes']) or '—'}" + (f" · thème : {a.theme}" if a.theme else ""))
    for i, x in enumerate(r["resultats"], 1):
        sec = f"§{x['section_num']} {x['section_titre']}".strip() if x["section_num"] or x["section_titre"] else "§ ?"
        _ecrire(f"\n[{i}] {_ref_doc(x)}")
        _ecrire(f"    {_ref_page(x)} · {sec} · passage #{x['id']}"
                + (" · PARTIEL : " + ", ".join(x["groupes_trouves"]) if x["partiel"] else ""))
        _ecrire(f"    {' '.join(x['extrait'].split())}")
    for w in r["avertissements"]:
        _ecrire(f"\n⚠ {w}")
    c = r["couverture_lexicale"]
    _ecrire(f"\nCouverture lexicale : {c['score']}/100 ({c['libelle']}) — {' ; '.join(c['raisons'])}")
    if r["resultats"]:
        _ecrire(f"(socle documentaire, pas une confiance : après lecture, `confiance --base {c['score']} --lus N …` "
                "calcule le score de la réponse)")
        _ecrire("\nLire avant de citer : `lire <passage>` (--contexte 1) ou `section <doc> <num>`.")


def cmd_confiance(a):
    from . import confiance
    r = confiance.calculer(a.base, a.lus, a.concordants, ancien=bool(a.ancien), contradiction=bool(a.contradiction),
                           web=bool(a.web), raisonnement=bool(a.raisonnement), non_couvert=bool(a.non_couvert))
    if a.json:
        return _json(r)
    for ligne in r["calcul"]:
        _ecrire(ligne)
    _ecrire(f"\nConfiance : {r['score']}/100 ({r['libelle']})")


def _afficher_passages(rows: list[dict], doc: dict | None = None):
    courant = None
    for p in rows:
        d = doc or p
        sec = f"§{p['section_num']} {p['section_titre']}".strip()
        cle = (p["doc_id"], p["page"], sec)
        if cle != courant:
            _ecrire(f"\n── {_ref_doc({**d, 'doc_id': p['doc_id']})} · {_ref_page(p)} · {sec} (passage #{p['id']})")
            courant = cle
        _ecrire(p["texte"])


def cmd_lire(a):
    rows = recherche.lire_passage(a.passage, a.contexte)
    _json(rows) if a.json else _afficher_passages(rows)


def _plage_pages(texte: str) -> tuple[int, int | None]:
    m = re.fullmatch(r"\s*(\d+)\s*(?:-\s*(\d+)\s*)?", texte)
    if not m or int(m[1]) < 1 or (m[2] and int(m[2]) < int(m[1])):
        raise ErreurValidation(f"Pages attendues : un numéro ou une plage croissante (ex. 31 ou 31-33), "
                               f"reçu : « {texte} ».")
    return int(m[1]), int(m[2]) if m[2] else None


MAX_CARACTERES = 15000   # sortie de `page` / `section` : ~4 000 tokens, lisible en une fois


def _borner(passages: list[dict], maximum: int) -> tuple[list[dict], list[dict]]:
    """(affichés, restants) : des passages entiers jusqu'à `maximum` caractères (au moins un).
    maximum <= 0 : pas de limite."""
    if maximum <= 0:
        return passages, []
    total = 0
    for i, p in enumerate(passages):
        total += len(p["texte"])
        if total > maximum and i:
            return passages[:i], passages[i:]
    return passages, []


def _reste_a_lire(doc_id: str, affiches: list[dict], restants: list[dict]) -> list[str]:
    """Commandes qui affichent la suite : la fin de la sous-section coupée (`page`), puis
    chaque sous-section restante (`section`), dans l'ordre du document."""
    lignes, vues = [], set()
    coupee = affiches[-1]["section_num"] if affiches else None
    for p in restants:
        num = p["section_num"]
        if num in vues:
            continue
        vues.add(num)
        pages = [q["page"] for q in restants if q["section_num"] == num]
        etendue = f"{min(pages)}" if min(pages) == max(pages) else f"{min(pages)}-{max(pages)}"
        titre = f"§{num} {p['section_titre']}".strip() if num or p["section_titre"] else "hors section"
        if num == coupee or not num:
            lignes.append(f"  - suite de {titre} : `page {doc_id} {etendue}`")
        else:
            lignes.append(f"  - {titre} (p. {etendue}) : `section {doc_id} {num}`")
    return lignes


def _afficher_borne(r: dict, maximum: int, json_: bool, par_pages: bool = False) -> None:
    affiches, restants = _borner(r["passages"], maximum)
    doc_id = r["document"]["doc_id"]
    reste = _reste_a_lire(doc_id, affiches, restants) if restants else []
    if restants and par_pages:
        pages = [p["page"] for p in restants]
        reste.insert(0, f"  - pages restantes : `page {doc_id} {min(pages)}-{max(pages)}`"
                        if min(pages) != max(pages) else f"  - page restante : `page {doc_id} {min(pages)}`")
    if json_:
        return _json({**r, "passages": affiches, "tronque": bool(restants),
                      "reste_a_lire": [l.strip(" -") for l in reste]})
    _afficher_passages(affiches, r["document"])
    if restants:
        affiche = sum(len(p["texte"]) for p in affiches)
        total = affiche + sum(len(p["texte"]) for p in restants)
        _ecrire(f"\n✂ Sortie tronquée : {affiche} caractères affichés sur {total} "
                f"({len(affiches)}/{len(affiches) + len(restants)} passages). Ne citer que ce qui précède. "
                "Reste à lire :")
        for ligne in reste:
            _ecrire(ligne)
        _ecrire("  (ou relancer avec --max-caracteres 0 pour tout afficher)")


def cmd_page(a):
    r = recherche.lire_pages(a.doc, *_plage_pages(a.pages))
    if not r["passages"] and not a.json:
        return _ecrire(f"Aucun texte indexé pour ces pages de {r['document']['doc_id']} "
                       f"({r['document']['nb_pages']} pages ; pages vides : {r['document']['pages_vides'] or 'aucune'}).")
    _afficher_borne(r, a.max_caracteres, a.json, par_pages=True)


def cmd_section(a):
    r = recherche.lire_section(a.doc, a.numero)
    if not r["passages"] and not a.json:
        return _ecrire(f"Section {a.numero} introuvable dans {r['document']['doc_id']} : voir `plan {a.doc}`.")
    _afficher_borne(r, a.max_caracteres, a.json)


def cmd_plan(a):
    r = recherche.plan(a.doc)
    if a.json:
        return _json(r)
    _ecrire(_ref_doc(r["document"]))
    for s in r["sections"]:
        if s["numero"] or a.tout:
            prof = s["numero"].count(".") if s["numero"] else 3
            _ecrire(f"{'  ' * prof}{s['numero']} {s['titre']}  (p. {s['page']})")


# ---------------------------------------------------------------- taxonomie

def cmd_themes(a):
    compte = {}
    for i in connaissances.lister():
        compte[i["theme_principal"]] = compte.get(i["theme_principal"], 0) + 1
    if a.json:
        return _json(taxonomie.themes())
    for niveau, t in taxonomie.arbre():
        etat = "" if t["statut"] == "actif" else f"  [OBSOLÈTE → {t.get('remplace_par') or '—'}]"
        nb = f"  ({compte[t['code']]} idées)" if t["code"] in compte else ""
        _ecrire(f"{'  ' * niveau}{t['code']:<{28 - 2 * niveau}} {t['libelle']}{nb}{etat}")


def cmd_theme(a):
    if a.action == "ajouter":
        t = taxonomie.ajouter(a.code, a.libelle, a.parent, [m.strip() for m in (a.mots_cles or "").split(",") if m.strip()],
                              a.motif, a.forcer)
        _ecrire(f"Thème ajouté : {taxonomie.chemin(t['code'])} ({t['code']})")
    elif a.action == "obsolete":
        taxonomie.rendre_obsolete(a.code, a.remplace_par, a.motif)
        _ecrire(f"Thème {a.code} marqué obsolète" + (f", remplacé par {a.remplace_par}" if a.remplace_par else "")
                + ". Les idées existantes gardent leur classement historique.")
    elif a.action == "proposer":
        for score, code in taxonomie.proposer(a.code):
            _ecrire(f"  {code:26} {taxonomie.chemin(code)}  (score {score})")


def cmd_couverture(a):
    rows = connaissances.couverture()
    if a.json:
        return _json(rows)
    _ecrire(f"{'thème':40} {'idées':>5} {'passages':>8}  état")
    for r in rows:
        _ecrire(f"{'  ' * r['niveau'] + r['libelle'][:38 - 2 * r['niveau']]:40} {r['idees']:>5} "
                f"{r['passages'] if r['passages'] is not None else '—':>8}  {r['etat']}")
    pistes = sorted((r for r in rows if r["etat"] != "correct" and (r["passages"] or 0) > 0),
                    key=lambda r: -(r["passages"] or 0))[:5]
    if pistes:
        _ecrire("\nThèmes pauvres en idées mais documentés dans les syllabus (pistes d'exploration) : "
                + ", ".join(f"{r['code']} ({r['passages']} passages)" for r in pistes))


# ---------------------------------------------------------------- idées

def _afficher_doublons(sim: list[dict]):
    for s in sim:
        _ecrire(f"  {s['verdict'].upper():16} {s['id']} « {s['titre']} » (similarité {s['score']}, {s['statut']})")


CHAMPS_DOUBLONS = ("titre", "resume", "probleme", "principe")


def cmd_idee(a):
    act = a.action
    if act == "modele":
        return _json(MODELE_IDEE)
    if act == "ajouter":
        r = connaissances.ajouter(_lire_donnees(a.fichier), forcer=a.forcer, motif=a.motif)
        if r["etat"] == "refuse":
            _ecrire(f"REFUSÉ — {r['message']}")
        else:
            _ecrire(f"Idée créée : {r['id']}")
        _afficher_doublons(r["doublons"])
        for w in r["avertissements"]:
            _ecrire(f"  ⚠ {w}")
        if r["etat"] == "refuse":
            return 2
    elif act == "doublons":
        # Forme en une ligne, sans accolades (#128) : en `claude -p`, un heredoc contenant
        # du JSON est bloqué par le contrôle d'expansion de Claude Code.
        champs = {k: getattr(a, k) for k in CHAMPS_DOUBLONS if getattr(a, k)}
        if champs and a.theme:
            champs["theme_principal"] = a.theme
        d, _ = connaissances.valider(champs or _lire_donnees(a.fichier), partiel=True)
        sim = connaissances.doublons(d)
        _ecrire("Aucune idée similaire." if not sim else "Idées similaires :")
        _afficher_doublons(sim)
        _ecrire("Thèmes suggérés : " + ", ".join(c for _, c in taxonomie.proposer(
            " ".join(str(d.get(k, "")) for k in ("titre", "resume", "principe")))))
    elif act == "modifier":
        r = connaissances.modifier(a.id, _lire_donnees(a.fichier), a.remplacer_listes, a.motif, a.forcer)
        _ecrire(f"{a.id} : {r['etat']}" + (f" ({', '.join(r['champs'])})" if r.get("champs") else ""))
        for w in r["avertissements"]:
            _ecrire(f"  ⚠ {w}")
    elif act == "statut":
        r = connaissances.changer_statut(a.id, a.statut, a.motif)
        _ecrire(f"{a.id} : {r['avant']} → {r['apres']}")
    elif act == "retour":
        r = connaissances.ajouter_retour(a.id, a.contexte, a.resultat, a.enseignement, a.date, a.forcer, a.motif)
        _ecrire(f"{a.id} : retour d'expérience enregistré ({r['retours']} au total)")
    elif act == "lier":
        if not a.cible or not a.type:
            raise ErreurValidation("Usage : idee lier QA-xxxx QA-yyyy --type "
                                   f"{'|'.join(connaissances.RELATIONS)} [--note …]")
        r = connaissances.lier(a.id, a.cible, a.type, a.note)
        _ecrire(f"{r['source']} —{r['type']}→ {r['cible']}")
    elif act == "retirer":
        r = connaissances.retirer(a.id, a.motif)
        _ecrire(f"{a.id} retirée (instantané conservé dans le journal)")
        for x in r["relations_entrantes_retirees"]:
            _ecrire(f"  relation {x['type']} depuis {x['source']} retirée")
    elif act == "voir":
        i = connaissances.voir(a.id)
        if a.json:
            return _json(i)
        _ecrire(f"{i['id']} — {i['titre']}")
        _ecrire(f"Thème : {taxonomie.chemin(i['theme_principal'])}"
                + (f" · secondaires : {', '.join(i['themes_secondaires'])}" if i["themes_secondaires"] else ""))
        _ecrire(f"Statut : {connaissances.STATUTS[i['statut']]} · maturité : {i['maturite']} "
                f"({connaissances.MATURITES[i['maturite']]})")
        _ecrire(f"Créée le {i['cree_le'][:10]} · mise à jour le {i['maj_le'][:10]} · provenance : {i.get('provenance', '?')}")
        for k, lib in (("resume", "Résumé"), ("probleme", "Problème"), ("principe", "Principe"),
                       ("domaine_application", "Domaine d'application"), ("prerequis", "Prérequis"),
                       ("benefices", "Bénéfices"), ("limites", "Limites et risques")):
            if i.get(k):
                _ecrire(f"\n{lib} : {i[k]}")
        if i["references"]:
            _ecrire("\nRéférences :")
            for r in i["references"]:
                loc = " ".join(x for x in (r.get("doc_id"), f"p. {r['pages']}" if r.get("pages") else "",
                                           f"§{r['section']}" if r.get("section") else "") if x)
                _ecrire(f"  - [{r['type']}] {r.get('titre', '')} {loc} {r.get('url', '')}".rstrip()
                        + (f" — « {r['extrait']} »" if r.get("extrait") else ""))
        for r in i["relations"]:
            _ecrire(f"  → {r['type']} {r['cible']} « {r['titre']} »" + (f" ({r['note']})" if r.get("note") else ""))
        for r in i["relations_entrantes"]:
            _ecrire(f"  ← {r['type']} depuis {r['source']} « {r['titre']} »")
        for r in i["retours"]:
            _ecrire(f"\nRetour {r.get('date', '')} : {r.get('contexte', '')} → {r.get('resultat', '')}"
                    + (f" — enseignement : {r['enseignement']}" if r.get("enseignement") else ""))
    elif act == "lister":
        rows = connaissances.lister(a.theme, a.statut)
        if a.json:
            return _json(rows)
        if not rows:
            return _ecrire("Aucune idée" + (f" pour le thème {a.theme}" if a.theme else "") + ".")
        for r in rows:
            _ecrire(f"{r['id']}  {r['theme_principal']:22} {r['statut']:12} {r['maturite']:10} {r['titre']}")
    elif act == "chercher":
        rows = connaissances.chercher(" ".join(a.requete or []), theme=a.theme)
        if a.json:
            return _json(rows)
        if not rows:
            return _ecrire("Aucune idée capitalisée ne correspond.")
        for r in rows:
            _ecrire(f"{r['id']}  [{r['statut']}/{r['maturite']}] {r['titre']} ({r['theme_principal']})")
            _ecrire(f"        {' '.join(r['extrait'].split())}")
    elif act == "verifier-refs":
        rows = connaissances.verifier_references()
        ko = [r for r in rows if r["problemes"]]
        _ecrire(f"{len(rows)} références ISTQB contrôlées, {len(ko)} à revoir.")
        for r in ko:
            _ecrire(f"  {r['idee']} {r['doc_id']} p. {r['pages']} : {'; '.join(r['problemes'])}")


def cmd_journal(a):
    for e in journal.lire(a.cible, a.n):
        _ecrire(f"{e['horodatage']} {e.get('auteur', '?'):12} {e['action']:20} {e['cible']}"
                + (f" — {e['motif']}" if e.get("motif") else ""))
        if a.details and e.get("details"):
            for ligne in json.dumps(e["details"], ensure_ascii=False, indent=1).splitlines():
                _ecrire(f"      {ligne}")


def cmd_diagnostic(a):
    from . import diagnostic
    noms = list(diagnostic.ASSISTANTS) if a.assistant == "tous" else [a.assistant] if a.assistant else []
    etats = diagnostic.diagnostic(noms)
    for etat, sujet, detail in etats:
        _ecrire(f"{etat:3} {sujet:26} {detail}")
    ko = sum(e[0] == "KO" for e in etats)
    _ecrire(f"\nDiagnostic : {'OK' if not ko else f'KO ({ko} point(s) bloquant(s))'}")
    if ko:
        raise SystemExit(1)


def cmd_evaluer(a):
    from . import evaluation
    r = evaluation.evaluer(a.k, {"reglage": False, "controle": True}.get(a.jeu))
    for x in r["details"]:
        _ecrire(f"{'OK ' if x['trouve'] else 'KO '} rang {x['rang'] or '-':>2}  {x['requete']}  → attendu {x['attendu']}")
    _ecrire(f"\nRappel@{a.k} : {r['rappel']:.0%} ({r['trouves']}/{r['total']}) · MRR : {r['mrr']:.2f}"
            + (f" · ignorées (document absent) : {r['ignorees']}" if r["ignorees"] else ""))
    if a.min_rappel is not None:
        # Seuil de non-régression (CI) : un jeu sans question évaluée n'atteint aucun seuil.
        if not r["total"]:
            raise ErreurValidation("aucune question évaluée (bibliothèque vide ou documents attendus absents) : "
                                   "lancer `actualiser` avant `evaluer --min-rappel`.")
        if r["rappel"] < a.min_rappel:
            raise ErreurValidation(f"rappel@{a.k} {r['rappel']:.0%} sous le seuil exigé "
                                   f"({a.min_rappel:.0%}) : la recherche a régressé.")


# ---------------------------------------------------------------- analyseur

NIVEAUX = ["fondation", "avance", "expert", "specialiste"]


def _date_iso(v: str) -> str:
    from datetime import date
    try:
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", v):
            return date.fromisoformat(v).isoformat()
    except ValueError:
        pass
    raise argparse.ArgumentTypeError(f"date AAAA-MM-JJ attendue (reçu : {v})")


def _entier_positif(v: str) -> int:
    try:
        n = int(v)
    except ValueError:
        n = 0
    if n < 1:
        raise argparse.ArgumentTypeError(f"entier ≥ 1 attendu (reçu : {v})")
    return n


def _proportion(v: str) -> float:
    try:
        r = float(v.replace(",", "."))
    except ValueError:
        r = -1.0
    if not 0 <= r <= 1:
        raise argparse.ArgumentTypeError(f"proportion entre 0 et 1 attendue, ex. 0.80 (reçu : {v})")
    return r


def analyseur() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="qa.py", description="QA Knowledge Agent — bibliothèque ISTQB et base QA.")
    sp = p.add_subparsers(dest="commande", required=True)

    def meta(x):
        for opt in ("code", "titre", "domaine", "version", "source"):
            x.add_argument(f"--{opt}")
        x.add_argument("--niveau", choices=NIVEAUX)
        x.add_argument("--langue", choices=["fr", "en"])
        x.add_argument("--type", choices=["syllabus", "bok", "glossaire", "notes", "examen", "document"])
        x.add_argument("--date", type=_date_iso, help="date de publication AAAA-MM-JJ")

    x = sp.add_parser("catalogue", help="syllabus officiels ISTQB et présence locale")
    x.add_argument("--verifier", action="store_true", help="interroger istqb.org (nouvelles versions)")
    x.add_argument("--niveau", choices=NIVEAUX)
    x.set_defaults(f=cmd_catalogue)
    x = sp.add_parser("telecharger", help="télécharger des syllabus officiels (istqb.org) et les indexer")
    x.add_argument("codes", nargs="*")
    x.add_argument("--tous", action="store_true")
    x.add_argument("--niveau", choices=NIVEAUX)
    x.set_defaults(f=cmd_telecharger)
    x = sp.add_parser("importer", help="importer des PDF / .txt / .md (fichiers ou dossiers)")
    x.add_argument("fichiers", nargs="+")
    meta(x)
    x.add_argument("--remplacer", action="store_true",
                   help="confirmer le nouveau contenu d'un fichier modifié sur place (avec --motif, journalisé)")
    x.add_argument("--motif", help="raison du remplacement (obligatoire avec --remplacer)")
    x.add_argument("--prive", action="store_true",
                   help="document interne : copié dans bibliotheque/prive/ (jamais versionné), pas dans sources/")
    x.set_defaults(f=cmd_importer)
    x = sp.add_parser("actualiser", help="réindexation incrémentale de bibliotheque/sources/")
    x.add_argument("--forcer", action="store_true", help="tout réextraire")
    x.set_defaults(f=cmd_actualiser)
    x = sp.add_parser("inventaire", help="documents indexés, versions, extractions à surveiller")
    x.add_argument("--json", action="store_true")
    x.set_defaults(f=cmd_inventaire)
    x = sp.add_parser("manquants", help="syllabus du catalogue officiel non indexés (par langue)")
    x.add_argument("--langue", choices=["en", "fr"], help="ne lister que les manquants dans cette langue")
    x.add_argument("--json", action="store_true")
    x.set_defaults(f=cmd_manquants)
    x = sp.add_parser("corriger", help="corriger les métadonnées détectées d'un document")
    x.add_argument("doc_id")
    meta(x)
    x.set_defaults(f=cmd_corriger)

    x = sp.add_parser("retirer", help="retirer un document de la bibliothèque (manifeste + index)")
    x.add_argument("doc_id")
    x.add_argument("--supprimer-fichier", action="store_true",
                   help="document privé seulement : supprime aussi le fichier de bibliotheque/prive/")
    x.set_defaults(f=cmd_retirer)

    x = sp.add_parser("chercher", help="recherche plein texte dans la bibliothèque")
    x.add_argument("requete", nargs="+")
    x.add_argument("-n", type=_entier_positif, default=8)
    x.add_argument("--doc", action="append", help="code ou doc_id (répétable)")
    x.add_argument("--niveau", choices=NIVEAUX)
    x.add_argument("--langue", choices=["fr", "en"])
    x.add_argument("--section", help="numéro de section, sous-sections incluses (ex. 4.2)")
    x.add_argument("--theme", help="code de thème de la taxonomie")
    x.add_argument("--toutes-versions", action="store_true", help="inclure les versions remplacées")
    x.add_argument("--sommaires", action="store_true", help="inclure tables des matières et index")
    x.add_argument("--par-doc", type=int, default=3, help="résultats max par document (défaut 3)")
    x.add_argument("--json", action="store_true")
    x.set_defaults(f=cmd_chercher)
    x = sp.add_parser("confiance", help="score de confiance d'une réponse, calculé avec la grille du skill")
    x.add_argument("--base", type=int, required=True, help="couverture lexicale de la requête principale (chercher)")
    x.add_argument("--lus", type=int, required=True, help="passages réellement lus (lire / section / page)")
    x.add_argument("--concordants", type=int, required=True, help="syllabus courants concordants, passages lus")
    for opt, aide in (("ancien", "seul un syllabus ancien (avant 2017) ou remplacé couvre le sujet"),
                      ("contradiction", "syllabus contradictoires non arbitrés"),
                      ("web", "une partie de la réponse repose sur le Web"),
                      ("raisonnement", "une partie repose sur un raisonnement sans source"),
                      ("non-couvert", "une notion de la question n'est couverte ni par un passage lu ni par le Web")):
        x.add_argument(f"--{opt}", type=int, choices=[0, 1], default=0, help=aide)
    x.add_argument("--json", action="store_true")
    x.set_defaults(f=cmd_confiance)
    x = sp.add_parser("lire", help="lire un passage (et son contexte)")
    x.add_argument("passage", type=int)
    x.add_argument("--contexte", type=int, default=0)
    x.add_argument("--json", action="store_true")
    x.set_defaults(f=cmd_lire)
    x = sp.add_parser("page", help="lire des pages d'un document (ex. 31 ou 31-33)")
    x.add_argument("doc")
    x.add_argument("pages")
    x.add_argument("--json", action="store_true")
    x.add_argument("--max-caracteres", type=int, default=MAX_CARACTERES,
                   help=f"borne de la sortie (défaut {MAX_CARACTERES} ; 0 = sans limite) : la fin indique quoi lire ensuite")
    x.set_defaults(f=cmd_page)
    x = sp.add_parser("section", help="lire une section entière (sous-sections incluses)")
    x.add_argument("doc")
    x.add_argument("numero")
    x.add_argument("--json", action="store_true")
    x.add_argument("--max-caracteres", type=int, default=MAX_CARACTERES,
                   help=f"borne de la sortie (défaut {MAX_CARACTERES} ; 0 = sans limite) : la fin indique quoi lire ensuite")
    x.set_defaults(f=cmd_section)
    x = sp.add_parser("plan", help="plan (sections) d'un document")
    x.add_argument("doc")
    x.add_argument("--tout", action="store_true", help="inclure les titres non numérotés")
    x.add_argument("--json", action="store_true")
    x.set_defaults(f=cmd_plan)

    x = sp.add_parser("themes", help="taxonomie QA")
    x.add_argument("--json", action="store_true")
    x.set_defaults(f=cmd_themes)
    x = sp.add_parser("theme", help="ajouter / rendre obsolète / proposer un thème")
    x.add_argument("action", choices=["ajouter", "obsolete", "proposer"])
    x.add_argument("code", help="code du thème (ou texte à classer pour « proposer »)")
    x.add_argument("--libelle")
    x.add_argument("--parent")
    x.add_argument("--mots-cles", help="liste séparée par des virgules (FR et EN)")
    x.add_argument("--remplace-par")
    x.add_argument("--motif")
    x.add_argument("--forcer", action="store_true")
    x.set_defaults(f=cmd_theme)
    x = sp.add_parser("couverture", help="richesse de la base par thème (et matière disponible)")
    x.add_argument("--json", action="store_true")
    x.set_defaults(f=cmd_couverture)

    x = sp.add_parser("idee", help="base de connaissances : ajouter, modifier, chercher…")
    x.add_argument("action", choices=["modele", "ajouter", "doublons", "modifier", "statut", "retour", "lier",
                                      "retirer", "voir", "lister", "chercher", "verifier-refs"])
    x.add_argument("id", nargs="?", help="identifiant QA-xxxx")
    x.add_argument("requete", nargs="*", help="texte (pour chercher)")
    x.add_argument("--fichier", default="-", help="JSON de l'idée (défaut : entrée standard)")
    for champ in CHAMPS_DOUBLONS:
        x.add_argument(f"--{champ}", help="doublons : champ de l'idée en une ligne, sans JSON (avec --theme)")
    x.add_argument("--forcer", action="store_true")
    x.add_argument("--motif")
    x.add_argument("--remplacer-listes", action="store_true")
    x.add_argument("--statut")
    x.add_argument("--theme")
    x.add_argument("--contexte")
    x.add_argument("--resultat")
    x.add_argument("--enseignement")
    x.add_argument("--date")
    x.add_argument("--cible")
    x.add_argument("--type", choices=list(connaissances.RELATIONS))
    x.add_argument("--note")
    x.add_argument("--json", action="store_true")
    x.set_defaults(f=cmd_idee)
    x = sp.add_parser("journal", help="historique des modifications")
    x.add_argument("--cible")
    x.add_argument("-n", type=int, default=30)
    x.add_argument("--details", action="store_true", help="détails de chaque entrée (avant/après, anomalies)")
    x.set_defaults(f=cmd_journal)
    x = sp.add_parser("diagnostic", help="contrôle de l'installation (index, recherche témoin, intégrations)")
    x.add_argument("--assistant", choices=["claude", "copilot", "gemini", "tous"],
                   help="vérifie aussi les fichiers et la CLI de cet assistant")
    x.set_defaults(f=cmd_diagnostic)
    x = sp.add_parser("evaluer", help="mesure la qualité de la recherche sur eval/requetes.json")
    x.add_argument("-k", type=_entier_positif, default=5)
    x.add_argument("--jeu", choices=["tout", "reglage", "controle"], default="tout",
                   help="« controle » = questions jamais utilisées pour régler le moteur")
    x.add_argument("--min-rappel", type=_proportion, metavar="R",
                   help="code retour 2 si le rappel est sous R (0 à 1) ou si aucune question n'est évaluée")
    x.set_defaults(f=cmd_evaluer)
    return p


def main(argv=None) -> int:
    for flux in (sys.stdout, sys.stderr):  # console Windows : sorties et erreurs en UTF-8
        if hasattr(flux, "reconfigure"):
            flux.reconfigure(encoding="utf-8")
    a = analyseur().parse_args(argv)
    try:
        if a.commande == "idee":
            _normaliser_idee(a)
        rc = a.f(a)
    except BrokenPipeError:  # sortie tronquée (`| head`) : pas une erreur
        sys.stderr.close()
        return 0
    except (ErreurValidation, KeyError, ValueError, PermissionError, FileNotFoundError) as exc:
        msg = exc.args[0] if exc.args else str(exc)
        sys.stderr.write(f"Erreur : {msg}\n")
        return 2
    except sqlite3.OperationalError as exc:
        if "locked" in str(exc) or "busy" in str(exc):
            sys.stderr.write("Erreur : la base est occupée par une autre commande (`actualiser`, import…) "
                             "depuis plus de 30 s. Relancer quand elle sera terminée.\n")
        else:
            sys.stderr.write(f"Erreur : base SQLite inutilisable ({exc}). Reconstruire l'index : "
                             "`python qa.py actualiser --forcer`.\n")
        return 2
    finally:
        # Base reconstruite depuis un JSONL modifié hors de l'outil : prévenir l'utilisateur.
        for w in connaissances.avertissements():
            if not sys.stderr.closed:
                sys.stderr.write(f"⚠ {w}\n")
    return rc if isinstance(rc, int) else 0


def _normaliser_idee(a) -> None:
    """« idee chercher texte libre » : l'id positionnel est alors le début de la requête ;
    « idee statut QA-1 validee » : le 2e positionnel est le statut."""
    if a.action in ("chercher",):
        a.requete = ([a.id] if a.id else []) + (a.requete or [])
        a.id = None
    elif a.action == "statut" and not a.statut and a.requete:
        a.statut = a.requete[0]
    elif a.action == "lier" and not a.cible and a.requete:
        a.cible = a.requete[0]
    elif a.action == "lister" and (a.id or a.requete):
        raise ErreurValidation("`idee lister` ne prend pas de texte : utiliser --theme <code> / --statut, "
                         "ou `idee chercher <texte>`.")
    besoin_id = {"modifier", "statut", "retour", "lier", "retirer", "voir"}
    if a.action in besoin_id and not a.id:
        raise ErreurValidation(f"`idee {a.action}` attend un identifiant (QA-xxxx).")
