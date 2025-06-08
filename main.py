# main.py

from datetime import date

from ContactData import ContactData
from PassportData import PassportData
from User import Customer, Clerk
from Account import AccountDebit, AccountDeposit, AccountCredit
from Loan import Loan


def main():
    passport_data = PassportData(
        name="John",
        surname="Doe",
        father_name="Michael",
        series=1234,
        number=567890,
        birth_date=date(1990, 1, 1),
        address_registration="123 Main St"
    )
    contact_data = ContactData(email="john.doe@example.com", phone_number=1234567890, address_fact="123 Main St")

    customer = Customer(
        id=1,
        passport_data=passport_data,
        contact_data=contact_data,
        encoded_pass="password123",
        status="active"
    )

    if customer.auth("password123"):
        print("Authentication successful")

        debit_account = customer.open_account("debit")
        debit_account.activate()
        debit_account.balance = 1000.0 
        print(f"Opened Debit Account: {debit_account.number}")

        deposit_account = customer.open_account("deposit")
        print(f"Opened Deposit Account: {deposit_account.number}")

        credit_account = customer.open_account("credit")
        print(f"Opened Credit Account: {credit_account.number}")

        clerk = Clerk(
            id=2,
            passport_data=PassportData(
                name="Jane",
                surname="Smith",
                father_name="Robert",
                series=4321,
                number=987654,
                birth_date=date(1985, 5, 5),
                address_registration="456 Elm St"
            ),
            contact_data=ContactData(email="jane.smith@example.com", phone_number=9876543210, address_fact="456 Elm St"),
            encoded_pass="clerkpass",
            position="Clerk"
        )

        loan = clerk.open_loan(customer, amount=10000)
        print(f"Opened Loan with ID: {loan.id}")

        debit_account.transfer_to(deposit_account, 500.0)

        deposit_account.calculate()

        credit_account.repay(500)

        loan.repay(1000)
    else:
        print("Authentication failed")


if __name__ == "__main__":
    main()