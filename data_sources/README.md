# 📦 Data Sources for Supply Chain Disruption & Resilience Analysis

Ce dossier regroupe des sources gratuites et accessibles.

---

## 📊 Données Supply Chain & Disruptions (Gratuites et Téléchargeables)

### 1. [HELCOM – Baltic Sea Shipping Accidents Database](https://maps.helcom.fi/website/mapservice/?datasetID=cae61cf8-0b3a-449a-aeaf-1df752dd3d80)
- **Transport** : Maritime (Baltique, accidents en mer et en zone portuaire)
- **Format** : ESRI Shapefile (fichiers .shp, .dbf, .shx, etc.)
- **Description**: Base de données exhaustive recensant tous les accidents de navires dans la mer Baltique, incluant la localisation, le type d’accident, la cause, la catégorie du navire, la météo, les dégâts matériels, les conséquences humaines et environnementales (pollution), etc.
- **Pourquoi ce choix ?** : Permet une analyse détaillée des risques maritimes liés aux accidents en zone portuaire et en mer : typologie, causes... Ce jeu de données est adapté à la construction d’indicateurs de criticité et de modules d’analyse de la résilience logistique maritime.

#### 1.1. [World Port Index – Port Data](https://fgmod.nga.mil/apps/WPI-Viewer/)
- Afin de compléter les données maritimes (localisations des accidents), un dataset contenant une liste (non exhaustive) des ports du monde a été utilisé.

### 1.2. [Natural Earth](https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/10m/physical/ne_10m_land.zip)
- Pour enrichir les données géographiques, le jeu de données Natural Earth a été utilisé. Il fournit des informations sur la position des côtes.

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