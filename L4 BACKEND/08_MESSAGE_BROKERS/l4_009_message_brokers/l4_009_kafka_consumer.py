from kafka import KafkaConsumer
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

CONSUMER_GROUP = "transaction-processing-group"

# -----------------------------------------------------------------------------
# Create Kafka Consumer
# -----------------------------------------------------------------------------

def l4_009CreateConsumer() -> KafkaConsumer:
    """
    Create Kafka consumer connection.
    """

    consumer = KafkaConsumer(

        TOPIC_NAME,

        bootstrap_servers=KAFKA_SERVER,

        # Read old messages if consumer starts first time.
        auto_offset_reset="earliest",

        # Automatically save processed offsets.
        enable_auto_commit=True,

        # Consumer group identifier.
        group_id=CONSUMER_GROUP,


        # Convert JSON bytes into Python dictionary.
        value_deserializer=lambda value: json.loads(
            value.decode("utf-8")
        )
    )

    return consumer

# -----------------------------------------------------------------------------
# Consume Transaction Events
# -----------------------------------------------------------------------------

def l4_009ConsumeTransactionEvents() -> None:
    """Consume transaction events from Kafka."""

    # Create Kafka consumer.
    consumer = l4_009CreateConsumer()

    print(
        "Waiting for transaction events..."
    )

    # Listen continuously.
    for message in consumer:

        # Extract event data.
        transaction_event = message.value

        print(
            "\nReceived transaction event:"
        )

        print(
            json.dumps(
                transaction_event,
                indent=4
            )
        )

        print(
            f"Partition: {message.partition}"
        )

        print(
            f"Offset: {message.offset}"
        )

        # Stop after one message for learning.
        break

# -----------------------------------------------------------------------------
# Program Entry Point
# -----------------------------------------------------------------------------

if __name__ == "__main__":

    l4_009ConsumeTransactionEvents()