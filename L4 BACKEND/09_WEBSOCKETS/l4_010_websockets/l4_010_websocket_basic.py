from fastapi import FastAPI, WebSocket

# -----------------------------------------------------------------------------
# Create FastAPI Application
# -----------------------------------------------------------------------------

app = FastAPI()

# -----------------------------------------------------------------------------
# Basic WebSocket Endpoint
# -----------------------------------------------------------------------------

@app.websocket("/ws")      # --> This creates a WebSocket endpoint
async def l4_010WebSocketEndpoint(websocket: WebSocket) -> None:
    """Handle a basic WebSocket connection."""

    # Accept WebSocket connection from client.
    await websocket.accept()

    # Wait for a message from the client.
    client_message = await websocket.receive()

    # Print received message.
    print(
        f"Client message: {client_message}"
    )

    # Send message back to the client. or server sending message to the client
    await websocket.send_text(
        f"Server received: {client_message}"
    )

    # Close WebSocket connection.
    await websocket.close()
