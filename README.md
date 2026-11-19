<p align="center">
  <img src="assets/banner.png" alt="Mémoire AIOS : ton système IA et ton second cerveau" width="100%">
</p>

<p align="center">
  <img alt="Licence MIT" src="https://img.shields.io/badge/licence-MIT-2F5BFF?style=flat-square">
  <img alt="Skill Claude" src="https://img.shields.io/badge/Claude-skill-060A14?style=flat-square">
  <img alt="Obsidian" src="https://img.shields.io/badge/Obsidian-second%20cerveau-8E9AB2?style=flat-square">
</p>

# memoire-aios

**Un skill Claude pour construire ton propre AIOS (un système complet autour de Claude) et le faire vivre avec un second cerveau Obsidian où tout est noté et relié : idées, décisions, erreurs, résumés de vidéos, habitudes, skills, sessions.**
*A Claude skill that builds your own AI operating system around Claude and keeps a linked Obsidian second brain up to date, automatically.*

## ✦ Ce que fait le skill

**Deux niveaux, au choix dès la première question**
- **Débutant** : un petit coffre de notes (Accueil, Moi en 6 fiches, tes thèmes, Notes en vrac, Plus tard, Archives, Journal). Une question à la fois, sans jargon. Marche dans Cowork avec un simple dossier, sans Python, sans Obsidian, sans agents ni Git.
- **Avancé** : l'AIOS complet décrit ci-dessous.

**Création, mode avancé (une seule fois)**
- 10 questions : qui tu es, tes objectifs, tes projets, ta façon de travailler, ton style, tes règles, tes sujets, tes outils.
- Un script crée tout le dossier : règles (`CLAUDE.md`), tableau de bord (`INDEX.md`), un dossier par projet, skills, agents, outils, et le second cerveau avec ses pôles, ses modèles et la configuration Obsidian (couleurs du graphe).
- Tout est relié : un vérificateur garantit qu'aucune note n'est isolée dans le graphe.

**Mémoire (à chaque session)**
- Au début : Claude lit la mémoire. Dis « vas-y » et il reprend où tu en es.
- Pendant : il note au moment où ça arrive chaque idée, décision, erreur (avec la règle pour ne pas refaire), source, habitude et skill.
- À la fin : note de session, tableau de bord et état du projet mis à jour, même sans « fin de session ».
- Plus tard : il répond « D'après tes notes… » en citant tes sources. Avant de te poser une question, il cherche : par le sens avec Smart Connections s'il est branché, puis par mot exact, puis avec `rappels.py`.
- Le graphe reste d'un seul tenant : `verifier_liens.py` après chaque série d'écritures, `relier_orphelins.py` pour réparer. Journal et décisions passent par `journal.py` (sauvegarde avant écriture, refus des secrets).

**Entretien (chaque semaine)**
- Contrôle de santé en lecture seule : STATE.md complets et à jour, projets sans STATE ou DECISIONS, sauvegardes à purger, fichiers en vrac (`controle_aios.py`).
- Consolidation, comme le sommeil : sessions anciennes résumées en récap mensuel, doublons et notes trop maigres signalés, rien n'est supprimé (`consolider.py`).

## ✦ Aperçu

Le graphe Obsidian d'un AIOS tout juste créé, puis la création en une phrase (sortie réelle des scripts, avec les réponses d'exemple) :

<p align="center">
  <img src="assets/apercu-1.png" alt="Aperçu 1 : vue graphe Obsidian" width="49%">
  <img src="assets/apercu-2.png" alt="Aperçu 2 : création de l'AIOS" width="49%">
</p>

<p align="center"><sub><i>Exemple fictif, à titre d'illustration.</i></sub></p>

## ✦ Prérequis

- **Débutant** : Claude avec accès à un dossier (Cowork dans l'application Claude pour ordinateur). C'est tout. [Obsidian](https://obsidian.md) (gratuit) est facultatif, pour voir le graphe.
- **Avancé** : Claude avec accès à un dossier (Cowork, Claude Code, ou chat lié à l'ordinateur), Python 3 et [Obsidian](https://obsidian.md).
- Conseillé : [Clearmind](https://github.com/horizonchapter/clearmind) comme skill de base.

## ✦ Installation

**Télécharger** : bouton vert **Code → Download ZIP**, ou :

```bash
git clone https://github.com/horizonchapter/memoire-aios.git
```

**Claude Code** (pour tous tes projets) :

```bash
cp -r memoire-aios/skills/memoire-aios ~/.claude/skills/
```

**Claude (app et web)** : importe le fichier [`memoire-aios.zip`](memoire-aios.zip) dans les réglages des skills de Claude.

## ✦ Utilisation

1. Dis à Claude : « crée mon second cerveau » (ou « crée mon AIOS »). Il te demande d'abord : débutant ou avancé.
2. Avancé : ouvre le dossier créé dans Obsidian (« Ouvrir un dossier comme coffre »), puis Ctrl+G.
3. Ensuite, à chaque session : « vas-y », « note ça », « retiens », « résume cette vidéo ».

## ✦ Structure

```
memoire-aios/
├── skills/memoire-aios/
│   ├── SKILL.md                 le skill
│   ├── scripts/
│   │   ├── creer_aios.py        crée l'AIOS à partir des réponses ; n'écrase jamais un fichier existant
│   │   ├── verifier_liens.py    vérifie que toutes les notes forment un seul réseau dans Obsidian
│   │   ├── rappels.py           retrouve les notes liées à un sujet
│   │   ├── controle_aios.py     contrôle de santé, en lecture seule
│   │   ├── consolider.py        consolidation hebdomadaire, sans rien supprimer
│   │   ├── journal.py           journal de bord, décisions, INDEX, sans abîmer les fichiers
│   │   └── relier_orphelins.py  relie les notes isolées à leur parent
│   └── exemples/                arborescence créée, réponses d'exemple, fiche source
├── memoire-aios.zip             le même skill, prêt à importer
└── assets/                      bannière et aperçus
```

Structure créée : voir [`arborescence.md`](skills/memoire-aios/exemples/arborescence.md). Exemple de réponses : [`reponses-exemple.json`](skills/memoire-aios/exemples/reponses-exemple.json).

## ✦ Voir aussi

- [clearmind](https://github.com/horizonchapter/clearmind) : le skill de base conseillé (lit tout, n'invente rien, donne un avis franc).
- [claude-second-brain](https://github.com/horizonchapter/claude-second-brain) : les modèles `CLAUDE.md` / `STATE.md` / `DECISIONS.md`.
- [context-transfer](https://github.com/horizonchapter/context-transfer) : reprendre dans un nouveau chat sans rien perdre.
- [chef-employe](https://github.com/horizonchapter/chef-employe) · [claude-routines](https://github.com/horizonchapter/claude-routines) · [mods-claude-code](https://github.com/horizonchapter/mods-claude-code) · [pdf-luxe](https://github.com/horizonchapter/pdf-luxe)

## ✦ Licence

[MIT](LICENSE). Libre d'utilisation, de modification et de partage.
