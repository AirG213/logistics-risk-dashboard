# 📦 Data Sources for Supply Chain Disruption & Resilience Analysis

Ce dossier regroupe des sources gratuites et accessibles.

---

## 📊 Données Supply Chain & Disruptions (Gratuites et Téléchargeables)

### 1. [Global Daily Port Activity and Trade Estimates](https://www.kaggle.com/datasets/arunvithyasegar/daily-port-activity-data-and-trade-estimates)
- **Transport** : Maritime (mondial)
- **Format** : CSV
- **Description**: Données quotidiennes sur l’activité et les volumes de commerce de 24 ports stratégiques dans le monde.
- **Pourquoi ce choix ?** : Permet d’identifier des pics de congestion, des anomalies ou des tendances révélant une fragilité portuaire. Son échelle journalière est idéale pour croiser les données avec des événements météo ou des crises ponctuelles, même si la cause exacte de chaque perturbation n’est pas explicitée.

---

### 2. [Railroad Accident and Incident Data](https://www.kaggle.com/datasets/chrico03/railroad-accident-and-incident-data)
- **Transport** : Ferroviaire
- **Format** : CSV
- **Description** : Détails d’incidents ferroviaires aux USA : causes, lieux, conséquences.
- **Pourquoi ce choix ?** : C’est un exemple-type de dataset “richesse + granularité” pour cartographier et typologiser les risques techniques, humains ou climatiques dans le secteur ferroviaire.

---

### 3. [Amazon Delivery Dataset](https://www.kaggle.com/datasets/sujalsuthar/amazon-delivery-dataset)
- **Transport** : Routier / Dernier kilomètre
- **Format** : CSV
- **Description** : Données d’Amazon sur la livraison de colis (statuts, retards, zones).
- **Pourquoi ce choix ?** : Utile pour illustrer des cas de retards, de congestion ou d’optimisation dans la distribution locale.

---

### 4. [USA Airline Delay Cause](https://www.kaggle.com/datasets/ryanjt/airline-delay-cause)
- **Transport** : Aérien
- **Format** : CSV
- **Description** : Données détaillées sur les retards, annulations, et leurs causes (météo, compagnie, sécurité, congestion, retard chaîne…)
- **Pourquoi ce choix ?** : Idéal pour visualiser les risques réels et la résilience dans l’aviation : permet d’identifier les principaux facteurs de perturbation, de suivre leur évolution dans le temps.

---

### 5. [Supply Chain Dataset – Natasha](https://www.kaggle.com/datasets/natasha0786/supply-chain-dataset/data)
- **Transport** : Général (fournisseurs, produits, ventes)
- **Format** : CSV
- **Description** : Propose des KPI et scores de risque, avec de multiples variables sur la performance, la fiabilité fournisseurs, les délais et les probabilités de disruption.
- **Pourquoi ce choix ?** :  Idéal pour la construction d’indicateurs avancés et pour analyser la propagation du risque à l’échelle d’une chaîne logistique complète.

---

### 6. [Time Series in Risk Assessment – Saurabh Shahane](https://www.kaggle.com/datasets/saurabhshahane/time-series-in-risk-assessment/data)
- **Domaine** : Risques (multisectoriels)
- **Format** : CSV
- **Description** : Données temporelles pour la modélisation de la gestion des risques (type, criticité, impact).
- **Pourquoi ce choix ?** : Permet d’étudier la stabilité et la résilience dans la durée, et de construire des courbes de tendance/scoring pour anticiper les périodes critiques.

---

## 🔎 Plateformes généralistes de recherche de datasets
- [Google Dataset Search](https://datasetsearch.research.google.com/)
- [Gigasheet – Free List of Logistics and Supply Chain Businesses (CSV)](https://www.gigasheet.com/sample-data/free-list-of-logistics-and-supply-chain-businessescsv)

---
## 🌦️ Source météo utilisée en complément : Meteostat API

Pour enrichir l’analyse de l’impact des conditions météorologiques sur les perturbations logistiques, nous utilisons l’API [Meteostat](https://meteostat.net/en/) :

- **Données fournies** : température, précipitations, vent, neige, etc., issues de milliers de stations météorologiques mondiales.
- **Période** : historiques multi-années, granularité quotidienne ou horaire possible.
- **Pourquoi ce choix ?** : Permet de croiser dynamiquement la météo du jour et du lieu d’un incident (aéroport, gare, port, entrepôt…).
- **Mise en œuvre** : Appels API via Python.

---
**À mettre à jour à chaque ajout/test.**  
N’oublie pas de décrire brièvement chaque dataset téléchargé dans ce README (structure, nombre de lignes, variables principales, etc).