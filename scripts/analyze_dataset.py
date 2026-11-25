from pathlib import Path
from collections import Counter
import pandas as pd

DATA_DIR = Path("data/raw/CIC-IDS2017")
files = sorted(DATA_DIR.rglob("*.csv"))

if not files:
    raise FileNotFoundError("Aucun fichier CSV trouvé.")

global_labels = Counter()
schemas = {}

print(f"Nombre de fichiers : {len(files)}")

for file in files:
    print(f"\nAnalyse : {file.name}")

    # Vérifier les colonnes
    columns = pd.read_csv(file, nrows=0).columns
    columns = [str(c).strip() for c in columns]
    schemas[file.name] = set(columns)

    if "Label" not in columns:
        print("ERREUR : colonne Label absente")
        continue

    file_labels = Counter()

    # Lire progressivement pour limiter la mémoire utilisée
    for chunk in pd.read_csv(file, chunksize=100000):
        chunk.columns = chunk.columns.str.strip()
        labels = chunk["Label"].astype("string").str.strip()
        file_labels.update(labels.dropna().tolist())

    global_labels.update(file_labels)

    print("Nombre de lignes :", sum(file_labels.values()))
    print("Classes :", dict(file_labels))

print("\n========== BILAN GLOBAL ==========")
print("Nombre total de lignes :", sum(global_labels.values()))
print("Répartition globale des classes :")

for label, count in global_labels.most_common():
    print(f"{label}: {count}")

print("\n========== VÉRIFICATION DES SCHÉMAS ==========")
reference = next(iter(schemas.values()))

for name, columns in schemas.items():
    if columns == reference:
        print(f"{name}: OK")
    else:
        print(f"{name}: DIFFERENT")
        print("Colonnes manquantes :", sorted(reference - columns))
        print("Colonnes supplémentaires :", sorted(columns - reference))
