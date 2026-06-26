from employee_cls import Employee , is_valid_email , is_valid_password ,check_email
employees = {}
def start_menu():
    while True:
        print("Main Menu :)")
        print("-"*24)
        print("1.Admin Panel")
        print("2.Train Employee Panel")
        print("3.Customer Panel")
        print("4.Exit")
        choice = input("(1-4)?: ")
        match choice:
            case "1":
                admin_login()
            case "2":
                pass
            case "3":
                pass
            case "4":
                print("Bye")
                print("Have a nice day :) ")
                break
            case _ :
                print("Valid choice !!!")


def admin_login():
    admin_info = ("Admin_Train" , "Pass_Train")
    while True:
        print("Admin Login")
        print("-"*24)
        print("0.Return")
        user_name = input("user name: ")
        if user_name == "0":
            return
        else :
            password = input("password: ")
            is_logged_in = False
            if (user_name, password) == admin_info :
                print("login success")
                admin_panel()
                return
            else :
                print("login failed")
                print("Please try again")

def admin_panel():
    while True:
        print("Admin Panel")
        print("-"*24)
        print("1.Insert Employee")
        print("2.Remove Employee")
        print("3.List of Employees")
        print("4.Exit")
        choice = input("(1-4)?: ")
        match choice:
            case "1":
                insert_employee()
            case "2":
                remove_employee()
            case "3":
                list_of_employees()
            case "4":
                break
            case _:
                print("Invalid choice !!!")


def employee_validation(password, email, employees_dict):
    if is_valid_password(password) == False:
        print("Password must included alphabet , digit , @ or & !!!")
        return False

    if is_valid_email(email) == False:
        print("Email format is wrong !!!")
        return False

    if check_email(email, employees_dict) == True:
        print("Email has been already submitted ! try a different one")
        return False

    return True



def insert_employee():
    while True:
        print("Insert Employee")
        print("0.Return")

        user_name = input("user name: ")
        if user_name == "0":
            return
        if user_name in employees :
            print("User name has been already submitted ! try a different one")
            continue
        password = input("password: ")
        first_name = input("first name: ")
        last_name = input("last name: ")
        email = input("email: ")

        is_valid = employee_validation(password, email, employees)

        if is_valid == False:
            print("Valid info ! try again")
            continue

        new_employee = Employee(user_name, password, first_name, last_name, email)
        employees[user_name] = new_employee
        print(f"Employee {first_name} {last_name} inserted successfully !")
        return


def remove_employee():
    while True:
        print("Remove Employee")
        print("0.Return")

        user_name = input("user name: ")
        if user_name == "0":
            return
        if user_name in employees :
            employees.pop(user_name)
            print("User removed successfully !")
            return
        else :
            print("User not found !")
            continue

def list_of_employees():
    while True:
        if len(employees) == 0:
            print("Null List")
            return
        else :
            print("List of Employees :")
            for employee in employees.values() :
                print(f"username:{employee.username} | Name:{employee.first_name} {employee.last_name} | Email:{employee.email}")

            bazgasht = input("0.Return: ")
            if bazgasht == "0":
                return
            else :
                print("Please just enter 0 for return !")
                continue