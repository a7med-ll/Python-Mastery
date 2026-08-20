# L4-010 WebSockets for Real-Time Features

## Overview

This task demonstrates how WebSockets work in backend systems.

WebSockets provide a persistent, bidirectional connection between a client and a server.

Unlike normal HTTP request-response communication, WebSockets allow both the client and server to send messages at any time while the connection remains open.

Basic flow:

```text
Client <====================> Server
        WebSocket Connection
```

This is commonly used for real-time features such as:

- Live chat
- Notifications
- Payment status updates
- Order tracking
- Taxi location updates
- Multiplayer applications
- Live dashboards
- Real-time monitoring

---

# Technologies Used

- Python
- FastAPI
- Uvicorn
- websockets library

---

# Project Structure

```text
l4_010_websockets/

├── l4_010_websocket_basic.py
├── l4_010_websocket_client.py
├── l4_010_websocket_connections.py
├── l4_010_websocket_broadcast.py
└── README.md
```

---

# Requirements

Install required packages:

```bash
pip install fastapi uvicorn websockets
```

---

# Activate Virtual Environment

Activate the existing project virtual environment:

```bash
source .venv/bin/activate
```

---

# 1. Basic WebSocket Server

File:

```text
l4_010_websocket_basic.py
```

Purpose:

Demonstrates the basic WebSocket lifecycle.

Flow:

```text
Client
   |
   | Connect
   v
Server
   |
   | Accept connection
   v
Client sends message
   |
   v
Server receives message
   |
   v
Server sends response
```

Run:

```bash
uvicorn l4_010_websocket_basic:app --reload
```

WebSocket endpoint:

```text
ws://127.0.0.1:8000/ws
```

The server:

- Accepts one WebSocket connection
- Receives one message
- Sends one response
- Closes the connection

---

# 2. WebSocket Client

File:

```text
l4_010_websocket_client.py
```

Purpose:

Connect to the FastAPI WebSocket server and exchange messages.

Run the server first:

```bash
uvicorn l4_010_websocket_basic:app --reload
```

Then open another terminal and run:

```bash
python3 l4_010_websocket_client.py
```

Example output:

```text
Connected to WebSocket server.

Sent:
Hello from WebSocket client

Received:
Server received: Hello from WebSocket client
```

The client demonstrates:

- Connecting to the WebSocket server
- Sending data
- Receiving data
- Closing the connection

---

# 3. Multiple WebSocket Connections

File:

```text
l4_010_websocket_connections.py
```

Purpose:

Manage multiple active WebSocket clients.

The server stores connected clients inside:

```text
active_connections
```

Example:

```text
Client A connects

[Client A]
```

Then:

```text
Client B connects

[Client A, Client B]
```

If Client A disconnects:

```text
[Client B]
```

Run:

```bash
uvicorn l4_010_websocket_connections:app --reload
```

Then run the client:

```bash
python3 l4_010_websocket_client.py
```

Example server output:

```text
Client connected. Active clients: 1

Received:
Hello from WebSocket client

Client disconnected. Active clients: 0
```

---

# Connection Manager

The connection manager is responsible for:

- Accepting WebSocket clients
- Tracking active clients
- Removing disconnected clients

Basic structure:

```text
Connection Manager

        |
        |
        +--> Client A
        |
        +--> Client B
        |
        +--> Client C
```

This pattern is commonly used in real-time backend applications.

---

# 4. WebSocket Broadcast

File:

```text
l4_010_websocket_broadcast.py
```

Purpose:

Send one message to every connected WebSocket client.

Flow:

```text
Client A
   |
   | Sends message
   v
Server
   |
   | Broadcast
   |
   +------> Client A
   |
   +------> Client B
   |
   +------> Client C
```

Run:

```bash
uvicorn l4_010_websocket_broadcast:app --reload
```

Then run a WebSocket client:

```bash
python3 l4_010_websocket_client.py
```

Example:

```text
Client sends:

Hello
```

Server broadcasts:

```text
Broadcast: Hello
```

Every connected client receives the same message.

---

# Important WebSocket Concepts

## Persistent Connection

A WebSocket connection stays open.

Normal HTTP:

```text
Client ---> Request ---> Server

Client <--- Response <--- Server

Connection/request ends
```

WebSocket:

```text
Client <====================> Server

Message 1 --->

<--- Response 1

Message 2 --->

<--- Response 2
```

The same connection can continue carrying messages.

---

# Bidirectional Communication

Both sides can send messages.

```text
Client ---> Server

Server ---> Client
```

The server does not need to wait for a new HTTP request before sending an update.

---

# WebSocket URLs

Normal HTTP:

```text
http://
https://
```

WebSocket:

```text
ws://
wss://
```

Example:

```text
ws://127.0.0.1:8000/ws
```

For secure production environments:

```text
wss://example.com/ws
```

---

# HTTP vs WebSocket

| HTTP | WebSocket |
|---|---|
| Request-response | Persistent connection |
| Client usually initiates | Both sides can send |
| Short-lived communication | Long-lived communication |
| Good for CRUD APIs | Good for real-time features |
| `http://` / `https://` | `ws://` / `wss://` |

---

# WebSockets Do Not Replace REST APIs

A production application normally uses both.

Example:

```text
REST API

POST /login
GET /users
GET /transactions
POST /payments
```

And:

```text
WebSocket

/ws/notifications
/ws/chat
/ws/tracking
```

REST is used for normal operations.

WebSockets are used when data must be pushed in real time.

---

# WebSocket Disconnect Handling

Clients may disconnect because of:

- Browser closed
- Application closed
- Network interruption
- Server restart
- Connection timeout

FastAPI provides:

```python
WebSocketDisconnect
```

This allows the server to detect disconnections and remove inactive clients from the connection manager.

---

# Real-World Example

## Payment Status Update

```text
Mobile App
    |
    | WebSocket connection
    v
Backend Server
    |
    | Payment processing
    |
    v
Payment completed
    |
    |
    +------> Client notification
```

Example pushed event:

```json
{
    "transaction_id": 1001,
    "status": "COMPLETED"
}
```

The mobile application receives the update immediately.

---

# Taxi Tracking Example

```text
Driver App
    |
    | Sends location
    v
Backend
    |
    | Broadcast/update
    v
Customer App
```

WebSockets allow location information to update continuously without repeated HTTP polling.

---

# Chat Application Example

```text
User A
   |
   | Message
   v
WebSocket Server
   |
   | Broadcast
   |
   +------> User A
   |
   +------> User B
   |
   +------> User C
```

---

# Key Learning Outcomes

After completing L4-010 WebSockets, you understand:

- What WebSockets are
- Why WebSockets are used
- Persistent connections
- Bidirectional communication
- FastAPI WebSocket endpoints
- Python WebSocket clients
- Connection management
- Client disconnect handling
- Broadcasting messages
- Real-time backend architecture

---

# Final Architecture

```text
                WebSocket Server

                      |
        --------------------------------
        |              |               |
        |              |               |
     Client A       Client B        Client C
        |              |               |
        |              |               |
        <---------- Real-Time ---------->
                 Communication
```

---

# Main Difference

Normal HTTP:

```text
Client asks for data repeatedly
```

WebSocket:

```text
Connection stays open
Server can push updates immediately
```

That is the core mechanism behind real-time backend systems.