---
name: memoire-aios
description: Crée et fait vivre un second cerveau avec Claude, en mode débutant (simple, sans code) ou avancé (AIOS complet). À utiliser pour crée mon second cerveau, crée mon AIOS, note ça, retiens, vas-y.
---

# Mémoire AIOS

Un **second cerveau** est un dossier de notes que Claude lit au début de chaque séance et complète au fil du travail : qui est l'utilisateur, ses objectifs, ses décisions, ses corrections, ses idées. Claude relit le texte exact au lieu de « se souvenir ».

Deux niveaux, choisis une fois pour toutes à la création :
- **Débutant** : un petit coffre de notes, quelques dossiers, aucun code. Marche dans Cowork (application Claude pour ordinateur) avec un dossier choisi. Obsidian est facultatif.
- **Avancé** : un **AIOS** complet (règles, tableau de bord, projets, skills, agents, outils, scripts d'entretien) avec un second cerveau Obsidian.

Et deux moments :
- **Création** : le dossier n'existe pas encore (ou l'utilisateur dit « crée mon second cerveau », « crée mon AIOS »).
- **Mémoire** : le dossier existe. La mémoire est alors toujours active. Le niveau se lit dans le `CLAUDE.md` du dossier (ligne `Niveau : débutant` ou `Niveau : avancé` ; sans cette ligne : avancé).

Règles communes aux deux niveaux :
- Jamais d'emojis, ni dans les notes ni dans les réponses.
- **Tout s'écrit au moment où ça arrive** (une décision, une correction, une idée, une info durable), pas seulement en fin de séance.
- On ne supprime rien : ce qui ne sert plus va dans `Archives` (débutant) ou `_corbeille/AAAA-MM-JJ/` (avancé).
- Aucun mot de passe, code, numéro de carte, donnée bancaire ni donnée personnelle d'un tiers dans les notes.
- **Aucune note isolée** : chaque note contient un lien `[[...]]` vers sa note parente. Le graphe doit former **un seul groupe**.
- Recommandé en complément : le skill [Clearmind](https://github.com/horizonchapter/clearmind) comme skill de base (lecture complète des demandes, avis honnête, rien d'inventé).

---

## Création : la première question

Pose cette seule question, puis attends la réponse :

> « On va créer ton second cerveau. Tu préfères la version **débutant** (quelques dossiers de notes, rien de technique) ou **avancé** (un système complet avec projets, agents et scripts) ? Si tu hésites, prends débutant : on pourra passer à l'avancé plus tard. »

Réponse « débutant », « simple », « je ne sais pas » ou aucune préférence : **mode débutant**. Réponse « avancé » : **mode avancé**.

---

## Mode débutant

Pas d'agents, pas de boîtes de messages, pas de Git, pas de mods, pas de scripts obligatoires. Vocabulaire simple : « coffre » pour le dossier, « note » pour un fichier. Une question à la fois, avec une proposition par défaut que l'utilisateur peut accepter d'un mot.

### 1. Vérifier l'accès au dossier
- Dans Cowork : l'utilisateur a choisi un dossier (« travailler dans un dossier »). Ce dossier est le coffre. S'il n'en a pas choisi, dis-lui : « Crée un dossier vide, par exemple Mon coffre dans Documents, puis choisis-le sous la zone de message. Un dossier dédié, jamais tout Documents ni le Bureau. »
- Sans accès aux fichiers (chat simple) : dis-le en une phrase, puis donne chaque note dans un bloc à copier, avec son nom de fichier. N'affirme jamais qu'une note est enregistrée si elle ne l'est pas.

### 2. Les questions, une à la fois
1. « Comment tu t'appelles, et que fais-tu dans la vie, en une ou deux phrases ? »
2. « Qu'est-ce que tu veux réussir dans les prochains mois ? Deux ou trois choses suffisent. »
3. « Comment tu aimes travailler avec moi ? Par exemple : réponses courtes, tutoiement, me demander avant de modifier un texte. »
4. « Quels grands thèmes veux-tu ranger ? Je te propose : Activité, Communication, Admin, Formations. Tu gardes, tu enlèves ou tu ajoutes. »
5. « Y a-t-il des mots ou des choses que je ne dois jamais écrire pour toi ? » (facultatif)

Une réponse manque : écris « À compléter » et continue. On n'invente rien.

### 3. Créer les notes avec l'outil d'écriture de fichiers
Aucun script n'est nécessaire : crée chaque fichier directement. Ne remplace jamais un fichier qui existe déjà : complète-le.

```
<coffre>/
├── CLAUDE.md                        les règles pour Claude (modèle ci-dessous)
├── Accueil.md                       la page d'ouverture, centre du graphe
├── Journal.md                       une ligne par séance
├── Moi/
│   ├── Identité.md
│   ├── Façon de travailler.md
│   ├── Objectifs.md
│   ├── Compétences.md
│   ├── Ce que Claude a appris de moi.md
│   └── Mes décisions.md
├── <Thème>/<Thème>.md               un dossier et une page par thème choisi
├── Notes en vrac/Notes en vrac.md
├── Plus tard/Plus tard.md
└── Archives/Archives.md
```

Contenu :
- `Accueil.md` : titre « Accueil », une phrase sur l'utilisateur, puis une liste de liens vers toutes les autres notes : `[[Moi/Identité|Identité]]`, `[[Moi/Objectifs|Objectifs]]`, chaque fiche de `Moi`, chaque page de thème, `[[Notes en vrac/Notes en vrac|Notes en vrac]]`, `[[Plus tard/Plus tard|Plus tard]]`, `[[Archives/Archives|Archives]]`, `[[Journal]]`.
- Chaque autre note : un titre, son contenu (les réponses de l'utilisateur, ou « À compléter »), et en dernière ligne `↑ [[Accueil]]`.
- `Mes décisions.md` et `Ce que Claude a appris de moi.md` : une ligne par entrée, `AAAA-MM-JJ : ... : pourquoi`.
- `Journal.md` : une première ligne `AAAA-MM-JJ : création du coffre`.
- `CLAUDE.md` :

```
# Règles pour Claude dans ce coffre
Niveau : débutant

## Au début de chaque séance
Lis Accueil.md puis les notes du dossier Moi. Ne me pose pas une question dont la réponse est déjà dans le coffre.

## Pendant
- Écris au moment où ça arrive : une décision dans Moi/Mes décisions.md, une correction de ma part dans Moi/Ce que Claude a appris de moi.md (avec mes mots), une idée pour plus tard dans Plus tard, le reste dans la page du bon thème.
- Une note = une idée, courte et datée. Complète une note qui existe plutôt que d'en créer une deuxième.
- Chaque nouvelle note se termine par ↑ [[Accueil]] ou par un lien vers la page de son thème.
- Ajouter une ligne : fais-le et dis-le en une phrase. Déplacer, renommer ou ranger plusieurs notes : montre ton plan et attends mon accord.
- Rien ne s'efface : ce qui ne sert plus va dans Archives.
- Jamais de mot de passe, de code, de numéro de carte ni de données personnelles de mes clients ou de mes proches.

## À la fin de la séance
Une ligne dans Journal.md : date, ce qu'on a fait, la prochaine étape.
```

### 4. Vérifier que tout est relié
- Si Python est disponible : `python3 scripts/verifier_liens.py "<coffre>"` doit afficher « 1 groupe ». Sinon, ajoute `↑ [[Accueil]]` aux notes listées et relance.
- Sans Python : relis chaque note créée et vérifie qu'elle contient un lien vers `Accueil` ou vers une page reliée à `Accueil`, et qu'`Accueil.md` cite chaque fiche.

### 5. Expliquer la suite en 3 lignes
1. « Ton coffre est prêt. À chaque séance, choisis ce dossier dans Cowork : je lis ton Accueil et tes fiches avant de répondre. »
2. « Dis "note ça" ou "retiens" quand tu veux garder quelque chose ; je note aussi tout seul tes décisions et tes corrections. »
3. « Plus tard, si tu veux voir tes notes sous forme de graphe : installe Obsidian (gratuit, obsidian.md) et ouvre ce dossier comme coffre. Rien à changer dans les notes. »

### Mémoire, mode débutant
- **Début** : lis `CLAUDE.md`, `Accueil.md`, les fiches de `Moi` et la dernière ligne de `Journal.md`. Sur « vas-y » : 3 lignes (où on en est, ce qui reste, la prochaine étape proposée), puis attends l'accord.
- **Pendant** : applique les règles du `CLAUDE.md` du coffre.
- **Retrouver une note** : si l'outil Smart Connections est disponible (module Obsidian ou connecteur), cherche d'abord par le sens ; sinon cherche par mots dans les noms et le contenu des notes.
- **Fin** : la ligne du `Journal.md`, puis une phrase : ce qui a été noté et où.
- **Passer à l'avancé** : seulement si l'utilisateur le demande. Garde toutes les notes existantes, passe la ligne `Niveau` à `avancé` et suis le mode avancé ci-dessous sans rien écraser.

---

## Mode avancé

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
3. Ajoute la ligne `Niveau : avancé` sous le titre du `CLAUDE.md` créé.
4. Lance `python3 scripts/verifier_liens.py "<chemin>/AIOS"` : il doit afficher « 1 groupe ». Sinon, ajoute `↑ [[pôle]]` aux notes listées et relance. (`relier_orphelins.py` ne touche pas une note modifiée depuis moins de 5 h : il sert à l'entretien, pas juste après la création.)
5. Sans Python : crée les fichiers de `exemples/arborescence.md` avec l'outil d'écriture, chacun terminé par `↑ [[pôle]]`. Sans accès au disque : génère les fichiers dans l'espace de travail et livre un zip à décompresser.

### 4. Brancher, en 4 étapes pour l'utilisateur
1. Obsidian → « Ouvrir un dossier comme coffre » → le dossier AIOS → « Faire confiance ».
2. Ctrl+G pour la vue graphe, ouvrir `Toi` puis `INDEX`.
3. Ajouter le dossier AIOS à chaque chat Claude qui doit s'en servir (Cowork, Claude Code, chats liés à l'ordinateur).
4. Ajouter dans les préférences globales de Claude : « Mon AIOS est le dossier <chemin> : lis INDEX.md puis 04-second-cerveau avant de me poser une question sur moi, et notes-y chaque décision, erreur ou info durable au moment où elle arrive. Quand je dis « vas-y », reprends où j'en suis. »

Facultatif, pour un coffre qui grossit : le module Obsidian **Smart Connections** (recherche par le sens, gratuit, local), et son serveur MCP en lecture seule pour que Claude Code l'interroge.

Puis passe en mode mémoire et crée la première note de session.

### Mémoire, mode avancé (toujours actif)

#### Début de session
1. Lis `INDEX.md`, `04-second-cerveau/Toi.md`, la dernière note de `Sessions/`, les notes d'`Erreurs/` liées au sujet et le STATE.md du projet.
2. Si une routine ou un autre outil a préparé une section « À importer dans le cerveau » (par exemple un suivi du soir ou une revue hebdomadaire dans Notion), ou des vidéos et articles marqués Utile ou Important pas encore importés : crée les notes correspondantes (une fiche par source dans `Connaissances/Sources/`) et marque la section comme importée.
3. Sur « vas-y » : 5 lignes (où on en est, décidé, reste à faire, prochaine action), puis attends l'accord.
4. Ne pose jamais une question dont la réponse est déjà dans la mémoire.

#### Chercher avant de demander, dans cet ordre
1. **Smart Connections** (recherche par le sens) s'il est branché : `search_by_text`, `search_similar`, `get_note`. Utile quand on ne connaît pas le mot exact.
2. Recherche par mot exact (Omnisearch dans Obsidian, ou recherche dans les fichiers).
3. `python3 scripts/rappels.py mot1 mot2 --aios "<chemin>"` : cite en une ligne les 1 à 3 notes utiles (idée, décision, erreur ancienne).
4. Journal, STATE.md des projets.
Seulement ensuite, poser la question à l'utilisateur.

#### Pendant : capturer au moment où ça arrive
Rien d'utile ne se perd, même si l'utilisateur ne demande rien. On écrit tout de suite, pas en fin de session. Une note = une idée. Courte, datée, reliée par `[[...]]`, terminée par `↑ [[pôle]]`. Mettre à jour plutôt que dupliquer. Aucune note isolée : chaque note est reliée à son pôle, au projet ou au sujet, et à la session du jour. Une capture d'écran envoyée : décrire ce qu'elle montre et noter le fait.

| Ce qui arrive | Dossier (dans 04-second-cerveau) | Nom et contenu |
|---|---|---|
| Idée | `Idées/` | `Idée - titre` : l'idée, pourquoi, prochaine étape |
| Décision | `Décisions/` | `AAAA-MM-JJ titre` : décision, pourquoi, ce que ça change |
| Erreur ou piège | `Erreurs/` | ce qui s'est passé + **règle pour ne pas refaire** |
| Vidéo, article, livre | `Connaissances/Sources/` | `Auteur - Titre` : auteur, lien, date, idées clés, à appliquer, sujets `[[...]]` ; puis mettre à jour la synthèse du sujet dans `Connaissances/Sujets/` |
| Façon de travailler qui revient | `Habitudes/` | ce que l'utilisateur fait → ce que Claude doit faire |
| Demande répétée (« refais pareil ») | `Habitudes/` + `02-skills/STATE.md` | proposer un modèle ou un skill |
| Skill créé, modifié, installé, utilisé, supprimé | `Skills/` | une note par skill : statut, à quoi il sert, historique daté (créé, modifié, supprimé, pourquoi), « Utilisé dans » (projet, date, verdict) |
| Info personnelle | `Personnel/` | jamais de mot de passe, numéro, donnée bancaire, adresse |
| Client, offre | `Clients/`, `Offres/` | modèles dans `Modèles/` |

Après chaque série d'écritures : `python3 scripts/verifier_liens.py "<chemin>"` doit rester à « 1 groupe » (réparation : relier à la main les notes listées ; pour les notes de plus de 5 h, `python3 scripts/relier_orphelins.py "<chemin>" --appliquer` relie chaque groupe isolé à son parent le plus proche).

#### Journal, décisions, INDEX : par le script
Ces fichiers sont modifiés par plusieurs sessions chaque jour ; à la main, ils finissent avec des octets NUL, des lignes hors ordre et des décisions collées. Depuis la racine du coffre (`scripts/` = dossier du skill) :
- `python3 scripts/journal.py journal <date> <projet> <fait> <décisions> <prochaine étape> <bloqué par>` : une seule ligne par projet et par jour. Si elle existe, elle est **remplacée** : relire l'ancienne (affichée par le script) et passer la ligne complète, pas seulement le nouveau.
- `python3 scripts/journal.py decision <DECISIONS.md> "<décision> — <pourquoi>"` : date du jour ajoutée si absente.
- `python3 scripts/journal.py index-date INDEX.md` : met « Mis à jour : » à la date du jour.
- `python3 scripts/journal.py verifier` : lecture seule (octets NUL, ordre, doublons projet+jour, décisions collées). Signaler les défauts, sans les corriger automatiquement.

Le script sauvegarde dans `_backup/AAAA-MM-JJ/` avant d'écrire, écrit de façon atomique, garde l'encodage et refuse un secret évident (code 2 : écrire « [secret retiré] »). Test : `python3 scripts/journal.py --selftest`. Sans Python : écrire la ligne à la main, en fin de fichier, au même format.

#### Fin de session (même sans « fin de session » : travail terminé ou plus d'une heure sans message)
1. `Sessions/AAAA-MM-JJ` : projet, fait (détaillé), décisions, erreurs, habitudes observées, prochaine étape, avec des liens vers chaque note créée. Pour un gros chantier, ajouter une note d'historique détaillée.
2. Ligne du projet dans `INDEX.md`, STATE.md du projet, une ligne dans `JOURNAL_DE_BORD.md` (par le script).
3. `python3 scripts/verifier_liens.py` : toujours « 1 groupe ».
4. Terminer par 3 lignes : ce qui a été noté, où, prochaine étape.

#### Entretien (une fois par semaine, ou sur « fais le ménage du cerveau »)
1. `python3 scripts/controle_aios.py "<chemin>"` : contrôle de santé en lecture seule (STATE.md complets et à jour, STATE et DECISIONS de chaque projet, sauvegardes à purger, fichiers en vrac). Corrige ce qui est listé.
2. `python3 scripts/consolider.py "<chemin>"` : sessions de plus de 28 jours à résumer dans un récap mensuel, doublons probables, notes trop maigres. Fusionne, résume, complète ; ne supprime jamais.
3. `python3 scripts/journal.py verifier`, puis `scripts/verifier_liens.py` : toujours « 1 groupe ».

#### Répondre depuis la mémoire
Question générale (« comment devenir riche ? ») : chercher d'abord dans `Connaissances/`, répondre « D'après tes notes… » en citant les fiches et leurs auteurs, puis compléter en le signalant.

---

## Si le dossier n'est pas accessible
Le dire en une phrase et donner les notes prêtes à coller. Ne jamais affirmer qu'une note est enregistrée si elle ne l'est pas.
