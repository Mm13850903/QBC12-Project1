from train import Train

def add_train_menu():
    train_id = input("Enter train id: ")
    train_name = input("Enter train name: ")
    line = input("Enter line: ")
    capacity = int(input("Enter capacity: "))
    train = Train(train_id, train_name, line, capacity)
    if train.add_train():
        print("Train added successfully")
    else:
        print("Train already exists")


def remove_train_menu():
    train_id = input("Enter train id: ")
    if Train.remove_train(train_id):
        print("Train removed successfully")
    else:
        print("Train not found")


def update_train_menu():
    train_id = input("Enter train id: ")
    train = Train.find_train(train_id)
    if train is None:
        print("Train not found")
        return

    while True:
        print("========== Update Train ==========")
        print("1. Train name")
        print("2. Line")
        print("3. Capacity")
        print("4. Speed")
        print("5. Stop")
        print("6. Quality")
        print("7. Price")
        print("0. Back")

        choice = input("Choice: ")

        match choice:
            case "1":
                value = input("Enter new train name: ")
                train.update_train_name(value)

            case "2":
                value = input("Enter new line: ")
                train.update_line(value)

            case "3":
                value = int(input("Enter new capacity: "))
                train.update_capacity(value)

            case "4":
                value = int(input("Enter new speed: "))
                train.update_speed(value)

            case "5":
                value = int(input("Enter new stop: "))
                train.update_stop(value)

            case "6":
                value = input("Enter new quality: ")
                train.update_quality(value)

            case "7":
                value = int(input("Enter new price: "))
                train.update_price(value)

            case "0":
                break

            case _:
                print("Invalid choice")


def show_trains_menu():
    trains = Train.get_all_trains()

    if not trains:
        print("No trains found")
        return

    for train in trains:
        print(train)


def main_menu():
    while True:
        print("========== Main Menu ==========")
        print("1. Add train")
        print("2. Remove train")
        print("3. Update train")
        print("4. Show trains")
        print("0. Exit")

        choice = input("Choice: ")

        match choice:
            case "1":
                add_train_menu()

            case "2":
                remove_train_menu()

            case "3":
                update_train_menu()

            case "4":
                show_trains_menu()

            case "0":
                print("Program finished")
                break

            case _:
                print("Invalid choice")


main_menu()
