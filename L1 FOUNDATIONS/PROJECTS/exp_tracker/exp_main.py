from exp_manage import ManageExpenses


def main():
    manager = ManageExpenses()

    while True:
        print("\n--- EXPENSE TRACKER ---")
        print("1. Add expense")
        print("2. List expenses")
        print("3. Total expenses")
        print("4. Export to CSV")
        print("5. Quit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            manager.add_expense()
        elif choice == "2":
            manager.list_expenses()
        elif choice == "3":
            manager.total_expenses()
        elif choice == "4":
            manager.export_to_csv()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid option, try again.")


if __name__ == "__main__":
    main()