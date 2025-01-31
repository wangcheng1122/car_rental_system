import uuid  # Import the uuid module for generating unique identifiers
import datetime  # Import the datetime module for handling dates and times

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes

from src.models.user import User  # Import the User class from the models.user module
from src.models.car import Car  # Import the Car class from the models.car module
from src.models.booking import Booking  # Import the Booking class from the models.booking module
from src.database.database_manager import \
    DatabaseManager  # Import the DatabaseManager class from the database.database_manager module


class CarRentalSystem:
    """
    Car rental system class responsible for managing users, cars, and bookings, and interacting with the database.
    """

    def __init__(self):
        """
        Initialize the car rental system, create lists for users, cars, and bookings, and an instance of the database manager. Load data from the database.
        """
        self.users = []  # List of users, storing User objects
        self.cars = []  # List of cars, storing Car objects
        self.bookings = []  # List of bookings, storing Booking objects
        self.db_manager = DatabaseManager()  # Instance of the database manager
        self.load_data()  # Load data from the database

    def load_data(self):
        """
        Load user, car, and booking data from the database.
        """
        # Load user data
        user_data = self.db_manager.load_users()
        self.users = [User(username, password, role) for username, password, role in user_data]

        # Load car data
        car_data = self.db_manager.load_cars()
        self.cars = [Car(car_id, make, model, year, mileage, available, min_rent_period, max_rent_period)
                     for car_id, make, model, year, mileage, available, min_rent_period, max_rent_period in car_data]

        # Load booking data
        booking_data = self.db_manager.load_bookings()
        self.bookings = [
            Booking(booking_id, customer_username, car_id, datetime.datetime.strptime(start_date, "%Y-%m-%d").date(),
                    datetime.datetime.strptime(end_date, "%Y-%m-%d").date(), status)
            for booking_id, customer_username, car_id, start_date, end_date, status in booking_data
        ]

    def save_data(self):
        """
        Save user, car, and booking data to the database.
        """
        self.db_manager.save_users(self.users)
        self.db_manager.save_cars(self.cars)
        self.db_manager.save_bookings(self.bookings)

    def register_user(self, username, password, role):
        """
        Register a new user.

        Args:
            username: Username
            password: Password
            role: Role (customer/admin)

        Returns:
            True if registration is successful, False if the username already exists.
        """
        if any(user.username == username for user in self.users):
            print("Username already exists.")
            return False
        hashed_password = self._hash_password(password)
        user = User(username, hashed_password, role)
        self.users.append(user)
        self.save_data()
        print("User registered successfully.")
        return True

    def login_user(self, username, password):
        """
        User login.

        Args:
            username: Username
            password: Password

        Returns:
            User object if the username and password match, otherwise None.
        """
        hashed_password = self._hash_password(password)
        user = next((user for user in self.users if user.username == username and user.password == hashed_password),
                    None)

        if user:
            return user
        print("Invalid username or password.")
        return None

    def add_car(self, make, model, year, mileage, min_rent_period, max_rent_period):
        """
        Add a new car.

        Args:
            make: Manufacturer
            model: Model
            year: Production year
            mileage: Mileage (in km)
            min_rent_period: Minimum rental period (days)
            max_rent_period: Maximum rental period (days)
        """
        car_id = str(uuid.uuid4())  # Generate a unique car ID
        car = Car(car_id, make, model, year, mileage, True, min_rent_period, max_rent_period)
        self.cars.append(car)
        self.save_data()
        print("Car added successfully.")

    def update_car(self, car_id, make=None, model=None, year=None, mileage=None, available=None, min_rent_period=None,
                   max_rent_period=None):
        """
        Update car information.

        Args:
            car_id: ID of the car to update
            make: New manufacturer (optional)
            model: New model (optional)
            year: New production year (optional)
            mileage: New mileage (optional)
            available: New availability status (optional)
            min_rent_period: New minimum rental period (optional)
            max_rent_period: New maximum rental period (optional)
        """
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
        """
        Delete a car.

        Args:
            car_id: ID of the car to delete
        """
        # Check if the car exists
        car_to_delete = next((car for car in self.cars if car.car_id == car_id), None)
        if car_to_delete:
            self.cars = [car for car in self.cars if car.car_id != car_id]
            self.save_data()
            print("Car deleted successfully.")
        else:
            print("Car not found.")

    def view_available_cars(self):
        """
        View all available cars.
        """
        available_cars = [car for car in self.cars if car.available]
        if available_cars:
            print("Available Cars:")
            for car in available_cars:
                print(car)
        else:
            print("No cars available.")

    def book_car(self, customer, car_id, start_date_str, end_date_str):
        """
        Book a car.

        Args:
            customer: Customer booking the car (User object)
            car_id: ID of the car to book
            start_date_str: Booking start date (YYYY-MM-DD)
            end_date_str: Booking end date (YYYY-MM-DD)
        """
        try:
            start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            return

        if start_date >= end_date:
            print("End date must be after start date.")
            return

        # Check if the start date is in the past
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

        booking_id = str(uuid.uuid4())  # Generate a unique booking ID
        booking = Booking(booking_id, customer.username, car_id, start_date, end_date)
        self.bookings.append(booking)
        self.save_data()
        print("Booking created successfully.")

    def calculate_rental_fee(self, car_id, start_date_str, end_date_str):
        """
        Calculate rental fee.

        Args:
            car_id: ID of the car to calculate the fee for
            start_date_str: Rental start date (YYYY-MM-DD)
            end_date_str: Rental end date (YYYY-MM-DD)

        Returns:
            Rental fee, or None if the car is not found or the date format is invalid.
        """
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
        if rental_days < car.min_rent_period or rental_days > car.max_rent_period:
            print(f"Rental period must be between {car.min_rent_period} and {car.max_rent_period} days.")
            return None

        # Assuming a fixed rate per day for simplicity
        rate_per_day = 50  # Example rate
        total_fee = rental_days * rate_per_day
        return total_fee

    def manage_bookings(self):
        """
        Manage bookings by approving or rejecting them.
        """
        print("Manage Bookings:")
        for booking in self.bookings:
            print(booking)

        booking_id = input("Enter booking ID to manage (It's recommended to copy and paste the ID): ")

        booking = next((booking for booking in self.bookings if booking.booking_id == booking_id), None)
        if not booking:
            print("Booking not found.")
            return

        action = input("Approve or Reject? (a/r): ").lower()
        if action == 'a':
            booking.status = "Approved"
            car = booking.get_car(self)  # Get the car associated with the booking
            if car:
                car.available = False  # Set the car to unavailable
            print("Booking approved.")
        elif action == 'r':
            booking.status = "Rejected"
            print("Booking rejected.")
        else:
            print("Invalid action.")
        self.save_data()

    def recommend_cars(self, year, mileage, start_date_str, end_date_str):
        """
        Recommend cars based on year, mileage, and rental dates.

        Args:
            year: Desired car year (optional)
            mileage: Maximum mileage (optional)
            start_date_str: Rental start date (YYYY-MM-DD)
            end_date_str: Rental end date (YYYY-MM-DD)

        Returns:
            List of cars that match the criteria.
        """
        try:
            start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            return []

        rental_days = (end_date - start_date).days

        # Check if year is an empty string, if so, set it to None
        if year == "":
            year = None

        # Check if mileage is an empty string, if so, set it to None
        if mileage == "":
            mileage = None

        recommended_cars = [
            car for car in self.cars
            if car.available and
               (year is None or car.year == int(year)) and
               (mileage is None or car.mileage <= int(mileage)) and
               rental_days >= car.min_rent_period and rental_days <= car.max_rent_period
        ]
        return recommended_cars

    def view_all_cars(self):
        """
        View all cars, including available and unavailable ones.
        """
        if self.cars:
            print("All Cars:")
            for car in self.cars:
                print(car)
        else:
            print("No cars found.")

    def _hash_password(self, password):
        """
        Hashes the password using MD5.

        Args:
            password: The password to hash.

        Returns:
            The hexadecimal representation of the hashed password.
        """
        password_bytes = password.encode('utf-8')
        hasher = hashes.Hash(hashes.MD5(), backend=default_backend())
        hasher.update(password_bytes)
        hashed_password = hasher.finalize()
        return hashed_password.hex()

    def run(self):
        """
        Run the main loop of the car rental system.
        """
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
                        # Enter the user menu and wait for the user to exit
                        self.user_menu(user)
                        # After the user exits, return to the main menu
                        continue  # Continue the main loop, allowing the user to log in again

                elif choice == '0':
                    print("Exiting Car Rental System.")
                    self.db_manager.close()  # Close the database connection
                    break

                else:
                    print("Invalid choice. Please try again.")
        except KeyboardInterrupt:
            print("\nProgram interrupted by user.")
            self.db_manager.close()  # Ensure the database connection is closed when the program is interrupted

    def user_menu(self, user):
        """
        User menu (display different options based on user role).

        Args:
            user: Currently logged-in user (User object)
        """
        while True:
            print(f"\nWelcome, {user.username} ({user.role})")

            if user.role == "customer":
                # Customer menu
                print("1. View Available Cars")
                print("2. Book a Car")
                print("3. Calculate Rental Fee")
                print("4. Smart Recommend Cars")  # Smart recommendation option
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
                elif choice == '4':  # Handle smart recommendation
                    year = input("Enter desired car year (or press Enter to skip): ")
                    mileage = input("Enter maximum car mileage (or press Enter to skip): ")
                    start_date = input("Enter start date (YYYY-MM-DD): ")
                    end_date = input("Enter end date (YYYY-MM-DD): ")
                    recommended_cars = self.recommend_cars(year, mileage, start_date, end_date)
                    if recommended_cars:
                        print("Recommended Cars:")
                        for i, car in enumerate(recommended_cars):
                            print(f"{i + 1}. {car}")
                        car_index = input("Enter the number of the car to book (or press Enter to skip): ")
                        if car_index:
                            try:
                                selected_car = recommended_cars[int(car_index) - 1]
                                self.book_car(user, selected_car.car_id, start_date, end_date)
                            except (ValueError, IndexError):
                                print("Invalid car selection.")
                    else:
                        print("No cars match your criteria.")
                elif choice == '0':
                    print("Logging out.")
                    break  # Exit the user menu
                else:
                    print("Invalid choice. Please try again.")

            elif user.role == "admin":
                print("1. Add Car")
                print("2. Update Car")
                print("3. Delete Car")
                print("4. Manage Bookings")
                print("5. View All Cars")  # Add option to view all cars
                print("0. Logout")

                choice = input("Enter your choice: ")

                if choice == '1':
                    make = input("Enter car make: ")
                    model = input("Enter car model: ")
                    year = input("Enter car year: ")
                    mileage = input("Enter car mileage (km): ")
                    min_rent_period = int(input("Enter minimum rent period (days): "))
                    max_rent_period = int(input("Enter maximum rent period (days): "))
                    self.add_car(make, model, year, mileage, min_rent_period, max_rent_period)

                elif choice == '2':
                    car_id = input("Enter car ID to update (It's recommended to copy and paste the ID): ")
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
                    car_id = input("Enter car ID to delete (It's recommended to copy and paste the ID): ")
                    self.delete_car(car_id)

                elif choice == '4':
                    self.manage_bookings()

                elif choice == '5':  # Handle view all cars option
                    self.view_all_cars()

                elif choice == '0':
                    print("Logging out.")
                    break

                else:
                    print("Invalid choice. Please try again.")
