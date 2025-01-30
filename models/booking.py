# models/booking.py
import datetime

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