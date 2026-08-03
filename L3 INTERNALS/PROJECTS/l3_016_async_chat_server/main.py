import asyncio

from server import L3_016ChatServer


#-----------------------------------------------------------------------------
# Run Chat Server
#-----------------------------------------------------------------------------

async def run_l3_016ChatServer() -> None:
    """Run the async chat server."""

    # Create the chat server instance.
    server = L3_016ChatServer(
        host="127.0.0.1",
        port=8888,
    )

    # Start the chat server.
    await server.l3_016Start()


#-----------------------------------------------------------------------------
# Program Entry Point
#-----------------------------------------------------------------------------

def main() -> None:
    """Program entry point."""

    asyncio.run(
        run_l3_016ChatServer()
    )


if __name__ == "__main__":
    main()