# Design Patterns and Innovation in a Car Rental System

## Design Patterns

### Singleton Pattern

**Use Case:** To ensure that there is only one instance of the database connection manager in the system, avoiding the creation of duplicate database connections, the Singleton Pattern is employed. The `DatabaseManager` class provides a unified database connection and operation management throughout the application.

### Factory Method Pattern

**Use Case:** In the system, there is a need to create different types of objects such as `User`, `Car`, and `Booking`. The Factory Method Pattern encapsulates the object creation process, decoupling it from the rest of the system. This enhances the system's flexibility and scalability.

### Strategy Pattern

**Use Case:** Different rental fee calculation methods or vehicle recommendation strategies can be dynamically selected based on varying user input conditions. The Strategy Pattern encapsulates these algorithms or strategies, allowing for runtime selection, which improves the system's flexibility and extensibility.

### Observer Pattern

**Use Case:** When the booking status changes (e.g., booking confirmation or cancellation), the system needs to promptly update related information (e.g., vehicle availability). The Observer Pattern allows relevant modules in the system to automatically receive notifications when the state changes, ensuring data consistency and real-time updates.

### Template Method Pattern

**Use Case:** The system provides different operation menus for various user roles (e.g., admin and customer). Using the Template Method Pattern, a framework for the operation flow is defined, while the specific steps are implemented by subclasses (or user input). This simplifies the code logic and enhances scalability.

## Innovation

The innovation in this car rental system is primarily reflected in the "Smart Recommend Cars" feature. Traditional car rental systems typically offer only basic vehicle search and booking functionalities. However, this system introduces an intelligent recommendation algorithm that can suggest the most suitable vehicles based on user rental requirements (e.g., desired vehicle year, maximum mileage, rental dates, etc.).

Specifically, the system implements this feature through the `recommend_cars` method. When a user selects the "Smart Vehicle Recommendation" option, the system prompts the user to input their desired vehicle year, maximum mileage, and rental start and end dates. The system then filters the available vehicles based on these criteria and presents them to the user in a sorted manner (e.g., by price, model, etc.).

This innovation not only enhances the user experience by enabling users to find vehicles that meet their needs more quickly and accurately but also provides additional marketing opportunities for the car rental company. The system can recommend relevant vehicles based on user preferences, thereby increasing rental rates.
