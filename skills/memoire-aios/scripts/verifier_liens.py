"""Vérifie qu'aucune note de l'AIOS n'est isolée dans le graphe Obsidian.
Usage : python3 verifier_liens.py "<chemin>/AIOS"
Respecte les exclusions d'Obsidian (.obsidian/app.json, chemins depuis la racine).
"""
import json, os, re, sys

R = os.path.abspath(sys.argv[1])
try:
    ign = json.load(open(os.path.join(R, ".obsidian", "app.json"), encoding="utf-8")).get("userIgnoreFilters", [])
except FileNotFoundError:
    ign = []
notes = {}
for root, ds, fs in os.walk(R):
    ds[:] = [d for d in ds if not d.startswith(".")]
    for f in fs:
        if f.endswith(".md"):
            rel = os.path.relpath(os.path.join(root, f), R).replace("\\", "/")
            if not any(rel.startswith(i.rstrip("/") + "/") for i in ign):
                notes[rel] = open(os.path.join(root, f), encoding="utf-8").read()
base = {}
for r in notes:
    base.setdefault(os.path.basename(r)[:-3], []).append(r)


def resoudre(t):
    t = t.replace("\\|", "|").split("|")[0].split("#")[0].strip()
    if t + ".md" in notes:
        return t + ".md"
    c = [x for x in base.get(os.path.basename(t), []) if x.endswith(t + ".md")] or base.get(os.path.basename(t), [])
    return c[0] if c else None


voisins = {r: set() for r in notes}
for r, t in notes.items():
    for m in re.findall(r"\[\[([^\]]+)\]\]", t):
        x = resoudre(m)
        if x and x != r:
            voisins[r].add(x); voisins[x].add(r)
vus, groupes = set(), []
for r in notes:
    if r in vus:
        continue
    pile, g = [r], set()
    while pile:
        x = pile.pop()
        if x not in g:
            g.add(x); pile.extend(voisins[x] - g)
    vus |= g; groupes.append(g)
groupes.sort(key=len, reverse=True)
print(f"{len(notes)} notes, {len(groupes)} groupe(s).")
for g in groupes[1:]:
    print("  à relier :", ", ".join(sorted(g)))
sys.exit(0 if len(groupes) <= 1 else 1)
