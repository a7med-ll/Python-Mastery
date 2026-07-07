from manage_contacts import ManageContacts

manage_contacts = ManageContacts()

while True:

    print("-----Welcome to the contact book-----")
    print("1. Add a new contact")
    print("2. List contacts")
    print("3. Search a contact")
    print("4. Sort a contact")
    print("5. Filter a contact")
    print("6. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        manage_contacts.add_contact()

    elif choice == "2":
        manage_contacts.list_contacts()

    elif choice == "3":
        manage_contacts.search_contact()

    elif choice == "4":
        manage_contacts.sort_contacts()

    elif choice == "5":
        manage_contacts.filter_contacts()

    elif choice == "6":
        print("GoodByee")
        break

    else:
        print("Please enter a valid choice")

