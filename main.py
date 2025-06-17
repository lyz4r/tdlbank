from datetime import date

from ContactData import ContactData
from PassportData import PassportData
from User import Customer, Clerk
from Account import AccountDebit, AccountDeposit, AccountCredit
from Loan import Loan

def main():
    # Создание паспортных данных для клиента
    passport_data = PassportData(
        name="Кирилл",
        surname="Дмитриевич",
        father_name="Мальцев",
        series=1234,
        number=567890,
        birth_date=date(2005, 12, 26),
        address_registration="г. Севастополь, проспект Генерала Острякова, д. 148, кв. 8"
    )
    # Создание контактных данных для клиента
    contact_data = ContactData(email="john.doe@example.com", phone_number=1234567890, address_fact="г. Севастополь, ул. Одесская, 27")

    # Создание клиента
    customer = Customer(
        id=1,
        passport_data=passport_data,
        contact_data=contact_data,
        encoded_pass="password123",
        status="active"
    )

    # Тест 1: Проверка аутентификации
    print("Тест 1: Аутентификация")
    if customer.auth("password123"):
        print("Аутентификация успешна")
    else:
        print("Аутентификация не удалась")

    # Тест 2: Проверка неудачной аутентификации
    if customer.auth("wrongpassword"):
        print("Аутентификация не удалась - неверный пароль")
    else:
        print("Попытка аутентификации произошла - неверный пароль (должна быть ошибка)")

    # Тест 3: Открытие и управление счетами
    print("\nТест 2: Операции со счетами")
    debit_account = customer.open_account("debit")
    debit_account.activate()
    debit_account.balance = 1000.0
    print(f"Открыт дебетовый счёт: {debit_account.number}, Баланс: {debit_account.balance}")

    deposit_account = customer.open_account("deposit")
    deposit_account.balance = 5000.0
    deposit_account.activate()
    print(f"Открыт депозитный счёт: {deposit_account.number}, Баланс: {deposit_account.balance}")

    credit_account = customer.open_account("credit")
    credit_account.activate()
    credit_account.borrowed = 2000.0
    credit_account.balance = 2000.0
    print(f"Открыт кредитный счёт: {credit_account.number}, Задолженность: {credit_account.borrowed}")

    # Тест 4: Переводы между счетами
    print("\nТест 3: Переводы")
    if debit_account.transfer_to(deposit_account, 500.0):
        print(f"После перевода - Дебетовый баланс: {debit_account.balance}, Депозитный баланс: {deposit_account.balance}")
    else:
        print("Перевод не удался")

    # Попытка перевода при недостатке средств
    if debit_account.transfer_to(deposit_account, 1000.0):
        print("Перевод успешен (должен быть неуспешным)")
    else:
        print("Перевод не удался - недостаточно средств")

    # Тест 5: Расчёт процентов
    print("\nТест 4: Расчёт процентов")
    deposit_interest = deposit_account.calculate()
    print(f"Проценты по депозитному счёту: {deposit_interest}, Новый баланс: {deposit_account.balance}")

    credit_interest = credit_account.calculate()
    print(f"Проценты по кредитному счёту: {credit_interest}, Новый баланс: {credit_account.balance}")

    # Тест 6: Погашение кредита
    print("\nТест 5: Погашение кредита")
    repaid = credit_account.repay(500.0)
    print(f"Погашено {repaid} с кредитного счёта, Новая задолженность: {credit_account.borrowed}, Баланс: {credit_account.balance}")

    # Попытка погасить больше, чем есть на балансе
    repaid = credit_account.repay(3000.0)
    print(f"Погашено {repaid} (должно быть 0 - недостаточно средств), Задолженность: {credit_account.borrowed}")

    # Тест 7: Изменение статуса счёта
    print("\nТест 6: Изменение статуса счёта")
    debit_account.freeze()
    print(f"Статус дебетового счёта: {debit_account.status}")
    if debit_account.transfer_to(deposit_account, 100.0):
        print("Перевод успешен (должен быть неуспешным)")
    else:
        print("Перевод не удался - счёт заморожен")

    debit_account.activate()
    print(f"Дебетовый счёт реактивирован, Статус: {debit_account.status}")

    # Тест 8: Операции клерка
    print("\nТест 7: Операции клерка")
    clerk = Clerk(
        id=2,
        passport_data=PassportData(
            name="Леонид",
            surname="Мальцев",
            father_name="Максимович",
            series=4321,
            number=987654,
            birth_date=date(2006, 7, 4),
            address_registration="г. Севастополь, ул. Одесская, 27"
        ),
        contact_data=ContactData(email="lyonya.goy@example.com", phone_number=9876543210, address_fact="г. Севастополь, ул. Одесская, 27"),
        encoded_pass="clerkpass",
        position="Clerk"
    )

    # Клерк открывает новый дебетовый счёт для клиента
    clerk_debit_account = clerk.open_account(customer, "debit")
    clerk_debit_account.balance = 2000.0
    clerk_debit_account.activate()
    print(f"Клерк открыл дебетовый счёт: {clerk_debit_account.number}, Баланс: {clerk_debit_account.balance}")

    # Тест 9: Операции с займами
    print("\nТест 8: Операции с займами")
    loan = clerk.open_loan(customer, amount=10000)
    print(f"Открыт заём с ID: {loan.id}, Сумма: {loan.amount}")

    loan_total_debt = loan.calculate()
    print(f"Общая задолженность по займу (с процентами): {loan_total_debt}")

    # Погашение части займа
    repaid = loan.repay(2000.0)
    print(f"Погашено {repaid} с займа, Остаток: {loan.amount}")

    # Попытка погасить больше, чем осталось
    repaid = loan.repay(10000.0)
    print(f"Погашено {repaid} (должно быть 0 - нельзя погасить больше), Остаток: {loan.amount}")

    # Тест 10: Несколько займов
    print("\nТест 9: Несколько займов")
    second_loan = clerk.open_loan(customer, amount=5000)
    print(f"Открыт второй заём с ID: {second_loan.id}, Сумма: {second_loan.amount}")

    # Вывод списка всех займов
    print("Займы клиента:")
    for loan in customer.get_loans():
        print(f"Заём ID: {loan.id}, Сумма: {loan.amount}, Статус: {loan.status}")

    # Тест 11: Вывод списка всех счетов
    print("\nТест 10: Вывод всех счетов")
    print("Счета клиента:")
    for account in customer.get_accounts():
        print(f"Счёт номер: {account.number}, Тип: {type(account).__name__}, Баланс: {account.balance}, Статус: {account.status}")

if __name__ == "__main__":
    main()