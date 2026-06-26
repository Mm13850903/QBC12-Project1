import datetime


def buy_ticket_panel(trains_list, lines_list):
    print("--- Panel Kharid Belit ---")

    if len(trains_list) == 0:
        print("No trains are currently available for purchase!")
        return


    for t in trains_list:
        destination = ""
        source = ""
        for line in lines_list:
            if line.name == t.line_name:
                destination = line.destination
                source = line.source
                break

        print(
            f"ID: {t.train_id} | Name: {t.name} | Masir: {source} be {destination} | Zarfiat Baghi Mandeh: {t.capacity} | Gheymat: {t.price}")


    while True:
        choice = input("ID ghatar baraye kharid ra vared konid (ya 'back'): ")
        if choice.lower() == "back":
            break

        found_train = None
        for t in trains_list:
            if t.train_id == choice:
                found_train = t
                break

        if found_train is None:
            print("Error: The train with this ID does not exist.")
            print("Please try again.")
            continue


        ticket = input(f"Number of tickets required for {found_train.name} ")
        if not ticket.isdigit():
            print("Error: The number of tickets must be a number!")
            continue

        count = int(ticket)
        if count <= 0:
            print("Error: The number of tickets must be a positive number.!")
            continue


        if found_train.capacity == 0:
            print("Error: This train is full!")
            print("capacity : 0")
        elif count > found_train.capacity:
            print(f"Error: The capacity of this train is not yet complete!")
            print(f"Remaining capacity : {found_train.capacity - count}")
        else:

            found_train.capacity = found_train.capacity - count
            total_price = count * found_train.price

            now = datetime.datetime.now()
            date = now.strftime("%Y-%m-%d")
            time = now.strftime("%H:%M:%S")
            day = now.strftime("%A")

            print(24 * "-")
            print("Purchase completed successfully :))")
            print(f"{count} ticket baraye masir '{found_train.line_name}' ba kharidari shod.")
            print(f"Mablaghe Nahaee ticket ha : {total_price}")
            print(f"Date: {date} | Day: {day} | Time: {time}")
            print(f" new remaining capacity: {found_train.capacity}")
            print(24 * "-")
            break