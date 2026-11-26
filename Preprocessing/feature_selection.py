
import glob
import pandas as pd

# 1. Load dataset
files = glob.glob("data/samples/*.jsonl")

df = pd.concat(
    [pd.read_json(f, lines=True) for f in files],
    ignore_index=True
)

print("=" * 55)
print("SOC-STREAM - FEATURE SELECTION")
print("=" * 55)

# 2. Separate metadata, features and targets
y = df["target"]
labels = df["Label"]

X = df.drop(columns=["event_id", "Label", "target"])

# 3. Remove constant features
constant_cols = X.columns[
    X.nunique(dropna=False) <= 1
].tolist()

X = X.drop(columns=constant_cols)

# 4. Remove exact duplicate features
duplicate_cols = X.columns[
    X.T.duplicated()
].tolist()

X = X.drop(columns=duplicate_cols)

# 5. Results
print("Initial features:", 78)
print("Constant features removed:", len(constant_cols))
print("Duplicate features removed:", len(duplicate_cols))
print("Remaining features:", X.shape[1])

print("\nConstant columns:")
print(constant_cols)

print("\nDuplicate columns:")
print(duplicate_cols)

# 6. Save selected dataset
result = X.copy()
result["target"] = y
result["Label"] = labels

result.to_parquet(
    "data/samples/soc_stream_selected.parquet",
    index=False
)

print("\nSelected dataset saved successfully.")
print("Final shape:", result.shape)
