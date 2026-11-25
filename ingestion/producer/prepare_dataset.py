from pathlib import Path
import pandas as pd

DATA_DIR = Path("data/raw/CIC-IDS2017")
OUTPUT_DIR = Path("data/samples")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

files = sorted(DATA_DIR.rglob("*.csv"))

for file in files:

    print(f"\nTraitement : {file.name}")

    df = pd.read_csv(file, nrows=1000)

    # Normalisation des noms de colonnes
    df.columns = df.columns.str.strip()

    # Normalisation du label
    df["Label"] = df["Label"].astype("string").str.strip()

    # Classification binaire
    df["target"] = (
        df["Label"].str.upper() != "BENIGN"
    ).astype(int)

    # Identifiant technique
    df.insert(
        0,
        "event_id",
        [f"{file.stem}_{i}" for i in range(len(df))]
    )

    # Export JSON
    output_file = OUTPUT_DIR / f"{file.stem}.jsonl"

    df.to_json(
        output_file,
        orient="records",
        lines=True,
        force_ascii=False
    )

    print("Nombre de flux :", len(df))
    print("Fichier créé :", output_file)

print("\nPréparation terminée.")