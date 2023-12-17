class Client:
    def __init__(self, phone_number: str):
        self.phone_number = phone_number
        self.shopping_cart: list = []
        self.bill: float = 0.0

    @property
    def phone_number(self):
        return self.__phone_number

    @phone_number.setter
    def phone_number(self, value):
        if len(value) != 10 or not value.isdigit() or value[0] != '0' or not isinstance(value, str):
            raise ValueError("Invalid phone number!")
        self.__phone_number = value
