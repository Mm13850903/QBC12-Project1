from classes import staff

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


def Admin_panel():
    while True:
        print("1.Add an employee to railway system")
        print("2.Remove an employee from railway system")
        print("3.See all employees")
        print("4.Return to main menu\n")
        choice = input("Please enter 1-4 to continue:")
        match choice:
            case "1":
                #fname = input("Employee's first name:")
                #lname = input("Employee's last name:")
                #email = input("Employee's email:")
                #username = input("Please enter :")
                pass
            case "2":
                pass
            case "3":
                pass
            case "4":
                return

def Admin_login():
    admin_essentials = ("Admin_Train", "Pass_train")
    while True:
        username = input("Please enter your username, Or enter 0 to exit to main menu:\n")
        if username == "0":
            break
        else:
            password = input("Please enter your password:")
            if (username, password) == admin_essentials:
                print("You've logged in successfuly")
                print("Welcome to admin panel.")
                Admin_panel()
                return
            else :
                print("username or password is incorrect.")



Main_menu()