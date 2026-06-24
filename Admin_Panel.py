
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
                pass
            case "2":
                pass
            case "3":
                pass
            case "4":
                break
            case _:
                print("Lotfan ye adad beyn 1 ta 4 entekhab kon !!!")


start_menu()