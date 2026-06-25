import re
class Employee:
    def __init__(self, username, password, first_name, last_name , email):
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
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
    if temp:
        return True
    else:
        return False

def check_email(email, employees_dict):
    for emp_object in employees_dict.values():
        if emp_object.email == email:
            return True
    return False