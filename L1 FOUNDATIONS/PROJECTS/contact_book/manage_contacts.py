from contacts_class import Contact

class ManageContacts:
    def __init__(self):
        self.ContactsList = []
        self.load_contacts()

    def add_contact(self):

        name = input("Please enter your name: ")
        phonenum =(input("Please enter your phone number: "))
        email = input("Please enter your email: ")

        contact = Contact(name, phonenum, email)
        self.ContactsList.append(contact)
        self.save_contacts()

    def list_contacts(self):

        if not self.ContactsList:
            print("No Contacts Found")

        else:
            for index, contact in enumerate(self.ContactsList):
                print(f"{index}: {contact.name} | {contact.phonenum}")


    def search_contact(self):

        usr_search = input("Please Enter The Name To Search: ")

        results =[]
        for contact in self.ContactsList:
            if usr_search.lower() in contact.name.lower():
                results.append(contact)


        if not results:
            print("No Contact Found")
        else:
            for contact in results:
                print(f"{contact.name} | {contact.phonenum} | {contact.email}")

    def sort_contacts(self):
        sorted_contacts = sorted(self.ContactsList, key=lambda contact: contact.name.lower())


        for contact in sorted_contacts:
            print(f"{contact.name} | {contact.phonenum} | {contact.email}")

    def filter_contacts(self):
        domain =input("Please Enter The Domain Name To Filter By (eg gmail.com) ")

        results = []
        for contact in self.ContactsList:

            if domain.lower() in contact.email.lower():
                results.append(contact)


        if not results:
            print("No Contact Found")

        else:
            for contact in results:
                print(f"{contact.name} | {contact.phonenum} | {contact.email}")

    def save_contacts(self):
        with open("contacts.txt", "w") as file:
            for contact in self.ContactsList:
                file.write(f"{contact.name}|{contact.phonenum}|{contact.email}\n")

    def load_contacts(self):
        try:
            with open("contacts.txt", "r") as file:
                for line in file:
                    line = line.strip()
                    if line:
                        name, phonenum, email = line.split("|")
                        contact = Contact(name, phonenum, email)
                        self.ContactsList.append(contact)

        except FileNotFoundError:
            pass