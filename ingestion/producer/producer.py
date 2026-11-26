
import json
import os
import time
from pathlib import Path
from datetime import datetime, timezone

from dotenv import load_dotenv
from kafka import KafkaProducer
from kafka.errors import KafkaError

# ==========================================
# SOC-STREAM - PYTHON KAFKA PRODUCER
# ==========================================

ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT_DIR / "data" / "samples"

load_dotenv(ROOT_DIR / ".env")

BOOTSTRAP_SERVERS = os.getenv(
    "KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"
)
TOPIC = os.getenv("KAFKA_TOPIC", "network-events")

# 100 événements pour le premier test.
# Mettre 0 pour envoyer tous les événements.
MAX_EVENTS = int(os.getenv("MAX_EVENTS", "100"))

DELAY_SECONDS = float(
    os.getenv("PRODUCER_DELAY_SECONDS", "0")
)

BATCH_SIZE = 500


def create_producer():
    return KafkaProducer(
        bootstrap_servers=BOOTSTRAP_SERVERS,
        value_serializer=lambda value: json.dumps(
            value, ensure_ascii=False
        ).encode("utf-8"),
        key_serializer=lambda key: key.encode("utf-8"),
        acks="all",
        retries=5,
    )


def main():

    files = sorted(DATA_DIR.glob("*.jsonl"))

    if not files:
        raise FileNotFoundError(
            f"Aucun fichier JSONL trouvé dans {DATA_DIR}"
        )

    print("=" * 55)
    print("SOC-STREAM - KAFKA PRODUCER")
    print("=" * 55)
    print("Kafka :", BOOTSTRAP_SERVERS)
    print("Topic :", TOPIC)
    print("Fichiers :", len(files))
    print("Limite :", MAX_EVENTS or "Tous les événements")

    producer = create_producer()

    total_sent = 0
    pending = []

    try:
        for file in files:

            print(f"\nLecture : {file.name}")

            with file.open("r", encoding="utf-8") as f:

                for line in f:

                    if MAX_EVENTS and total_sent + len(pending) >= MAX_EVENTS:
                        break

                    if not line.strip():
                        continue

                    event = json.loads(line)

                    event["source_file"] = file.name
                    event["ingestion_timestamp"] = (
                        datetime.now(timezone.utc).isoformat()
                    )

                    event_id = str(event["event_id"])

                    future = producer.send(
                        TOPIC,
                        key=event_id,
                        value=event
                    )

                    pending.append(future)

                    if len(pending) >= BATCH_SIZE:
                        for result in pending:
                            result.get(timeout=30)

                        total_sent += len(pending)
                        pending.clear()

                        print("Événements envoyés :", total_sent)

                    if DELAY_SECONDS > 0:
                        time.sleep(DELAY_SECONDS)

            if MAX_EVENTS and total_sent + len(pending) >= MAX_EVENTS:
                break

        # Envoyer les derniers événements
        for result in pending:
            result.get(timeout=30)

        total_sent += len(pending)
        producer.flush()

        print("\n======================================")
        print("ENVOI TERMINÉ")
        print("Total envoyé :", total_sent)
        print("Topic :", TOPIC)
        print("======================================")

    except (KafkaError, OSError, ValueError, KeyError) as error:
        print("Erreur pendant l'envoi :", error)
        raise

    finally:
        producer.close()


if __name__ == "__main__":
    main()
