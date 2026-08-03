from dataclasses import dataclass
from asyncio import StreamReader, StreamWriter

@dataclass(slots=True)      # --> this dataclass represents a connected client.
class L3_016ClientSession:
    """Represent one connected chat client."""

    nickname: str
    reader: StreamReader
    writer: StreamWriter