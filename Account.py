# Account.py

from datetime import date
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from User import Customer


class Account:
    def __init__(
        self,
        number: int,
        owner: 'Customer',
        balance: float,
        open_date: date,
        status: str,
        limit: int
    ):
        self.number = number
        self.owner = owner
        self.balance = balance
        self.open_date = open_date
        self.status = status
        self.limit = limit

    def activate(self) -> bool:
        self.status = "active"
        return True

    def block(self) -> bool:
        self.status = "blocked"
        return True

    def close(self) -> bool:
        self.status = "closed"
        return True

    def freeze(self) -> bool:
        self.status = "frozen"
        return True


class AccountDebit(Account):
    def transfer_to(self, towards: 'Account', amount: float) -> bool:
        if (self.balance >= amount) and (self.status == "active"):
            self.balance -= amount
            towards.balance += amount
            print(f"Transferred {amount} to account {towards.number}")
            return True
        elif self.status != "active":
            print("Account is not active")
            return False
        else:
            print("Insufficient funds")
            return False


class AccountDeposit(Account):
    def __init__(self, number: int, owner: 'Customer', balance: float, open_date: date, status: str, limit: int, rate_deposit: float, last_calculated: date):
        super().__init__(number, owner, balance, open_date, status, limit)
        self.rate_deposit = rate_deposit
        self.last_calculated = last_calculated

    def calculate(self) -> float:
        days_passed = (date.today() - self.last_calculated).days
        interest = self.balance * self.rate_deposit * (days_passed / 365)
        self.balance += interest
        self.last_calculated = date.today()
        return interest

    def transfer_among_accounts(self, towards: 'Account', amount: float) -> bool:
        if self.balance >= amount and self.status == "active":
            self.balance -= amount
            towards.balance += amount
            print(f"Transferred {amount} to account {towards.number}")
            return True
        elif self.status != "active":
            print("Account is not active")
            return False
        else:
            print("Insufficient funds")
            return False


class AccountCredit(Account):
    def __init__(self, number: int, owner: 'Customer', balance: float, open_date: date, status: str, limit: int, rate_credit: float, borrowed: float, last_calculated: date):
        super().__init__(number, owner, balance, open_date, status, limit)
        self.rate_credit = rate_credit
        self.borrowed = borrowed
        self.last_calculated = last_calculated

    def calculate(self) -> float:
        days_passed = (date.today() - self.last_calculated).days
        interest = self.borrowed * self.rate_credit * (days_passed / 365)
        self.balance += interest
        self.last_calculated = date.today()
        return interest

    def repay(self, sum: float) -> float:
        if self.balance >= sum:
            self.balance -= sum
            self.borrowed -= sum
            print(f"Repaid {sum} from credit account")
            return sum
        else:
            print("Insufficient funds to repay")
            return 0