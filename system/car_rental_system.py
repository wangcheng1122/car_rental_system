import uuid
import datetime
from models.user import User
from models.car import Car
from models.booking import Booking
from database.database_manager import DatabaseManager


class CarRentalSystem:

    def __init__(self):
        self.users = []
        self.cars = []
        self.bookings = []
        self.db_manager = DatabaseManager()
        self.load_data()

    def load_data(self):
        # Load users
        user_data = self.db_manager.load_users()
        self.users = [User(username, password, role) for username, password, role in user_data]

        # Load cars
        car_data = self.db_manager.load_cars()
        self.cars = [Car(car_id, make, model, year, mileage, available, min_rent_period, max_rent_period)
                     for car_id, make, model, year, mileage, available, min_rent_period, max_rent_period in car_data]

        # Load bookings
        booking_data = self.db_manager.load_bookings()
        self.bookings = [
            Booking(booking_id, customer_username, car_id, datetime.datetime.strptime(start_date, "%Y-%m-%d").date(),
                    datetime.datetime.strptime(end_date, "%Y-%m-%d").date(), status)
            for booking_id, customer_username, car_id, start_date, end_date, status in booking_data
        ]

    def save_data(self):
        self.db_manager.save_users(self.users)
        self.db_manager.save_cars(self.cars)
        self.db_manager.save_bookings(self.bookings)

    def register_user(self, username, password, role):
        if any(user.username == username for user in self.users):
            print("Username already exists.")
            return False
        user = User(username, password, role)
        self.users.append(user)
        self.save_data()
        print("User registered successfully.")
        return True

    def login_user(self, username, password):
        user = next((user for user in self.users if user.username == username and user.password == password), None)
        if user:
            return user
        print("Invalid username or password.")
        return None

    def add_car(self, make, model, year, mileage, min_rent_period, max_rent_period):
        car_id = str(uuid.uuid4())
        car = Car(car_id, make, model, year, mileage, True, min_rent_period, max_rent_period)
        self.cars.append(car)
        self.save_data()
        print("Car added successfully.")

    def update_car(self, car_id, make=None, model=None, year=None, mileage=None, available=None, min_rent_period=None,
                   max_rent_period=None):
        car = next((car for car in self.cars if car.car_id == car_id), None)
        if car:
            if make: car.make = make
            if model: car.model = model
            if year: car.year = year
            if mileage: car.mileage = mileage
            if available is not None: car.available = available
            if min_rent_period: car.min_rent_period = min_rent_period
            if max_rent_period: car.max_rent_period = max_rent_period
            self.save_data()
            print("Car updated successfully.")
        else:
            print("Car not found.")

    def delete_car(self, car_id):
        self.cars = [car for car in self.cars if car.car_id != car_id]
        self.save_data()
        print("Car deleted successfully.")

    def view_available_cars(self):
        available_cars = [car for car in self.cars if car.available]
        if available_cars:
            print("Available Cars:")
            for car in available_cars:
                print(car)
        else:
            print("No cars available.")

    def book_car(self, customer, car_id, start_date_str, end_date_str):
        try:
            start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            return

        if start_date >= end_date:
            print("End date must be after start date.")
            return

        # 新增检查：开始日期是否在未来
        if start_date < datetime.date.today():
            print("Start date cannot be in the past.")
            return

        car = next((car for car in self.cars if car.car_id == car_id and car.available), None)
        if not car:
            print("Car not found or not available.")
            return

        if (end_date - start_date).days < car.min_rent_period or (end_date - start_date).days > car.max_rent_period:
            print(f"Rental period must be between {car.min_rent_period} and {car.max_rent_period} days.")
            return

        booking_id = str(uuid.uuid4())
        booking = Booking(booking_id, customer.username, car_id, start_date, end_date)
        self.bookings.append(booking)
        self.save_data()
        print("Booking created successfully.")

    def calculate_rental_fee(self, car_id, start_date_str, end_date_str):
        try:
            start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            return None

        car = next((car for car in self.cars if car.car_id == car_id), None)
        if not car:
            print("Car not found.")
            return None

        rental_days = (end_date - start_date).days
        daily_rate = 50  # Example daily rate
        total_fee = daily_rate * rental_days
        return total_fee

    def manage_bookings(self):
        if not self.bookings:
            print("No bookings found.")
            return

        print("Pending Bookings:")
        for booking in self.bookings:
            if booking.status == "Pending":
                print(booking)

        booking_id = input(
            "Enter booking ID to approve or reject (or 'skip' to skip) (It's recommended to copy and paste the ID): ")
        if booking_id.lower() == "skip":
            return

        booking = next((booking for booking in self.bookings if booking.booking_id == booking_id), None)
        if not booking:
            print("Booking not found.")
            return

        action = input("Approve or Reject? (a/r): ").lower()
        if action == 'a':
            booking.status = "Approved"
            car = booking.get_car(self)
            if car:
                car.available = False
            print("Booking approved.")
        elif action == 'r':
            booking.status = "Rejected"
            print("Booking rejected.")
        else:
            print("Invalid action.")
        self.save_data()

    def recommend_cars(self, year, mileage, start_date_str, end_date_str):
        try:
            start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            return []

        rental_days = (end_date - start_date).days
        recommended_cars = [
            car for car in self.cars
            if car.available and
               (year is None or car.year == int(year)) and
               (mileage is None or car.mileage <= int(mileage)) and
               rental_days >= car.min_rent_period and rental_days <= car.max_rent_period
        ]
        return recommended_cars

    def run(self):
        try:
            while True:
                print("\nCar Rental System Menu:")
                print("1. Register User")
                print("2. Login User")
                print("0. Exit")

                choice = input("Enter your choice: ")

                if choice == '1':
                    username = input("Enter username: ")
                    password = input("Enter password: ")
                    role = input("Enter role (customer/admin): ").lower()
                    self.register_user(username, password, role)

                elif choice == '2':
                    username = input("Enter username: ")
                    password = input("Enter password: ")
                    user = self.login_user(username, password)
                    if user:
                        self.user_menu(user)
                        continue  # 关键：登录成功并从 user_menu 返回后，跳到下一次循环

                elif choice == '0':
                    print("Exiting Car Rental System.")
                    self.db_manager.close()
                    break

                else:
                    print("Invalid choice. Please try again.")
        except KeyboardInterrupt:
            print("\nProgram interrupted by user.")
            self.db_manager.close()  # 确保在中断时关闭数据库连接

    def user_menu(self, user):
        while True:
            print(f"\nWelcome, {user.username} ({user.role})")

            if user.role == "customer":
                print("1. View Available Cars")
                print("2. Book a Car")
                print("3. Calculate Rental Fee")
                print("4. Smart Recommend Cars")  # 新增智能推荐选项
                print("0. Logout")

                choice = input("Enter your choice: ")

                if choice == '1':
                    self.view_available_cars()
                elif choice == '2':
                    car_id = input("Enter car ID to book (It's recommended to copy and paste the ID): ")
                    start_date = input("Enter start date (YYYY-MM-DD): ")
                    end_date = input("Enter end date (YYYY-MM-DD): ")
                    self.book_car(user, car_id, start_date, end_date)
                elif choice == '3':
                    car_id = input("Enter car ID to calculate fee (It's recommended to copy and paste the ID): ")
                    start_date = input("Enter start date (YYYY-MM-DD): ")
                    end_date = input("Enter end date (YYYY-MM-DD): ")
                    fee = self.calculate_rental_fee(car_id, start_date, end_date)
                    if fee is not None:
                        print(f"Total rental fee: ${fee}")
                elif choice == '4':  # 处理智能推荐
                    year = input("Enter desired car year (or press Enter to skip): ")
                    mileage = input("Enter maximum car mileage (or press Enter to skip, unit: km): ")
                    start_date = input("Enter start date (YYYY-MM-DD): ")
                    end_date = input("Enter end date (YYYY-MM-DD): ")
                    recommended_cars = self.recommend_cars(year, mileage, start_date, end_date)
                    if recommended_cars:
                        print("Recommended Cars:")
                        for i, car in enumerate(recommended_cars):
                            print(f"{i + 1}. {car}")
                        car_id_input = input("Enter the car ID to book (or press Enter to skip): ")
                        if car_id_input:
                            selected_car = next((car for car in recommended_cars if car.car_id == car_id_input), None)
                            if selected_car:
                                self.book_car(user, selected_car.car_id, start_date, end_date)
                            else:
                                print("Invalid car ID. Please select a car from the list.")
                    else:
                        print("No cars match your criteria.")
                elif choice == '0':
                    print("Logging out.")
                    break
                else:
                    print("Invalid choice. Please try again.")
