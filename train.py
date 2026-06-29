class Train:
    def __init__(self, train_id, name, line_name, speed, stop_time, quality, price, capacity, departure_time, distance):
        self.train_id = train_id
        self.name = name
        self.line_name = line_name
        self.speed = speed
        self.stop_time = stop_time
        self.quality = quality
        self.price = price
        self.capacity = capacity
        self.booked_seats = 0
        self.departure_time = departure_time
        self.distance = distance

    @staticmethod
    def time_to_minutes(time_str):
        hours, minutes = map(int, time_str.split(":"))
        return hours * 60 + minutes

    @staticmethod
    def validate_non_negative(value, field_name):
        if value < 0:
            print(f"{field_name} cannot be negative.")
            return False
        return True

    @property
    def train_id(self):
        return self.__train_id

    @train_id.setter
    def train_id(self, value):
        if not value:
            print("Train ID cannot be empty.")
            return
        self.__train_id = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if not value.strip():
            print("Train name cannot be empty.")
            return
        self.__name = value

    @property
    def line_name(self):
        return self.__line_name

    @line_name.setter
    def line_name(self, value):
        if not value.strip():
            print("Line name cannot be empty.")
            return
        self.__line_name = value

    @property
    def speed(self):
        return self.__speed

    @speed.setter
    def speed(self, value):
        if not self.validate_non_negative(value, "Speed"):
            return
        self.__speed = value

    @property
    def stop_time(self):
        return self.__stop_time

    @stop_time.setter
    def stop_time(self, value):
        if not self.validate_non_negative(value, "Stop time"):
            return
        self.__stop_time = value

    @property
    def quality(self):
        return self.__quality

    @quality.setter
    def quality(self, value):
        val = int(value)
        if not self.validate_non_negative(val, "Quality"):
            return
        self.__quality = val

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value):
        if not self.validate_non_negative(value, "Price"):
            return
        self.__price = value

    @property
    def capacity(self):
        return self.__capacity

    @capacity.setter
    def capacity(self, value):
        if not self.validate_non_negative(value, "Capacity"):
            return
        self.__capacity = value

    @property
    def departure_time(self):
        return self.__departure_time

    @departure_time.setter
    def departure_time(self, value):
        self.__departure_time = value

    @property
    def distance(self):
        return self.__distance

    @distance.setter
    def distance(self, value):
        if not self.validate_non_negative(value, "Distance"):
            return
        self.__distance = value

    def show_information(self):
        print(f"ID: {self.train_id}")
        print(f"Name: {self.name}")
        print(f"Line: {self.line_name}")
        print(f"Speed: {self.speed} km/h")
        print(f"Stop Time: {self.stop_time} min")
        print(f"Quality: {self.quality}")
        print(f"Price: {self.price}")
        print(f"Capacity: {self.capacity}")
        print(f"Booked Seats: {self.booked_seats}")
        print(f"Available seats:{self.capacity - self.booked_seats}")
        print(f"Departure Time: {self.departure_time}")
        print(f"Distance: {self.distance}")

    def has_collision(self, other_train):
        if self.line_name != other_train.line_name:
            return False

        if self.speed == 0 or other_train.speed == 0:
            return False

        self_start = self.time_to_minutes(self.departure_time)
        other_start = self.time_to_minutes(other_train.departure_time)

        self_arrival = self_start + (self.distance / self.speed) * 60
        self_departure = self_arrival + self.stop_time

        other_arrival = other_start + (other_train.distance / other_train.speed) * 60
        other_departure = other_arrival + other_train.stop_time

        return not (self_departure <= other_arrival or self_arrival >= other_departure)

    def __str__(self):
        return (f"Train ID: {self.train_id}, Name: {self.name}, Line: {self.line_name}, "
                f"Speed: {self.speed}, Stop Time: {self.stop_time}, Quality: {self.quality}, "
                f"Price: {self.price}, Capacity: {self.capacity}, Departure Time: {self.departure_time}, "
                f"Distance: {self.distance}, Booked Seats: {self.booked_seats} available seats:{self.capacity - self.booked_seats}")


    def get_a_passenger(self):
        available_seats = self.capacity - self.booked_seats
        if not available_seats > 0:
            return False
        self.booked_seats +=1
        return True
