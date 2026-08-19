"""only publishes the message. It does not consume it yet."""

import pika

# -----------------------------------------------------------------------------
# RabbitMQ Connection Settings
# -----------------------------------------------------------------------------

RABBITMQ_HOST = "localhost"
QUEUE_NAME = "notification_queue"

# -----------------------------------------------------------------------------
# Publish Message
# -----------------------------------------------------------------------------

def l4_009PublishMessage() -> None:
    """Publish a message to RabbitMQ."""

    # Create connection to RabbitMQ.
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=RABBITMQ_HOST,
        )
    )

    # Create communication channel.
    channel = connection.channel()

    # Create the notification queue.
    channel.queue_declare(                # --> Does notification_queue exist? if yes -> Use it
        queue=QUEUE_NAME,                 # --> -----------------------------? if no -> Create it
        durable = True,
    )

    # Create message.
    message = "Send welcome email to Ahmed"

    # Publish message to RabbitMQ queue.
    channel.basic_publish(
        exchange="",
        routing_key=QUEUE_NAME,
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2,
        ),
    )

    # Print published message.
    print(
        f"Published: {message}"
    )

    # Close RabbitMQ connection.
    connection.close()

# -----------------------------------------------------------------------------
# Program Entry Point
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    l4_009PublishMessage()