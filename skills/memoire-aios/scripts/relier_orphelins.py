"""Relie automatiquement les notes isolées du graphe Obsidian (groupes hors du groupe principal).
Pour chaque groupe isolé, ajoute en fin de la note la plus ancienne du groupe une ligne `↑ [[parent]]`
vers le CLAUDE.md, SOMMAIRE.md ou STATE.md le plus proche dans les dossiers parents (qui est dans le groupe principal).
Usage : python relier_orphelins.py <AIOS> [--appliquer]   (sans --appliquer : liste seulement)
Ne touche pas un fichier modifié depuis moins de 5 h (agent peut-être dessus) : il est signalé.
Usage dans le skill : python3 scripts/relier_orphelins.py "<chemin>" --appliquer
"""
import json, os, re, sys, time

R = os.path.abspath(sys.argv[1]); APPLY = "--appliquer" in sys.argv
try: ign = json.load(open(os.path.join(R, ".obsidian", "app.json"), encoding="utf-8")).get("userIgnoreFilters", [])
except FileNotFoundError: ign = []
notes = {}
for root, ds, fs in os.walk(R):
    ds[:] = [d for d in ds if not d.startswith(".")]
    for f in fs:
        if f.endswith(".md"):
            rel = os.path.relpath(os.path.join(root, f), R).replace("\\", "/")
            if not any(rel.startswith(i.rstrip("/") + "/") for i in ign):
                notes[rel] = open(os.path.join(root, f), encoding="utf-8").read()
base = {}
for r in notes: base.setdefault(os.path.basename(r)[:-3], []).append(r)

def resoudre(t):
    t = t.replace(chr(92) + "|", "|").split("|")[0].split("#")[0].strip()
    if t + ".md" in notes: return t + ".md"
    c = [x for x in base.get(os.path.basename(t), []) if x.endswith(t + ".md")] or base.get(os.path.basename(t), [])
    return c[0] if c else None

voisins = {r: set() for r in notes}
for r, t in notes.items():
    for m in re.findall(r"\[\[([^\]]+)\]\]", t):
        x = resoudre(m)
        if x and x != r: voisins[r].add(x); voisins[x].add(r)
vus, groupes = set(), []
for r in notes:
    if r in vus: continue
    pile, g = [r], set()
    while pile:
        x = pile.pop()
        if x not in g: g.add(x); pile.extend(voisins[x] - g)
    vus |= g; groupes.append(g)
groupes.sort(key=len, reverse=True)
if len(groupes) <= 1: print("1 groupe : rien à relier."); sys.exit(0)
principal = groupes[0]

def parent(rel):
    d = os.path.dirname(rel)
    while True:
        for n in ("Accueil.md", "SOMMAIRE.md", "CLAUDE.md", "STATE.md", "INDEX.md"):
            c = (d + "/" + n) if d else n
            if c in principal and c != rel: return c
        if not d: return next((n for n in ("INDEX.md", "Accueil.md") if n in principal), None)
        d = os.path.dirname(d)

faits = 0
for g in groupes[1:]:
    fich = sorted(g, key=lambda r: os.path.getmtime(os.path.join(R, r)))
    cible = fich[0]; p = parent(cible)
    chemin = os.path.join(R, cible)
    if p is None: print("pas de parent :", cible); continue
    if time.time() - os.path.getmtime(chemin) < 5 * 3600:
        print("récent (< 5 h), signalé :", cible, "->", p); continue
    ligne = f"\n\n↑ [[{p[:-3]}|{os.path.basename(p)[:-3]}]]\n"
    print(("lié" if APPLY else "à lier"), ":", cible, "->", p)
    if APPLY:
        with open(chemin, "a", encoding="utf-8") as f: f.write(ligne)
        faits += 1
print(f"{len(groupes)-1} groupe(s) isolé(s), {faits} lié(s).")
