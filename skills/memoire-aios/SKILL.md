---
name: memoire-aios
description: Crée et fait vivre un AIOS, un système complet autour de Claude (projets, skills, agents, règles, outils) avec un second cerveau Obsidian où tout est noté et relié. À utiliser pour « crée mon AIOS », « /memoire-aios », et ensuite à chaque session où le dossier AIOS est accessible, ou quand l'utilisateur dit « note ça », « retiens », « résume cette vidéo », « vas-y ».
---

# Mémoire AIOS

Un **AIOS** est un dossier qui réunit tout ce que Claude doit savoir : règles (`CLAUDE.md`), tableau de bord (`INDEX.md`), projets, skills, agents, outils, et un **second cerveau** (`04-second-cerveau/`) ouvert comme coffre Obsidian, où chaque idée, décision, erreur, connaissance et session est notée et reliée.

Deux modes :
- **Création** : le dossier AIOS n'existe pas encore (ou l'utilisateur dit « crée mon AIOS »).
- **Mémoire** : le dossier existe : la mémoire est toujours active.

Jamais d'emojis, ni dans les notes ni dans les réponses.

---

## Mode création

### 1. Expliquer en 4 lignes
Ce qu'on va construire, où (un dossier, par défaut `Bureau/AIOS`), qu'il faut **Obsidian** (gratuit, obsidian.md) pour la vue graphe, et que rien d'existant ne sera supprimé.

### 2. Poser les questions (en une fois, avec l'outil de questions s'il existe, sinon en liste)
1. Ton prénom ou ta marque, et ce que tu fais en une phrase.
2. Tes objectifs des 3 à 12 prochains mois.
3. Ta situation (statut, pays, contraintes).
4. Tes projets (nom + mission en une phrase chacun) et lequel est prioritaire.
5. Ta façon de travailler (horaires, dictée, ce qui t'agace, ce que tu refais souvent).
6. Ton style : ton d'écriture, style visuel.
7. Tes règles pour Claude (exemples : « tu prépares, je valide », « chiffres étiquetés », « pas d'emojis »).
8. Les sujets que tu veux apprendre ou suivre (pour classer tes résumés de vidéos et d'articles).
9. Tes outils (Claude chat, Cowork, Claude Code, Notion, Gmail, GitHub…).
10. Où créer le dossier.

Si une réponse manque, mets « À compléter » et continue : on n'invente rien.

### 3. Construire
1. Écris les réponses dans `reponses.json` (format : `exemples/reponses-exemple.json`).
2. Lance `python3 scripts/creer_aios.py --dossier "<chemin>/AIOS" --config reponses.json`. Le script crée toute l'arborescence, les notes reliées, les modèles, les agents et la configuration Obsidian (couleurs du graphe, dossier des modèles). Il n'écrase jamais un fichier existant.
3. Lance `python3 scripts/verifier_liens.py "<chemin>/AIOS"` : il doit afficher « 1 groupe ». Sinon, relie les notes listées à leur pôle.
4. Sans accès au disque : génère les fichiers dans l'espace de travail et livre un zip à décompresser.

### 4. Brancher, en 4 étapes pour l'utilisateur
1. Obsidian → « Ouvrir un dossier comme coffre » → le dossier AIOS → « Faire confiance ».
2. Ctrl+G pour la vue graphe, ouvrir `Toi` puis `INDEX`.
3. Ajouter le dossier AIOS à chaque chat Claude qui doit s'en servir (Cowork, Claude Code, chats liés à l'ordinateur).
4. Ajouter dans les préférences globales de Claude : « Mon AIOS est le dossier <chemin> : lis INDEX.md puis 04-second-cerveau avant de me poser une question sur moi, et notes-y chaque décision, erreur ou info durable. Quand je dis « vas-y », reprends où j'en suis. »

Puis passe en mode mémoire et crée la première note de session.

---

## Mode mémoire (toujours actif)

### Début de session
1. Lis `INDEX.md`, `04-second-cerveau/Toi.md`, la dernière note de `Sessions/`, les notes d'`Erreurs/` liées au sujet et le STATE.md du projet.
2. Sur « vas-y » : 5 lignes (où on en est, décidé, reste à faire, prochaine action), puis attends l'accord.
3. Ne pose jamais une question dont la réponse est déjà dans la mémoire.

### Pendant : capturer
Une note = une idée. Courte, datée, reliée par `[[...]]`, terminée par `↑ [[pôle]]`. Mettre à jour plutôt que dupliquer. Aucune note isolée.

| Ce qui arrive | Dossier (dans 04-second-cerveau) | Nom et contenu |
|---|---|---|
| Idée | `Idées/` | `Idée - titre` |
| Décision | `Décisions/` | `AAAA-MM-JJ titre` : décision, pourquoi, ce que ça change |
| Erreur ou piège | `Erreurs/` | ce qui s'est passé + **règle pour ne pas refaire** |
| Vidéo, article, livre | `Connaissances/Sources/` | `Auteur - Titre` : idées clés, à appliquer, sujets ; puis mettre à jour la synthèse du sujet dans `Connaissances/Sujets/` |
| Façon de travailler qui revient | `Habitudes/` | ce que l'utilisateur fait → ce que Claude doit faire |
| Demande répétée (« refais pareil ») | `Habitudes/` | proposer un modèle ou un skill |
| Skill créé, modifié, installé, utilisé, supprimé | `Skills/` | historique daté + « utilisé dans » |
| Info personnelle | `Personnel/` | jamais de mot de passe, numéro, donnée bancaire, adresse |
| Client, offre | `Clients/`, `Offres/` | modèles dans `Modèles/` |

### Fin de session (même sans « fin de session » : travail terminé ou plus d'une heure sans message)
1. `Sessions/AAAA-MM-JJ` : projet, fait (détaillé), décisions, erreurs, habitudes observées, prochaine étape, avec des liens vers chaque note créée.
2. Ligne du projet dans `INDEX.md`, STATE.md du projet, une ligne dans `JOURNAL_DE_BORD.md`.
3. Si des notes ont été créées : `python3 scripts/verifier_liens.py` doit rester à « 1 groupe ».
4. Terminer par 3 lignes : ce qui a été noté, où, prochaine étape.

### Répondre depuis la mémoire
Question générale (« comment devenir riche ? ») : chercher d'abord dans `Connaissances/`, répondre « D'après tes notes… » en citant les fiches et leurs auteurs, puis compléter en le signalant.

### Si le dossier n'est pas accessible
Le dire en une phrase et donner les notes prêtes à coller. Ne jamais affirmer qu'une note est enregistrée si elle ne l'est pas.
