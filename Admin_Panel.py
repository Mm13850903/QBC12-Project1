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
                pass
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
