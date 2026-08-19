from kafka import KafkaProducer
import json
import warnings

# -----------------------------------------------------------------------------
# Disable Kafka Library Deprecation Warnings
# -----------------------------------------------------------------------------

warnings.filterwarnings(
    "ignore",
    category=DeprecationWarning
)

# -----------------------------------------------------------------------------
# Kafka Settings
# -----------------------------------------------------------------------------

KAFKA_SERVER = "localhost:9092"

TOPIC_NAME = "transaction-events"

# -----------------------------------------------------------------------------
# Create Kafka Producer
# -----------------------------------------------------------------------------

def l4_009CreateProducer() -> KafkaProducer:
    """Create Kafka producer connection."""

    producer = KafkaProducer(
        bootstrap_servers=KAFKA_SERVER,

        # Convert Python dictionary into JSON bytes.
        value_serializer=lambda value: json.dumps(value).encode("utf-8")
    )

    return producer

# -----------------------------------------------------------------------------
# Publish Transaction Event
# -----------------------------------------------------------------------------

def l4_009PublishTransactionEvent() -> None:
    """Publish transaction event to Kafka producer."""

    # Create Kafka producer.
    producer = l4_009CreateProducer()

    # Create transaction event.
    transaction_event = {

        "transaction_id": 1002,

        "customer_id": "C002",

        "amount": 7500,

        "currency": "NPR",

        "status": "COMPLETED"
    }

    # Send event to Kafka topic.
    producer.send(
        TOPIC_NAME,
        transaction_event
    )

    # Wait until Kafka confirms delivery.
    producer.flush()

    # Print published event.
    print(
        "Transaction event published:"
    )

    print(
        json.dumps(
            transaction_event,
            indent=4
        )
    )

    # Close producer connection.
    producer.close()

# -----------------------------------------------------------------------------
# Program Entry Point
# -----------------------------------------------------------------------------

if __name__ == "__main__":

    l4_009PublishTransactionEvent()