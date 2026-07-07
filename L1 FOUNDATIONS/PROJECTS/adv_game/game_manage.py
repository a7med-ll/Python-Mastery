from game_class import Item, Room, Player

class ManageGame:
    def __init__(self):
        self.player = None
        self.build_world()

    def build_world(self):
        hall = Room("Hall", "A dusty entrance hall with cracked marble floors.")
        library = Room("Library", "Shelves of ancient books line the walls.")
        kitchen = Room("Kitchen", "An old kitchen with a cold, unused stove.")

        hall.set_exit("north", library)
        hall.set_exit("east", kitchen)

        library.set_exit("south", hall)
        kitchen.set_exit("west", hall)

        library.add_item(Item("Old Key", "A rusty key with a faded engraving."))
        kitchen.add_item(Item("Knife", "A sharp kitchen knife."))

        self.player = Player(hall)

    def describe_current_room(self):
        room = self.player.current_room
        print(f"\n--- {room.name} ---")
        print(room.description)

        if room.items:
            print("Items here:")
            for item in room.items:
                print(f"  - {item}")
        else:
            print("There is nothing here.")

        if room.exits:
            print("Exits:", ", ".join(room.exits.keys()))

    def move_player(self, direction):
        direction = direction.lower()
        current_room = self.player.current_room

        if direction in current_room.exits:
            self.player.current_room = current_room.exits[direction]
            self.describe_current_room()
        else:
            print("You can't go that way.")

    def take_item(self, item_name):
        room = self.player.current_room

        for item in room.items:
            if item.name.lower() == item_name.lower():
                room.items.remove(item)
                self.player.inventory.append(item)
                print(f"You picked up: {item.name}")
                return

        print("That item isn't here.")

    def show_inventory(self):
        if not self.player.inventory:
            print("Your inventory is empty.")
        else:
            print("You are carrying:")
            for item in self.player.inventory:
                print(f"  - {item}")