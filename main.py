from employee import Employee
from line import Line
from train import Train
from employee_panel import login_employee

# ۱. ساخت لیست کارمندان و تعریف یک کارمند نمونه
# نکته: رمز عبور باید با الگوی ریجکس شما مطابقت داشته باشد (حرف بزرگ، حرف کوچک، عدد و کاراکتر خاص مثل @ یا &)
employees_list = [
    Employee("admin", "Admin@123", "Fatemeh", "fatemeh@email.com")
]

# ۲. تست تابع لاگین
print("--- Step 1: Login Test ---")
# برای تست، نام کاربری "admin" و رمز عبور "Admin@123" را وارد کنید
logged_in_user = login_employee(employees_list)

if logged_in_user:
    print(f"Login successful! Welcome, {logged_in_user.name}.\n")
    
    # ۳. تست ساخت خط ریلی
    print("--- Step 2: Line Creation Test ---")
    line1 = Line("Tehran-Mashhad", "Tehran", "Mashhad", 3, ["Tehran", "Semnan", "Mashhad"])
    line1.show_information()
    print("Line test completed successfully!\n")

    # ۴. تست ساخت قطار و بررسی تداخل (Collision)
    print("--- Step 3: Train and Collision Test ---")
    train1 = Train(101, "Simoorgh", "Tehran-Mashhad", 120, 15, 5, 250000, 400, "08:00", 900)
    train2 = Train(102, "Ghazal", "Tehran-Mashhad", 110, 10, 4, 200000, 300, "08:30", 900)
 
    print(f"Train 1 Info: {train1}")
    print(f"Train 2 Info: {train2}")
    
    # بررسی تداخل زمانی بین دو قطار
    collision = train1.has_collision(train2)
    if collision:
        print("⚠️ Warning: Temporal collision detected between Train 1 and Train 2!")
    else:
        print("✅ No collisions detected.")

else:
    print("Login test failed.")
