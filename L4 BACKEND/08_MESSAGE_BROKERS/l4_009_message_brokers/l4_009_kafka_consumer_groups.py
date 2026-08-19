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

# -----------------------------------------------------------------------------
# Create Kafka Consumer
# -----------------------------------------------------------------------------

def l4_009CreateConsumer(
    consumer_group: str
) -> KafkaConsumer:
    """
    Create Kafka consumer with specific consumer group.
    """

    consumer = KafkaConsumer(

        TOPIC_NAME,

        bootstrap_servers=KAFKA_SERVER,

        # Read messages from beginning
        # when this group has no previous offset.
        auto_offset_reset="earliest",

        # Automatically store processed offsets.
        enable_auto_commit=True,

        # Different groups behave independently.
        group_id=consumer_group,


        # Convert JSON bytes into Python dictionary.
        value_deserializer=lambda value: json.loads(
            value.decode("utf-8")
        )
    )


    return consumer

# -----------------------------------------------------------------------------
# Consume Notification Events
# -----------------------------------------------------------------------------

def l4_009NotificationConsumer() -> None:
    """
        Consumer group for notification service.
        """

    consumer = l4_009CreateConsumer(
        "notification-service-group"
    )

    print(
        "Notification Service waiting for events..."
    )

    for message in consumer:
        transaction_event = message.value

        print(
            "\nNotification Service received:"
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

        break


# -----------------------------------------------------------------------------
# Consume Fraud Detection Events
# -----------------------------------------------------------------------------

def l4_009FraudConsumer() -> None:
    """
    Consumer group for fraud detection service.
    """

    consumer = l4_009CreateConsumer(
        "fraud-detection-group"
    )

    print(
        "Fraud Detection Service waiting for events..."
    )

    for message in consumer:
        transaction_event = message.value

        print(
            "\nFraud Detection Service received:"
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

        break


# -----------------------------------------------------------------------------
# Program Entry Point
# -----------------------------------------------------------------------------

if __name__ == "__main__":

    l4_009NotificationConsumer()