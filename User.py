from PassportData import PassportData
from ContactData import ContactData
from Account import Account, AccountDebit, AccountDeposit, AccountCredit
from Loan import Loan
from datetime import date

class User:
    def __init__(self, id: int, passport_data: PassportData, contact_data: ContactData, encoded_pass: str):
        self.id = id
        self.passport_data = passport_data
        self.contact_data = contact_data
        self.encoded_pass = encoded_pass

    def auth(self, password: str) -> bool:
        # Аутентификация пользователя
        return self.encoded_pass == password

    def get_user_info(self) -> str:
        # Получение информации о пользователе
        return f"ID: {self.id}, Name: {self.passport_data.name} {self.passport_data.surname}"
    
class Customer(User):
    def __init__(self, id: int, passport_data: PassportData, contact_data: ContactData, encoded_pass: str, status: str):
        super().__init__(id, passport_data, contact_data, encoded_pass)
        self.status = status
        self.accounts = []
        self.loans = []

    def open_account(self, account_type: str) -> 'Account':
        # Генерация номера счёта (пример)
        account_number = len(self.accounts) + 1000  # начиная с 1000
        balance = 0.0
        status = "active"
        limit = 1000.0 if account_type == "debit" else float('inf')  # например
        open_date = date.today()

        if account_type == "debit":
            new_account = AccountDebit(
                number=account_number,
                owner=self,
                balance=balance,
                open_date=open_date,
                status=status,
                limit=limit
            )
        elif account_type == "deposit":
            new_account = AccountDeposit(
                number=account_number,
                owner=self,
                balance=balance,
                open_date=open_date,
                status=status,
                limit=limit,
                rate_deposit=0.05,
                last_calculated=open_date
            )
        elif account_type == "credit":
            new_account = AccountCredit(
                number=account_number,
                owner=self,
                balance=balance,
                open_date=open_date,
                status=status,
                limit=limit,
                rate_credit=0.15,
                borrowed=0.0,
                last_calculated=open_date
            )
        else:
            raise ValueError("Invalid account type")

        self.accounts.append(new_account)
        return new_account

    def get_accounts(self) -> list:
        # Получение списка всех счетов клиента
        return self.accounts

    def get_loans(self) -> list:
        # Получение списка всех займов клиента
        return self.loans
    
class Clerk(User):
    def __init__(self, id: int, passport_data: PassportData, contact_data: ContactData, encoded_pass: str, position: str):
        super().__init__(id, passport_data, contact_data, encoded_pass)
        self.position = position

    def open_account(self, customer: Customer) -> 'Account':
        # Открытие нового счета для клиента
        account_type = input("Enter account type (debit, deposit, credit): ")
        return customer.open_account(account_type)

    def open_loan(self, customer: Customer, amount: float) -> 'Loan':
        # Генерация ID на основе количества займов у клиента
        loan_id = len(customer.loans) + 1

        # Процентная ставка по умолчанию
        rate_interest = 0.12  # 12%

        # Срок кредита — например, 365 дней от текущей даты
        term = date.today().replace(year=date.today().year + 1)

        # Статус по умолчанию
        status = "active"

        # Создание экземпляра Loan
        loan = Loan(
            id=loan_id,
            amount=amount,
            rate_interest=rate_interest,
            term=term,
            status=status,
            customer=customer
        )

        customer.loans.append(loan)
        return loan