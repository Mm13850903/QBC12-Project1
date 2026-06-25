from employee import Employee
from line import Line
from train import Train


employees_list = [Employee("karmand1", "Kd@1", "reza", "sam@email.com")]
lines_list = []
trains_list = []

def get_valid_number(prompt):
    while True:
        user_input = input(prompt).strip()
        if user_input.lower() == "exit": return user_input
        try:
            number = float(user_input)
            if number < 0:
                print("Number must not be negative, try again")
                continue
            return number
        except ValueError:
            print("Please enter only numbers!")

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
    print("--- Add New Line (Type 'exit' to cancel) ---")

    name = input("Enter Line Name: ").strip()
    if name.lower() == "exit": return
    
    for line in lines_list:
        if line.name == name:
            print(f"Error: Line '{name}' already exists!")
            return
    
    source = input("Enter Source: ").strip()
    if source.lower() == "exit": return

    destination = input("Enter Destination: ").strip()
    if destination.lower() == "exit": return

    station_count = input("Enter number of stations: ").strip()
    if station_count.lower() == "exit": return
    station_count = int(station_count)

    stations_names = []
    print(f"Please enter the names of {station_count} stations:")
    for i in range(station_count):
        s_name = input(f"Station {i+1} Name: ").strip()
        if s_name.lower() == "exit": return
        stations_names.append(s_name)

    
    new_line = Line(name, source, destination, station_count, stations_names)
    lines_list.append(new_line)

    print(f"Line '{name}' created successfully with {station_count} stations!")

def edit_line(lines_list):
    print("--- Edit Line (Type 'exit' to cancel) ---")

    selected_line = None

    while True:
        target_name = input("Enter the Line Name you want to edit (or 'exit' to back): ").strip()

        if target_name.lower() == "exit" : return
        
        for line in lines_list:
            if line.name == target_name:
                selected_line = line
                break

        if selected_line:
            selected_line.show_information()
            break
        else:
            print(f"Error: Line '{target_name}' not found. Please try again.")
    
    print("1. Edit Name")
    print("2. Edit Source")
    print("3. Edit Destination")
    print("4. Edit Station_count")
    print("5. Edit Stations")
    print("6. Back")

    choice = input("What do you want to update?")

    match choice:
        case "1":
            new_name = input("Enter new name: ").strip()
            if new_name.lower() == "exit": return

            name_exists = False
            for l in lines_list:
                if l.name == new_name:
                    name_exists = True
                    break
            
            if name_exists:
                print(f"Error: {new_name} is already taken!")
            else:
                selected_line.name = new_name
                print("Name Updated!")

        case "2":
            new_source = input("Enter new source: ").strip()
            if new_source.lower() == "exit": return
            selected_line.source = new_source
            print("Source Updated!")

        case "3":
            new_destination = input("Enter new destination: ").strip()
            if new_destination.lower() == "exit": return
            selected_line.destination = new_destination
            print("Destination Updated!")

        case "4" | "5":
            print("Updating stations information...")
            count_input = input("Enter new number of stations: ").strip()
            if count_input.isdigit():
                selected_line.station_count = int(count_input)
                
                new_stations_list = []
                for i in range(selected_line.station_count):
                    s_name = input(f"Station {i+1} Name: ").strip()
                    new_stations_list.append(s_name)
                
                selected_line.stations = new_stations_list
                print("Stations Updated!")
            else:
                print("Invalid number!")

        case "6":
            return

def delete_line(lines_list):
    print("--- Delete Line (Type 'exit' to cancel) ---")

    selected_line = None

    while True:
        line_name = input("Enter line name to delete: ").strip()

        if line_name.lower() == "exit": return

        for line in lines_list:
            if line.name == line_name:
                selected_line = line
                break

        if selected_line is None:
            print("Line not found! Please try again.")
            continue

        selected_line.show_information()
        lines_list.remove(selected_line)

        print("Line Deleted!")
        return

def add_train(trains_list, lines_list):
    print("--- Add New Train (Type 'exit' to cancel) ---")

    while True:
        train_id = input("Enter Train ID: ").strip()
        if train_id.lower() == "exit": return

        if any(t.train_id == train_id for t in trains_list):
            print("This ID already exists!")
            continue
        break
        
    if not lines_list:
        print("No lines available! Create a line first.")
        return
    
    print("Available Lines:")
    for i, line in enumerate(lines_list,1):
        print(f"{i} . {line.line_name}")

    line_choice = get_valid_number("Select Line Number (by index): ")
    if line_choice == "exit" : return
        
    try:
        selected_line = lines_list[int(line_choice) - 1]
    except (IndexError, ValueError):
        print("Invalid line selection!")
        return
    
    name = input("Enter Train Name: ").strip()
    if name.lower() == "exit" : return

    speed = get_valid_number("Enter Speed: ")
    if speed == "exit" : return

    stop_time = get_valid_number("Enter Speed: ")
    if stop_time == "exit" : return

    quality = get_valid_number("Enter Quality (1-5): ")
    if quality == "exit" : return

    price = get_valid_number("Enter Price: ")
    if price == "exit" : return

    capacity = get_valid_number("Enter Capacity: ")
    if capacity == "exit" : return

    new_train = Train(train_id, name, selected_line.line_name, speed, stop_time, quality, price, capacity)
    trains_list.append(new_train)
    print(f"Train '{name}' added!")
             

             


    
            


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
                edit_line(lines_list)

            case "3":
                delete_line(lines_list)

            case "4":
                print("--- Information Lines ---")

                if not lines_list:
                    print("No lines have been registered yet!")
                else:
                    print("--- Registered Railway Lines ---")
                    for line in lines_list:
                        line.show_information()

                input("Press Enter to return to menu...")

            case "5":
                if not lines_list:
                    print("No lines available! Please add a line first.")
                else:
                    add_train(trains_list, lines_list)

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







