import pika


# -----------------------------------------------------------------------------
# RabbitMQ Connection Settings
# -----------------------------------------------------------------------------

RABBITMQ_HOST = "localhost"
QUEUE_NAME = "notification_queue"

# -----------------------------------------------------------------------------
# Publish Message
# -----------------------------------------------------------------------------

def l4_009PublishNotification(                # --> real producer receives events dynamically. previously we had message = xyz
        message: str
) -> None:
    """Publish notification message to RabbitMQ."""

    # Create connection to RabbitMQ.
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=RABBITMQ_HOST,
        )
    )

    # Create communication channel.
    channel = connection.channel()

    # Ensure notification queue exists.
    channel.queue_declare(
        queue=QUEUE_NAME,
        durable=True,
    )

    # Publish message to queue.
    channel.basic_publish(
        exchange="",
        routing_key=QUEUE_NAME,
        body=message,
        properties=pika.BasicProperties(       # --> Store message persistently
            delivery_mode=2,
        )
    )

    # Print published message.
    print(
        f"Message published: {message}"
    )

    # Close RabbitMQ connection.
    connection.close()

# -----------------------------------------------------------------------------
# Program Entry Point
# -----------------------------------------------------------------------------

if __name__ == "__main__":

    l4_009PublishNotification(
        "ORDER_CREATED: Welcome email required for Ahmed"
    )