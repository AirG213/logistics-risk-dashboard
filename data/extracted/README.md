# 🗂️ Dossier `/extracted/`

Ce dossier contient **les jeux de données extraits** (CSV ou XLSX) depuis les ZIP du dossier `/raw/`. Chaque dataset est rangé dans un sous-dossier pour garder la structure claire.

**Consignes** :
- Aucun fichier ne doit être modifié ici : c’est la version *extrait* du ZIP, rien d’autre.
- Toujours garder le nom d’origine du CSV (ou le documenter dans ce README).

## Structure
/extracted/
├── Amazon_Delivery_Dataset/
│ └── amazon_delivery.csv
├── Global_Daily_Port_Activity_and_Trade_Estimates/
│ └── Daily_Port_Activity_Data_and_Trade_Estimates.csv
├── Railroad_Accident_Incident_Data/
│ └── Rail_Equipment_Accident_Incident_Data.csv
├── Supply_chain_dataset/
│ └── dynamic_supply_chain_logistics_dataset_with_country.csv
├── Time_Series_in_Risk_Assessment/
│ ├── SCRM_timeSeries_2018_train.csv
│ └── SCRM_timeSeries_2018_test.csv
├── USA_Airline_Delay_Cause/
│ └── Airline_Delay_Cause.cs

## Suivi d’extraction
| Dataset                                | Fichier extrait                                      | Dossier                                    |
|----------------------------------------|------------------------------------------------------|--------------------------------------------|
| Amazon Delivery                        | amazon_delivery.csv                                  | Amazon_Delivery_Dataset/                   |
| Global Daily Port Activity             | Daily_Port_Activity_Data_and_Trade_Estimates.csv     | Global_Daily_Port_Activity_and_Trade_Estimates/ |
| Railroad Accident & Incident           | Rail_Equipment_Accident_Incident_Data.csv            | Railroad_Accident_Incident_Data/           |
| Supply Chain Dataset                   | dynamic_supply_chain_logistics_dataset_with_country.csv | Supply_chain_dataset/                   |
| Time Series in Risk Assessment         | SCRM_timeSeries_2018_train.csv, SCRM_timeSeries_2018_test.csv | Time_Series_in_Risk_Assessment/    |
| USA Airline Delay Cause                | Airline_Delay_Cause.csv                              | USA_Airline_Delay_Cause/                   |