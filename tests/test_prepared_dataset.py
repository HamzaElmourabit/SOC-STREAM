from pathlib import Path
import json

files = list(Path("data/samples").glob("*.jsonl"))

assert len(files) == 8, f"8 fichiers attendus, {len(files)} trouvés"

total = 0

for file in files:
    count = 0

    with file.open(encoding="utf-8") as f:
        for line in f:
            event = json.loads(line)

            assert "event_id" in event
            assert "Label" in event
            assert "target" in event

            assert event["target"] in [0, 1]

            expected = 0 if event["Label"] == "BENIGN" else 1
            assert event["target"] == expected

            count += 1

    print(f"{file.name}: {count} événements")
    total += count

print("\nTOTAL:", total)
print("Tous les contrôles sont réussis.")