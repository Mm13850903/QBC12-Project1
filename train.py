class Train:
    train_list = []
    def __init__(self, train_id, train_name, line, capacity):
        self.train_id = train_id
        self.train_name = train_name
        self.line = line
        self.capacity = capacity
        self.speed = 0
        self.stop = 0
        self.quality = ""
        self.price = 0

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
    def update_capacity(self, capacity):
        self.capacity = capacity
    def update_speed(self, speed):
        self.speed = speed
    def update_stop(self, stop):
        self.stop = stop
    def update_quality(self, quality):
        self.quality = quality
    def update_price(self, price):
        self.price = price

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
