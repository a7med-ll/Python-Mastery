import asyncio

from models import L3_016ClientSession

#-----------------------------------------------------------------------------
# Server Class and Client Storage
#-----------------------------------------------------------------------------

class L3_016ChatServer:
    """Manage connected clients and chat-server operations."""

    def __init__(self,host: str,port: int) -> None:

        self._host = host     # --> Store the host.
        self._port = port     # --> Store the port.

        self._clients: list[L3_016ClientSession] = []   # --> a collection that will later hold many client sessions

        self._clients_lock = asyncio.Lock()   # --> Create an asyncio lock for shared client state.

    @property
    def client_count(self) -> int:
        """Return the number of connected clients."""

        return len(self._clients)    # --> return the length of the client collection

    #-----------------------------------------------------------------------------
    # Register and Remove Clients
    #-----------------------------------------------------------------------------

    async def l3_016RegisterClient(self, client: L3_016ClientSession) -> None:
        """Register one connected client."""

        async with self._clients_lock:    # --> Acquire the client lock.
            self._clients.append(client)  # --> Add the client to the collection.

    async def l3_016RemoveClient(self, client: L3_016ClientSession) -> None:
        """Remove one disconnected client."""

        async with self._clients_lock:     # -->Acquire the client lock.
            if client in self._clients:    # --> Remove the client only if it exists.
                self._clients.remove(client)

    #-----------------------------------------------------------------------------
    # Broadcast Messages
    #-----------------------------------------------------------------------------

    async def l3_016Broadcast(self, message: str, excluded_client: L3_016ClientSession | None = None) -> None:
        """Send one message to all connected clients."""

        # Encode the message into bytes.
        encoded_message = (message + "\n").encode("utf-8")   # --> UTF-8 and add a newline so the receiving client can read one full line.

        # Safely copy the current client list.
        async with self._clients_lock:
            clients = self._clients.copy()

        # Loop through the copied clients.
        for client in clients:

            # Skip excluded_client when provided.
            if client is excluded_client:
                continue

            try:

                # For each client:
                #
                # call client.writer.write(...)
                # then await client.writer.drain()

                client.writer.write(encoded_message)
                await client.writer.drain()

            # Handle ConnectionError
            except ConnectionError:
                continue

    # -----------------------------------------------------------------------------
    # Client Connection Handler
    # -----------------------------------------------------------------------------

    async def l3_016HandleClient(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        """Handle one connected chat client."""

        client: L3_016ClientSession | None = None

        try:

            # Ask the client for a nickname.
            writer.write(b"Enter your nickname: ")
            await writer.drain()

            # Read the nickname from the stream.
            response = await reader.readline()

            # Handle a client that disconnects before sending a nickname.
            if not response:
                return

            # Decode and clean the nickname.
            nickname = response.decode("utf-8").strip()

            # Reject an empty nickname.
            if not nickname:
                return

            # Create a client session.

            client = L3_016ClientSession(

                nickname=nickname,
                reader=reader,
                writer=writer,
            )

            # Register the client.
            await self.l3_016RegisterClient(client)

            # Send a welcome message to the connected client.
            welcome_message = f"Welcome {nickname}!\n"

            # encode it as bytes
            encoded_message = welcome_message.encode("utf-8")

            # and then write it
            client.writer.write(encoded_message)
            await client.writer.drain()

            # Broadcast a join message to the other clients.
            join_message = f"{nickname} joined the chat"

            await self.l3_016Broadcast(
                join_message,
                excluded_client=client,
            )

            # Read chat messages in a loop.
            while True:

                # Read one message from the client.
                data = await reader.readline()

                # Stop if the client disconnects
                if not data:
                    break

                # Decode and clean the message.
                message = data.decode("utf-8").strip()

                # Skip empty messages.
                if not message:
                    continue

                # Format the chat message.
                formatted_message = f"{nickname}: {message}"

                # Broadcast to other clients.
                await self.l3_016Broadcast(
                    formatted_message,
                    excluded_client=client,
                )

        except ConnectionError:
            # Handle client disconnect or connection failure.
            pass

        finally:

            # Remove the client if it was registered.
            if client is not None:

                await self.l3_016RemoveClient(client)

                # Broadcast leave message to remaining clients.
                leave_message = f"{client.nickname} left the chat"

                await self.l3_016Broadcast(
                    leave_message,
                    excluded_client=client,
                )

            # Close the client connection.
            writer.close()

            # Wait until the writer is fully closed.
            await writer.wait_closed()

    # -----------------------------------------------------------------------------
    # Start Async Server
    # -----------------------------------------------------------------------------

    async def l3_016Start(self) -> None:
        """Start the async chat server."""

        # Create the TCP server.
        server = await asyncio.start_server(
            self.l3_016HandleClient,
            self._host,
            self._port,
        )

        # Print server startup information.
        print(
            f"Chat server started on {self._host}:{self._port}"
        )

        # Keep the server running forever.
        async with server:
            await server.serve_forever()





