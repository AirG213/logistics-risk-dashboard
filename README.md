# 📦 Supply Chain Resilience & Risk Analysis

## 🔍 Objectif du projet

Ce projet vise à **analyser les risques et la résilience logistique** à travers différents modes de transport : routier, ferroviaire, aérien, maritime.
Il repose sur un **pipeline de traitement de données entièrement automatisé** couplé à un **dashboard interactif Streamlit**.

L’utilisateur peut en une seule commande :

- Créer un environnement Python propre
- Télécharger les données depuis Kaggle (via token intégré)
- Nettoyer et structurer chaque dataset via des notebooks d’analyse EDA
- Lancer un dashboard prêt à l’emploi, sans configuration manuelle

---

## ⚙️ Pré-requis

- **Python 3.9+** doit être installé sur votre machine

---

## 🚀 Lancement du projet 

> Pas besoin de cloner manuellement des données, ni d’installer les paquets vous-même.

### 🧪 1. Télécharger le dépôt

```bash
git clone https://github.com/AirG213/logistics-risk-dashboard.git
cd logistics-risk-dashboard
```

### 🏁 2. Lancer l’orchestration complète

```bash
python run_project.py
```

Ce script va automatiquement :

- [1/4] Créer un environnement virtuel `.venv` s’il n’existe pas
- [2/4] Installer les dépendances (`requirements.txt`)
- [3/4] Télécharger les datasets (via Kaggle CLI + token intégré dans le code)
- [4/4] Lancer le dashboard interactif avec Streamlit

> ⚠️ Si un fichier ou dataset manque ou échoue au téléchargement, lancer manuellemnt /data_sources/data_pipeline.ipynb, sinon si le **token privé** a expiré.  
> Merci de contacter un membre du projet pour obtenir un nouveau token (1 dataset sur 6 est privé).

---

## ⏳ Temps de traitement

**⛔ Important : Le temps d'exécution du pipeline dépend fortement de :**
- La **vitesse de votre connexion Internet** (téléchargement des datasets depuis Kaggle)
- La **puissance de votre machine** pour exécuter les notebooks d’analyse (certains EDA prennent plusieurs minutes)

👉 **Soyez patient lors du premier lancement**, une fois les fichiers générés, les relances suivantes seront bien plus rapides.

---
## 🗂️ Structure du projet

```
├── run_project.py              # Script principal (orchestration complète)
├── /data_sources/
│   └── data_pipeline.ipynb     # Pipeline automatisé Download → Extract → EDA
├── /data/
│   ├── raw/                    # ZIP Kaggle téléchargés
│   ├── extracted/              # Fichiers extraits (non modifiés)
│   └── cleaned/                # Fichiers nettoyés
├── /notebooks/                 # Notebooks EDA un par dataset
├── /dashboard/                 # Application Streamlit (app.py + modules)
├── requirements.txt            # Dépendances Python
```

---

## 📊 Datasets analysés automatiquement

| Domaine              | Source Kaggle                                                   | Données analysées                        |
|----------------------|-----------------------------------------------------------------|------------------------------------------|
| Routier (USA)        | `sobhanmoosavi/us-accidents`                                    | Accidents routiers 2016–2023             |
| Aérien (USA)         | `ryanjt/airline-delay-cause`                                    | Retards & annulations aéroportuaires     |
| Ferroviaire (USA)    | `chrico03/railroad-accident-and-incident-data`                  | Incidents de train, causes et coûts      |
| Supply Chain global  | `natasha0786/supply-chain-dataset`                              | KPI logistiques, fiabilité, risques      |
| Livraison Amazon     | `sujalsuthar/amazon-delivery-dataset`                           | **Simulation** de livraison colis        |
| Maritime             | `gabrielcabart/maritime-accidents-and-port-data`                | Accidents maritimes, ports, zones à risque

ℹ️ Pour plus de détails sur chaque source de données, voir le fichier `/data_sources/README.md`.

---

## 👨‍💻 Authors

- GOUADFEL Rayan — [@AirG213](https://github.com/AirG213)  
- ARRIGHI Fabien — [@arrighi-fabien](https://github.com/arrighi-fabien)  
- Encadré par Ali SKAF — [@skafali](https://github.com/skafali)
