# SOC-STREAM

## Big Data Network Intrusion Detection Platform

SOC-STREAM est une plateforme Big Data de détection d'intrusions réseau basée sur le dataset CIC-IDS2017. Elle vise à traiter des événements réseau, distinguer le trafic **BENIGN** du trafic **ATTACK**, produire des indicateurs et présenter les résultats dans un dashboard.

## Architecture

Le projet adopte une **architecture Kappa** organisée selon les couches Medallion **Bronze, Silver et Gold**.

Le schéma détaillé, les responsabilités des composants, les flux de données, les choix techniques et les limites sont documentés ici :

➡️ **[Consulter l'architecture technique SOC-STREAM](docs/architecture.md)**

Vue synthétique :

```text
CIC-IDS2017 (CSV)
       |
Python Producer / NiFi
       |
Kafka — network-events
       |
Spark Structured Streaming
       |
MinIO + Apache Iceberg
  Bronze -> Silver -> Gold
                 |
          +------+------+
          |             |
      Spark SQL      Spark MLlib
          |          Random Forest
          |             |
          +------ PostgreSQL
                     |
              Streamlit Dashboard
                     |
              Grafana Monitoring

Transversal : Great Expectations, Airflow, MLflow,
catalogue de métadonnées et gouvernance/RGPD.
```

## Technologies prévues

- Python, Apache Kafka et Apache NiFi pour l'ingestion
- Apache Spark Structured Streaming et Spark SQL
- MinIO et Apache Iceberg pour le Lakehouse
- Great Expectations pour la qualité des données
- Spark MLlib pour la classification BENIGN / ATTACK
- Airflow pour l'orchestration et MLflow pour le suivi des expériences
- PostgreSQL pour les prédictions et alertes
- Streamlit pour le dashboard et Grafana pour le monitoring
- Docker Compose pour le déploiement local

## Dataset

- **Source :** CIC-IDS2017
- **Page officielle :** https://www.unb.ca/cic/datasets/ids-2017.html
- Les fichiers bruts sont conservés localement et ne sont pas versionnés dans ce dépôt.
- Le producteur publiera progressivement les enregistrements CSV dans Kafka afin de simuler un flux d'événements.

## Structure du projet

- `data/` : données locales (non versionnées)
- `ingestion/` : préparation des données et producteur
- `streaming/` : traitement Spark Structured Streaming
- `storage/` : stockage Lakehouse et couches Medallion
- `data_quality/` : contrôles de qualité
- `analytics/` : requêtes et indicateurs
- `ml/` : entraînement et scoring
- `orchestration/` : workflows Airflow
- `database/` : schéma PostgreSQL
- `dashboard/` : application Streamlit
- `monitoring/` : configuration de monitoring
- `tests/` : tests automatisés
- `docs/architecture.md` : architecture technique détaillée

## État du projet

L'analyse et la préparation initiale du dataset CIC-IDS2017 ainsi que les premiers contrôles sur les échantillons JSONL ont été réalisés localement. Les composants Kafka, Spark, MinIO/Iceberg, ML, base de données et interfaces doivent être considérés comme **à implémenter ou à valider** tant que leurs tests d'intégration n'ont pas été exécutés.

## Exécution

Les instructions de déploiement seront complétées au fur et à mesure de la mise en place du fichier `docker-compose.yml`.
