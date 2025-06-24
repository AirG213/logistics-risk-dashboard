# 🧹 Dossier `/cleaned/`

Ici sont stockés **les jeux de données après nettoyage et harmonisation** (formats, dates, colonnes renommées, enrichissement, etc.).
Ces fichiers sont ceux utilisés pour toutes les analyses, visualisations et modélisations.

**Convention** :
- Garder le même nom que le fichier source, suffixé par `_cleaned.csv`.
- Documenter dans ce README les traitements appliqués à chaque fichier.

## Suivi des fichiers nettoyés

| Dataset                    | Fichier nettoyé                      | script utilisé |
|----------------------------|--------------------------------------|----------------|
| Amazon_Delivery_Dataset            | amazon_delivery_cleaned.csv          | EDA_Amazon_Delivery_Dataset.ipynb  |
| Global_Daily_Port_Activity_and_Trade_Estimates | port_activity_cleaned.csv            | [à compléter]  |
| Railroad_Accident_Incident_Data | railroad_accident_cleaned.csv      | EDA_Railroad_Accident_Incident_Data.ipynb  |
| Supply_chain_dataset       | supply_chain_cleaned.csv     | EDA_Supply_chain_dataset.ipynb  |
| USA_Airline_Delay_Cause    | airline_delay_cause_cleaned.csv      | EDA_Airline_Delay_Cause.ipynb  |
| USA_Accidents   | usa_accidents_traffic_cleaned.csv      | EDA_Accident_Traffic.ipynb  |