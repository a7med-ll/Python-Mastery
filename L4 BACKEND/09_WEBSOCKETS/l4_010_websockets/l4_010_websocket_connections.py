from fastapi import FastAPI, WebSocket, WebSocketDisconnect

# -----------------------------------------------------------------------------
# Create FastAPI Application
# -----------------------------------------------------------------------------

app = FastAPI()

# -----------------------------------------------------------------------------
# Connection Manager
# -----------------------------------------------------------------------------

class l4_010ConnectionManager:
    """Manage active WebSocket connections."""

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
    # Get Connection Count
    # -------------------------------------------------------------------------

    def connection_count(self) -> int:
        """Return number of active connections."""

        return len(
            self.active_connections
        )

# -----------------------------------------------------------------------------
# Create Connection Manager
# -----------------------------------------------------------------------------

manager = l4_010ConnectionManager()

# -----------------------------------------------------------------------------
# WebSocket Endpoint
# -----------------------------------------------------------------------------

@app.websocket("/ws")
async def l4_010WebSocketConnections(
    websocket: WebSocket
) -> None:
    """Handle WebSocket client connections."""

    # Connect client.
    await manager.connect(
        websocket
    )

    print(
        f"Client connected. Active clients: {manager.connection_count()}"
    )

    try:

        # Keep connection open.
        while True:

            # Wait for message from client.
            message = await websocket.receive_text()

            print(
                f"Received: {message}"
            )

            # Send response to same client.
            await websocket.send_text(
                f"Server received: {message}"
            )

    except WebSocketDisconnect:

        # Remove disconnected client.
        manager.disconnect(
            websocket
        )

        print(
            f"Client disconnected. Active clients: {manager.connection_count()}"
        )