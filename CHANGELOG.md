# Changelog
## 2.3.0 (2026-11-19)
- Première question du skill : mode **débutant** ou **avancé**. Le mode avancé reste le comportement précédent.
- Mode débutant : un petit coffre (Accueil, Moi en 6 fiches, thèmes, Notes en vrac, Plus tard, Archives, Journal), une question à la fois, vocabulaire simple. Marche dans Cowork, sans Python ni Obsidian : les notes sont créées directement avec l'outil d'écriture de fichiers. Pas d'agents, pas de Git, pas de mods.
- Mémoire en temps réel : tout s'écrit au moment où ça arrive, captures d'écran comprises.
- Chercher avant de demander : Smart Connections (recherche par le sens) en premier s'il est branché, puis mot exact, puis `rappels.py`.
- Graphe : `verifier_liens.py` après chaque série d'écritures (toujours 1 groupe) ; nouveau `relier_orphelins.py` qui relie les notes isolées à leur parent.
- Nouveau `journal.py` : journal de bord (une ligne par projet et par jour), décisions, date de l'INDEX, `verifier` en lecture seule, sauvegarde avant écriture, refus des secrets évidents, `--selftest`.
- Description du skill raccourcie (moins de 200 caractères) pour l'import dans claude.ai.
- Clearmind recommandé comme skill de base.
## 2.2.0 (2026-11-10)
- Trois scripts d'entretien : `rappels.py` (notes liées à un sujet), `controle_aios.py` (contrôle de santé en lecture seule), `consolider.py` (récaps mensuels, doublons, notes maigres, sans rien supprimer).
- Mode mémoire : rappels avant de répondre et entretien hebdomadaire.
## 2.1.0 (2026-11-03)
- Mode mémoire : import des sections « À importer dans le cerveau » préparées par les routines, fiches sources plus complètes (auteur, lien, date), une note complète par skill, idées avec pourquoi et prochaine étape, note d'historique pour les gros chantiers.
## 2.0.0 (2026-11-03)
- Mode création : 10 questions et un script qui construit tout l'AIOS (projets, skills, agents, outils, second cerveau, configuration Obsidian).
- Vérificateur de liens : aucune note isolée dans le graphe.
- Mode mémoire toujours actif (début et fin de session automatiques), historique des skills, aucun emoji.
## 1.0.0 (2026-11-03)
- Première version : capture des idées, décisions, erreurs, sources, habitudes et sessions.
