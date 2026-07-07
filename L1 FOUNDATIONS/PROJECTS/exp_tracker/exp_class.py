class NegativeAmountError(Exception):
    pass


class InvalidCategoryError(Exception):
    pass

class Expense:
    VALID_CATEGORIES = ["Food", "Transport", "Rent", "Entertainment", "Other"]

    def __init__(self, amount, category, description):
        if amount <= 0:
            raise NegativeAmountError("Amount must be greater than zero.")

        if category.title() not in self.VALID_CATEGORIES:
            raise InvalidCategoryError(f"'{category}' is not a valid category.")

        self.amount = amount
        self.category = category.title()
        self.description = description

    def __str__(self):
        return f"{self.category}: {self.amount} - {self.description}"