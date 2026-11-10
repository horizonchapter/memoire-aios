"""Controle de sante de l'AIOS (lecture seule, aucune ecriture).
Usage : python3 scripts/controle_aios.py [chemin_AIOS]   (par défaut : dossier courant)
Sortie Markdown. Code de sortie 0 = RAS, 1 = au moins une alerte."""
import os, re, sys, json, time, datetime, unicodedata

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
TODAY = datetime.date.today()

SKIP_NAMES = {"node_modules", "_corbeille", "_backup", ".git"}
SKIP_PREFIX = ("sauvegardes-",)
SKIP_PATHS = []
try:
    cfg = json.load(open(os.path.join(ROOT, ".obsidian", "app.json"), encoding="utf-8"))
    SKIP_PATHS = [p.strip("/").replace("\\", "/") for p in cfg.get("userIgnoreFilters", []) if p.strip("/")]
except Exception:
    pass

def rel(p): return os.path.relpath(p, ROOT).replace("\\", "/")
def norm(t): return "".join(c for c in unicodedata.normalize("NFD", t.lower()) if unicodedata.category(c) != "Mn")
def read(p):
    try: return open(p, encoding="utf-8", errors="replace").read()
    except Exception: return ""

def skipped(path, name):
    if name in SKIP_NAMES or name.startswith(SKIP_PREFIX): return True
    r = rel(path)
    return any(r == s or r.startswith(s + "/") for s in SKIP_PATHS)

states, backups, corbeilles = [], [], []
for d, dirs, files in os.walk(ROOT):
    keep = []
    for n in dirs:
        full = os.path.join(d, n)
        if n == "_backup": backups.append(full)
        elif n == "_corbeille": corbeilles.append(full)
        if not skipped(full, n): keep.append(n)
    dirs[:] = keep
    if "STATE.md" in files: states.append(os.path.join(d, "STATE.md"))

alerts = {}
def alert(section, msg): alerts.setdefault(section, []).append(msg)

# 1. STATE.md
REQ = ["reprise exacte", "objectif", "decide", "demandes ouvertes", "pieges deja rencontres",
       "fichiers, liens et chiffres cles", "outils et connecteurs", "attend une validation", "questions ouvertes"]
S1 = "1. STATE.md"
for p in sorted(states):
    t = read(p); r = rel(p)
    n = len(t.splitlines()); c = len(t)
    if n > 80: alert(S1, f"`{r}` : {n} lignes (max 80)")
    if c > 10000: alert(S1, f"`{r}` : {c} caracteres (max 10 000)")
    heads = [norm(m.group(1)).strip() for m in re.finditer(r"^##\s+(.+?)\s*$", t, re.M)]
    miss = [s for s in REQ if not any(h.startswith(s) for h in heads)]
    if miss: alert(S1, f"`{r}` : sections manquantes : " + ", ".join(miss))
    mt = datetime.date.fromtimestamp(os.path.getmtime(p))
    ds = []
    for m in re.finditer(r"\b(20\d\d)-(\d\d)-(\d\d)\b", t):
        try:
            d = datetime.date(int(m[1]), int(m[2]), int(m[3]))
            if d <= TODAY + datetime.timedelta(days=1): ds.append(d)
        except ValueError: pass
    last = max(ds) if ds else None
    age = (TODAY - mt).days
    if age > 3: alert(S1, f"`{r}` : a rafraichir (modifie le {mt}, il y a {age} j ; derniere date citee : {last or 'aucune'})")
    elif last and last > mt + datetime.timedelta(days=1): alert(S1, f"`{r}` : date citee {last} posterieure a la modification {mt}")

# 2. Projets
S2 = "2. Projets"
P = os.path.join(ROOT, "01-projets")
def subdirs(p): return sorted(n for n in os.listdir(p) if os.path.isdir(os.path.join(p, n))) if os.path.isdir(p) else []
for n in subdirs(P):
    for f in ("STATE.md", "DECISIONS.md"):
        if not os.path.isfile(os.path.join(P, n, f)): alert(S2, f"`01-projets/{n}` : {f} absent")

# 3. AGENTS.md
S5 = "3. Miroir AGENTS.md"
heads = lambda t: {re.sub(r"\s+", " ", m.group(1)).strip() for m in re.finditer(r"^##\s+(.+?)\s*$", t, re.M)}
for d, dirs, files in os.walk(ROOT):
    dirs[:] = [n for n in dirs if not skipped(os.path.join(d, n), n)]
    if "CLAUDE.md" in files and "AGENTS.md" in files:
        miss = sorted(heads(read(os.path.join(d, "CLAUDE.md"))) - heads(read(os.path.join(d, "AGENTS.md"))))
        if miss: alert(S5, f"`{rel(os.path.join(d, 'AGENTS.md'))}` : titres absents : " + " ; ".join(miss))

# 6. Sauvegardes et corbeille
S6 = "4. Sauvegardes et corbeille"
def has_keep(p):
    if "NE-PAS-SUPPRIMER" in os.path.basename(p): return True
    for d, ds, fs in os.walk(p):
        if any("NE-PAS-SUPPRIMER" in x for x in ds + fs): return True
    return False
for b in backups:
    for e in sorted(os.listdir(b)):
        full = os.path.join(b, e)
        m = re.match(r"(\d{4})-(\d\d)-(\d\d)", e)
        if not (m and os.path.isdir(full)): continue
        try: d = datetime.date(int(m[1]), int(m[2]), int(m[3]))
        except ValueError: continue
        if (TODAY - d).days > 5 and not has_keep(full):
            alert(S6, f"`{rel(full)}` : {(TODAY - d).days} j sans NE-PAS-SUPPRIMER (a purger)")
for c in corbeilles:
    for e in sorted(os.listdir(c)):
        full = os.path.join(c, e)
        if re.match(r"\d{4}-\d\d-\d\d", e) and os.path.isdir(full) and not os.path.isfile(os.path.join(full, "MANIFESTE.md")):
            alert(S6, f"`{rel(full)}` : MANIFESTE.md absent")

# 7. Vrac
S7 = "5. Fichiers en vrac a la racine de 01-projets"
if os.path.isdir(P):
    for e in sorted(os.listdir(P)):
        if os.path.isfile(os.path.join(P, e)): alert(S7, f"`01-projets/{e}`")

# Sortie
SECTIONS = [S1, S2, S5, S6, S7]
total = sum(len(v) for v in alerts.values())
print(f"# Controle AIOS - {TODAY}\n")
print(f"Racine : `{ROOT}` | STATE.md controles : {len(states)} | alertes : {total}\n")
for s in SECTIONS:
    items = alerts.get(s, [])
    print(f"## {s} : {'RAS' if not items else str(len(items)) + ' alerte(s)'}")
    for i in items: print(f"- {i}")
    print()
print("Resultat : " + ("RAS" if total == 0 else f"{total} alerte(s)"))
sys.exit(0 if total == 0 else 1)
