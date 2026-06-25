class Train:
    def __init__(self, train_id, name, line_name, speed, stop_time, quality, price, capacity):
        self.train_id = train_id
        self.name = name
        self.line_name = line_name
        self.speed = speed
        self.stop_time = stop_time
        self.quality = quality
        self.price = price
        self.capacity = capacity

    @staticmethod
    def validate_non_negative(value, field_name):
        if value < 0:
            raise ValueError(f"{field_name} cannot be negative.")

    @property
    def train_id(self):
        return self._train_id

    @train_id.setter
    def train_id(self, value):
        if not value:
            raise ValueError("Train ID cannot be empty.")
        self._train_id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value.strip():
            raise ValueError("Train name cannot be empty.")
        self._name = value

    @property
    def line_name(self):
        return self._line_name

    @line_name.setter
    def line_name(self, value):
        if not value.strip():
            raise ValueError("Line name cannot be empty.")
        self._line_name = value

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        self.validate_non_negative(value, "Speed")
        self._speed = value

    @property
    def stop_time(self):
        return self._stop_time

    @stop_time.setter
    def stop_time(self, value):
        self.validate_non_negative(value, "Stop time")
        self._stop_time = value

    @property
    def quality(self):
        return self._quality

    @quality.setter
    def quality(self, value):
        self.validate_non_negative(value, "Quality")
        self._quality = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        self.validate_non_negative(value, "Price")
        self._price = value

    @property
    def capacity(self):
        return self._capacity

    @capacity.setter
    def capacity(self, value):
        self.validate_non_negative(value, "Capacity")
        self._capacity = value

    def __str__(self):
        return f"Train ID: {self.train_id}, Name: {self.name}, Line: {self.line_name}, Speed: {self.speed}, Stop Time: {self.stop_time}, Quality: {self.quality}, Price: {self.price}, Capacity: {self.capacity}"
