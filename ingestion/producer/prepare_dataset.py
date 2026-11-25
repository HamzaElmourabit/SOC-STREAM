
from pathlib import Path
import pandas as pd
import numpy as np

# =====================================================
# CONFIGURATION SOC-STREAM
# =====================================================

DATA_DIR = Path("data/raw/CIC-IDS2017")
OUTPUT_DIR = Path("data/samples")

MAX_BENIGN_PER_FILE = 2000
MAX_PER_ATTACK_CLASS = 1000
RANDOM_STATE = 42

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def prepare_file(file: Path) -> None:
    print(f"\nTraitement : {file.name}")

    # 1. Charger le CSV original
    df = pd.read_csv(
        file,
        encoding="utf-8-sig",
        low_memory=False
    )

    # 2. Normaliser les noms des colonnes
    df.columns = df.columns.str.strip()

    if "Label" not in df.columns:
        raise ValueError(f"Colonne Label absente dans {file.name}")

    # 3. Nettoyer les labels
    df["Label"] = df["Label"].astype("string").str.strip()

    # Corriger le caractère de remplacement
    df["Label"] = df["Label"].str.replace(
        "\ufffd", "–", regex=False
    )

    # Supprimer les labels vides
    df = df[df["Label"].notna() & df["Label"].ne("")]

    # 4. Échantillonnage par catégorie
    sampled_groups = []

    for label, group in df.groupby("Label", sort=True):

        if label.upper() == "BENIGN":
            limit = MAX_BENIGN_PER_FILE
        else:
            limit = MAX_PER_ATTACK_CLASS

        n = min(len(group), limit)

        sampled = group.sample(
            n=n,
            random_state=RANDOM_STATE
        )

        sampled_groups.append(sampled)

        print(f"  {label}: {n}/{len(group)} flux")

    # 5. Fusionner et mélanger les catégories
    result = pd.concat(
        sampled_groups,
        ignore_index=True
    )

    result = result.sample(
        frac=1,
        random_state=RANDOM_STATE
    ).reset_index(drop=True)

    # 6. Nettoyage des valeurs numériques
    numeric_columns = result.select_dtypes(
        include="number"
    ).columns

    # Remplacer +inf et -inf par NaN
    result[numeric_columns] = result[numeric_columns].replace(
        [np.inf, -np.inf],
        np.nan
    )

    # Remplacer les valeurs numériques manquantes par 0
    result[numeric_columns] = result[numeric_columns].fillna(0)

    # 7. Classification binaire
    result["target"] = (
        result["Label"].str.upper() != "BENIGN"
    ).astype("int8")

    # 8. Identifiant unique des événements
    result.insert(
        0,
        "event_id",
        [f"{file.stem}_{i}" for i in range(len(result))]
    )

    # 9. Vérification de la qualité des données
    missing_values = result.isnull().sum().sum()

    numeric_data = result.select_dtypes(include="number")
    infinite_values = np.isinf(numeric_data.to_numpy()).sum()

    if missing_values > 0:
        raise ValueError(
            f"{missing_values} valeurs manquantes détectées dans {file.name}"
        )

    if infinite_values > 0:
        raise ValueError(
            f"{infinite_values} valeurs infinies détectées dans {file.name}"
        )

    # 10. Export JSONL
    output_file = OUTPUT_DIR / f"{file.stem}.jsonl"

    result.to_json(
        output_file,
        orient="records",
        lines=True,
        force_ascii=False
    )

    # 11. Résumé
    print(f"\nNombre de flux générés : {len(result)}")
    print("Distribution :")
    print(result["Label"].value_counts().to_string())

    print(f"Valeurs manquantes : {missing_values}")
    print(f"Valeurs infinies : {infinite_values}")
    print(f"Fichier créé : {output_file}")


def main():
    files = sorted(DATA_DIR.rglob("*.csv"))

    if not files:
        raise FileNotFoundError(
            f"Aucun fichier CSV trouvé dans {DATA_DIR}"
        )

    print("=" * 55)
    print("SOC-STREAM - DATASET PREPARATION")
    print("=" * 55)

    for file in files:
        prepare_file(file)

    print("\nPréparation terminée avec succès.")


if __name__ == "__main__":
    main()
