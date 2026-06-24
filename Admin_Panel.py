
def start_menu():
    while True:
        print("salam ! khosh oomadi :)")
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
    admin_list = {"Admin_Train" : "Pass_Train"}
    while True:
        print("1.Bazgasht")
        user_name = input("user name: ")
        if user_name == "1":
            return
        else :
            password = input("password: ")
            is_logged_in = False
            for k , v in admin_list.items():
                if k == user_name and v == password:
                    is_logged_in = True
                    break
            if is_logged_in :
                print("login success")
                admin_panel()
                return
            else :
                print("login failed")
                print("Dobare emtehan kon")

def admin_panel():
    print("welcome to admin panel")
    input() #place holder

