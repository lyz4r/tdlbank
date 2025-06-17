# Loan.py

from datetime import date
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from User import Customer


class Loan:
    def __init__(self, id: int, amount: float, rate_interest: float, term: date, status: str, customer: 'Customer'):
        self.id = id
        self.amount = amount
        self.rate_interest = rate_interest
        self.term = term
        self.status = status
        self.customer = customer

    def calculate(self) -> float:
        days_passed = (date.today() - self.term).days
        interest = self.amount * self.rate_interest * (days_passed / 365)
        total_debt = self.amount + interest
        return total_debt

    def repay(self, sum: float) -> float:
        if self.amount >= sum:
            self.amount -= sum
            print(f"Оплачено {sum} из задолженности {self.id}")
            return sum
        else:
            print("Невозможно оплатить больше, чем задолженность")
            return 0