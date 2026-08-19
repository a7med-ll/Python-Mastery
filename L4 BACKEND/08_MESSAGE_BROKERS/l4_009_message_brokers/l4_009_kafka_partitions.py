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

TOPIC_NAME = "transaction-events-partitioned"


# -----------------------------------------------------------------------------
# Create Kafka Producer
# -----------------------------------------------------------------------------

def l4_009CreateProducer() -> KafkaProducer:
    """
    Create Kafka producer connection.
    """

    producer = KafkaProducer(

        bootstrap_servers=KAFKA_SERVER,

        # Convert dictionary into JSON bytes.
        value_serializer=lambda value: json.dumps(value).encode("utf-8")
    )

    return producer



# -----------------------------------------------------------------------------
# Create Topic With Partitions
# -----------------------------------------------------------------------------

def l4_009CreatePartitionTopic() -> None:
    """
    Topic creation is handled using Kafka CLI.

    This function only documents
    the required configuration.
    """

    print(
        "Create topic with 3 partitions:"
    )

    print(
        """
        kafka-topics.sh
        --create
        --topic transaction-events-partitioned
        --partitions 3
        --replication-factor 1
        """
    )



# -----------------------------------------------------------------------------
# Publish Events With Keys
# -----------------------------------------------------------------------------

def l4_009PublishPartitionEvents() -> None:
    """
    Publish events using customer_id as key.

    Same key always goes to the same partition.
    """

    producer = l4_009CreateProducer()


    transactions = [

        {
            "transaction_id": 2001,
            "customer_id": "C001",
            "amount": 5000
        },

        {
            "transaction_id": 2002,
            "customer_id": "C002",
            "amount": 7000
        },

        {
            "transaction_id": 2003,
            "customer_id": "C001",
            "amount": 9000
        },

        {
            "transaction_id": 2004,
            "customer_id": "C003",
            "amount": 3000
        }
    ]


    for transaction in transactions:


        producer.send(

            TOPIC_NAME,

            # Kafka uses key for partition selection.
            key=transaction["customer_id"].encode("utf-8"),

            value=transaction
        )


        print(
            "Published:"
        )

        print(
            json.dumps(
                transaction,
                indent=4
            )
        )


    producer.flush()

    producer.close()



# -----------------------------------------------------------------------------
# Consume Partition Information
# -----------------------------------------------------------------------------

def l4_009ConsumePartitionEvents() -> None:
    """
    Consume events and display partition details.
    """


    consumer = KafkaConsumer(

        TOPIC_NAME,

        bootstrap_servers=KAFKA_SERVER,

        auto_offset_reset="earliest",

        enable_auto_commit=True,

        group_id="partition-demo-group",


        value_deserializer=lambda value:
            json.loads(
                value.decode("utf-8")
            )
    )


    print(
        "Waiting for partition events..."
    )


    for message in consumer:


        print(
            "\nReceived Event:"
        )


        print(
            json.dumps(
                message.value,
                indent=4
            )
        )


        print(
            f"Partition: {message.partition}"
        )


        print(
            f"Offset: {message.offset}"
        )



# -----------------------------------------------------------------------------
# Program Entry Point
# -----------------------------------------------------------------------------

if __name__ == "__main__":


    # Run producer example.
    l4_009PublishPartitionEvents()


    time.sleep(2)


    # Run consumer example.
    l4_009ConsumePartitionEvents()