"""Règle unique « une citation est-elle lue ? » (#275), partagée par le relevé du serveur MCP
(`passages_lus`, #206) et le contrôle des essais (`scripts/essais_agents.py`).

Une citation `[DOC, §x.y, p. N]` (ou `pp. N-M`) n'est LUE que si CHAQUE page citée a été
affichée, dans le même document ET dans la section citée ou l'une de ses sous-sections
(`section x.y` affiche aussi x.y.1, x.y.2…). Une page affichée sous une section sœur ne
suffit pas : §1.3 qui commence sur la page où se termine §1.2 n'a pas été lue pour autant.
Une plage de sections (`§1.3.1 à §1.3.5`, `§1.3.1-1.3.2`) couvre chaque section de la
plage et leurs sous-sections.

Le document est identifié par son sigle, sa version et sa langue (#280), qu'il soit écrit
comme un identifiant (`CT-MAT-2019-fr`, en-tête de passage) ou comme une référence
(`CT-MAT v2019 FR`, ligne « Citer : ») : CT-MAT FR p. 18 n'est pas CT-MAT EN p. 18, et
CTAL-TA 2019 n'est pas CTAL-TA v4.0. Un Body of Knowledge (`BoK`) n'est pas le syllabus."""
import re
from collections.abc import Iterable

_NUM = r"[0-9A-Za-z]+(?:\.[0-9A-Za-z]+)*"
_NUMERO = re.compile(rf"§?\s*({_NUM})")
# « 1.3.1 à 1.3.5 », « 1.3 à §1.3.6 », « 1.3.1-1.3.2 », « 2.1.2–2.1.3 » (second numéro : un chiffre d'abord).
_PLAGE = re.compile(rf"§?\s*({_NUM})\s*(?:à|au|-|–)\s*§?\s*([0-9]+(?:\.[0-9A-Za-z]+)*)")


def numero_section(texte: str) -> str:
    """Numéro de section d'un fragment de référence : `§1.3.2` (« Citer : »), `§1.3.2 Titre`
    (en-tête de passage), `§3.2 à 3.2.5 (pp. 35-37` (réponse d'agent) → `1.3.2`, `3.2` ;
    chaîne vide si le fragment ne nomme aucune section."""
    m = _NUMERO.match((texte or "").strip())
    return m[1].rstrip(".") if m else ""


def bornes_section(texte: str) -> tuple[str, str]:
    """(première, dernière) section citée : `§1.3.1 à 1.3.5` → (`1.3.1`, `1.3.5`) ;
    une section seule donne deux bornes égales."""
    m = _PLAGE.match((texte or "").strip())
    if m:
        return m[1].rstrip("."), m[2].rstrip(".")
    n = numero_section(texte)
    return n, n


# Identifiant (`CTFL-4.0.1-en`, `CT-ATLaS-BoK-2.0-fr`) ou référence (`CTFL v4.0.1 EN`,
# `CT-MAT 2019 FR`, `CTAL-TM`) : sigle, puis BoK, version et langue, chacun facultatif.
_DOCUMENT = re.compile(r"(?P<sigle>.+?)(?:[\s-]+(?P<bok>BoK))?(?:[\s-]+v?(?P<version>\d+(?:\.\d+)*|\?))?"
                       r"(?:[\s-]+(?P<langue>en|fr))?", re.I)


def identite_document(texte: str) -> tuple[str, bool, str, str]:
    """(sigle, BoK ?, version, langue) d'un document : `CT-MAT-2019-fr` et `CT-MAT v2019 FR`
    donnent tous deux (`CT-MAT`, False, `2019`, `fr`). Version sans « v » ni « .0 » final
    (`v4.0` = `4`) ; chaîne vide pour ce que le texte ne précise pas (`CTAL-TM` seul)."""
    m = _DOCUMENT.fullmatch(" ".join((texte or "").split()))
    if not m:
        return "", False, "", ""
    version = re.sub(r"(?:\.0)+$", "", m["version"] or "").replace("?", "")
    return m["sigle"].upper(), bool(m["bok"]), version, (m["langue"] or "").lower()


def meme_document(a: str, b: str) -> bool:
    """`a` et `b` désignent-ils le même document ? Même sigle et même nature (BoK ou
    syllabus) ; version et langue identiques dès que les deux les précisent. Une référence
    qui tait sa langue ou sa version (`CTAL-TM, §1.3, p. 29`) n'est pas contredite par
    elle ; une référence qui en nomme une autre que la lecture l'est (#280)."""
    sa, ba, va, la = identite_document(a)
    sb, bb, vb, lb = identite_document(b)
    return bool(sa) and sa == sb and ba == bb and not (va and vb and va != vb) and not (la and lb and la != lb)


def _cle(numero: str) -> tuple:
    return tuple((0, int(x), "") if x.isdigit() else (1, 0, x) for x in numero.split("."))


def _sous_section(citee: str, lue: str) -> bool:
    return lue == citee or (bool(citee) and lue.startswith(citee + "."))


def section_couvre(citee: str, lue: str) -> bool:
    """La section `lue` est-elle la section `citee`, l'une de ses sous-sections, ou (plage
    `a à b`) une section comprise entre a et b ? Fragments que `bornes_section` sait lire."""
    debut, fin = bornes_section(citee)
    lue = numero_section(lue)
    if _sous_section(debut, lue) or _sous_section(fin, lue):
        return True
    return bool(debut and fin and lue) and _cle(debut) < _cle(lue) < _cle(fin)


def lectures_couvrantes(doc: str, section: str, debut: int, fin: int, lues: Iterable[tuple]) -> list:
    """Pour la citation (doc, section, pages debut..fin), l'étiquette d'une lecture qui couvre
    chaque page, dans l'ordre des pages ; liste vide si une seule page manque (ou si
    l'intervalle est inversé). `lues` : (document, section, page, étiquette) de chaque
    passage affiché ; l'étiquette est libre (référence relevée, None…). Le document lu doit
    être celui de la citation (`meme_document` : sigle, version, langue, #280)."""
    if fin < debut:
        return []
    par_page: dict[int, object] = {}
    for d, sec, page, etiquette in lues:
        if debut <= page <= fin and meme_document(doc, d) and section_couvre(section, sec):
            par_page.setdefault(page, etiquette)
    pages = range(debut, fin + 1)
    return [par_page[p] for p in pages] if all(p in par_page for p in pages) else []
