"""Rappels : retrouve dans le second cerveau les notes liées à un sujet.
Usage : python3 scripts/rappels.py mot1 mot2 ... [--n 5] [--aios chemin]   (par défaut : dossier courant)
Claude le lance avant de répondre sur un sujet et cite en une ligne les 1 à 3 notes utiles (idée, décision, erreur ancienne)."""
import os, re, sys, unicodedata, datetime
POIDS = {"Erreurs": 3, "Décisions": 3, "Idées": 3, "Habitudes": 2, "Toi": 2, "Connaissances": 2, "Sessions": 1}
def norm(t): return "".join(c for c in unicodedata.normalize("NFD", t.lower()) if unicodedata.category(c) != "Mn")
argv = sys.argv[1:]
aios = "."
if "--aios" in argv:
    i = argv.index("--aios"); aios = argv[i + 1]; del argv[i:i + 2]
RACINE = os.path.join(os.path.abspath(aios), "04-second-cerveau")
args = [a for a in argv if not a.startswith("--")]
n = int(argv[argv.index("--n") + 1]) if "--n" in argv else 5
if "--n" in argv: args.remove(str(n))
mots = [norm(a) for a in args if len(a) > 2]
if not mots: sys.exit("Donne au moins un mot-clé.")
res = []
for d, _, fs in os.walk(RACINE):
    if "Modèles" in d: continue
    for f in fs:
        if not f.endswith(".md"): continue
        p = os.path.join(d, f); titre = norm(f[:-3])
        try: corps = norm(open(p, encoding="utf-8").read())
        except Exception: continue
        score = sum(3 * titre.count(m) + corps.count(m) for m in mots)
        if not score: continue
        dossier = os.path.relpath(d, RACINE).split(os.sep)[0]
        score *= POIDS.get(dossier, 1)
        res.append((score, p, dossier))
res.sort(reverse=True)
for score, p, dossier in res[:n]:
    lignes = [l.strip() for l in open(p, encoding="utf-8") if l.strip() and not l.startswith(("---", "#", "tags", "maj", "name", "description"))]
    date = datetime.date.fromtimestamp(os.path.getmtime(p))
    print(f"[{dossier}] {os.path.basename(p)[:-3]} ({date}) : {(lignes[0] if lignes else '')[:140]}")
if not res: print("Aucun rappel.")
