class InsufficientFundsError(Exception):
    pass


class InvalidAmountError(Exception):
    pass


class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise InvalidAmountError("Deposit amount must be positive")
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            raise InsufficientFundsError(f"Withdrawal amount exceeds balance amount {self.balance}")
        if amount <= 0:
            raise InvalidAmountError("Withdrawal amount must be positive")
        self.balance -= amount

    def __str__(self):
        return f"BankAccount(owner={self.owner}, balance={self.balance})"

    def __eq__(self, other):
        return self.balance == other.balance

    def __lt__(self, other):
        return self.balance < other.balance