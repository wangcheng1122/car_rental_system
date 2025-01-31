from src.system.car_rental_system import CarRentalSystem


def display_welcome_banner():
    print(r"  ____        _   _       _       ")
    print(r" |  _ \      | | | |     | |      ")
    print(r" | |_) | ___ | |_| |_ ___| | ___  ")
    print(r" |  _ < / _ \| __| __/ _ \ |/ _ \ ")
    print(r" | |_) | (_) | |_| ||  __/ | (_) |")
    print(r" |____/ \___/ \__|\__\___|_|\___/ ")
    print(r"----------------------------------")
    print(r"       CarRentalSystem          ")
    print(r"----------------------------------")

if __name__ == "__main__":
    display_welcome_banner()
    system = CarRentalSystem()
    system.run()