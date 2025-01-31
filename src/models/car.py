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
        availability_str = "Available" if self.available else "Not Available"
        return (f"ID: {self.car_id}, Make: {self.make}, Model: {self.model}, Year: {self.year}, "
                f"Mileage: {self.mileage} km, Status: {availability_str}, "
                f"Min Rent Period: {self.min_rent_period} days, Max Rent Period: {self.max_rent_period} days")