class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __str__(self):
        return f"{self.name} - {self.description}"

class Room:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.items = []
        self.exits = {}

    def __str__(self):
        return f"{self.name}: {self.description}"

    def add_item(self, item):
        self.items.append(item)

    def set_exit(self, direction, room):
        self.exits[direction.lower()] = room

class Player:
    def __init__(self, current_room):
        self.current_room = current_room
        self.inventory = []

    def __str__(self):
        return f"Player at {self.current_room.name}"