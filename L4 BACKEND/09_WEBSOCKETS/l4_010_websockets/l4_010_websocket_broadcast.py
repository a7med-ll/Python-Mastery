from fastapi import FastAPI, WebSocket, WebSocketDisconnect

# -----------------------------------------------------------------------------
# Create FastAPI Application
# -----------------------------------------------------------------------------

app = FastAPI()

# -----------------------------------------------------------------------------
# Connection Manager
# -----------------------------------------------------------------------------

class l4_010BroadcastManager:
    """Manage WebSocket connections and broadcast messages."""

    def __init__(self) -> None:

        # Store all active WebSocket connections.
        self.active_connections: list[WebSocket] = []

    # -------------------------------------------------------------------------
    # Connect Client
    # -------------------------------------------------------------------------

    async def connect(
        self,
        websocket: WebSocket
    ) -> None:
        """Accept and store WebSocket connection."""

        # Accept WebSocket connection.
        await websocket.accept()

        # Store connected client.
        self.active_connections.append(
            websocket
        )

    # -------------------------------------------------------------------------
    # Disconnect Client
    # -------------------------------------------------------------------------

    def disconnect(
        self,
        websocket: WebSocket
    ) -> None:
        """Remove disconnected WebSocket connection."""

        # Remove client from active connections.
        self.active_connections.remove(
            websocket
        )

    # -------------------------------------------------------------------------
    # Broadcast Message
    # -------------------------------------------------------------------------

    async def broadcast(
        self,
        message: str
    ) -> None:
        """Send message to all connected clients."""

        # Loop through every active connection.
        for connection in self.active_connections:

            # Send message to connected client.
            await connection.send_text(
                message
            )

# -----------------------------------------------------------------------------
# Create Broadcast Manager
# -----------------------------------------------------------------------------

manager = l4_010BroadcastManager()

# -----------------------------------------------------------------------------
# WebSocket Endpoint
# -----------------------------------------------------------------------------

@app.websocket("/ws")
async def l4_010WebSocketBroadcast(
    websocket: WebSocket
) -> None:
    """Receive and broadcast WebSocket messages."""

    # Connect client.
    await manager.connect(
        websocket
    )

    print(
        f"Client connected. Active clients: {len(manager.active_connections)}"
    )

    try:

        # Keep connection open.
        while True:

            # Wait for message from client.
            message = await websocket.receive_text()

            print(
                f"Received: {message}"
            )

            # Broadcast message to every connected client.
            await manager.broadcast(
                f"Broadcast: {message}"
            )

    except WebSocketDisconnect:

        # Remove disconnected client.
        manager.disconnect(
            websocket
        )

        print(
            f"Client disconnected. Active clients: {len(manager.active_connections)}"
        )