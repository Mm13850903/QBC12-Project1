import re

from card import Card
from BANK import API


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
        self.__my_wallet = 0

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

    @property
    def my_wallet(self):
        return self.__my_wallet

    @login_required
    def charge_wallet(self, card_id, exp_month, exp_year, password, cvv2, value):
        return self.__charge_wallet(card_id, exp_month, exp_year, password, cvv2, value)

    @login_required
    def charge_wallet_with_saved_card(self, card_id, password, value):
        if value <= 0:
            return False
        card = self.find_card(card_id)
        if card is None:
            return False
        if not card.check_password(password):
            return False
        if not card.withdraw(value):
            return False
        payment_id = API.generate_payment_id(card.card_id, value)
        self.__my_wallet += value
        return payment_id

    def __charge_wallet(self, card_id, exp_month, exp_year, password, cvv2, value):
        if value <= 0:
            return False
        if not API.validate(card_id, exp_month, exp_year, password, cvv2):
            return False
        card = Card.find_card(card_id)
        if card is None:
            return False
        if not card.check_password(password):
            return False
        if not card.check_cvv2(cvv2):
            return False
        if not card.check_exp_month(exp_month):
            return False
        if not card.check_exp_year(exp_year):
            return False
        if not card.withdraw(value):
            return False
        payment_id = API.generate_payment_id(card_id, value)
        self.__my_wallet += value
        if card not in self.my_cards:
            self.my_cards.append(card)
        return payment_id

    @login_required
    def buy_ticket(self, ticket_price):
        if ticket_price < 0:
            return False
        if self.my_wallet < ticket_price:
            return False
        self.__my_wallet -= ticket_price
        return True

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
            if str(card.card_id) == str(card_id):
                return card
        return None

    @login_required
    def remove_card(self, card_id):
        found_card = self.find_card(card_id)
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
            f"Wallet: {self.my_wallet}\n"
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
    while True:
        print("""
===== Sign Up =====
1. Enter sign up information
2. Back
""")

        choice = input("Choose an option: ").strip()

        match choice:
            case "1":
                username = input("Enter username or 0 to back: ").strip()
                if username == "0":
                    print("Sign up cancelled")
                    return
                if not username:
                    print("Username cannot be empty")
                    continue

                name = input("Enter name or 0 to back: ").strip()
                if name == "0":
                    print("Sign up cancelled")
                    return
                if not name:
                    print("Name cannot be empty")
                    continue

                email = input("Enter email or 0 to back: ").strip()
                if email == "0":
                    print("Sign up cancelled")
                    return
                if not email:
                    print("Email cannot be empty")
                    continue

                password = input("Enter password or 0 to back: ")
                if password == "0":
                    print("Sign up cancelled")
                    return
                if not password:
                    print("Password cannot be empty")
                    continue

                try:
                    customer = Customer.signup(username, name, email, password)

                    if customer is None:
                        print("Sign up failed")
                        continue

                    print("Sign up successful")
                    break

                except ValueError as error:
                    print(error)
                    continue

            case "2":
                break

            case _:
                print("Invalid option")


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
                while True:
                    username = input("Enter username or 0 to back: ").strip()

                    if username == "0":
                        print("Login cancelled")
                        return None

                    if not username:
                        print("Username cannot be empty")
                        continue

                    password = input("Enter password or 0 to back: ")

                    if password == "0":
                        print("Login cancelled")
                        return None

                    if not password:
                        print("Password cannot be empty")
                        continue

                    customer = Customer.authenticate(username, password)

                    if customer is not None:
                        return customer

                    print("Invalid username or password. Please try again.")

            case "2":
                return None

            case _:
                print("Invalid option")


def customer_panel(customer):
    while customer.is_logged_in:
        print("""
===== Customer Panel =====
1. View Profile
2. Edit Profile
3. Wallet
4. My Cards
5. Buy Ticket
6. Logout
""")

        choice = input("Choose an option: ").strip()

        match choice:
            case "1":
                print("""
===== Profile Information =====
""")
                print(customer.view_profile())

            case "2":
                edit_profile_menu(customer)

            case "3":
                wallet_menu(customer)

            case "4":
                my_cards_menu(customer)

            case "5":
                buy_ticket_menu(customer)

            case "6":
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
    while True:
        new_name = input("Enter new name or 0 to back: ").strip()

        if new_name == "0":
            print("Edit name cancelled")
            return

        if not new_name:
            print("Name cannot be empty")
            continue

        if customer.update_profile(name=new_name):
            print("Name updated successfully")
            print("\nUpdated Profile:")
            print(customer.view_profile())
            return

        print("Update failed")
        return


def edit_email(customer):
    while True:
        new_email = input("Enter new email or 0 to back: ").strip()

        if new_email == "0":
            print("Edit email cancelled")
            return

        if not new_email:
            print("Email cannot be empty")
            continue

        try:
            if customer.update_profile(email=new_email):
                print("Email updated successfully")
                print("\nUpdated Profile:")
                print(customer.view_profile())
                return

            print("Update failed")
            return

        except ValueError as error:
            print(error)
            continue


def edit_password(customer):
    while True:
        old_password = input("Enter current password or 0 to back: ")

        if old_password == "0":
            print("Change password cancelled")
            return

        if not old_password:
            print("Current password cannot be empty")
            continue

        new_password = input("Enter new password or 0 to back: ")

        if new_password == "0":
            print("Change password cancelled")
            return

        if not new_password:
            print("Password cannot be empty")
            continue

        try:
            if customer.change_password(old_password, new_password):
                print("Password changed successfully")
                print("\nUpdated Profile:")
                print(customer.view_profile())
                return

            print("Current password is incorrect")
            continue

        except ValueError as error:
            print(error)
            continue


def wallet_menu(customer):
    while customer.is_logged_in:
        print(f"""
===== Wallet =====
Current Balance: {customer.my_wallet}

1. Charge Wallet With New Card
2. Charge Wallet With Saved Card
3. Back
""")

        choice = input("Choose an option: ").strip()

        match choice:
            case "1":
                charge_wallet_with_new_card(customer)

            case "2":
                charge_wallet_with_saved_card(customer)

            case "3":
                break

            case _:
                print("Invalid option")


def charge_wallet_with_new_card(customer):
    while True:
        print("""
===== Charge Wallet With New Card =====
""")

        card_id = input("Enter card id or 0 to back: ").strip()
        if card_id == "0":
            print("Charge wallet cancelled")
            return
        if not card_id:
            print("Card id cannot be empty")
            continue

        exp_month = input("Enter exp month or 0 to back: ").strip()
        if exp_month == "0":
            print("Charge wallet cancelled")
            return
        if not exp_month:
            print("Exp month cannot be empty")
            continue

        exp_year = input("Enter exp year or 0 to back: ").strip()
        if exp_year == "0":
            print("Charge wallet cancelled")
            return
        if not exp_year:
            print("Exp year cannot be empty")
            continue

        password = input("Enter card password or 0 to back: ")
        if password == "0":
            print("Charge wallet cancelled")
            return
        if not password:
            print("Card password cannot be empty")
            continue

        cvv2 = input("Enter cvv2 or 0 to back: ").strip()
        if cvv2 == "0":
            print("Charge wallet cancelled")
            return
        if not cvv2:
            print("CVV2 cannot be empty")
            continue

        value = input("Enter amount or 0 to back: ").strip()
        if value == "0":
            print("Charge wallet cancelled")
            return
        if not value:
            print("Amount cannot be empty")
            continue

        try:
            value = int(value)
        except ValueError:
            print("Amount must be a number")
            continue

        if value <= 0:
            print("Amount must be greater than 0")
            continue

        payment_id = customer.charge_wallet(
            card_id,
            exp_month,
            exp_year,
            password,
            cvv2,
            value
        )

        if payment_id:
            print("Wallet charged successfully")
            print(f"Payment ID: {payment_id}")
            print(f"New Balance: {customer.my_wallet}")
            print("Card saved successfully")
            return

        print("Payment failed")
        print("Please check card information or card balance")


def charge_wallet_with_saved_card(customer):
    while True:
        print("""
===== Charge Wallet With Saved Card =====
""")

        if not customer.my_cards:
            print("No saved cards found")
            return

        show_saved_cards(customer)

        card_id = input("Enter card id or 0 to back: ").strip()

        if card_id == "0":
            print("Charge wallet cancelled")
            return

        if not card_id:
            print("Card id cannot be empty")
            continue

        card = customer.find_card(card_id)

        if card is None:
            print("Card not found")
            continue

        password = input("Enter card password or 0 to back: ")

        if password == "0":
            print("Charge wallet cancelled")
            return

        if not password:
            print("Card password cannot be empty")
            continue

        value = input("Enter amount or 0 to back: ").strip()

        if value == "0":
            print("Charge wallet cancelled")
            return

        if not value:
            print("Amount cannot be empty")
            continue

        try:
            value = int(value)
        except ValueError:
            print("Amount must be a number")
            continue

        if value <= 0:
            print("Amount must be greater than 0")
            continue

        payment_id = customer.charge_wallet_with_saved_card(
            card_id,
            password,
            value
        )

        if payment_id:
            print("Wallet charged successfully")
            print(f"Payment ID: {payment_id}")
            print(f"New Balance: {customer.my_wallet}")
            return

        print("Payment failed")
        print("Invalid password or not enough card balance")


def my_cards_menu(customer):
    while customer.is_logged_in:
        print("""
===== My Cards =====
1. View Saved Cards
2. Remove Card
3. Back
""")

        choice = input("Choose an option: ").strip()

        match choice:
            case "1":
                show_saved_cards(customer)

            case "2":
                remove_saved_card(customer)

            case "3":
                break

            case _:
                print("Invalid option")


def show_saved_cards(customer):
    print("""
===== Saved Cards =====
""")

    if not customer.my_cards:
        print("No saved cards found")
        return

    for index, card in enumerate(customer.my_cards, start=1):
        print(f"{index}. {mask_card_id(card.card_id)}")


def remove_saved_card(customer):
    while True:
        print("""
===== Remove Card =====
""")

        if not customer.my_cards:
            print("No saved cards found")
            return

        show_saved_cards(customer)

        card_id = input("Enter card id to remove or 0 to back: ").strip()

        if card_id == "0":
            print("Remove card cancelled")
            return

        if not card_id:
            print("Card id cannot be empty")
            continue

        if customer.remove_card(card_id):
            print("Card removed successfully")
            return

        print("Card not found")


def buy_ticket_menu(customer):
    while True:
        print(f"""
===== Buy Ticket =====
Current Wallet Balance: {customer.my_wallet}
""")

        ticket_price = input("Enter ticket price or 0 to back: ").strip()

        if ticket_price == "0":
            print("Buy ticket cancelled")
            return

        if not ticket_price:
            print("Ticket price cannot be empty")
            continue

        try:
            ticket_price = int(ticket_price)
        except ValueError:
            print("Ticket price must be a number")
            continue

        if ticket_price <= 0:
            print("Ticket price must be greater than 0")
            continue

        if customer.buy_ticket(ticket_price):
            print("Ticket purchased successfully")
            print(f"Remaining Balance: {customer.my_wallet}")
            return

        print("Not enough wallet balance")
        print("Please charge your wallet")


def mask_card_id(card_id):
    card_id = str(card_id)

    if len(card_id) <= 4:
        return card_id

    return "*" * (len(card_id) - 4) + card_id[-4:]


customer_auth_menu()
