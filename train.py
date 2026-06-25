class Train:
    train_list = []
    def __init__(self, train_id, train_name, line, capacity):
        self.train_id = train_id
        self.train_name = train_name
        self.line = line
        self._capacity = capacity
        self._speed = 0
        self._stop = 0
        self.quality = ""
        self._price = 0

    def add_train(self):
        if Train.find_train(self.train_id) is None:
            Train.train_list.append(self)
            return True
        return False

    @classmethod
    def find_train(cls, train_id):
        for train in cls.train_list:
            if train.train_id == train_id:
                return train
        return None

    @classmethod
    def remove_train(cls, train_id):
        train = cls.find_train(train_id)
        if train is None:
            return False
        cls.train_list.remove(train)
        return True

    def update_train_name(self, train_name):
        self.train_name = train_name
    def update_line(self, line):
        self.line = line
    def update_quality(self, quality):
        self.quality = quality

    @classmethod
    def get_all_trains(cls):
        return cls.train_list
    def __str__(self):
        return f"""
    
Train id: {self.train_id}
Train name: {self.train_name}
Line: {self.line}
Capacity: {self.capacity}
Speed: {self.speed}
Stop: {self.stop}
Quality: {self.quality}
Price: {self.price}
"""

    @staticmethod
    def validate_positive(value, field_name):
        if value <= 0:
            raise ValueError(f"{field_name} must be positive")

    @property
    def capacity(self):
        return self._capacity
    @capacity.setter
    def capacity(self, value):
        Train.validate_positive(value, "Capacity")
        self._capacity = value

    @property
    def speed(self):
        return self._speed
    @speed.setter
    def speed(self, value):
        Train.validate_positive(value, "Speed")
        self._speed = value

    @property
    def stop(self):
        return self._speed

    @stop.setter
    def stop(self, value):
        Train.validate_positive(value, "Stop")
        self._stop = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        Train.validate_positive(value, "price")
        self._price = value
