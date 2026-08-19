# L4_009 Message Brokers - Kafka & RabbitMQ

## Overview

This task demonstrates how message brokers work in backend systems.

Implemented examples:

- RabbitMQ Producer
- RabbitMQ Consumer
- Kafka Producer
- Kafka Consumer
- Kafka Consumer Groups
- Kafka Partitions

The purpose is to understand asynchronous communication between services using message queues and event streaming platforms.

---

# Technologies Used

- Python 3
- RabbitMQ
- Apache Kafka
- Docker
- kafka-python
- pika

---

# Project Structure

```
L4_009_message_brokers/

│
├── l4_009_rabbitmq_basic.py
├── l4_009_rabbitmq_producer.py
├── l4_009_rabbitmq_consumer.py
│
├── l4_009_kafka_basic.py
├── l4_009_kafka_producer.py
├── l4_009_kafka_consumer.py
├── l4_009_kafka_consumer_groups.py
├── l4_009_kafka_partitions.py
│
└── README.md
```

---

# Setup Virtual Environment

Activate Python virtual environment:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install kafka-python pika
```

---

# RabbitMQ Setup

Start RabbitMQ using Docker:

```bash
docker run -d \
--name rabbitmq \
-p 5672:5672 \
-p 15672:15672 \
rabbitmq:management
```

RabbitMQ UI:

```
http://localhost:15672
```

Default credentials:

```
username: guest
password: guest
```

---

# RabbitMQ Examples

## Run Producer

```bash
python3 l4_009_rabbitmq_producer.py
```

Example output:

```
Message published:
ORDER_CREATED: Welcome email required for Ahmed
```

---

## Run Consumer

```bash
python3 l4_009_rabbitmq_consumer.py
```

Example output:

```
Message received:
ORDER_CREATED: Welcome email required for Ahmed
```

---

# Kafka Setup

Kafka is running using Docker.

Check containers:

```bash
docker ps
```

Expected:

```
kafka
kafka-ui
```

Kafka broker:

```
localhost:9092
```

Kafka UI:

```
http://localhost:8080
```

---

# Create Kafka Topic

Create transaction topic:

```bash
docker exec -it kafka \
/opt/kafka/bin/kafka-topics.sh \
--create \
--topic transaction-events \
--bootstrap-server kafka:9092 \
--partitions 1 \
--replication-factor 1
```

Verify topic:

```bash
docker exec -it kafka \
/opt/kafka/bin/kafka-topics.sh \
--list \
--bootstrap-server kafka:9092
```

Expected:

```
transaction-events
```

---

# Kafka Producer

The producer publishes transaction events.

Run:

```bash
python3 l4_009_kafka_producer.py
```

Example event:

```json
{
    "transaction_id": 1001,
    "customer_id": "C001",
    "amount": 5000,
    "currency": "NPR",
    "status": "COMPLETED"
}
```

---

# Kafka Consumer

The consumer listens for transaction events.

Run:

```bash
python3 l4_009_kafka_consumer.py
```

Example output:

```
Waiting for transaction events...

Received transaction event:

{
    "transaction_id":1001,
    "customer_id":"C001",
    "amount":5000
}

Partition: 0
Offset: 0
```

---

# Kafka Consumer Groups

Consumer groups allow multiple consumers to share message processing.

Example:

```
transaction-processing-group
```

Run:

```bash
python3 l4_009_kafka_consumer_groups.py
```

Kafka assigns messages between consumers in the same group.

Example:

```
Notification Service received:

transaction_id:1001
```

---

# Kafka Partitions

Partitions allow Kafka topics to scale horizontally.

A topic can contain multiple partitions:

```
transaction-events

Partition 0
Partition 1
Partition 2
```

Create topic with multiple partitions:

```bash
docker exec -it kafka \
/opt/kafka/bin/kafka-topics.sh \
--create \
--topic transaction-events \
--bootstrap-server kafka:9092 \
--partitions 3 \
--replication-factor 1
```

Messages are distributed based on partitioning strategy.

---

# Kafka UI Monitoring

Open:

```
http://localhost:8080
```

You can view:

- Topics
- Messages
- Partitions
- Consumer Groups
- Offsets
- Message size

---

# Learning Outcomes

After completing this task:

- Understand message broker architecture
- Understand asynchronous communication
- Create Kafka producers and consumers
- Understand consumer groups
- Understand Kafka partitions
- Monitor events using Kafka UI
- Understand the difference between queues and event streaming

---

# Key Concepts

## RabbitMQ

Message queue system.

Flow:

```
Producer
   |
   v
Queue
   |
   v
Consumer
```

Used for:

- Background jobs
- Task processing
- Notifications


## Kafka

Distributed event streaming platform.

Flow:

```
Producer
    |
    v
Topic
    |
    v
Consumer Group
    |
    v
Consumers
```

Used for:

- Event-driven architecture
- Microservices communication
- High-volume streaming