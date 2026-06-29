from employee import Employee
from employee_panel import login_employee, display_employee_panel


def main():
    # لیست اولیه کارمندان سیستم
    employees_list = [
        Employee("admin", "Admin@123", "Fatemeh", "fatemeh@email.com")
    ]

    print("=== Railway Management System ===")

    # لاگین کارمند
    logged_in_user = login_employee(employees_list)

    if logged_in_user:
        # ورود به پنل مدیریتی
        display_employee_panel(logged_in_user)
    else:
        print("Login failed. Exiting program.")


if __name__ == "__main__":
    main()
