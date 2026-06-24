import re

class Employee:
    def __init__(self, username, password, name, email):
        self.username = username
        self.password = password
        self.name = name
        self.email = email

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


           


