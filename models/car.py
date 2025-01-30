# models/car.py
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