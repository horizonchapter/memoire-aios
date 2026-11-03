"""Crée un AIOS complet (dossier + second cerveau Obsidian) à partir d'un fichier de réponses JSON.

Usage : python3 creer_aios.py --dossier "<chemin>/AIOS" --config reponses.json
Le script ne supprime et n'écrase jamais rien : un fichier existant est laissé tel quel.
"""
import argparse, json, os, re, datetime

AUJ = datetime.date.today().isoformat()
NOTES_CREEES = []


def ecrire(base, rel, texte):
    p = os.path.join(base, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    if os.path.exists(p):
        return
    with open(p, "w", encoding="utf-8") as f:
        f.write(texte.strip() + "\n")
    NOTES_CREEES.append(rel)


def note(base, rel, titre, corps, pole, tags):
    ecrire(base, rel, f"---\ntags: [{tags}]\nmaj: {AUJ}\n---\n# {titre}\n\n{corps.strip()}\n\n---\n↑ [[{pole}]]")


def slug(s):
    s = re.sub(r"[^\w\s-]", "", s.lower(), flags=re.U).strip()
    return re.sub(r"[\s_]+", "-", s)


def liste(items):
    return "\n".join(f"- {x}" for x in items) if items else "- À compléter."


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dossier", required=True)
    ap.add_argument("--config", required=True)
    a = ap.parse_args()
    c = json.load(open(a.config, encoding="utf-8"))
    R = os.path.abspath(a.dossier)
    C = "04-second-cerveau"
    nom = c.get("prenom", "Moi")
    projets = c.get("projets", [])
    dossiers_projets = [f"{i+1:02d}-{slug(p['nom'])}" for i, p in enumerate(projets)]

    # ---------- Règles et centre ----------
    regles = c.get("regles") or [
        "Règle du bouton : Claude prépare, je valide. Jamais de publication, paiement, envoi ou création de compte sans mon accord.",
        "Un seul projet prioritaire à la fois.",
        "Chiffres importants étiquetés : VÉRIFIÉ (source datée), ESTIMÉ, HYPOTHÈSE, INCONNU.",
        "Jamais d'emojis.",
    ]
    ecrire(R, "CLAUDE.md", f"""
# Règles communes de mon AIOS

## Rôle
Tu es mon second cerveau. {c.get('role_claude', 'Associé, expert et critique honnête.')} Réponds en {c.get('langue', 'français')}.

## Règles
{liste(regles)}

## Démarrage en un mot
Quand je dis « vas-y », « reprends » ou « où j'en suis » : lis `INDEX.md`, `{C}/Toi.md`, la dernière note de `{C}/Sessions/`, les erreurs liées et le STATE.md du projet en cours. Réponds en 5 lignes (où on en est, décidé, reste à faire, prochaine action), puis attends mon accord.

## Mémoire toujours active
Applique `{C}/PROTOCOLE.md` à chaque session : idées, décisions, erreurs, connaissances, habitudes, skills, informations personnelles, et une note `Sessions/AAAA-MM-JJ` en fin de session. Avant d'agir, relis les erreurs liées au sujet. Ne me pose jamais une question dont la réponse est déjà dans la mémoire.

## Fin de session automatique
Travail terminé ou plus d'une heure sans message : note de session, ligne du projet dans `INDEX.md`, STATE.md du projet, une ligne dans `JOURNAL_DE_BORD.md`.

## Structure
```
AIOS/
├── CLAUDE.md  INDEX.md  JOURNAL_DE_BORD.md
├── 00-inbox/           dépôt en vrac
├── 01-projets/         un dossier par projet
├── 02-skills/          source de mes skills
├── 03-agents/          mes sous-agents (copie active : .claude/agents/)
├── {C}/   ma mémoire longue (Obsidian)
├── 05-outils/          connecteurs, chats, routines
└── 06-github/          projets publiés (si besoin)
```
""")
    lignes = "\n".join(
        f"| [[01-projets/{d}/CLAUDE\\|{p['nom']}]] · [[01-projets/{d}/STATE\\|état]] | {p.get('mission', '')} | À définir |"
        for d, p in zip(dossiers_projets, projets))
    ecrire(R, "INDEX.md", f"""
# MON-AIOS : tableau de bord

Point d'entrée de mon second cerveau. Tout chat commence ici. Mis à jour : {AUJ}.

## Branches
| Branche | Où | Point d'entrée |
|---|---|---|
| Règles | `CLAUDE.md` | [[CLAUDE|règles communes]] |
| Projets | `01-projets/` | [[{C}/Tes projets|tes projets]] |
| Skills | `02-skills/` | [[02-skills/STATE|skills et statuts]] |
| Agents | `03-agents/` | [[03-agents/AGENTS|tes agents]] |
| Second cerveau | `{C}/` | [[{C}/Toi|Toi]] |
| Outils | `05-outils/` | [[05-outils/OUTILS|tes outils]] |
| Inbox | `00-inbox/` | [[00-inbox/INBOX|inbox]] |

## Projet prioritaire
{c.get('projet_prioritaire') or 'À désigner (un seul à la fois).'}

## Projets
| Projet | Mission | Prochaine action |
|---|---|---|
{lignes}

## Journal
[[JOURNAL_DE_BORD|journal de bord]]
""")
    ecrire(R, "JOURNAL_DE_BORD.md", "# Journal de bord\n\nUne ligne par session : date | projet | fait | décisions | prochaine étape.\n\n↑ [[INDEX]]")
    ecrire(R, "00-inbox/INBOX.md", "# Inbox\n\nTout en vrac ici. L'agent [[trieur]] range chaque élément au bon endroit.\n\n## À trier\n- \n\n↑ [[INDEX]]")

    # ---------- Projets ----------
    for d, p in zip(dossiers_projets, projets):
        base = f"01-projets/{d}"
        ecrire(R, f"{base}/CLAUDE.md", f"# {p['nom']}\n\nMission : {p.get('mission', 'à préciser')}\n\n## Règles du projet\n{liste(p.get('regles', []))}\n\n---\nRetour : [[INDEX]] · état : [[01-projets/{d}/STATE|STATE]] · décisions : [[01-projets/{d}/DECISIONS|DECISIONS]]")
        ecrire(R, f"{base}/STATE.md", f"# STATE : {p['nom']}\n\n## Objectif en cours\n{p.get('objectif', 'À définir.')}\n\n## Fait\n- Rien pour l'instant.\n\n## Prochaine action\n- À définir.\n\n---\n↑ [[01-projets/{d}/CLAUDE|{p['nom']}]]")
        ecrire(R, f"{base}/DECISIONS.md", f"# Décisions : {p['nom']}\n\nUne ligne datée par décision. On ajoute, on n'efface pas.\n\n---\n↑ [[01-projets/{d}/CLAUDE|{p['nom']}]]")
        os.makedirs(os.path.join(R, base, "fiches"), exist_ok=True)
        os.makedirs(os.path.join(R, base, "a_valider"), exist_ok=True)

    # ---------- Skills, agents, outils ----------
    ecrire(R, "02-skills/STATE.md", "# Skills\n\n| Skill | Statut | Note |\n|---|---|---|\n\nStatuts : idée · en cours · à tester · prêt à publier · publié.\nChaque skill a aussi sa note dans [[Tes skills]].\n\n↑ [[INDEX]]")
    agents = {
        "chercheur": ("haiku", "Recherche web rapide et synthèse sourcée.", "Cherche des sources sérieuses et datées, réponds en 10 lignes maximum, étiquette les chiffres (VÉRIFIÉ, ESTIMÉ, HYPOTHÈSE, INCONNU), termine par les sources."),
        "relecteur": ("sonnet", "Relit un livrable avant publication ou envoi.", "Vérifie dans l'ordre : données personnelles ou secrets, erreurs factuelles, cohérence avec mon style, fautes et clarté. Donne la correction exacte. Si tout est bon, dis « Prêt »."),
        "trieur": ("haiku", "Range l'inbox dans les bons projets et notes.", "Pour chaque élément de 00-inbox : choisis la destination (projet, idée, connaissance), range-le, puis retire-le de l'inbox. Ne supprime jamais un fichier : déplace-le."),
    }
    for n, (m, d, b) in agents.items():
        t = f"---\nname: {n}\ndescription: {d}\nmodel: {m}\n---\n\n{b}\n"
        ecrire(R, f"03-agents/{n}.md", t + "\n↑ [[AGENTS]]")
        ecrire(R, f".claude/agents/{n}.md", t)
    ecrire(R, "03-agents/AGENTS.md", "# Agents\n\n" + "\n".join(f"- [[{n}]] : {v[1]}" for n, v in agents.items()) + "\n\nCopie active pour Claude Code : `.claude/agents/`.\n\n↑ [[INDEX]]")
    outils = c.get("outils", [])
    ecrire(R, "05-outils/OUTILS.md", "# Outils\n\n" + liste(outils) + "\n\n- [[Chats et rôles]]\n\n↑ [[INDEX]]")
    ecrire(R, "05-outils/Chats et rôles.md", "# Chats et rôles\n\n| Chat | Rôle |\n|---|---|\n| Chat principal | chef d'orchestre de l'AIOS |\n\nTous les chats lisent [[INDEX]] puis [[Toi]] avant de me poser une question sur moi.\n\n↑ [[OUTILS]]")

    # ---------- Second cerveau ----------
    poles = {
        "Ton style": ("Style", "Comment j'écris, je parle et je dessine.", "style", [
            ("Ton d'écriture", c.get("style", {}).get("ton", "À compléter.")),
            ("Style visuel", c.get("style", {}).get("visuel", "À compléter.")),
            ("Format des réponses", "Clair, direct, structuré. Jamais d'emojis.")]),
        "Ta méthode": ("Méthode", "Mes règles de travail.", "methode", [(r.split(" :")[0][:60], r) for r in regles]),
        "Tes projets": ("Projets", "Chaque projet et son dossier.", "projet",
                        [(f"Projet {p['nom']}", f"{p.get('mission', '')}\n\nDossier : [[01-projets/{d}/CLAUDE|{p['nom']}]] · [[01-projets/{d}/STATE|état]]") for d, p in zip(dossiers_projets, projets)]),
        "Tes connaissances": ("Connaissances/Sujets", "Ce que j'apprends, classé par sujet. Fiches sources dans `Connaissances/Sources/`.", "sujet",
                              [(s, "## Ce que je sais\n_Synthèse mise à jour à chaque nouvelle source._") for s in c.get("sujets", ["Business", "IA", "Productivité"])]),
        "Tes erreurs": ("Erreurs", "Ce qu'on ne refait plus : une note par erreur, avec la règle.", "erreur", []),
        "Tes décisions": ("Décisions", "Les décisions datées.", "decision", [(f"{AUJ} Création de l'AIOS", "Mise en place de mon AIOS et de mon second cerveau.")]),
        "Tes idées": ("Idées", "Les idées en attente d'évaluation.", "idee", []),
        "Tes habitudes": ("Habitudes", "Comment je fonctionne, et ce que Claude doit faire en conséquence.", "habitude", [(h[:60], h) for h in c.get("facon_de_travailler", [])]),
        "Tes skills": ("Skills", "Mes skills et ceux que j'utilise : historique, usage.", "skill", [("memoire-aios", "- Statut : installé\n- Sert à : garder la mémoire de l'AIOS toujours active.\n- Historique :\n  - " + AUJ + " : installé.")]),
        "Tes sessions": ("Sessions", "Une note par session de travail.", "session", [(AUJ, "**Fait** : création de l'AIOS.\n**Décisions** : [[" + AUJ + " Création de l'AIOS]]\n**Prochaine étape** : choisir le projet prioritaire.")]),
        "Tes offres": ("Offres", "Ce que je vends ou vendrai.", "offre", []),
        "Tes clients": ("Clients", "Qui achète, pourquoi il reste.", "client", []),
        "Ta vie perso": ("Personnel", "Ce qui me concerne personnellement (jamais de données sensibles).", "perso", []),
        "Tes récaps": ("Récaps", "Un récap par semaine : fait, erreurs, décisions, priorités.", "recap", []),
    }
    for pole, (dossier, desc, tag, items) in poles.items():
        for titre, corps in items:
            note(R, f"{C}/{dossier}/{titre.replace('/', '-')}.md", titre, corps, pole, tag)
        liens = " · ".join(f"[[{t.replace('/', '-')}]]" for t, _ in items) or "_Aucune note pour l'instant._"
        ecrire(R, f"{C}/{pole}.md", f"# {pole}\n\n{desc}\n\n{liens}\n\n---\n↑ [[Toi]]")
    # Toi : identité
    toi_items = [("Identité", c.get("identite", nom)), ("Objectifs", liste(c.get("objectifs", []))), ("Situation", c.get("situation", "À compléter."))]
    for t, corps in toi_items:
        note(R, f"{C}/Toi/{t}.md", t, corps, "Toi", "toi")
    ecrire(R, f"{C}/Toi.md", f"""
# Toi : centre du second cerveau

{nom}. Tout part d'ici. Claude lit ce cerveau avant de me poser une question sur moi.

- Qui je suis : {' · '.join(f'[[{t}]]' for t, _ in toi_items)}
- {' · '.join(f'[[{p}]]' for p in poles)}
- Règles de capture : [[PROTOCOLE]] · Tableau de bord : [[INDEX]] · Outils : [[OUTILS]]
""")
    ecrire(R, f"{C}/PROTOCOLE.md", f"""
# Protocole de capture

Objectif : aucune information utile ne se perd. Chaque note est courte, datée, reliée, et finit par `↑ [[pôle]]`. On met à jour une note existante plutôt que créer un doublon. Jamais d'emojis.

| Quand | Où |
|---|---|
| Idée | `Idées/` (`Idée - titre`) |
| Décision | `Décisions/` (`AAAA-MM-JJ titre`) |
| Erreur | `Erreurs/` (avec la règle pour ne pas refaire) |
| Vidéo, article, livre | `Connaissances/Sources/` (`Auteur - Titre`), relié à un sujet de `Connaissances/Sujets/` |
| Façon de travailler | `Habitudes/` |
| Skill créé, modifié, installé, supprimé | `Skills/` (historique daté) |
| Info perso | `Personnel/` (jamais de données sensibles) |
| Fin de session | `Sessions/AAAA-MM-JJ` + [[INDEX]] |

↑ [[Toi]]
""")
    modeles = {
        "Fiche source": "# {{title}}\n\n- Auteur :\n- Type :\n- Lien :\n- Date :\n- Sujets : [[ ]]\n- Idées clés :\n  1.\n- À appliquer :\n\n↑ [[Tes connaissances]]",
        "Fiche erreur": "# {{title}}\n\n- Date :\n- Projet :\n- Erreur :\n- Règle pour ne pas refaire :\n\n↑ [[Tes erreurs]]",
        "Fiche décision": "# {{date}} {{title}}\n\n- Décision :\n- Pourquoi :\n- Ce que ça change :\n\n↑ [[Tes décisions]]",
        "Fiche idée": "# Idée - {{title}}\n\n- L'idée :\n- Pourquoi :\n- Prochaine étape :\n\n↑ [[Tes idées]]",
        "Fiche session": "# {{date}}\n\n**Projet** :\n**Fait** :\n**Décisions** :\n**Erreurs** :\n**Prochaine étape** :\n\n↑ [[Tes sessions]]",
    }
    for n, t in modeles.items():
        ecrire(R, f"{C}/Modèles/{n}.md", t)

    # ---------- Obsidian ----------
    rgb = lambda h: int(h.lstrip("#"), 16)
    groupes = [("file:INDEX", "#FFFFFF"), ("file:Toi", "#FFFFFF"), (f"path:{C}/Erreurs", "#FF4D4D"), (f"path:{C}/Connaissances", "#FFD23F"),
               (f"path:{C}/Décisions", "#7BE3B0"), (f"path:{C}/Habitudes", "#2FD3C7"), (f"path:{C}/Skills", "#FF7A45"), (f"path:{C}/Projets", "#B48CFF"),
               (f"path:{C}/Sessions", "#C0C6D4"), (f"path:{C}", "#EEF2F8"), ("path:01-projets", "#B48CFF"), ("path:02-skills", "#FF7A45"),
               ("path:03-agents", "#2FD3C7"), ("path:05-outils", "#3D9BFF"), ("path:00-inbox", "#FFC59A")]
    obs = os.path.join(R, ".obsidian")
    os.makedirs(obs, exist_ok=True)
    fichiers = {
        "graph.json": {"colorGroups": [{"query": q, "color": {"a": 1, "rgb": rgb(h)}} for q, h in groupes], "showOrphans": True, "hideUnresolved": True, "showTags": False, "showAttachments": False},
        "app.json": {"userIgnoreFilters": [f"{C}/Modèles/", "06-github/"], "newFileLocation": "folder", "newFileFolderPath": "00-inbox", "alwaysUpdateLinks": True},
        "templates.json": {"folder": f"{C}/Modèles", "dateFormat": "YYYY-MM-DD"},
    }
    for n, d in fichiers.items():
        p = os.path.join(obs, n)
        if not os.path.exists(p):
            json.dump(d, open(p, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"AIOS créé dans {R} : {len(NOTES_CREEES)} fichiers.")


if __name__ == "__main__":
    main()
