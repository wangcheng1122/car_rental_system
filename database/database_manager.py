# database/database_manager.py
import sqlite3
import datetime

class DatabaseManager:
    def __init__(self, db_name='car_rental.db'):
        self.db_connection = sqlite3.connect(db_name)
        self.db_cursor = self.db_connection.cursor()
        self.create_tables()

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

    def load_users(self):
        self.db_cursor.execute('SELECT * FROM users')
        return [(username, password, role) for username, password, role in self.db_cursor.fetchall()]

    def load_cars(self):
        self.db_cursor.execute('SELECT * FROM cars')
        return [(car_id, make, model, year, mileage, available, min_rent_period, max_rent_period)
                     for car_id, make, model, year, mileage, available, min_rent_period, max_rent_period in self.db_cursor.fetchall()]

    def load_bookings(self):
        self.db_cursor.execute('SELECT * FROM bookings')
        return [
            (booking_id, customer_username, car_id, start_date, end_date, status)
            for booking_id, customer_username, car_id, start_date, end_date, status in self.db_cursor.fetchall()
        ]

    def save_users(self, users):
        self.db_cursor.executemany('''
            INSERT OR REPLACE INTO users (username, password, role) VALUES (?, ?, ?)
        ''', [(user.username, user.password, user.role) for user in users])
        self.db_connection.commit()

    def save_cars(self, cars):
        self.db_cursor.executemany('''
            INSERT OR REPLACE INTO cars (car_id, make, model, year, mileage, available, min_rent_period, max_rent_period) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', [(car.car_id, car.make, car.model, car.year, car.mileage, car.available, car.min_rent_period, car.max_rent_period) for car in cars])
        self.db_connection.commit()

    def save_bookings(self, bookings):
        self.db_cursor.executemany('''
            INSERT OR REPLACE INTO bookings (booking_id, customer_username, car_id, start_date, end_date, status) VALUES (?, ?, ?, ?, ?, ?)
        ''', [(booking.booking_id, booking.customer_username, booking.car_id,
               booking.start_date.strftime("%Y-%m-%d"), booking.end_date.strftime("%Y-%m-%d"), booking.status) for booking in bookings])
        self.db_connection.commit()

    def close(self):
        self.db_connection.close()