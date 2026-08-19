import pika

# -----------------------------------------------------------------------------
# RabbitMQ Connection Settings
# -----------------------------------------------------------------------------

RABBITMQ_HOST = "localhost"
QUEUE_NAME = "notification_queue"

# -----------------------------------------------------------------------------
# Message Callback Function
# -----------------------------------------------------------------------------

def l4_009ProcessMessage(
        channel,                 # --> The RabbitMQ communication channel.
        method,                # --> Contains delivery information.
        properties,
        body,                     # --> This is the actual message.
) -> None:
    """Process received RabbitMQ message."""

    # Convert message bytes into string.
    message = body.decode()                 # --> RabbitMQ sends it as bytes: so we decode to string

    # Print received message.
    print(
        f"Received message: {message}"
    )

    # Simulate message processing.
    print(
        "Processing message..."
    )

    # Confirm successful processing.
    channel.basic_ack(
        delivery_tag=method.delivery_tag,
    )

    # Print acknowledgement.
    print(
        "Message processed successfully. ACK sent."
    )

# -----------------------------------------------------------------------------
# Start Consumer
# -----------------------------------------------------------------------------

def l4_009StartConsumer() -> None:
    """Start RabbitMQ consumer."""

    # Create connection to RabbitMQ.
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=RABBITMQ_HOST,
        )
    )

    # Create communication channel.
    channel = connection.channel()

    # Ensure queue exists.
    channel.queue_declare(
        queue=QUEUE_NAME,
        durable=True,
    )

    # Start consuming messages. ***
    channel.basic_consume(
        queue=QUEUE_NAME,                                # --> queue is notification_queue
        on_message_callback=l4_009ProcessMessage,        # --> message callback is going to be l4_009ProcessMessage
        auto_ack=False,                                  # --> manual acknowledgement
    )

    print(
        "Waiting for messages..."
    )

    # Keep consumer running.
    channel.start_consuming()

# -----------------------------------------------------------------------------
# Program Entry Point
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    l4_009StartConsumer()