from dataclasses import dataclass

@dataclass
class Post:

    userId: int
    id:  int
    title: str
    body: str