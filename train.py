class Train:
    train_list = []
    def __init__(self, train_id, train_name, line,capacity):
        self.train_id = train_id
        self.train_name = train_name
        self.line = line
        self.capacity = capacity
        self.speed = 0
        self.stop = 0
        self.quality = ""
        self.price = 0


    def add_train(self):
        if self not in Train.train_list:
            Train.train_list.append(self)
        else:
            print("Train already exist")

    def remove_train(self,train_id):
        for i in Train.train_list:
            if i.train_id == train_id:
                Train.train_list.remove(i)
            else:
                print("Train not exist")


    def update_train(self,train_id):
        for train in Train.train_list:
            if train.train_id == train_id:
                while True:
                    print("just enter the number of the option that you want to update:")
                    print("1. Train name")
                    print("2. Line")
                    print("3. Capacity")
                    print("4. Speed")
                    print("5. Stop")
                    print("6. Quality")
                    print("7. Price")
                    print("0. Exit")
                    choice = input()
                    match choice:
                        case "1":
                            self.train_name = input("Enter new train name: ")
                        case "2":
                            self.line = input("Enter new train line: ")
                        case "3":
                            self.capacity = int(input("Enter new train capacity: "))
                        case "4":
                            self.speed = int(input("Enter new train speed: "))
                        case "5":
                            self.stop = int(input("Enter new train stop: "))
                        case "6":
                            self.quality = input("Enter new train quality: ")
                        case "7":
                            self.price = int(input("Enter new train price: "))
                        case "0":
                            break
                        case _: print("Invalid input")
            else:
                print("Invalid Train id")

    def __str__(self):
        return f'''
            "Train id": {self.train_id}
            "Train name": {self.train_name}
            "Line": {self.line}
            "Capacity": {self.capacity}
            "Speed": {self.speed}
            "Quality": {self.quality}
            "Price": {self.price}
                '''
    @classmethod
    def show_trains(cls):
        for train in cls.train_list:
            print(train)

train1 = Train("0001", "my_train","west line",25)
train1.add_train()
train1.show_trains()
