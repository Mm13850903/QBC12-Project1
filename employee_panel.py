from employee import Employee
from line import Line
from train import Train
import re

#employees_list = []
lines_list = []
trains_list = []

def get_valid_time():
    while True:
        departure_time = input("Enter departure time (HH:MM): ")

        if re.fullmatch(r"([01]\d|2[0-3]):[0-5]\d", departure_time):
            return departure_time

        print("Invalid time format. Please enter time as HH:MM (example: 08:30)")

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

def login_employee(employees_list: list[Employee]):
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

    station_count = get_valid_number("Enter number of stations: ")
    if station_count == "exit":
        return
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

    if not lines_list:
        print("There are no lines to edit.")
        return

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
            count_input = get_valid_number("Enter new number of stations: ")
            if count_input == "exit" : return
            count_input = int(count_input)
            selected_line.station_count = int(count_input)
                
            new_stations_list = []
            for i in range(selected_line.station_count):
                s_name = input(f"Station {i+1} Name: ").strip()                    
                new_stations_list.append(s_name)
                
            selected_line.stations = new_stations_list
            print("Stations Updated!")

        case "6":
            return

def delete_line(lines_list):
    print("--- Delete Line (Type 'exit' to cancel) ---")

    if not lines_list:
        print("There are no lines to delete.")
        return

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

    stop_time = get_valid_number("Enter Stop Time: ")
    if stop_time == "exit" : return

    quality = get_valid_number("Enter Quality (1-5): ")
    if quality == "exit" : return

    price = get_valid_number("Enter Price: ")
    if price == "exit" : return

    capacity = get_valid_number("Enter Capacity: ")
    if capacity == "exit" : return

    departure_time = get_valid_time("Enter Departure Time: ")
    if departure_time == "exit": return

    distance = get_valid_number("Enter Distance to Station: ")
    if distance == "exit": return


    new_train = Train(train_id, name, selected_line.line_name, speed, stop_time, quality, price, capacity, departure_time, distance)
    collision_found = False
    for train in trains_list:
        if new_train.has_collision(train):
            collision_found = True
            break

    if collision_found:
        print("This train has a collision with another train on the same line!")
    else:
        trains_list.append(new_train)
        print(f"Train '{name}' added!")
           
def edit_train(trains_list, lines_list):
    print("--- Edit Train (Type 'exit' to cancel) ---")

    if not trains_list:
        print("The train list is empty.")
        return
    
    while True:
        target_id = input("Enter Train ID to update (or 'exit' to return): ").strip()
        if target_id.lower() == 'exit':
            return
        
        selected_train = next((t for t in trains_list if t.train_id == target_id), None)
        
        if selected_train:
            break
        else:
            print("No train found with this ID. Try again.")

    while True:
        print(f"--- Updating Train: {selected_train.name} (ID: {selected_train.train_id}) ---")
        print("1. Edit Train ID")
        print("2. Edit Name")
        print("3. Edit Line Name")
        print("4. Edit Speed")
        print("5. Edit Stop Time")
        print("6. Edit Quality")
        print("7. Edit Price")
        print("8. Edit Capacity")
        print("9. Edit Departure Time")
        print("10. Edit Distance")
        print("11. Exit")

        choice = input("What do you want to update? ").strip()

        match choice:
            case "1":
                new_id = input("Enter new train ID: ").strip()
                if new_id.lower() == "exit":
                    return

                if not new_id:
                    print("Train ID not changed (input was empty).")
                    continue

                id_exists = False
                for train in trains_list:
                    if train.train_id != selected_train.train_id and train.train_id == new_id:
                        id_exists = True
                        break

                if id_exists:
                    print(f"Error: '{new_id}' is already used by another train.")
                else:
                    selected_train.train_id = new_id
                    print("Train ID Updated!")

            case "2":
                new_name = input("Enter new name: ").strip()
                if new_name.lower() == "exit":
                    return

                if not new_name:
                    print("Name not changed (input was empty).")
                    continue

                name_exists = False
                for train in trains_list:
                    if train.train_id != selected_train.train_id and train.name.lower() == new_name.lower():
                        name_exists = True
                        break

                if name_exists:
                    print(f"Error: '{new_name}' is already taken by another train.")
                else:
                    selected_train.name = new_name
                    print("Name Updated!")

            case "3":
                if not lines_list:
                    print("No lines available.")
                    continue

                print("\nAvailable Lines:")
                for i, line in enumerate(lines_list, 1):
                    print(f"{i}. {line.name}")

                line_choice = input("Select new line number: ").strip()
                if line_choice.lower() == "exit":
                    return

                try:
                    line_index = int(line_choice) - 1
                    if 0 <= line_index < len(lines_list):
                        selected_train.line_name = lines_list[line_index].name
                        print("Line Name Updated!")
                    else:
                        print("Invalid line number.")
                except ValueError:
                    print("Please enter a valid number.")

            case "4":
                new_speed = get_valid_number(f"Enter new speed (current: {selected_train.speed}): ")
                if new_speed.lower() == "exit": return

                if new_speed == 0:
                    print("Speed must be greater than zero.")
                    return
                
                selected_train.speed = new_speed
                print("Speed Updated!")

            case "5":
                new_stop_time_str = input(f"Enter new stop time (current: {selected_train.stop_time}): ").strip()
                if new_stop_time_str.lower() == "exit":
                    return

                if not new_stop_time_str:
                    print("Stop time not changed (input was empty).")
                    continue

                try:
                    selected_train.stop_time = float(new_stop_time_str)
                    print("Stop Time Updated!")
                except ValueError as e:
                    print(f"Error: {e}")

            case "6":
                new_quality_str = input(f"Enter new quality (current: {selected_train.quality}): ").strip()
                if new_quality_str.lower() == "exit":
                    return

                if not new_quality_str:
                    print("Quality not changed (input was empty).")
                    continue

                try:
                    selected_train.quality = int(new_quality_str)
                    print("Quality Updated!")
                except ValueError as e:
                    print(f"Error: {e}")

            case "7":
                new_price_str = input(f"Enter new price (current: {selected_train.price}): ").strip()
                if new_price_str.lower() == "exit":
                    return

                if not new_price_str:
                    print("Price not changed (input was empty).")
                    continue

                try:
                    selected_train.price = float(new_price_str)
                    print("Price Updated!")
                except ValueError as e:
                    print(f"Error: {e}")

            case "8":
                new_capacity_str = input(f"Enter new capacity (current: {selected_train.capacity}): ").strip()
                if new_capacity_str.lower() == "exit":
                    return

                if not new_capacity_str:
                    print("Capacity not changed (input was empty).")
                    continue

                try:
                    selected_train.capacity = int(new_capacity_str)
                    print("Capacity Updated!")
                except ValueError as e:
                    print(f"Error: {e}")

            case "9":
                new_departure_time = get_valid_time("Enter new departure time: ")
                if new_departure_time == "exit":
                    continue

                old_departure_time = selected_train.departure_time
                selected_train.departure_time = new_departure_time

                collision_found = False
                for other_train in trains_list:
                    if other_train != selected_train and selected_train.has_collision(other_train):
                        collision_found = True
                        break

                if collision_found:
                    selected_train.departure_time = old_departure_time
                    print("This change causes a collision! Update cancelled.")
                else:
                    print("Departure time updated.")

            case "10":
                new_distance = get_valid_number("Enter new distance: ")
                if new_distance == "exit":
                    continue

                old_distance = selected_train.distance
                selected_train.distance = new_distance

                collision_found = False
                for other_train in trains_list:
                    if other_train != selected_train and selected_train.has_collision(other_train):
                        collision_found = True
                        break

                if collision_found:
                    selected_train.distance = old_distance
                    print("This change causes a collision! Update cancelled.")
                else:
                    print("Distance updated successfully.")

            case "11":
                print("Returning...")
                break

            case _:
                print("Invalid choice. Please try again.")

def delete_train(trains_list):
    print("--- Delete Train (Type 'exit' to cancel) ---")

    if not trains_list:
        print("The train list is empty. Nothing to delete.")
        return
    
    while True:
        target_id = input("Enter Train ID to delete (or type 'exit' to return): ")

        if target_id.lower() == "exit" : return

        selected_train = next((t for t in trains_list if t.train_id == target_id), None)

        if selected_train:
            trains_list.remove(selected_train)
            print(f"Train with ID '{target_id}' has been deleted successfully.")
        else:
            print(f"Error: No train found with ID '{target_id}'. Please try again.")
            continue

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
                edit_train(trains_list, lines_list)

            case "7":
                delete_train(trains_list, lines_list)

            case "8":
                print("--- Information Trains ---")

                if not trains_list:
                    print("No trains have been registered yet!")
                else:
                    print("--- Registered Trains ---")
                    for train in trains_list:
                        train.show_information()

                input("Press Enter to return to menu...")

            case "9":
                print("Exiting Employee Panel. Returning to the start menu...")
                break

            case _:
                print("Invalid choice. Please enter a number between 1 and 9.")
                input("Press Enter to continue...")

def get_all_trains_info(trains_list):
    trains_data = []

    for train in trains_list:
        train_dict = {
            "train_id": train.train_id,
            "name": train.name,
            "line_name": train.line_name,
            "speed": train.speed,
            "stop_time": train.stop_time,
            "quality": train.quality,
            "price": train.price,
            "capacity": train.capacity,
            "departure_time": train.departure_time,
            "distance": train.distance,
        }
        trains_data.append(train_dict)

    return trains_data