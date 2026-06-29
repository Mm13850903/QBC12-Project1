import re

from card import Card
from BANK import API
from train import Train
from employee_panel import get_all_trains_info, trains_list


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
        self.transactions = []

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
        self.add_transaction(
            transaction_type="wallet_charge",
            amount=value,
            description="Wallet charged with saved card",
            payment_id=payment_id
        )
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
        self.add_transaction(
            transaction_type="wallet_charge",
            amount=value,
            description="Wallet charged with new card",
            payment_id=payment_id
        )
        if card not in self.my_cards:
            self.my_cards.append(card)
        return payment_id

    @login_required
    def buy_ticket(self, train):
        if train is None:
            return False
        ticket_price = train.price
        if ticket_price <= 0:
            return False
        if self.my_wallet < ticket_price:
            return False
        if not train.get_a_passenger():
            return "full"
        self.__my_wallet -= ticket_price
        self.add_transaction(
            transaction_type="ticket_purchase",
            amount=ticket_price,
            description=f"Ticket purchased for train {train.train_id}"
        )
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

    def add_transaction(self, transaction_type, amount, description, payment_id=None):
        transaction = {
            "type": transaction_type,
            "amount": amount,
            "description": description,
            "payment_id": payment_id,
            "wallet_balance": self.my_wallet
        }
        self.transactions.append(transaction)
        return transaction

    @login_required
    def view_transactions(self):
        if not self.transactions:
            return "No transactions found"
        result = "===== Transactions =====\n"
        for index, transaction in enumerate(self.transactions, start=1):
            result += f"""
    Transaction {index}
    Type: {transaction["type"]}
    Amount: {transaction["amount"]}
    Description: {transaction["description"]}
    Payment ID: {transaction["payment_id"]}
    Wallet Balance: {transaction["wallet_balance"]}
    """
        return result


def export_trains_to_txt(trains):
    if not trains:
        return False
    with open("trains_list.txt", "w", encoding="utf-8") as file:
        file.write("===== Trains List =====\n\n")
        for index, train in enumerate(trains, start=1):
            available_seats = train.capacity - train.booked_seats
            file.write(f"----- Train {index} -----\n")
            file.write(f"Ticket ID: {train.train_id}\n")
            file.write(f"Name: {train.name}\n")
            file.write(f"Line: {train.line_name}\n")
            file.write(f"Departure Time: {train.departure_time}\n")
            file.write(f"Price: {train.price}\n")
            file.write(f"Capacity: {train.capacity}\n")
            file.write(f"Booked Seats: {train.booked_seats}\n")
            file.write(f"Available Seats: {available_seats}\n")
            file.write("-" * 30 + "\n\n")
    return True


def export_transactions_to_txt(customer):
    if not customer.transactions:
        return False
    file_name = f"{customer.username}_transactions.txt"
    with open(file_name, "w", encoding="utf-8") as file:
        file.write("===== Customer Transactions =====\n\n")
        file.write(f"Username: {customer.username}\n")
        file.write(f"Name: {customer.name}\n")
        file.write(f"Current Wallet Balance: {customer.my_wallet}\n")
        file.write("=" * 40 + "\n\n")
        for index, transaction in enumerate(customer.transactions, start=1):
            file.write(f"Transaction {index}\n")
            file.write(f"Type: {transaction['type']}\n")
            file.write(f"Amount: {transaction['amount']}\n")
            file.write(f"Description: {transaction['description']}\n")
            file.write(f"Payment ID: {transaction['payment_id']}\n")
            file.write(f"Wallet Balance: {transaction['wallet_balance']}\n")
            file.write("-" * 30 + "\n\n")

    return file_name


def export_ticket_to_txt(customer, train):
    file_name = f"ticket_{customer.username}_{train.train_id}.txt"
    with open(file_name, "w", encoding="utf-8") as file:
        file.write("===== Train Ticket =====\n\n")
        file.write(f"Passenger Username: {customer.username}\n")
        file.write(f"Passenger Name: {customer.name}\n")
        file.write("-" * 30 + "\n")
        file.write(f"Ticket ID: {train.train_id}\n")
        file.write(f"Train Name: {train.name}\n")
        file.write(f"Line: {train.line_name}\n")
        file.write(f"Departure Time: {train.departure_time}\n")
        file.write(f"Ticket Price: {train.price}\n")
        file.write("-" * 30 + "\n")
        file.write(f"Remaining Wallet Balance: {customer.my_wallet}\n")
        file.write(f"Available Seats After Purchase: {train.capacity - train.booked_seats}\n")

    return file_name


def transactions_menu(customer):
    while True:
        print("""
===== Transactions Menu =====
1. View Transactions
2. Export Transactions To TXT
3. Back
""")

        choice = input("Choose an option: ").strip()
        match choice:
            case "1":
                print(customer.view_transactions())
            case "2":
                file_name = export_transactions_to_txt(customer)
                if file_name:
                    print(f"Transactions exported successfully to {file_name}")
                else:
                    print("No transactions found")
            case "3":
                break
            case _:
                print("Invalid option")


def main_menu():
    while True:
        print("""
===== Main Menu =====
1. Customer Menu
2. Card Management
3. Exit
""")

        choice = input("Choose an option: ").strip()

        match choice:
            case "1":
                customer_auth_menu()

            case "2":
                card_management_menu()

            case "3":
                print("Goodbye")
                break

            case _:
                print("Invalid option")


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
6. Transactions
7. Logout
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
                print(customer.view_transactions())
            case "7":
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
            exp_month = int(exp_month)
            exp_year = int(exp_year)
            value = int(value)
        except ValueError:
            print("Exp month, exp year and amount must be numbers")
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

        if not trains_list:
            print("No trains available")
            return

        print("===== Available Trains =====")

        for index, train in enumerate(trains_list, start=1):
            available_seats = train.capacity - train.booked_seats

            print(f"""
----- Train {index} -----
Ticket ID: {train.train_id}
Name: {train.name}
Line: {train.line_name}
Departure Time: {train.departure_time}
Price: {train.price}
Capacity: {train.capacity}
Booked Seats: {train.booked_seats}
Available Seats: {available_seats}
""")

        print("""
1. Buy Ticket
2. Export Trains List To TXT
3. Back
""")

        choice = input("Choose an option: ").strip()

        match choice:
            case "1":
                ticket_id = input("Enter ticket id or 0 to back: ").strip()
                if ticket_id == "0":
                    print("Buy ticket cancelled")
                    continue
                if not ticket_id:
                    print("Ticket ID cannot be empty")
                    continue
                selected_train = None
                for train in trains_list:
                    if str(train.train_id) == str(ticket_id):
                        selected_train = train
                        break
                if selected_train is None:
                    print("Train not found")
                    continue
                available_seats = selected_train.capacity - selected_train.booked_seats
                if available_seats <= 0:
                    print("Train capacity is full")
                    continue
                if customer.my_wallet < selected_train.price:
                    print("Not enough wallet balance")
                    print("Please charge your wallet")
                    continue
                result = customer.buy_ticket(selected_train)
                if result == "full":
                    print("Train capacity is full")
                    continue
                if result:
                    print("Ticket purchased successfully")
                    print(f"Train ID: {selected_train.train_id}")
                    print(f"Train Name: {selected_train.name}")
                    print(f"Remaining Balance: {customer.my_wallet}")
                    print(f"Available Seats: {selected_train.capacity - selected_train.booked_seats}")
                    export_choice = input("Do you want to export this ticket to TXT? (y/n): ").strip().lower()
                    if export_choice == "y":
                        file_name = export_ticket_to_txt(customer, selected_train)
                        print(f"Ticket exported successfully to {file_name}")
                    return
                print("Ticket purchase failed")
            case "2":
                if export_trains_to_txt(trains_list):
                    print("Trains list exported successfully to trains_list.txt")
                else:
                    print("No trains available")
            case "3":
                return

            case _:
                print("Invalid option")


def card_management_menu():
    while True:
        print("""
===== Card Management =====
1. Create Card
2. Deposit To Card
3. View All Cards
4. Back
""")

        choice = input("Choose an option: ").strip()

        match choice:
            case "1":
                create_card_menu()

            case "2":
                deposit_to_card_menu()

            case "3":
                view_all_cards()

            case "4":
                break

            case _:
                print("Invalid option")


def create_card_menu():
    while True:
        print("""
===== Create Card =====
""")

        name = input("Enter card holder name or 0 to back: ").strip()
        if name == "0":
            print("Create card cancelled")
            return
        if not name:
            print("Name cannot be empty")
            continue

        exp_month = input("Enter exp month or 0 to back: ").strip()
        if exp_month == "0":
            print("Create card cancelled")
            return
        if not exp_month:
            print("Exp month cannot be empty")
            continue

        exp_year = input("Enter exp year or 0 to back: ").strip()
        if exp_year == "0":
            print("Create card cancelled")
            return
        if not exp_year:
            print("Exp year cannot be empty")
            continue

        password = input("Enter card password or 0 to back: ")
        if password == "0":
            print("Create card cancelled")
            return
        if not password:
            print("Card password cannot be empty")
            continue

        balance = input("Enter initial balance or 0 to back: ").strip()
        if balance == "0":
            print("Create card cancelled")
            return
        if not balance:
            print("Initial balance cannot be empty")
            continue

        try:
            balance = int(balance)
        except ValueError:
            print("Initial balance must be a number")
            continue

        if balance < 0:
            print("Initial balance cannot be negative")
            continue

        try:
            card = Card.create_card(name, exp_month, exp_year, password, balance)
            print("Card created successfully")
            print()
            print(card)
            return

        except ValueError as error:
            print(error)
            continue


def deposit_to_card_menu():
    while True:
        print("""
===== Deposit To Card =====
""")

        if not Card.card_list:
            print("No cards found")
            return

        view_all_cards()

        card_id = input("Enter card id or 0 to back: ").strip()
        if card_id == "0":
            print("Deposit cancelled")
            return
        if not card_id:
            print("Card id cannot be empty")
            continue

        card = Card.find_card(card_id)

        if card is None:
            print("Card not found")
            continue

        amount = input("Enter amount or 0 to back: ").strip()
        if amount == "0":
            print("Deposit cancelled")
            return
        if not amount:
            print("Amount cannot be empty")
            continue

        try:
            amount = int(amount)
        except ValueError:
            print("Amount must be a number")
            continue

        if amount <= 0:
            print("Amount must be greater than 0")
            continue

        if card.deposit(amount):
            print("Deposit successful")
            print(f"New Card Balance: {card.balance}")
            return

        print("Deposit failed")


def view_all_cards():
    print("""
===== All Cards =====
""")

    if not Card.card_list:
        print("No cards found")
        return

    for index, card in enumerate(Card.card_list, start=1):
        print(f"----- Card {index} -----")
        print(card)
        print()


def mask_card_id(card_id):
    card_id = str(card_id)
    return "*" * (len(card_id) - 4) + card_id[-4:]


main_menu()
