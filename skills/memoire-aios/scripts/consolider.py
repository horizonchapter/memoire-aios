"""Consolidation hebdomadaire du second cerveau (comme le sommeil pour un humain).
Usage : python3 scripts/consolider.py [chemin_AIOS]   (par défaut : dossier courant)
Liste ce que Claude doit traiter : sessions de plus de 28 jours à résumer dans un récap mensuel,
notes probablement en double, notes trop maigres. Claude agit ensuite : il fusionne, résume,
complète, puis relance verifier_liens.py. Il ne supprime jamais : les anciennes sessions restent,
le récap mensuel en garde l'essentiel."""
import os, re, difflib, datetime, unicodedata
import sys
R = os.path.join(os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "."), "04-second-cerveau")
def norm(t): return "".join(c for c in unicodedata.normalize("NFD", t.lower()) if unicodedata.category(c) != "Mn")
today = datetime.date.today()
RC, SE = os.path.join(R, "Récaps"), os.path.join(R, "Sessions")
recaps = " ".join(open(os.path.join(RC, f), encoding="utf-8").read() for f in os.listdir(RC) if f.endswith(".md")) if os.path.isdir(RC) else ""
print("== Sessions à résumer (plus de 28 jours, absentes des récaps) ==")
for f in sorted(os.listdir(SE) if os.path.isdir(SE) else []):
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})\.md$", f)
    if m and (today - datetime.date(*map(int, m.groups()))).days > 28 and f[:-3] not in recaps:
        print(" -", f[:-3], "-> Récap mois", f[:7])
print("== Doublons probables (même dossier, titres proches) ==")
for d, _, fs in os.walk(R):
    if "Modèles" in d or d.endswith("Sessions"): continue
    t = [f[:-3] for f in fs if f.endswith(".md")]
    for i, a in enumerate(t):
        for b in t[i + 1:]:
            if difflib.SequenceMatcher(None, norm(a), norm(b)).ratio() > 0.82:
                print(" -", os.path.relpath(d, R), ":", a, "|", b)
print("== Notes trop maigres (moins de 80 caractères de contenu, hors pôles) ==")
for d, _, fs in os.walk(R):
    if "Modèles" in d or d == R: continue
    for f in fs:
        if not f.endswith(".md"): continue
        L = [l for l in open(os.path.join(d, f), encoding="utf-8") if l.strip() and not l.startswith(("---", "#", "↑", "tags", "maj", "name", "description", "sources", "aliases"))]
        if len("".join(L).strip()) < 80: print(" -", os.path.relpath(os.path.join(d, f), R))
