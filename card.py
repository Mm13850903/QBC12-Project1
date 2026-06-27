import random

class Card:
    card_list = []
    def __init__(self,name, balance=0):
        self.card_id = Card.generate_card_number()
        Card.card_list.append(self)
        self.name = name
        self.__balance = balance

    def deposit(self,amount):
        if not self.validate_positive(amount):
            return False
        self.__balance += amount
        return True

    def withdraw(self,amount):
        if not self.validate_positive(amount):
            return False
        self.__balance -= amount
        return True


    @staticmethod
    def validate_positive(amount):
        if amount > 0:
            return amount
        return False

    @staticmethod
    def validate_card_id(card_id):
        if len(card_id) == 16:
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

    @classmethod
    def find_card(cls, card_id):
        for card in cls.card_list:
            if card.card_id == card_id:
                return card
        return None



