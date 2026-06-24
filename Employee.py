import re

class Employee:
    def __init__(self, username, password, name, email):
        self.username = username
        self.password = password
        self.name = name
        self.email = email

class Line:
    def __init__(self, name, source, destination, station_count, stations):
        self.name = name
        self.source = source
        self.destination = destination
        self.station_count = station_count
        self.stations = stations

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

def is_valid_password(password):
    pattern = r'^(?=.*[a-zA-Z])(?=.*\d)(?=.*[&@])[a-zA-Z0-9&@]+$'
    temp = re.match(pattern, password)
    if temp:
        return True
    else:
        return False

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$'
    temp = re.match(pattern, email)
    if temp :
        return True
    else:
        return False


def check_username(username, target_list):
    for item in target_list:
        if item.username == username:
            return True
    return False


def check_email(email, target_list):
    for item in target_list:
        if item.email == email:
            return True
    return False


           


