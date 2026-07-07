from exp_class import Expense, NegativeAmountError, InvalidCategoryError
import csv


class ManageExpenses:
    def __init__(self):
        self.expenses = []

    def add_expense(self):
        try:
            amount = float(input("Enter amount: "))
            category = input(f"Enter category {Expense.VALID_CATEGORIES}: ")
            description = input("Enter description: ")

            expense = Expense(amount, category, description)
            self.expenses.append(expense)
            print("Expense added successfully.")

        except NegativeAmountError as e:
            print(f"Error: {e}")

        except InvalidCategoryError as e:
            print(f"Error: {e}")

        except ValueError:
            print("Invalid amount — please enter a number.")

    def list_expenses(self):
        if not self.expenses:
            print("No expenses recorded yet.")
        else:
            for index, expense in enumerate(self.expenses, start=1):
                print(f"{index}. {expense}")

    def total_expenses(self):
        if not self.expenses:
            print("No expenses to total.")
            return

        choice = input("Total all expenses or by category? (all/category): ").strip().lower()

        if choice == "all":
            total = sum(expense.amount for expense in self.expenses)
            print(f"Total spending: {total}")

        elif choice == "category":
            category = input(f"Enter category {Expense.VALID_CATEGORIES}: ")
            total = sum(expense.amount for expense in self.expenses if expense.category == category)
            print(f"Total spending in {category}: {total}")

        else:
            print("Invalid choice.")

    def export_to_csv(self):
        if not self.expenses:
            print("No expenses to export.")
            return

        with open("expenses.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Category", "Amount", "Description"])

            for expense in self.expenses:
                writer.writerow([expense.category, expense.amount, expense.description])

        print("Expenses exported to expenses.csv")