# ContactData.py

class ContactData:
    def __init__(self, email: str, phone_number: int, address_fact: str):
        self.email = email
        self.phone_number = phone_number
        self.address_fact = address_fact

    def bind(self):
        pass  # Метод для привязки контактных данных