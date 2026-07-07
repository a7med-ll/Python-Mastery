from game_manage import ManageGame

def main():
    game = ManageGame()

    print("=== TEXT ADVENTURE ===")
    print("Commands: go <direction>, take <item>, inventory, look, quit")

    game.describe_current_room()

    while True:
        command = input("\n> ").strip().lower()

        if command == "quit":
            print("Goodbye!")
            break

        elif command == "look":
            game.describe_current_room()

        elif command == "inventory":
            game.show_inventory()

        elif command.startswith("go "):
            direction = command[3:].strip()
            game.move_player(direction)

        elif command.startswith("take "):
            item_name = command[5:].strip()
            game.take_item(item_name)

        else:
            print("I don't understand that command.")


if __name__ == "__main__":
    main()