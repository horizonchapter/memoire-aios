"""Tient à jour le journal de bord, les décisions et l'INDEX d'un AIOS sans abîmer les fichiers.

Usage (depuis la racine du coffre ; chemins relatifs à cette racine) :
  python3 journal.py journal <date> <projet> <fait> <décisions> <prochaine étape> <bloqué par> [--fichier JOURNAL_DE_BORD.md]
  python3 journal.py decision <DECISIONS.md> "<décision — pourquoi>"
  python3 journal.py index-date <INDEX.md> [AAAA-MM-JJ]
  python3 journal.py verifier [fichiers...]        (lecture seule ; défaut : JOURNAL_DE_BORD.md DECISIONS.md)
  python3 journal.py --selftest
Option de chaque commande : --racine <dossier> (défaut : dossier courant), où vit _backup/.

Avant toute écriture : copie dans _backup/AAAA-MM-JJ/<chemin d'origine>, verrou contre les écritures
simultanées, écriture atomique (fichier temporaire puis remplacement). Encodage et fins de ligne conservés,
octets NUL retirés. Rien n'est supprimé, sauf la ligne remplacée du même projet et du même jour.
Codes de sortie : 0 succès, 1 défauts trouvés ou erreur, 2 secret probable (rien écrit).
"""
import argparse, contextlib, datetime, os, re, shutil, sys, tempfile, time

AUJ = datetime.date.today().isoformat()
DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
LIGNE_DATEE = re.compile(r"^\s*(?:[|-]\s*)?(\d{4}-\d{2}-\d{2})")
# Motif simple : préfixes de clés connus, JWT, ou « mot de passe / token / clé : valeur ».
SECRET = re.compile(
    r"\b(?:sk|pk|rk)-[A-Za-z0-9_-]{16,}|\bgh[pousr]_[A-Za-z0-9]{20,}|\bAKIA[0-9A-Z]{16}\b|\bxox[abpr]-[A-Za-z0-9-]{10,}"
    r"|\bAIza[0-9A-Za-z_-]{30,}|\beyJ[\w-]{10,}\.[\w-]{10,}\."
    r"|(?i:api[ _-]?key|cl[ée] api|mot de passe|password|passwd|secret|token)\s*[:=]\s*[^\s\[<]\S{7,}")
COLLEE = re.compile(r"(?<=[^\W\d_])\d{4}-\d{2}-\d{2}")  # date collée à un mot : « Alex2026-11-05 »
DEC_INTERNE = re.compile(r"\d{4}-\d{2}-\d{2} — ")  # deuxième décision dans la même ligne


class Erreur(Exception):
    pass


def lire(p):
    """Renvoie (texte, encodage, octets NUL retirés)."""
    if not os.path.exists(p):
        return "", "utf-8", 0
    b = open(p, "rb").read()
    if b[:2] in (b"\xff\xfe", b"\xfe\xff"):
        return b.decode("utf-16"), "utf-16", 0
    nul = b.count(b"\x00")
    b = b.replace(b"\x00", b"")
    if b.startswith(b"\xef\xbb\xbf"):
        return b[3:].decode("utf-8"), "utf-8-sig", nul
    for enc in ("utf-8", "cp1252"):
        try:
            return b.decode(enc), enc, nul
        except UnicodeDecodeError:
            pass
    raise Erreur(f"{p} : encodage non reconnu, rien écrit (corriger à la main).")


def fin_de_ligne(t):
    return "\r\n" if t.count("\r\n") * 2 > t.count("\n") else "\n"


def sauvegarder(p, racine):
    if not os.path.exists(p):
        return None
    try:
        rel = os.path.relpath(os.path.abspath(p), racine)
    except ValueError:  # autre lecteur sous Windows
        rel = os.path.basename(p)
    if rel.startswith(".."):
        rel = os.path.basename(p)
    d = os.path.join(racine, "_backup", AUJ, rel)
    if os.path.exists(d):  # jamais d'écrasement d'une sauvegarde
        base, ext = os.path.splitext(d)
        d = f"{base}_{datetime.datetime.now():%Hh%Mm%S_%f}{ext}"
    os.makedirs(os.path.dirname(d), exist_ok=True)
    shutil.copy2(p, d)
    return d


@contextlib.contextmanager
def verrou(p, attente=15, abandon=30):
    v = p + ".lock"
    t0 = time.time()
    while True:
        try:
            fd = os.open(v, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            break
        except FileExistsError:
            try:
                if time.time() - os.path.getmtime(v) > abandon:
                    os.remove(v)  # verrou laissé par un agent interrompu
                    continue
            except FileNotFoundError:
                continue
            if time.time() - t0 > attente:
                raise Erreur(f"{p} est en cours d'écriture par un autre agent ; réessayer.")
            time.sleep(0.2)
    try:
        yield
    finally:
        os.close(fd)
        with contextlib.suppress(FileNotFoundError):
            os.remove(v)


def modifier(p, racine, transformer):
    """Lit, transforme, sauvegarde puis remplace le fichier de façon atomique. Renvoie (message, nul, sauvegarde)."""
    p = os.path.abspath(p)
    with verrou(p):
        texte, enc, nul = lire(p)
        nouveau, msg = transformer(texte)
        donnees = nouveau.encode(enc)  # échoue avant toute écriture si un caractère n'existe pas dans l'encodage
        sauve = sauvegarder(p, racine)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        fd, tmp = tempfile.mkstemp(dir=os.path.dirname(p), prefix=".tmp-", suffix=".md")
        try:
            with os.fdopen(fd, "wb") as f:
                f.write(donnees)
                f.flush()
                os.fsync(f.fileno())
            os.replace(tmp, p)
        except BaseException:
            with contextlib.suppress(FileNotFoundError):
                os.remove(tmp)
            raise
    return msg, nul, sauve


def _refus():
    print("Refus : secret probable (clé, mot de passe ou token). Rien écrit. Écrire « [secret retiré] » et où le retrouver.")
    sys.exit(2)


def propre(champ):
    """Un champ = une cellule : pas de retour à la ligne, pas de « | », pas de NUL."""
    c = " ".join(champ.replace("\x00", "").split()).replace("|", "/")
    return c or "-"


def colonnes(ligne):
    s = ligne.strip().strip("|").strip()
    if not DATE.match(s):
        return None
    parts = [x.strip() for x in s.split("|")]
    return parts if len(parts) >= 2 else None


def cle(projet):
    return " ".join(projet.split()).casefold()


def pied(L):
    """Index du début du pied de page (lignes finales vides, « --- » ou « ↑ [[...]] »)."""
    i = len(L)
    while i > 0 and (L[i - 1].strip() in ("", "---") or L[i - 1].lstrip().startswith("↑")):
        i -= 1
    return i


def inserer(L, pos, ligne, fin):
    if pos > 0 and not L[pos - 1].endswith(("\n", "\r")):
        L[pos - 1] += fin
    L.insert(pos, ligne + fin)


def maj_journal(texte, date, projet, ligne):
    fin = fin_de_ligne(texte)
    if not texte:
        texte = f"# Journal de bord{fin}Format : date | projet | fait | décisions | prochaine étape | bloqué par{fin}"
    L = texte.splitlines(keepends=True)
    k = cle(projet)
    pareilles = [i for i, l in enumerate(L) if (c := colonnes(l)) and c[0] == date and cle(c[1]) == k]
    if pareilles:
        i = pareilles[-1]
        corps = L[i].rstrip("\r\n")
        L[i] = ligne + (L[i][len(corps):] or fin)
        msg = f"ligne {i + 1} mise à jour (même projet, même jour). Ancienne : {corps}"
        if len(pareilles) > 1:
            msg += f"\nAttention : {len(pareilles)} lignes pour ce projet ce jour-là (lignes {', '.join(str(x + 1) for x in pareilles)}), seule la dernière a été remplacée."
        return "".join(L), msg
    datees = [(i, m.group(1)) for i, l in enumerate(L) if (m := LIGNE_DATEE.match(l))]
    avant = [i for i, d in datees if d <= date]
    pos = avant[-1] + 1 if avant else datees[0][0] if datees else pied(L)
    inserer(L, pos, ligne, fin)
    return "".join(L), f"ligne ajoutée en position {pos + 1}."


def ajout_decision(texte, d):
    fin = fin_de_ligne(texte)
    if not texte:
        texte = f"# Décisions{fin}"
    L = texte.splitlines(keepends=True)
    pos = pied(L)
    inserer(L, pos, d, fin)
    return "".join(L), f"décision ajoutée ligne {pos + 1}."


def maj_index(texte, date):
    n, k = re.subn(r"(Mis à jour\s*:\s*)\d{4}-\d{2}-\d{2}", lambda m: m.group(1) + date, texte, count=1)
    if not k:
        raise Erreur("aucune mention « Mis à jour : AAAA-MM-JJ » dans le fichier ; rien écrit.")
    return n, f"date de mise à jour : {date}."


def date_valide(d):
    try:
        datetime.date.fromisoformat(d)
        return d
    except ValueError:
        raise Erreur(f"date invalide « {d} » (format AAAA-MM-JJ).")


def verifier(fichiers):
    """Lecture seule. Renvoie {type de défaut: nombre} et affiche le détail par ligne."""
    total = {"octets NUL": 0, "lignes hors ordre": 0, "doublons projet+jour": 0, "décisions collées": 0, "encodage illisible": 0}
    for p in fichiers:
        if not os.path.exists(p):
            print(f"{p} : absent.")
            continue
        try:
            texte, enc, nul = lire(p)
        except Erreur as e:
            print(e)
            total["encodage illisible"] += 1
            continue
        nom = os.path.basename(p).upper()
        L = texte.splitlines()
        print(f"{p} : {len(L)} lignes, encodage {enc}.")
        if nul:
            print(f"  {nul} octet(s) NUL.")
            total["octets NUL"] += nul
        for i, l in enumerate(L):
            s = l.strip().lstrip("|-").strip()
            debut = 10 if DATE.match(s) else 0
            if COLLEE.search(s) or ("DECISION" in nom and DEC_INTERNE.search(s[debut:])):
                print(f"  ligne {i + 1} : deux entrées collées.")
                total["décisions collées"] += 1
        if "JOURNAL" in nom:
            datees = [(i, m.group(1)) for i, l in enumerate(L) if (m := LIGNE_DATEE.match(l))]
            for (i, d), (j, e) in zip(datees, datees[1:]):
                if e < d:
                    print(f"  ligne {j + 1} ({e}) placée après la ligne {i + 1} ({d}).")
                    total["lignes hors ordre"] += 1
            vus = {}
            for i, l in enumerate(L):
                if c := colonnes(l):
                    vus.setdefault((c[0], cle(c[1])), []).append(i + 1)
            for (d, _), lignes in vus.items():
                if len(lignes) > 1:
                    print(f"  {d} : {len(lignes)} lignes pour le même projet (lignes {', '.join(map(str, lignes))}).")
                    total["doublons projet+jour"] += len(lignes) - 1
    print("Bilan : " + ", ".join(f"{k} {v}" for k, v in total.items()))
    return total


def selftest():
    d = tempfile.mkdtemp(prefix="journal-selftest-")
    try:
        j = os.path.join(d, "JOURNAL_DE_BORD.md")
        open(j, "wb").write("# Journal\r\nFormat : date | projet | fait\r\n2026-01-01 | A | x | - | - | -\r\n"
                            "2026-01-03 | B | y | - | - | -\r\n2026-01-02 | C | z | - | - | -\r\nfin sans retour\x00".encode("utf-8"))
        t = verifier([j])
        assert t["octets NUL"] == 1 and t["lignes hors ordre"] == 1, t
        msg, nul, sauve = modifier(j, d, lambda x: maj_journal(x, "2026-01-02", "Neuf", "2026-01-02 | Neuf | n | - | - | -"))
        L = open(j, "rb").read().decode("utf-8").split("\r\n")
        assert nul == 1 and "\x00" not in "".join(L) and sauve and os.path.exists(sauve), (nul, sauve)
        assert L[5].startswith("2026-01-02 | Neuf"), L  # après la dernière ligne datée <= 2026-01-02
        modifier(j, d, lambda x: maj_journal(x, "2026-01-02", " neuf ", "2026-01-02 | neuf | n2 | - | - | -"))
        txt = open(j, encoding="utf-8").read()
        assert txt.count("| neuf") + txt.count("| Neuf") == 1 and "n2" in txt, txt
        modifier(j, d, lambda x: maj_journal(x, "2025-12-31", "Z", "2025-12-31 | Z | - | - | - | -"))
        assert open(j, encoding="utf-8").read().splitlines()[2].startswith("2025-12-31"), "insertion avant la 1re date"
        assert len(os.listdir(os.path.join(d, "_backup", AUJ))) == 3, "une sauvegarde par écriture"
        assert SECRET.search("token: ghp_abcdefghijklmnopqrstuvwx") and SECRET.search("mot de passe = Hunter2024!")
        assert not SECRET.search("token Discord rangé dans le fichier d'environnement") and not SECRET.search("mot de passe : [secret retiré]")
        dec = os.path.join(d, "DECISIONS.md")
        open(dec, "wb").write("# Décisions\n2026-01-01 — a — b\n2026-01-02 — c — par Alex2026-01-03 — d — e".encode("utf-8"))
        assert verifier([dec])["décisions collées"] == 1
        modifier(dec, d, lambda x: ajout_decision(x, "2026-01-04 — f — g"))
        assert open(dec, encoding="utf-8").read().endswith("— e\n2026-01-04 — f — g\n")
        gen = os.path.join(d, "DEC2.md")
        open(gen, "w", encoding="utf-8-sig").write("# Décisions\n\n---\n↑ [[CLAUDE]]")
        modifier(gen, d, lambda x: ajout_decision(x, "2026-01-05 — h — i"))
        b = open(gen, "rb").read()
        assert b.startswith(b"\xef\xbb\xbf") and b.decode("utf-8-sig").splitlines()[1] == "2026-01-05 — h — i", b
        idx = os.path.join(d, "INDEX.md")
        open(idx, "w", encoding="utf-8").write("> Tableau. Mis à jour : 2026-01-01.\n")
        modifier(idx, d, lambda x: maj_index(x, "2026-02-02"))
        assert "Mis à jour : 2026-02-02." in open(idx, encoding="utf-8").read()
        print("selftest : OK")
    finally:
        shutil.rmtree(d, ignore_errors=True)


def main():
    if "--selftest" in sys.argv:
        return selftest()
    commun = argparse.ArgumentParser(add_help=False)
    commun.add_argument("--racine", default=os.getcwd())
    ap = argparse.ArgumentParser(description="Journal, décisions et INDEX de l'AIOS.")
    sp = ap.add_subparsers(dest="cmd", required=True)
    j = sp.add_parser("journal", parents=[commun])
    for c in ("date", "projet", "fait", "decisions", "prochaine", "bloque"):
        j.add_argument(c)
    j.add_argument("--fichier", default="JOURNAL_DE_BORD.md")
    d = sp.add_parser("decision", parents=[commun])
    d.add_argument("fichier")
    d.add_argument("texte")
    i = sp.add_parser("index-date", parents=[commun])
    i.add_argument("fichier")
    i.add_argument("date", nargs="?", default=AUJ)
    v = sp.add_parser("verifier", parents=[commun])
    v.add_argument("fichiers", nargs="*", default=["JOURNAL_DE_BORD.md", "DECISIONS.md"])
    a = ap.parse_args()
    racine = os.path.abspath(a.racine)
    chemin = lambda f: f if os.path.isabs(f) else os.path.join(racine, f)
    try:
        if a.cmd == "verifier":
            t = verifier([chemin(f) for f in a.fichiers])
            return 1 if any(t.values()) else 0
        if a.cmd == "journal":
            date = date_valide(a.date)
            champs = [date] + [propre(x) for x in (a.projet, a.fait, a.decisions, a.prochaine, a.bloque)]
            if champs[1] == "-":  # projet vide : remplacerait n'importe quelle ligne « - » du jour
                raise Erreur("projet vide ; rien écrit.")
            if any(SECRET.search(c) for c in champs):
                _refus()
            ligne = " | ".join(champs)
            msg, nul, sauve = modifier(chemin(a.fichier), racine, lambda x: maj_journal(x, date, champs[1], ligne))
        elif a.cmd == "decision":
            t = " ".join(a.texte.replace("\x00", "").split())
            if SECRET.search(t):
                _refus()
            if not DATE.match(t):
                t = f"{AUJ} — {t}"
            msg, nul, sauve = modifier(chemin(a.fichier), racine, lambda x: ajout_decision(x, t))
        else:
            date = date_valide(a.date)
            p = chemin(a.fichier)
            if not os.path.exists(p):
                raise Erreur(f"{p} absent ; rien écrit.")
            msg, nul, sauve = modifier(p, racine, lambda x: maj_index(x, date))
    except Erreur as e:
        print(f"Erreur : {e}")
        return 1
    print(msg)
    if nul:
        print(f"{nul} octet(s) NUL retiré(s).")
    if sauve:
        print(f"Sauvegarde : {os.path.relpath(sauve, racine)}")
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
