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


    def get_train_id(self):
        return self.train_id
    def get_name(self):
        return self.name
    def get_line_name(self):
        return self.line_name
    def get_speed(self):
        return self.speed
    def get_stop_time(self):
        return self.stop_time
    def get_quality(self):
        return self.quality
    def get_price(self):
        return self.price
    def get_capacity(self):
        return self.capacity
