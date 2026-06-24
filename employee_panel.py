from employee import Employee
from line import Line
from train import Train


employees_list = [Employee("karmand1", "Kd@1", "reza", "sam@email.com")]
lines_list = []
trains_list = []

def login_employee(employees_list):
    print("--- Employee Login ---")
    counter = 0

    while counter < 3:
        username = input("Username: ")
        password = input("Password: ")

        found_emp = None

        for emp in employees_list:
            if emp.username == username and emp.password == password :
                found_emp = emp
                break
        if found_emp:
            print(f"Welcome {found_emp.name}")
            return found_emp
        else:
            counter += 1
            remaining = 3 - counter
            if counter < 3:
                print(f"Error: Incorrect username or password. {remaining} attempts left. Please try again.")
            else:
                print("Error: Your account has been temporarily blocked due to 3 failed attempts.")
                return None

def add_line(lines_list):
    print("--- Add New Line ---")

    name = input("Enter Line Name: ").strip()
    for line in lines_list:
        if line.name == name:
            print(f"Error: Line '{name}' already exists!")
            return
    
    source = input("Enter Source: ").strip()

    destination = input("Enter Destination: ").strip()

    station_count = int(input("Enter number of stations: ").strip())

    stations_names = []
    print(f"Please enter the names of {station_count} stations:")
    for i in range(stations_names):
         s_name = input(f"Station {i+1} Name: ").strip()
         stations_names.append(s_name)

    
    new_line = Line(name, source, destination, station_count, stations_names)
    lines_list.append(new_line)

    print(f"Line '{name}' created successfully with {station_count} stations!")


def display_employee_panel(current_employee):
    while True:

        print("1.Add line")
        print("2.Update one line information")
        print("3.Delete line")
        print("4.View line list")
        print("5.Add a train")
        print("6.Update information about a train")
        print("7.Delete the train")
        print("8.View train list")
        print("9.Log out of account")

        choice = input("Please select an option (1-9):")

        match choice:
            case "1":
                  add_line(lines_list)

                  
            case "2":

                            while True:
                                nema = input("Kodam Khat baray update mikhay")
                                if name.lower() == 'back':
                                    break

                                temp = None
                                for line in lines_list:
                                    if line.name == name:
                                        temp = line
                                        break

                                if temp is None:
                                    print("Error: In khat mojood nist!")
                                    print("try again")
                                    continue

                                print(f"Khat yaft shod! :)) ---> Name: {temp.name} || Mabda: {temp.source} || Maghsad: {temp.destination} || Tedad Istgah-ha: {temp.station_count}")
                                print("1. Edit Name Khat")
                                print("2. Edit Mabda")
                                print("3. Edit Maghsad")
                                print("4. Edit Tedad Va Name Istgah-Ha")

                                temp1 = input("Enter yout choice: ")

                                if temp1 =="1":
                                    new_name = input("Name Jadide Khat : ")
                                    duplicate = False
                                    for line in lines_list:
                                        if line.name == new_name and line != temp:
                                            duplicate = True
                                            break
                                    if duplicate:
                                        print("Error: Name Jadide Khat Tekrari Hast Va Baraye Khati Diger Sabt Shodeh ast!")


                                    else:
                                        for train in trains_list:
                                            if train.line_name == temp.name:
                                                train.line_name = new_name
                                        temp.name = new_name
                                        print("Name Khat Ba Mofaghiat Update Shod")

                                elif temp1 =="2":
                                    temp.source = input("Mabda jadid: ")
                                    print("Mabda Ba Mofaghiat Update Shod")

                                elif temp1 == "3":
                                    temp.destination = input("Maghsad jadid: ")
                                    print("Maghsad Ba Mofaghiat Update Shod.")

                                elif temp1 == "4":
                                    new_count = input("Tedad Istgah hay Jadid: ")
                                    if new_count.isdigit():
                                        new_count = int(new_count)
                                        temp.station_count = new_count

                                    new_stations = []
                                    for i in range(new_count):
                                        station_name = input(f"Name Istgah {i + 1}: ")
                                        new_stations.append(station_name)
                                    temp.stations = new_stations

                                    print("Tedad Va List Istgah-ha Ba Mofaghiat Update Shod.")
                                else:

                                    print("Error: Tedad istgah bayad int bashad!")
                                break

            case "3":
                            while True:
                                name = input("Name Khat Baraye Hazf: ")

                                temp = None
                                for line in lines_list:
                                    if line.name == name:
                                        temp = line
                                        break

                                if temp is None:
                                    print("Error : In Khat mojood nist! :((")
                                    continue

                                lines_list.remove(temp)
                                print("line Ba Mofaghiat Remove Shod")

                                break
            case "4":

                            print(" List Khatoot Sabt Shodeh ")
                            if len(lines_list) == 0:
                                print("Hich khati sabt nashodeh ast.")
                            for line in lines_list:
                                res = ""
                                for station in line.stations:
                                    res += station + " ---->> "
                                print(
                                    f"Khat: {line.name} | Masir: {line.source} be {line.destination} | Istgah-ha: {res} End")
                            input("Baraye bazgasht Enter bezanid...")
            case "5":

                            while True:
                                print("Baray bazgasht type <bach> please ")
                                train_id = input("ID Ghatar :")
                                if train_id.islower() == "back":
                                    break

                                duplicate = False
                                for t in trains_list:
                                    if t.train_id == train_id:
                                        duplicate = True
                                        break

                                if duplicate:
                                    print("Error: ID Ghatar tekrari Hast!")
                                    continue

                                line_name = input("Name Khat Baray Harkat: ")

                                line_exists = False
                                for line in lines_list:
                                    if line.name == line_name:
                                        line_exists = True
                                        break

                                if line_exists == False:
                                    print("Error: IN Khat Mojood Nist ya Hazf Shodeh ast :))" )

                                name = input("Name Ghatar: ")
                                speed = input("Sorat Motevasset: ")
                                stop_time = input("Mizan Tavaghof Dar Har Istgah : ")
                                quality = input("Darajeh Keifiat: ")
                                price = input("Hazineh Belit: ")
                                capacity = input("Zarfiat: ")

                                if speed.isdigit():
                                    speed = int(speed)
                                if stop_time.isdigit():
                                    stop_time = int(stop_time)
                                if price.isdigit():
                                    price = int(price)
                                if capacity.isdigit():
                                    capacity = int(capacity)

                                new_train = Train.Train(train_id, name, speed, stop_time, quality, price, capacity)
                                trains_list.append(new_train)
                                print("Ghatar ba Mofaghiat ezafeh Shod :))")
                                break
            case "6":

                            while True:
                                train_id = input("ID Ghatar Baraye update: ")
                                if train_id.lower() == 'back':
                                        break

                                found_train = None
                                for t in trains_list:
                                    if t.train_id == train_id:
                                        found_train = t
                                        break

                                if found_train is None:
                                    print("Error: Ghatar ba in ID mojood nist!")
                                    continue

                                print(f"Ghatar yaft shod! --->> ID: {found_train.train_id} || Name: {found_train.name} || Khat: {found_train.line_name}")
                                print("1. Edit ID Ghatar")
                                print("2. Edit Name Ghatar")
                                print("3. Edit Khat Harakat ")
                                print("4. Edit Sorat Motevasset")
                                print("5. Edit Mizan Tavaghof Dar Istgah")
                                print("6. Edit Darajeh Keifiat")
                                print("7. Edit Hazineh Belit")
                                print("8. Edit Zarfiat")
                                print(24 * "-")

                                ch = input("Enter your choice (1-8): ")

                                if ch == "1":
                                    new_id = input("ID jadide ghatar ra vared konid: ")
                                    duplicate = False
                                    for t in trains_list:
                                        if t.train_id == new_id and t != found_train:
                                            duplicate = True
                                            break
                                    if duplicate:
                                        print("Error: In ID ghablan baraye ghatari diger sabt shodeh ast!")
                                    else:
                                        found_train.train_id = new_id
                                        print("ID ghatar ba mofaghaghiat update shod.")


                                elif ch == "2":
                                    found_train.name = input("Name jadid: ")
                                    print("Name ghatar ba mofaghaghiat update shod.")


                                elif ch == "3":
                                    new_line_name = input("Name Khat Harakat jadid: ")
                                    line_exists = False
                                    for line in lines_list:
                                        if line.name == new_line_name:
                                            line_exists = True
                                            break
                                    if not line_exists:
                                        print("Error: In khat mojood nist! Avval bayad khat ra besazid.")
                                    else:
                                        found_train.line_name = new_line_name
                                        print("Khat harakat ghatar ba mofaghaghiat update shod.")


                                elif ch == "4":
                                    speed = input("Sorat Motevasset jadid: ")
                                    if speed.isdigit():
                                        found_train.speed = int(speed)
                                        print("Sorat ba mofaghaghiat update shod.")
                                    else:
                                        print("Error: Sorat bayad adad bashad!")


                                elif ch == "5":
                                    stop_time = input("Mizan Tavaghof jadid (Daghigheh): ")
                                    if stop_time.isdigit():
                                        found_train.stop_time = int(stop_time)
                                        print("Mizan tavaghof ba mofaghaghiat update shod.")
                                    else:
                                        print("Error: Zaman tavaghof bayad adad bashad!")


                                elif ch == "6":
                                    found_train.quality = input("Darajeh Keifiat jadid: ")
                                    print("Darajeh keifiat ba mofaghaghiat update shod.")


                                elif ch == "7":
                                    price = input("Hazineh Belit jadid: ")
                                    if price.isdigit():
                                        found_train.price = int(price)
                                        print("Hazineh belit ba mofaghaghiat update shod.")
                                    else:
                                        print("Error: Hazineh belit bayad adad bashad!")


                                elif ch == "8":
                                    capacity = input("Zarfiat jadid: ")
                                    if capacity.isdigit():
                                        found_train.capacity = int(capacity)
                                        print("Zarfiat ba mofaghaghiat update shod.")
                                    else:
                                        print("Error: Zarfiat bayad adad bashad!")
                                break
            case "7":

                            while True:
                                train_id = input("ID Ghatar Baray Hazf")
                                if train_id.islower() == "back":
                                    break

                                found_train = None
                                for t in trains_list:
                                    if t.train_id == train_id:
                                        found_train = t
                                        break

                                if found_train is None:
                                    print("Error: Ghatar ba in ID mojood nist! :((")
                                    continue

                                trains_list.remove(found_train)
                                print("Ghatar Ba Mofaghiat Remove Shod :))")
                                break
            case "8":
                            print("List Ghatar hay Sabt Shodeh ")
                            if len(trains_list) == 0:
                                print("Hich Ghatari sabt nashodeh ast")

                            for t in trains_list:
                                print(f"ID: {t.train_id} || Name: {t.name} || Khat: {t.line_name} || Keifiat: {t.quality} || Gheymat: {t.price} || Zarfiat: {t.capacity}")
                                input("Baraye bazgasht Enter bezanid...")

            case "9":
                            print("Khorooj az Panel Karmand")
                            break
                    break


            case _ :
                    count +=1
                    if count >= 3:
                        print("Az Kol Shans Hat Estefadeh Kardi!")
                        input("Baraye bazgasht Enter bezanid...")
                        break
                    print("Error: Username Ya Password eshtebah hast ")
                    print(f" Shoma {3-count} bar dige forsat darid")
                    print("Please Try again")







