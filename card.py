import random


class Card:
    card_list = []

    def __init__(self, name, exp_month, exp_year, password, balance=0):

        self.card_id = Card.generate_card_number()
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Name cannot be empty")
        self.name = name
        self.__set_exp_month(exp_month)
        self.__set_exp_year(exp_year)
        self.__set_password(password)
        self.__cvv2 = Card.generate_cvv2()
        if not isinstance(balance, (int, float)) or balance < 0:
            raise ValueError("Balance must be a non-negative number")
        self.__balance = balance
        Card.card_list.append(self)

    def __set_password(self, value):
        value = str(value)
        if not (len(value) == 6 and value.isdigit()):
            raise ValueError("Password must be only 6 digits")
        self.__password = value

    def check_password(self, password):
        return self.__password == str(password)

    def check_cvv2(self, cvv2):
        return self.__cvv2 == str(cvv2)

    def __set_exp_month(self, exp_month):
        if not str(exp_month).isdigit():
            raise ValueError("Exp month must be a number")
        exp_month = int(exp_month)
        if not (1 <= exp_month <= 12):
            raise ValueError("Exp month must be between 1 and 12")
        self.__exp_month = exp_month

    def check_exp_month(self, exp_month):
        if not str(exp_month).isdigit():
            return False
        return self.__exp_month == int(exp_month)

    def __set_exp_year(self, exp_year):
        if not str(exp_year).isdigit():
            raise ValueError("Exp year must be a number")
        exp_year = int(exp_year)
        if exp_year < 1403 or exp_year > 1408:
            raise ValueError("Exp year must be between 1403 and 1408")
        self.__exp_year = exp_year

    def check_exp_year(self, exp_year):
        if not str(exp_year).isdigit():
            return False
        return self.__exp_year == int(exp_year)

    @property
    def balance(self):
        return self.__balance

    def deposit(self, amount):
        if not self.validate_positive(amount):
            return False
        self.__balance += amount
        return True

    def withdraw(self, amount):
        if not self.validate_positive(amount):
            return False
        if self.__balance >= amount:
            self.__balance -= amount
            return True
        return False

    @staticmethod
    def validate_positive(amount):
        return isinstance(amount, (int, float)) and amount > 0

    @staticmethod
    def validate_card_id(card_id):
        card_id = str(card_id)
        if len(card_id) == 16 and card_id.isdigit():
            return card_id
        return False

    @classmethod
    def generate_card_number(cls):
        while True:
            first_digit = str(random.randint(1, 9))
            other_digits = ''.join(str(random.randint(0, 9)) for _ in range(15))
            card_id = first_digit + other_digits
            if cls.find_card(card_id) is None:
                return card_id

    @staticmethod
    def generate_cvv2():
        return ''.join(str(random.randint(0, 9)) for _ in range(3))

    @classmethod
    def find_card(cls, card_id):
        card_id = str(card_id)
        for card in cls.card_list:
            if card.card_id == card_id:
                return card
        return None

    def __str__(self):
        return (
            f"Card ID: {self.card_id}\n"
            f"Name: {self.name}\n"
            f"Balance: {self.__balance}"
        )
