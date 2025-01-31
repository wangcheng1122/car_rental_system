# Car Rental System

## Introduction

This system is a command-line car rental system developed in Python 3, designed to simulate and simplify the daily operations of a car rental company. The system utilizes object-oriented programming principles and implements core functionalities such as user management, vehicle management, and rental booking and management. It aims to improve rental efficiency, reduce manual errors, and enhance customer satisfaction.

## Features

### User Management

*   **User Registration:** Allows new users to register as system users, choosing either a customer or administrator role.
*   **User Login:** Allows registered users to log in to the system using their username and password.
*   **Role Differentiation:** The system distinguishes between customer and administrator roles, granting different operational permissions based on the role.
    *   **Customers:** Can view available vehicles, book vehicles, calculate rental fees, and use smart recommendation features.
    *   **Administrators:** Can add, update, and delete vehicles, and manage rental bookings.

### Vehicle Management

*   **Vehicle Database:** The system maintains a vehicle database containing detailed information about each vehicle, such as:
    *   Vehicle ID (unique identifier)
    *   Make (Brand)
    *   Model
    *   Year
    *   Mileage
    *   Availability (Available)
    *   Minimum Rent Period
    *   Maximum Rent Period
*   **Vehicle Management Operations:** Administrators can perform the following operations:
    *   **Add Vehicle:** Add new vehicle records to the database.
    *   **Update Vehicle:** Modify the details of existing vehicles.
    *   **Delete Vehicle:** Remove vehicle records from the database.

### Rental Booking

*   **View Available Vehicles:** Customers can view a list of currently available vehicles and their details.
*   **Book a Vehicle:** Customers can select a vehicle, specify the start and end dates of the rental, and submit a booking request.
*   **Rental Fee Calculation:** The system calculates the rental fee based on the selected vehicle, rental duration, and a preset daily rate.
*   **Booking Restrictions:** The system checks if the rental dates are within the vehicle's allowed rental period and ensures that the start date is not earlier than today.

### Rental Management

*   **Manage Booking Requests:** Administrators can view all pending booking requests.
*   **Approve/Reject Bookings:** Administrators can approve or reject booking requests based on availability and other criteria.
*   **Booking Status Updates:** Once a booking request is approved, the vehicle's availability status is updated.

### Smart Recommendation

*   **Smart Vehicle Recommendation:** Customers can get a list of smart recommended vehicles based on the vehicle's year, mileage, and rental date range.

## How to Configure, Install, and Run

### Environment Requirements

*   **Operating System:** Compatible with major operating systems like Windows, macOS, and Linux.
*   **Python Version:** Python 3.6 or higher.
*   **Dependencies:** No additional third-party modules are required, as this project only uses the `sqlite3` module from the Python standard library.

### Installation Steps

1.  **Obtain Project Files:**
    Place the project files (including `main.py`, the `models` folder, the `database` folder, and the `data` folder) in a directory on your local computer.
2.  **Navigate to Project Directory:**
    Open a command-line terminal (Command Prompt or PowerShell for Windows users, Terminal for macOS and Linux users) and use the `cd` command to navigate to the directory containing the project files.

    ```bash
    cd D:\ITsoft\pythonproject\car_rental_system (Please follow your actual path.)
    ```
3.  **(Optional) Create and activate a virtual environment  :**
    ```bash
    python -m venv myenv  # Create a virtual environment (if venv is not installed, install it first: pip install virtualenv)
    source myenv/bin/activate  # Activate virtual environment (Linux/macOS)
    myenv\Scripts\activate  # Activate virtual environment (Windows)
    ```
4. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
5.  **Run the Main Program:**

    ```bash
    python -m src.main (important：Using the -m argument allows the Python interpreter to treat src as a package.)
    ```
    
    This will launch the car rental system and display the main menu.

## Usage Instructions

### Register User

1.  In the main menu, select "1. Register User".
2.  Follow the prompts to enter a username, password, and role (customer or admin).
3.  Upon successful registration, the system will display a success message.

### Login User

1.  In the main menu, select "2. Login User".
2.  Follow the prompts to enter your registered username and password.
3.  Upon successful login, the system will display a menu specific to your role.

### Customer Functions

*   **View Available Cars:** Select "1. View Available Cars" to see a list of currently available vehicles.
*   **Book a Car:** Select "2. Book a Car" and follow the prompts to enter the vehicle ID, start date, and end date.
*   **Calculate Rental Fee:** Select "3. Calculate Rental Fee" and follow the prompts to enter the vehicle ID, start date, and end date. The system will calculate and display the rental fee.
*   **Smart Recommend Cars:** Select "4. Smart Recommend Cars" and follow the prompts to enter the vehicle year, maximum mileage, and rental date range. The system will recommend suitable vehicles.
*   **Logout:** Select "0. Logout" to return to the main menu.

### Administrator Functions

*   **Add Car:** Select "1. Add Car" and follow the prompts to enter the vehicle's make, model, year, mileage, minimum rental period, and maximum rental period.
*   **Update Car:** Select "2. Update Car" and follow the prompts to enter the ID of the vehicle to update, as well as the new vehicle information.
*   **Delete Car:** Select "3. Delete Car" and follow the prompts to enter the ID of the vehicle to delete.
*   **Manage Bookings:** Select "4. Manage Bookings". The system will display pending booking requests, and the administrator can choose to approve or reject them.
*   **Logout:** Select "0. Logout" to return to the main menu.

## File Descriptions
# Project Directory Structure

    car_rental_system/
    ├── .venv/                        # Virtual environment directory
    ├── doc/                          # Documentation directory
    │   ├── Class Diagram.png         # Class diagram
    │   ├── Sequence Diagram.png      # Sequence diagram
    │   ├── System Documentation.md   # System documentation
    │   └── Use Case Diagram.png      # Use case diagram
    ├── database/                     # Database directory
    │   ├── car_rental.db             # SQLite database file
    │   └── database_manager.py       # Database management class
    ├── models/                       # Data models module
    │   ├── booking.py                # Booking class
    │   ├── car.py                    # Car class
    │   └── user.py                   # User class
    ├── src/                          # Source code directory
    │   ├── main.py                   # Main program entry point
    │   └── ...                       # Other source code files
    ├── README.md                     # README file
    └── requirements.txt              # Dependencies file




### `main.py`

*   The main program entry point, containing user interaction logic and the system's main loop.

### `models/`

*   Contains data model classes, representing entities in the system:
    *   `user.py`: User class, containing attributes like username, password, and role.
    *   `car.py`: Car class, containing detailed vehicle information.
    *   `booking.py`: Booking class, containing detailed booking information.

### `database/`

*   Contains database management classes for handling database operations:
    *   `database_manager.py`: Database management class, responsible for connecting to the database, loading, and saving data.

### `data/`

*   Contains the database file:
    *   `car_rental.db`: SQLite database file, used to store user, vehicle, and booking data.
