from employee import Employee
from line import Line
from train import Train
import re


def print_header(title):
    print("\n" + f" {title} ".center(40, "="))
    print()


def print_separator():
    print("=" * 40 + "\n")


# employees_list = []
lines_list = []
trains_list = []


def get_valid_time(prompt="Enter departure time (HH:MM): "):
    while True:
        departure_time = input(prompt).strip()
        if departure_time.lower() == "exit":
            return "exit"
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
            if emp.username == username and emp.password == password:
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
    print_header("Add New Line (Type 'exit' to cancel)")
    count = 0
    while count < 3:
        name = input("Enter Line Name: ").strip()
        if name.lower() == "exit":
            return

        if name == "":
            count += 1
            print("Error: Line name cannot be empty")
            print(f"{3 - count} attempts left.")
            print("Please try again")
            continue

        if any(line.name.lower() == name.lower() for line in lines_list):
            count += 1
            print(f"Error: Line '{name}' already exists")
            print(f"{3 - count} attempts left.")
            print("Please try again")
            continue

        source = input("Enter Source: ").strip()
        if source.lower() == "exit": return

        destination = input("Enter Destination: ").strip()
        if destination.lower() == "exit": return

        while destination.lower() == source.lower():

            if destination.lower() == "exit":
                return
            print("Error: Destination cannot be the same as Source.")
            print("If your source and destination are the same, don't you feel like it's better to travel with Snap ?")
            destination = input("Please enter a different destination: ")

        station_count = get_valid_number("Enter number of stations: ")
        if station_count == "exit":
            return

        station_count = int(station_count)
        stations_names = []

        print(f"Please enter the names of {station_count} stations:")
        for i in range(station_count):
            while True:
                s_name = input(f"Station {i + 1} Name: ").strip()
                if s_name.lower() == "exit":
                    return
                if s_name == "":
                    print("Error: Station name cannot be empty.")
                    print("Please try again.")
                else:
                    stations_names.append(s_name)
                    break

        new_line = Line(name, source, destination, station_count, stations_names)
        lines_list.append(new_line)

        print(f"Line '{name}' created successfully with {station_count} stations!")
        return

    print("Error: Your account has been temporarily blocked due to 3 failed attempts")
    print("Returning to previous menu")
    return


def edit_line(lines_list):
    print_header("Edit Line (Type 'exit' to cancel)")

    if not lines_list:
        print("There are no lines to edit.")
        return

    selected_line = None

    count = 0
    while count < 3:
        target_name = input("Enter the Line Name you want to edit (or 'exit' to back): ").strip()
        if target_name.lower() == "exit": return

        if not target_name:
            count += 1
            remaining = 3 - count
            print("Error: Line name cannot be empty.")
            print(f"{remaining} attempts left.")
            print("Please try again.")
            continue

        for line in lines_list:
            if line.name == target_name:
                selected_line = line
                break

        if selected_line:
            selected_line.show_information()
            break
        else:
            count += 1
            remaining = 3 - count
            print(f"Error: Line '{target_name}' not found.")
            print(f"{remaining} attempts left.")
            print("Please try again.")
    else:
        print("Error: Your account has been temporarily blocked due to 3 failed attempts.")
        print("Returning to previous menu.")
        return

    print("\n1. Edit Name")
    print("2. Edit Source")
    print("3. Edit Destination")
    print("4. Edit Station_count")
    print("5. Edit Stations")
    print("6. Back")

    choice = input("What do you want to update? ").strip()

    match choice:
        case "1":
            count = 0
            while count < 3:
                new_name = input("Enter new name: ").strip()
                if new_name.lower() == "exit": return

                if not new_name:
                    count += 1
                    remaining = 3 - count
                    print("Error: Name cannot be empty.")
                    print(f"{remaining} attempts left.")
                    print("Please try again.")
                    continue

                name_exists = False
                for l in lines_list:
                    if l.name == new_name:
                        name_exists = True
                        break

                if name_exists:
                    count += 1
                    remaining = 3 - count
                    print(f"Error: '{new_name}' is already taken!")
                    print(f"{remaining} attempts left.")
                    print("Please try again.")
                else:
                    selected_line.name = new_name
                    print("Name Updated successfully!")
                    break
            else:
                print("Error: Your account has been temporarily blocked due to 3 failed attempts.")
                return

        case "2":
            count = 0
            while count < 3:
                new_source = input("Enter new source: ").strip()
                if new_source.lower() == "exit": return

                if not new_source:
                    count += 1
                    remaining = 3 - count
                    print("Error: Source cannot be empty.")
                    print(f"{remaining} attempts left.")
                    print("Please try again.")
                else:
                    selected_line.source = new_source
                    print("Source Updated successfully!")
                    break
            else:
                print("Error: Your account has been temporarily blocked due to 3 failed attempts.")
                return

        case "3":
            count = 0
            while count < 3:
                new_destination = input("Enter new destination: ").strip()
                if new_destination.lower() == "exit": return

                if not new_destination:
                    count += 1
                    remaining = 3 - count
                    print("Error: Destination cannot be empty.")
                    print(f"{remaining} attempts left.")
                    print("Please try again.")
                else:
                    selected_line.destination = new_destination
                    print("Destination Updated successfully!")
                    break
            else:
                print("Error: Your account has been temporarily blocked due to 3 failed attempts.")
                return

        case "4" | "5":
            print("Updating stations information...")
            count = 0
            while count < 3:
                count_input = get_valid_number("Enter new number of stations: ")
                if count_input == "exit": return

                if count_input is None or int(count_input) <= 0:
                    count += 1
                    remaining = 3 - count
                    print("Error: Invalid number of stations.")
                    print(f"{remaining} attempts left.")
                    print("Please try again.")
                else:
                    station_count = int(count_input)
                    selected_line.station_count = station_count
                    break
            else:
                print("Error: Your account has been temporarily blocked due to 3 failed attempts.")
                return

            new_stations_list = []
            for i in range(selected_line.station_count):
                count = 0
                while count < 3:
                    s_name = input(f"Station {i + 1} Name: ").strip()
                    if s_name.lower() == "exit": return

                    if not s_name:
                        count += 1
                        remaining = 3 - count
                        print("Error: Station name cannot be empty.")
                        print(f"{remaining} attempts left.")
                        print("Please try again.")
                    else:
                        new_stations_list.append(s_name)
                        break
                else:
                    print("Error: Your account has been temporarily blocked due to 3 failed attempts.")
                    return

            selected_line.stations = new_stations_list
            print("Stations Updated successfully!")

        case "6":
            return

        case _:
            print("Invalid choice! Returning to menu.")


def delete_line(lines_list):
    print_header("Delete Line (Type 'exit' to cancel)")

    if not lines_list:
        print("There are no lines to delete.")
        return

    count = 0
    while count < 3:
        line_name = input("Enter line name to delete: ").strip()
        if line_name.lower() == "exit": return

        if not line_name:
            count += 1
            remaining = 3 - count
            print("Error: Line name cannot be empty.")
            print(f"{remaining} attempts left.")
            print("Please try again.")
            continue

        selection_line = None
        for line in lines_list:
            if line.name == line_name:
                selection_line = line
                break

        if selection_line:
            selection_line.show_information()
            lines_list.remove(selection_line)
            print("Line Deleted Successfully!")
            break
        else:
            count += 1
            remaining = 3 - count
            print(f"Error: Line '{line_name}' not found.")
            print(f"{remaining} attempts left.")
            print("Please try again.")
    else:
        print("Error: Your account has been temporarily blocked due to 3 failed attempts.")
        print("Returning to menu.")
        return


def add_train(trains_list, lines_list):
    print_header("Add New Train (Type 'exit' to cancel)")

    count = 0
    while count < 3:
        train_id = input("Enter Train ID: ").strip()
        if train_id.lower() == "exit": return

        if not train_id:
            count += 1
            remaining = 3 - count
            print("Error: Train ID cannot be empty.")
            print(f"{remaining} attempts left.")
            print("Please try again.")
            continue

        is_duplicate = False
        for t in trains_list:
            if t.train_id == train_id:
                is_duplicate = True
                break

        if is_duplicate:
            count += 1
            remaining = 3 - count
            print("Error: This ID already exists!")
            print(f"{remaining} attempts left.")
            print("Please try again.")
        else:
            break
    else:
        print("Error: Your account has been temporarily blocked due to 3 failed attempts.")
        print("Returning to previous menu.")
        return

    if not lines_list:
        print("No lines available! Create a line first.")
        return

    print("Available Lines:")
    for i, line in enumerate(lines_list, 1):
        print(f"{i}. {line.name}")

    count = 0
    while count < 3:
        line_choice = get_valid_number("Select Line Number (by index): ")
        if line_choice == "exit": return

        try:
            idx = int(line_choice) - 1
            if idx < 0 or idx >= len(lines_list):
                raise IndexError
            selected_line = lines_list[idx]
            break
        except (IndexError, ValueError):
            count += 1
            remaining = 3 - count
            print("Error: Invalid line selection!")
            print(f"{remaining} attempts left.")
            print("Please try again.")
    else:
        print("Error: Your account has been temporarily blocked due to 3 failed attempts.")
        print("Returning to previous menu.")
        return

    count = 0
    while count < 3:
        name = input("Enter Train Name: ").strip()
        if name.lower() == "exit": return

        if not name:
            count += 1
            remaining = 3 - count
            print("Error: Train name cannot be empty.")
            print(f"{remaining} attempts left.\nPlease try again.")
        else:
            break
    else:
        print("Error: Your account has been temporarily blocked due to 3 failed attempts.")
        print("Returning to previous menu.")
        return

    count = 0
    while count < 3:
        speed = get_valid_number("Enter Speed: ")
        if speed == "exit": return
        if float(speed) <= 0:
            count += 1
            remaining = 3 - count
            print("Error: Speed must be greater than zero.")
            print(f"{remaining} attempts left.")
            print("Please try again.")
        else:
            break
    else:
        print("Error: Your account has been temporarily blocked due to 3 failed attempts.")
        print("Returning to previous menu.")
        return

    stop_time = get_valid_number("Enter Stop Time: ")
    if stop_time == "exit": return

    count = 0
    while count < 3:
        quality = get_valid_number("Enter Quality (1-5): ")
        if quality == "exit": return
        if int(quality) < 1 or int(quality) > 5:
            count += 1
            remaining = 3 - count
            print("Error: Quality must be a number between 1 and 5.")
            print(f"{remaining} attempts left.")
            print("Please try again.")
        else:
            break
    else:
        print("Error: Your account has been temporarily blocked due to 3 failed attempts.")
        print("Returning to previous menu.")
        return

    price = get_valid_number("Enter Price: ")
    if price == "exit": return

    count = 0
    while count < 3:
        capacity = get_valid_number("Enter Capacity: ")
        if capacity == "exit": return
        if int(capacity) <= 0:
            count += 1
            remaining = 3 - count
            print("Error: Capacity must be greater than zero.")
            print(f"{remaining} attempts left.")
            print("Please try again.")
        else:
            break
    else:
        print("Error: Your account has been temporarily blocked due to 3 failed attempts.")
        print("Returning to previous menu.")
        return

    departure_time = get_valid_time("Enter Departure Time: ")
    if departure_time == "exit": return

    distance = get_valid_number("Enter Distance to Station: ")
    if distance == "exit": return

    try:
        new_train = Train(
            train_id,
            name,
            selected_line.name,
            speed,
            stop_time,
            quality,
            price,
            capacity,
            departure_time,
            distance
        )

    except ValueError as error:
        print(error)
        print("Train creation failed. Returning to previous menu.")
        return

    collision_found = False
    for train in trains_list:
        if new_train.has_collision(train):
            collision_found = True
            break

    if collision_found:
        print("Error: This train has a collision with another train on the same line! Train not added.")
    else:
        trains_list.append(new_train)
        print(f"Success: Train '{name}' added successfully!")


def edit_train(trains_list, lines_list):
    print_header("Edit Train (Type 'exit' to cancel)")

    if not trains_list:
        print("The train list is empty.")
        return

    selected_train = None
    count = 0
    while count < 3:
        target_id = input("Enter Train ID to update (or 'exit' to return): ").strip()
        if target_id.lower() == 'exit':
            return

        if not target_id:
            count += 1
            remaining = 3 - count
            print("Error: Train ID cannot be empty.")
            print(f"{remaining} attempts left.")
            print("Please try again.")
            continue

        selected_train = next((t for t in trains_list if t.train_id == target_id), None)

        if selected_train:
            break
        else:
            count += 1
            remaining = 3 - count
            print("Error: No train found with this ID.")
            print(f"{remaining} attempts left. Please try again.")
    else:
        print("Error: Your account has been temporarily blocked due to 3 failed attempts.")
        print("Returning to previous menu.")
        return

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
        print("11. Exit (Back to Menu)")

        choice = input("What do you want to update? ").strip()

        match choice:
            case "1":
                count = 0
                while count < 3:
                    new_id = input("Enter new train ID: ").strip()
                    if new_id.lower() == "exit": return

                    if not new_id:
                        count += 1
                        remaining = 3 - count
                        print("Error: Train ID cannot be empty.")
                        print(f"{remaining} attempts left.")
                        print("Please try again.")
                        continue

                    id_exists = False
                    for train in trains_list:
                        if train.train_id != selected_train.train_id and train.train_id == new_id:
                            id_exists = True
                            break

                    if id_exists:
                        count += 1
                        remaining = 3 - count
                        print(f"Error: '{new_id}' is already used by another train.")
                        print(f"{remaining} attempts left.")
                        print("Please try again.")
                    else:
                        selected_train.train_id = new_id
                        print("Train ID Updated successfully!")
                        break
                else:
                    print("Error: Account temporarily blocked. Returning to menu.")
                    return

            case "2":
                count = 0
                while count < 3:
                    new_name = input("Enter new name: ").strip()
                    if new_name.lower() == "exit": return

                    if not new_name:
                        count += 1
                        remaining = 3 - count
                        print("Error: Name cannot be empty.")
                        print(f"{remaining} attempts left.")
                        print("Please try again.")
                        continue

                    name_exists = False
                    for train in trains_list:
                        if train.train_id != selected_train.train_id and train.name.lower() == new_name.lower():
                            name_exists = True
                            break

                    if name_exists:
                        count += 1
                        remaining = 3 - count
                        print(f"Error: '{new_name}' is already taken by another train.")
                        print(f"{remaining} attempts left.")
                        print("Please try again.")
                    else:
                        selected_train.name = new_name
                        print("Name Updated successfully!")
                        break
                else:
                    print("Error: Account temporarily blocked. Returning to menu.")
                    return

            case "3":
                if not lines_list:
                    print("No lines available.")
                    continue

                print("\nAvailable Lines:")
                for i, line in enumerate(lines_list, 1):
                    print(f"{i}. {line.name}")

                count = 0
                while count < 3:
                    line_choice = input("Select new line number: ").strip()
                    if line_choice.lower() == "exit": return

                    if not line_choice:
                        count += 1
                        remaining = 3 - count
                        print("Error: Input cannot be empty.")
                        print(f"{remaining} attempts left.")
                        print("Please try again.")
                        continue

                    try:
                        line_index = int(line_choice) - 1
                        if 0 <= line_index < len(lines_list):
                            selected_train.line_name = lines_list[line_index].name
                            print("Line Name Updated successfully!")
                            break
                        else:
                            raise ValueError
                    except ValueError:
                        count += 1
                        remaining = 3 - count
                        print("Error: Invalid line number.")
                        print(f"{remaining} attempts left.")
                        print("Please try again.")
                else:
                    print("Error: Account temporarily blocked. Returning to menu.")
                    return

            case "4":
                count = 0
                while count < 3:
                    new_speed = get_valid_number(f"Enter new speed (current: {selected_train.speed}): ")
                    if new_speed == "exit": return

                    if float(new_speed) <= 0:
                        count += 1
                        remaining = 3 - count
                        print("Error: Speed must be greater than zero.")
                        print(f"{remaining} attempts left.")
                        print("Please try again.")
                    else:
                        try:
                            selected_train.speed = new_speed
                            print("Speed Updated successfully!")
                            break
                        except ValueError as error:
                            count += 1
                            remaining = 3 - count
                            print(error)
                            print(f"{remaining} attempts left.")
                            print("Please try again.")
                else:
                    print("Error: Account temporarily blocked. Returning to menu.")
                    return

            case "5":
                count = 0
                while count < 3:
                    new_stop_time_str = input(f"Enter new stop time (current: {selected_train.stop_time}): ").strip()
                    if new_stop_time_str.lower() == "exit": return

                    try:
                        if not new_stop_time_str:
                            raise ValueError("Input cannot be empty.")
                        val = float(new_stop_time_str)
                        if val < 0:
                            raise ValueError("Stop time cannot be negative.")

                        selected_train.stop_time = val
                        print("Stop Time Updated successfully!")
                        break
                    except ValueError:
                        count += 1
                        remaining = 3 - count
                        print("Error: Invalid stop time.")
                        print(f"{remaining} attempts left.")
                        print("Please try again.")
                else:
                    print("Error: Account temporarily blocked. Returning to menu.")
                    return

            case "6":
                count = 0
                while count < 3:
                    new_quality_str = input(f"Enter new quality 1-5 (current: {selected_train.quality}): ").strip()
                    if new_quality_str.lower() == "exit": return

                    try:
                        val = int(new_quality_str)
                        if val < 1 or val > 5:
                            raise ValueError("Out of range")

                        selected_train.quality = val
                        print("Quality Updated successfully!")
                        break
                    except ValueError:
                        count += 1
                        remaining = 3 - count
                        print("Error: Quality must be a number between 1 and 5.")
                        print(f"{remaining} attempts left.")
                        print("Please try again.")
                else:
                    print("Error: Account temporarily blocked. Returning to menu.")
                    return

            case "7":
                count = 0
                while count < 3:
                    new_price_str = input(f"Enter new price (current: {selected_train.price}): ").strip()
                    if new_price_str.lower() == "exit": return

                    try:
                        if not new_price_str:
                            raise ValueError
                        selected_train.price = float(new_price_str)
                        print("Price Updated successfully!")
                        break
                    except ValueError:
                        count += 1
                        remaining = 3 - count
                        print("Error: Invalid price.")
                        print(f"{remaining} attempts left.")
                        print("Please try again.")
                else:
                    print("Error: Account temporarily blocked. Returning to menu.")
                    return

            case "8":
                count = 0
                while count < 3:
                    new_capacity_str = input(f"Enter new capacity (current: {selected_train.capacity}): ").strip()
                    if new_capacity_str.lower() == "exit": return

                    try:
                        if not new_capacity_str:
                            raise ValueError
                        selected_train.capacity = int(new_capacity_str)
                        print("Capacity Updated successfully!")
                        break
                    except ValueError:
                        count += 1
                        remaining = 3 - count
                        print("Error: Invalid capacity.")
                        print(f"{remaining} attempts left.")
                        print("Please try again.")
                else:
                    print("Error: Account temporarily blocked. Returning to menu.")
                    return

            case "9":
                count = 0
                while count < 3:
                    new_departure_time = get_valid_time("Enter new departure time: ")
                    if new_departure_time == "exit": return

                    old_departure_time = selected_train.departure_time
                    selected_train.departure_time = new_departure_time

                    collision_found = False
                    for other_train in trains_list:
                        if other_train != selected_train and selected_train.has_collision(other_train):
                            collision_found = True
                            break

                    if collision_found:
                        selected_train.departure_time = old_departure_time
                        count += 1
                        remaining = 3 - count
                        print("Error: This time causes a collision with another train!")
                        print(f"{remaining} attempts left.")
                        print("Please try again.")
                    else:
                        print("Departure time updated successfully!")
                        break
                else:
                    print("Error: Account temporarily blocked. Returning to menu.")
                    return

            case "10":
                count = 0
                while count < 3:
                    new_distance = get_valid_number("Enter new distance: ")
                    if new_distance == "exit": return

                    old_distance = selected_train.distance
                    selected_train.distance = new_distance

                    collision_found = False
                    for other_train in trains_list:
                        if other_train != selected_train and selected_train.has_collision(other_train):
                            collision_found = True
                            break

                    if collision_found:
                        selected_train.distance = old_distance
                        count += 1
                        remaining = 3 - count
                        print("Error: This distance causes a collision with another train!")
                        print(f"{remaining} attempts left.")
                        print("Please try again.")
                    else:
                        print("Distance updated successfully!")
                        break
                else:
                    print("Error: Account temporarily blocked. Returning to menu.")
                    return

            case "11":
                print("Returning to previous menu...")
                break

            case _:
                print("Invalid choice. Please enter a number between 1 and 11.")


def delete_train(trains_list):
    print_header("Delete Train (Type 'exit' to cancel)")

    if not trains_list:
        print("The train list is empty. Nothing to delete.")
        return

    count = 0
    while count < 3:
        target_id = input("Enter Train ID to delete (or type 'exit' to return): ").strip()

        if target_id.lower() == "exit": return

        if not target_id:
            count += 1
            remaining = 3 - count
            print("Error: Train ID cannot be empty.")
            print(f"{remaining} attempts left.")
            print("Please try again.")
            continue

        selected_train = next((t for t in trains_list if t.train_id == target_id), None)

        if selected_train:
            trains_list.remove(selected_train)
            print(f"Success: Train with ID '{target_id}' has been deleted successfully.")
            break
        else:
            count += 1
            remaining = 3 - count
            print(f"Error: No train found with ID '{target_id}'.")
            print(f"{remaining} attempts left.")
            print("Please try again.")
    else:
        print("Error: Your account has been temporarily blocked due to 3 failed attempts.")
        print("Returning to previous menu.")
        return


def display_employee_panel(current_employee):
    while True:
        print("\n" + "=" * 18 + "EMPLOYEE PANEL" + "=" * 18)
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
                print_header("Information Lines")

                if not lines_list:
                    print("No lines have been registered yet!")
                else:
                    for line in lines_list:
                        line.show_information()

                print_separator()
                input("Press Enter to return to menu...")

            case "5":
                if not lines_list:
                    print("No lines available! Please add a line first.")
                else:
                    add_train(trains_list, lines_list)

            case "6":
                edit_train(trains_list, lines_list)

            case "7":
                delete_train(trains_list)

            case "8":
                print_header("Information Trains")

                if not trains_list:
                    print("No trains have been registered yet!")
                else:
                    for train in trains_list:
                        train.show_information()

                print_separator()
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
            "booked_seats": train.booked_seats,
            "available_seats": train.capacity - train.booked_seats,
            "departure_time": train.departure_time,
            "distance": train.distance,
        }
        trains_data.append(train_dict)

    return trains_data
