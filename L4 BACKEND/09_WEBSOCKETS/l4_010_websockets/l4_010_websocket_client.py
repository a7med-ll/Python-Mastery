import asyncio
import websockets

# -----------------------------------------------------------------------------
# WebSocket Settings
# -----------------------------------------------------------------------------

WEBSOCKET_URL = "ws://127.0.0.1:8000/ws"

# -----------------------------------------------------------------------------
# Connect To WebSocket Server
# -----------------------------------------------------------------------------

async def l4_010ConnectWebSocket() -> None:
    """Connect to WebSocket server and exchange a message."""

    # Create WebSocket connection.
    async with websockets.connect(
        WEBSOCKET_URL,
    ) as websocket:

        print(
            "Connected to WebSocket server."
        )

        # Create message.
        message = "Hello from WebSocket client"

        # Send message to server.
        await websocket.send(
            message
        )

        print(
            f"Sent: {message}"
        )

        # Wait for response from server.
        response = await websocket.recv()

        print(
            f"Received: {response}"
        )

# -----------------------------------------------------------------------------
# Run WebSocket Client
# -----------------------------------------------------------------------------

def run_l4_010WebSocketClient() -> None:
    """Run WebSocket client."""

    asyncio.run(
        l4_010ConnectWebSocket()
    )

# -----------------------------------------------------------------------------
# Program Entry Point
# -----------------------------------------------------------------------------

if __name__ == "__main__":

    run_l4_010WebSocketClient()