from employee_cls import Employee , is_valid_email , is_valid_password ,check_email
employees = {}
def start_menu():
    while True:
        print("salam ! khosh oomadi :)")
        print("-"*24)
        print("1.Admin Panel")
        print("2.Train Employee Panel")
        print("3.Customer Panel")
        print("4.Exit")
        choice = input("koja beram ?: ")
        match choice:
            case "1":
                admin_login()
            case "2":
                pass
            case "3":
                pass
            case "4":
                print("Khodafez!")
                print("Rooze khoobi dashte bashid :)")
                break
            case _ :
                print("Lotfan ye adad beyn 1 ta 4 entekhab kon !!!")


def admin_login():
    admin_info = ("Admin_Train" , "Pass_Train")
    while True:
        print("0.Bazgasht")
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
                print("Dobare emtehan kon")

def admin_panel():
    while True:
        print("Khosh oomadi admin jan :)")
        print("-"*24)
        print("1.Insert Employee")
        print("2.Remove Employee")
        print("3.List of Employees")
        print("4.Exit")
        choice = input("koja beram ?: ")
        match choice:
            case "1":
                insert_employee()
            case "2":
                pass
            case "3":
                pass
            case "4":
                break
            case _:
                print("Lotfan ye adad beyn 1 ta 4 entekhab kon !!!")


def employee_validation(password, email, employees_dict):
    if is_valid_password(password) == False:
        print("Password bayad shamel hoorof , adad , @ ya & bashad !")
        return False

    if is_valid_email(email) == False:
        print("Format email eshtebah ast")
        return False

    if check_email(email, employees_dict) == True:
        print("Email ghablan sabt shode ! Yeki dige emtehan kon")
        return False

    return True



def insert_employee():
    while True:
        print("Ezafe kardane karmand")
        print("0.bazgasht")

        user_name = input("user name: ")
        if user_name == "0":
            return
        if user_name in employees :
            print("In username ghablan sabt shode ! Yeki dige emtehan kon")
            continue
        password = input("password: ")
        first_name = input("first name: ")
        last_name = input("last name: ")
        email = input("email: ")

        is_valid = employee_validation(password, email, employees)

        if is_valid == False:
            print("Moshkeli to etelaat hast ! Dobare ba deghat por konid")
            continue

        new_employee = Employee(user_name, password, first_name, last_name, email)
        employees[user_name] = new_employee
        print(f"Karmande {first_name} {last_name} ba movafaghiyat ezafe shod !")
        return