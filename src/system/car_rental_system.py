import uuid  # 导入uuid模块，用于生成唯一标识符
import datetime  # 导入datetime模块，用于处理日期和时间
from src.models.user import User  # 从models.user模块导入User类
from src.models.car import Car  # 从models.car模块导入Car类
from src.models.booking import Booking  # 从models.booking模块导入Booking类
from src.database.database_manager import DatabaseManager  # 从database.database_manager模块导入DatabaseManager类


class CarRentalSystem:
    """
    汽车租赁系统类，负责管理用户、车辆和预订，并与数据库交互。
    """

    def __init__(self):
        """
        初始化汽车租赁系统，创建用户列表、车辆列表、预订列表和数据库管理器实例，并从数据库加载数据。
        """
        self.users = []  # 用户列表，存储User对象
        self.cars = []  # 车辆列表，存储Car对象
        self.bookings = []  # 预订列表，存储Booking对象
        self.db_manager = DatabaseManager()  # 数据库管理器实例
        self.load_data()  # 从数据库加载数据

    def load_data(self):
        """
        从数据库加载用户、车辆和预订数据。
        """
        # 加载用户数据
        user_data = self.db_manager.load_users()
        self.users = [User(username, password, role) for username, password, role in user_data]

        # 加载车辆数据
        car_data = self.db_manager.load_cars()
        self.cars = [Car(car_id, make, model, year, mileage, available, min_rent_period, max_rent_period)
                     for car_id, make, model, year, mileage, available, min_rent_period, max_rent_period in car_data]

        # 加载预订数据
        booking_data = self.db_manager.load_bookings()
        self.bookings = [
            Booking(booking_id, customer_username, car_id, datetime.datetime.strptime(start_date, "%Y-%m-%d").date(),
                    datetime.datetime.strptime(end_date, "%Y-%m-%d").date(), status)
            for booking_id, customer_username, car_id, start_date, end_date, status in booking_data
        ]

    def save_data(self):
        """
        将用户、车辆和预订数据保存到数据库。
        """
        self.db_manager.save_users(self.users)
        self.db_manager.save_cars(self.cars)
        self.db_manager.save_bookings(self.bookings)

    def register_user(self, username, password, role):
        """
        注册新用户。

        Args:
            username: 用户名
            password: 密码
            role: 角色 (customer/admin)

        Returns:
            如果注册成功返回True，如果用户名已存在返回False。
        """
        if any(user.username == username for user in self.users):
            print("Username already exists.")
            return False
        user = User(username, password, role)
        self.users.append(user)
        self.save_data()
        print("User registered successfully.")
        return True

    def login_user(self, username, password):
        """
        用户登录。

        Args:
            username: 用户名
            password: 密码

        Returns:
            如果用户名和密码匹配，返回User对象，否则返回None。
        """
        user = next((user for user in self.users if user.username == username and user.password == password), None)
        if user:
            return user
        print("Invalid username or password.")
        return None

    def add_car(self, make, model, year, mileage, min_rent_period, max_rent_period):
        """
        添加新车辆。

        Args:
            make: 制造商
            model: 型号
            year: 生产年份
            mileage: 里程（单位：km）
            min_rent_period: 最小租赁期限（天）
            max_rent_period: 最大租赁期限（天）
        """
        car_id = str(uuid.uuid4())  # 生成唯一的车辆ID
        car = Car(car_id, make, model, year, mileage, True, min_rent_period, max_rent_period)
        self.cars.append(car)
        self.save_data()
        print("Car added successfully.")

    def update_car(self, car_id, make=None, model=None, year=None, mileage=None, available=None, min_rent_period=None,
                   max_rent_period=None):
        """
        更新车辆信息。

        Args:
            car_id: 要更新的车辆ID
            make: 新的制造商（可选）
            model: 新的型号（可选）
            year: 新的生产年份（可选）
            mileage: 新的里程（可选）
            available: 新的可用状态（可选）
            min_rent_period: 新的最小租赁期限（可选）
            max_rent_period: 新的最大租赁期限（可选）
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
        删除车辆。

        Args:
            car_id: 要删除的车辆ID
        """
        # 检查车辆是否存在
        car_to_delete = next((car for car in self.cars if car.car_id == car_id), None)
        if car_to_delete:
            self.cars = [car for car in self.cars if car.car_id != car_id]
            self.save_data()
            print("Car deleted successfully.")
        else:
            print("Car not found.")

    def view_available_cars(self):
        """
        查看所有可用车辆。
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
        预订车辆。

        Args:
            customer: 预订车辆的客户 (User对象)
            car_id: 要预订的车辆ID
            start_date_str: 预订开始日期 (YYYY-MM-DD)
            end_date_str: 预订结束日期 (YYYY-MM-DD)
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

        # 检查开始日期是否在过去
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

        booking_id = str(uuid.uuid4())  # 生成唯一的预订ID
        booking = Booking(booking_id, customer.username, car_id, start_date, end_date)
        self.bookings.append(booking)
        self.save_data()
        print("Booking created successfully.")

    def calculate_rental_fee(self, car_id, start_date_str, end_date_str):
        """
        计算租赁费用。

        Args:
            car_id: 要计算费用的车辆ID
            start_date_str: 租赁开始日期 (YYYY-MM-DD)
            end_date_str: 租赁结束日期 (YYYY-MM-DD)

        Returns:
            租赁费用，如果车辆未找到或日期格式无效，返回None。
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
        daily_rate = 50  # 示例每日租金
        total_fee = daily_rate * rental_days
        return total_fee

    def manage_bookings(self):
        """
        管理预订（管理员功能）。允许管理员批准或拒绝待处理的预订。
        """
        if not self.bookings:
            print("No bookings found.")
            return

        print("Pending Bookings:")
        for booking in self.bookings:
            if booking.status == "Pending":
                print(booking)

        booking_id = input(
            "Enter booking ID to approve or reject (It's recommended to copy and paste the ID): ")

        booking = next((booking for booking in self.bookings if booking.booking_id == booking_id), None)
        if not booking:
            print("Booking not found.")
            return

        action = input("Approve or Reject? (a/r): ").lower()
        if action == 'a':
            booking.status = "Approved"
            car = booking.get_car(self)  # 获取预订关联的车辆
            if car:
                car.available = False  # 将车辆设置为不可用
            print("Booking approved.")
        elif action == 'r':
            booking.status = "Rejected"
            print("Booking rejected.")
        else:
            print("Invalid action.")
        self.save_data()

    def recommend_cars(self, year, mileage, start_date_str, end_date_str):
        """
        根据年份、里程和租赁日期推荐车辆。

        Args:
            year: 期望的车辆年份（可选）
            mileage: 最大里程（可选）
            start_date_str: 租赁开始日期 (YYYY-MM-DD)
            end_date_str: 租赁结束日期 (YYYY-MM-DD)

        Returns:
            符合条件的车辆列表。
        """
        try:
            start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            return []

        rental_days = (end_date - start_date).days

        # 检查 year 是否为空字符串，如果是，则将其设置为 None
        if year == "":
            year = None

        # 检查 mileage 是否为空字符串，如果是，则将其设置为 None
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
        查看所有车辆，包括可用和不可用的。
        """
        if self.cars:
            print("All Cars:")
            for car in self.cars:
                print(car)
        else:
            print("No cars found.")

    def run(self):
        """
        运行汽车租赁系统的主循环。
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
                        # 进入用户菜单，并等待用户退出
                        self.user_menu(user)
                        # 用户退出后，回到主菜单
                        continue  # 继续主循环，允许用户重新登录

                elif choice == '0':
                    print("Exiting Car Rental System.")
                    self.db_manager.close()  # 关闭数据库连接
                    break

                else:
                    print("Invalid choice. Please try again.")
        except KeyboardInterrupt:
            print("\nProgram interrupted by user.")
            self.db_manager.close()  # 确保在程序被中断时关闭数据库连接

    def user_menu(self, user):
        """
        用户菜单（根据用户角色显示不同的选项）。

        Args:
            user: 当前登录的用户 (User对象)
        """
        while True:
            print(f"\nWelcome, {user.username} ({user.role})")

            if user.role == "customer":
                # 客户菜单
                print("1. View Available Cars")
                print("2. Book a Car")
                print("3. Calculate Rental Fee")
                print("4. Smart Recommend Cars")  # 智能推荐选项
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
                    break  # 退出用户菜单
                else:
                    print("Invalid choice. Please try again.")

            elif user.role == "admin":
                print("1. Add Car")
                print("2. Update Car")
                print("3. Delete Car")
                print("4. Manage Bookings")
                print("5. View All Cars")  # 添加查看所有车辆的选项
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

                elif choice == '5':  # 处理查看所有车辆的选项
                    self.view_all_cars()

                elif choice == '0':
                    print("Logging out.")
                    break

                else:
                    print("Invalid choice. Please try again.")
