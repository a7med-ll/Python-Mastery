from kafka import KafkaProducer, KafkaConsumer
import json
import time
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
        value_serializer=lambda value: json.dumps(
            value
        ).encode("utf-8")
    )

    return producer


# -----------------------------------------------------------------------------
# Publish Event
# -----------------------------------------------------------------------------

def l4_009PublishEvent() -> None:
    """Publish transaction event to Kafka topic."""

    # Create Kafka producer.
    producer = l4_009CreateProducer()


    # Create transaction event.
    event_message = {

        "transaction_id": 1001,

        "customer_id": "C001",

        "amount": 6000,

        "currency": "NPR",

        "status": "COMPLETED"

    }


    # Send event to Kafka topic.
    producer.send(
        TOPIC_NAME,
        event_message
    )


    # Ensure message is sent.
    producer.flush()


    # Print published event.
    print(
        "Event published:"
    )

    print(
        json.dumps(
            event_message,
            indent=4
        )
    )


    # Close producer.
    producer.close()



# -----------------------------------------------------------------------------
# Create Kafka Consumer
# -----------------------------------------------------------------------------

def l4_009CreateConsumer() -> KafkaConsumer:
    """Create Kafka consumer connection."""

    consumer = KafkaConsumer(

        TOPIC_NAME,

        bootstrap_servers=KAFKA_SERVER,


        # Read old messages also.
        auto_offset_reset="earliest",


        # Store consumer progress.
        enable_auto_commit=True,


        # New group to read fresh messages.
        group_id="transaction-basic-demo-v3",


        # Stop waiting after 10 seconds.
        consumer_timeout_ms=10000,


        # Convert JSON bytes back to Python object.
        value_deserializer=lambda value: json.loads(
            value.decode("utf-8")
        )

    )


    return consumer



# -----------------------------------------------------------------------------
# Consume Event
# -----------------------------------------------------------------------------

def l4_009ConsumeEvent() -> None:
    """Consume transaction event from Kafka topic."""


    # Create Kafka consumer.
    consumer = l4_009CreateConsumer()


    print(
        "Waiting for events..."
    )


    try:

        # Read messages.
        for message in consumer:


            event_message = message.value


            print(
                "Received event:"
            )


            print(
                json.dumps(
                    event_message,
                    indent=4
                )
            )


            # Stop after first message.
            break


    finally:

        # Close consumer.
        consumer.close()



# -----------------------------------------------------------------------------
# Program Entry Point
# -----------------------------------------------------------------------------

if __name__ == "__main__":


    # Publish message.
    l4_009PublishEvent()


    # Give Kafka time to store event.
    time.sleep(2)


    # Consume message.
    l4_009ConsumeEvent()