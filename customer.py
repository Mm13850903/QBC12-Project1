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
        self.__set_password(password)
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

    def __set_password(self, value):
        if not Customer.password_pattern.fullmatch(value):
            raise ValueError("Password must contain letter, digit and one of @ or &")
        self.__password = value

    def check_password(self, password):
        return self.__password == password

    @login_required
    def change_password(self, old_password, new_password):
        if not self.check_password(old_password):
            return False
        self.__set_password(new_password)
        return True

    @property
    def is_logged_in(self):
        return self.__is_logged_in

    def add_customer(self):
        found_username = Customer.find_username(self.username)
        if found_username is not None and found_username is not self:
            return False
        found_email = Customer.find_email(self.email)
        if found_email is not None and found_email is not self:
            return False
        if self not in Customer.customer_list:
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
    def update_profile(self, name=None, email=None):
        if name is not None:
            self.name = name
        if email is not None:
            self.email = email
        return True

    @classmethod
    def validate_username(cls, username):
        if cls.find_username(username):
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


def customer_auth_menu():
    while True:
        print("""
===== Customer Menu =====
1. Sign Up
2. Login
3. Back
""")

        choice = input("Choose an option: ").strip()
        match choice:
            case "1":
                signup_customer()
            case "2":
                customer = login_customer()
                if customer is not None:
                    print("Login successful")
                    customer_panel(customer)
            case "3":
                break
            case _:
                print("Invalid option")

def signup_customer():
    username = input("Enter username: ").strip()
    name = input("Enter name: ").strip()
    email = input("Enter email: ").strip()
    password = input("Enter password: ")
    
    if not username:
        print("Username cannot be empty")
        return
    if not name:
        print("Name cannot be empty")
        return
    try:

        customer = Customer.signup(username, name, email, password)
        if customer is None:
            print("Sign up failed")
        else:
            print("Sign up successful")
    except ValueError as error:
        print(error)

def login_customer():
    while True:
        print("""
===== Login =====
1. Enter username and password
2. Back
""")
        choice = input("Choose an option: ").strip()
        match choice:
            case "1":
                username = input("Enter username: ").strip()
                password = input("Enter password: ")
                customer = Customer.authenticate(username, password)
                if customer is not None:
                    return customer
                print("Invalid username or password")
            case "2":
                return None
            case _:
                print("Invalid option")

def customer_panel(customer):
    while customer.is_logged_in:
        print("""
===== Customer Panel =====
1. Edit Profile
2. Logout
""")
        choice = input("Choose an option: ").strip()
        match choice:
            case "1":
                edit_profile_menu(customer)
            case "2":
                customer.logout()
                print("Logged out successfully")
            case _:
                print("Invalid option")

def edit_profile_menu(customer):
    while customer.is_logged_in:
        print("""
===== Profile Information =====
""")
        print(customer.view_profile())
        print("""
===== Edit Profile =====
1. Edit Name
2. Edit Email
3. Change Password
4. Back
""")
        choice = input("Choose an option: ").strip()
        match choice:
            case "1":
                edit_name(customer)
            case "2":
                edit_email(customer)
            case "3":
                edit_password(customer)
            case "4":
                break
            case _:
                print("Invalid option")

def edit_name(customer):
    new_name = input("Enter new name: ").strip()
    if not new_name:
        print("Name cannot be empty")
        return
    if customer.update_profile(name=new_name):
        print("Name updated successfully")
    else:
        print("Update failed")

def edit_email(customer):
    new_email = input("Enter new email: ").strip()
    try:
        if customer.update_profile(email=new_email):
            print("Email updated successfully")
        else:
            print("Update failed")
    except ValueError as error:
        print(error)

def edit_password(customer):
    old_password = input("Enter current password: ")
    new_password = input("Enter new password: ")
    
    try:
        if customer.change_password(old_password, new_password):
            print("Password changed successfully")
        else:
            print("Current password is incorrect")
    except ValueError as error:
        print(error)


customer_auth_menu()
