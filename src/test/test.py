import sqlite3
import datetime
import uuid


class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

    def __str__(self):
        return f"Username: {self.username}, Role: {self.role}"


class Car:
    def __init__(self, car_id, make, model, year, mileage, available, min_rent_period, max_rent_period):
        self.car_id = car_id
        self.make = make
        self.model = model
        self.year = year
        self.mileage = mileage
        self.available = available
        self.min_rent_period = min_rent_period
        self.max_rent_period = max_rent_period

    def __str__(self):
        return f"ID: {self.car_id}, Make: {self.make}, Model: {self.model}, Year: {self.year}, Available: {self.available}"


class Booking:
    def __init__(self, booking_id, customer_username, car_id, start_date, end_date, status="Pending"):
        self.booking_id = booking_id
        self.customer_username = customer_username  # Store username instead of User object
        self.car_id = car_id  # Store car_id instead of Car object
        self.start_date = start_date
        self.end_date = end_date
        self.status = status

    def get_customer(self, system):
        return next((user for user in system.users if user.username == self.customer_username), None)

    def get_car(self, system):
        return next((car for car in system.cars if car.car_id == self.car_id), None)

    def __str__(self):
        return f"Booking ID: {self.booking_id}, Customer: {self.customer_username}, Car ID: {self.car_id}, Start: {self.start_date}, End: {self.end_date}, Status: {self.status}"


class CarRentalSystem:
    def __init__(self):
        self.users = []
        self.cars = []
        self.bookings = []
        self.db_connection = sqlite3.connect('car_rental.db')
        self.db_cursor = self.db_connection.cursor()
        self.create_tables()
        self.load_data()

    def create_tables(self):
        # Create tables if they don't exist
        self.db_cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT,
                role TEXT
            )
        ''')

        self.db_cursor.execute('''
            CREATE TABLE IF NOT EXISTS cars (
                car_id TEXT PRIMARY KEY,
                make TEXT,
                model TEXT,
                year INTEGER,
                mileage INTEGER,
                available BOOLEAN,
                min_rent_period INTEGER,
                max_rent_period INTEGER
            )
        ''')

        self.db_cursor.execute('''
            CREATE TABLE IF NOT EXISTS bookings (
                booking_id TEXT PRIMARY KEY,
                customer_username TEXT,
                car_id TEXT,
                start_date TEXT,
                end_date TEXT,
                status TEXT,
                FOREIGN KEY (customer_username) REFERENCES users(username),
                FOREIGN KEY (car_id) REFERENCES cars(car_id)
            )
        ''')

    def load_data(self):
        # Load users
        self.db_cursor.execute('SELECT * FROM users')
        self.users = [User(username, password, role) for username, password, role in self.db_cursor.fetchall()]

        # Load cars
        self.db_cursor.execute('SELECT * FROM cars')
        self.cars = [Car(car_id, make, model, year, mileage, available, min_rent_period, max_rent_period)
                     for car_id, make, model, year, mileage, available, min_rent_period, max_rent_period in self.db_cursor.fetchall()]

        # Load bookings
        self.db_cursor.execute('SELECT * FROM bookings')
        self.bookings = [
            Booking(booking_id, customer_username, car_id, datetime.datetime.strptime(start_date, "%Y-%m-%d").date(),
                    datetime.datetime.strptime(end_date, "%Y-%m-%d").date(), status)
            for booking_id, customer_username, car_id, start_date, end_date, status in self.db_cursor.fetchall()
        ]

    def save_data(self):
        # Save users
        self.db_cursor.executemany('''
            INSERT OR REPLACE INTO users (username, password, role) VALUES (?, ?, ?)
        ''', [(user.username, user.password, user.role) for user in self.users])

        # Save cars
        self.db_cursor.executemany('''
            INSERT OR REPLACE INTO cars (car_id, make, model, year, mileage, available, min_rent_period, max_rent_period) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', [(car.car_id, car.make, car.model, car.year, car.mileage, car.available, car.min_rent_period, car.max_rent_period) for car in self.cars])

        # Save bookings
        self.db_cursor.executemany('''
            INSERT OR REPLACE INTO bookings (booking_id, customer_username, car_id, start_date, end_date, status) VALUES (?, ?, ?, ?, ?, ?)
        ''', [(booking.booking_id, booking.customer_username, booking.car_id,
               booking.start_date.strftime("%Y-%m-%d"), booking.end_date.strftime("%Y-%m-%d"), booking.status) for booking in self.bookings])

        self.db_connection.commit()

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

    def update_car(self, car_id, make=None, model=None, year=None, mileage=None, available=None, min_rent_period=None, max_rent_period=None):
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

        booking_id = input("Enter booking ID to approve or reject (or 'skip' to skip): ")
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

    def run(self):
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

            elif choice == '0':
                print("Exiting Car Rental System.")
                self.db_connection.close()
                break

            else:
                print("Invalid choice. Please try again.")

    def user_menu(self, user):
        while True:
            print(f"\nWelcome, {user.username} ({user.role})")

            if user.role == "customer":
                print("1. View Available Cars")
                print("2. Book a Car")
                print("3. Calculate Rental Fee")
                print("0. Logout")

                choice = input("Enter your choice: ")

                if choice == '1':
                    self.view_available_cars()
                elif choice == '2':
                    car_id = input("Enter car ID to book: ")
                    start_date = input("Enter start date (YYYY-MM-DD): ")
                    end_date = input("Enter end date (YYYY-MM-DD): ")
                    self.book_car(user, car_id, start_date, end_date)
                elif choice == '3':
                    car_id = input("Enter car ID to calculate fee: ")
                    start_date = input("Enter start date (YYYY-MM-DD): ")
                    end_date = input("Enter end date (YYYY-MM-DD): ")
                    fee = self.calculate_rental_fee(car_id, start_date, end_date)
                    if fee is not None:
                        print(f"Total rental fee: ${fee}")
                elif choice == '0':
                    print("Logging out.")
                    break
                else:
                    print("Invalid choice. Please try again.")

            elif user.role == "admin":
                print("1. Add Car")
                print("2. Update Car")
                print("3. Delete Car")
                print("4. Manage Bookings")
                print("0. Logout")

                choice = input("Enter your choice: ")

                if choice == '1':
                    make = input("Enter car make: ")
                    model = input("Enter car model: ")
                    year = input("Enter car year: ")
                    mileage = input("Enter car mileage: ")
                    min_rent_period = int(input("Enter minimum rent period (days): "))
                    max_rent_period = int(input("Enter maximum rent period (days): "))
                    self.add_car(make, model, year, mileage, min_rent_period, max_rent_period)

                elif choice == '2':
                    car_id = input("Enter car ID to update: ")
                    make = input("Enter new make (or press Enter to skip): ")
                    model = input("Enter new model (or press Enter to skip): ")
                    year = input("Enter new year (or press Enter to skip): ")
                    mileage = input("Enter new mileage (or press Enter to skip): ")
                    available_input = input("Enter new availability (True/False, or press Enter to skip): ").lower()
                    available = None if not available_input else available_input == 'true'
                    min_rent_period = input("Enter new minimum rent period (or press Enter to skip): ")
                    max_rent_period = input("Enter new maximum rent period (or press Enter to skip): ")
                    self.update_car(car_id, make or None, model or None, year or None, mileage or None, available,
                                    min_rent_period or None, max_rent_period or None)

                elif choice == '3':
                    car_id = input("Enter car ID to delete: ")
                    self.delete_car(car_id)

                elif choice == '4':
                    self.manage_bookings()

                elif choice == '0':
                    print("Logging out.")
                    break

                else:
                    print("Invalid choice. Please try again.")


if __name__ == "__main__":
    system = CarRentalSystem()
    system.run()
