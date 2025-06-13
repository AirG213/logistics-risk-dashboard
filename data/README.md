# Structure du dossier `/data`

Ce dossier contient **l’ensemble des sources de données utilisées dans le projet**, rangées pour garantir la traçabilité et la reproductibilité des analyses.

---

- `/raw/` : fichiers ZIP d’origine **téléchargés sur Kaggle** (non modifiés, non extraits).
- `/extracted/` : dossiers par dataset, contenant les fichiers **CSV extraits** (ou XLSX, le cas échéant) directement issus des ZIP de `/raw/`.
- `/cleaned/` : jeux de données **nettoyés, harmonisés et enrichis**, prêts pour l’analyse et la visualisation.

⚠️ *Les dossiers `/data/` ne sont pas versionnés sur GitHub* (voir `.gitignore`) pour éviter d’alourdir le dépôt avec des fichiers volumineux.

Chaque sous-dossier contient un `README.md` précisant son rôle, la structure et la liste des fichiers.