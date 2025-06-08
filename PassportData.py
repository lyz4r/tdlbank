# PassportData.py

from datetime import date

class PassportData:
    def __init__(self, name: str, surname: str, father_name: str, series: int, number: int, birth_date: date, address_registration: str):
        self.name = name
        self.surname = surname
        self.father_name = father_name
        self.series = series
        self.number = number
        self.birth_date = birth_date
        self.address_registration = address_registration

    def bind(self):
        pass  # Метод для привязки паспортных данных