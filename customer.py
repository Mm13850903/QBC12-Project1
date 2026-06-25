import re


def login_required(func):
    def wrapper(self, *args, **kwargs):
        if not self.is_logged_in:
            return False
        return func(self, *args, **kwargs)

    return wrapper


class Customer:
    email_pattern = re.compile(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
    password_pattern = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@&]).+$')
    customer_list = []

    def __init__(self, username, name, email, password):
        Customer.validate_username(username)
        self.__username = username
        self.name = name
        self.email = email
        self.password = password
        self.my_cards = []
        self.__is_logged_in = False

    @property
    def username(self):
        return self.__username

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        if not Customer.email_pattern.fullmatch(value):
            raise ValueError("Invalid email address")
        found_email = Customer.find_email(value)
        if found_email is not None and found_email is not self:
            raise ValueError("Email already exists")
        self.__email = value

    @property
    def password(self):
        raise AttributeError("Password is write-only")

    @password.setter
    def password(self, value):
        if not Customer.password_pattern.fullmatch(value):
            raise ValueError("Password must contain letter, digit and one of @ or &")
        self.__password = value

    def check_password(self, password):
        return self.__password == password

    @property
    def is_logged_in(self):
        return self.__is_logged_in

    def add_customer(self):
        if Customer.find_username(self.username) is not None:
            return False
        if Customer.find_email(self.email) is not None:
            return False
        Customer.customer_list.append(self)
        return True

    @login_required
    def add_card(self, card):
        found_card = self.find_card(card.card_id)
        if found_card is not None:
            return False
        self.my_cards.append(card)
        return True

    @classmethod
    def find_username(cls, username):
        for customer in cls.customer_list:
            if customer.username == username:
                return customer
        return None

    @classmethod
    def find_email(cls, email):
        for customer in cls.customer_list:
            if customer.email == email:
                return customer
        return None

    def find_card(self, card_id):
        for card in self.my_cards:
            if card.card_id == card_id:
                return card
        return None

    @login_required
    def remove_card(self, card):
        found_card = self.find_card(card.card_id)
        if found_card is None:
            return False
        self.my_cards.remove(found_card)
        return True

    def login(self, password):
        if self.check_password(password):
            self.__is_logged_in = True
            return True
        return False

    def logout(self):
        self.__is_logged_in = False

    @classmethod
    def authenticate(cls, username, password):
        customer = cls.find_username(username)
        if customer is None:
            return None
        if customer.login(password):
            return customer
        return None

    @login_required
    def update_profile(self,name=None, email=None, password=None):
        if name is not None:
            self.name = name
        if email is not None:
            self.email = email
        if password is not None:
            self.password = password
        return True

    @staticmethod
    def validate_username(username):
        if Customer.find_username(username):
            raise ValueError("Username already exists")

    @classmethod
    def signup(cls, username, name, email, password):
        customer = cls(username, name, email, password)
        if not customer.add_customer():
            return None
        return customer

    def __str__(self):
        return (
            f"Username: {self.username}\n"
            f"Name: {self.name}\n"
            f"Email: {self.email}\n"
            f"Cards: {len(self.my_cards)}"
        )

    @login_required
    def view_profile(self):
        return str(self)
