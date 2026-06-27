from classes import Employee, is_valid_email, is_valid_password, check_email

def Main_menu():
    while True:
        print("Welcome to Quera railway")
        print("1.Admin panel")
        print("2.Train employee panel")
        print("3.Customer panel")
        print("4.Exit railway!\n")
        choice = input("Please enter 1-4 to continue:\n")
        if choice == "1":
            Admin_login()
        elif choice == "2":
            pass
        elif choice == "3":
            pass
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Wrong input! Please try again.\n")

employee_list = {}
def employee_validation(password, email, employees_list):
    
    if is_valid_password(password) == False:
        print("Password must include alphabet, numbers, @ or &!")
        return False
    
    if is_valid_email(email) == False:
        print("Email format is incorrect!")
        return False
    
    if check_email(email, employees_list) == True:
        print("This Email is already submitted, try another one!")
        return False
    
    return True


def add_employee():
    while True:
        username = input("Please enter a username for new employee, Or enter 0 to return to admin panel:")
        if username == "0":
            return
        if username in  employee_list:
            print("This username already belonge to a crew member.Try another one")
            continue
        password = input("Please enter a password for the new employee:")
        first_name = input("Please enter employee's first name:")
        last_name = input("Please enter employee's last name:")
        email = input("Please enter employee's Email:")
        is_valid = employee_validation(password, email, employee_list)
        if is_valid == False:
            print("Youre information isn't valid! Try again.")
            continue
        new_employee = Employee(username, password, first_name, last_name, email)
        employee_list[username] = new_employee
        print(f"{first_name} {last_name} is now a Quera railway employee")
        return

def remove_employee():
    pass

def Admin_panel():
    while True:
        print("1.Add an employee to railway system")
        print("2.Remove an employee from railway system")
        print("3.See all employees")
        print("4.Return to main menu\n")
        choice = input("Please enter 1-4 to continue:\n")
        match choice:
            case "1":
                add_employee()
            case "2":
                pass
            case "3":
                pass
            case "4":
                return

def Admin_login():
    admin_essentials = ("Username", "Password")
    count = 0
    while True:
        username = input("Please enter your username, Or enter 0 to exit to main menu:\n")
        if username == "0":
            break
        else:
            password = input("Please enter your password:\n")
            if (username, password) == admin_essentials:
                print("You've logged in successfuly")
                print("Welcome to admin panel.")
                Admin_panel() #goes to admin panel
                return
            else :
                count += 1
                print("username or password is incorrect.")
                print (f"you have {3-count} chances left.\n")
                if count >= 3:
                    break





Main_menu()