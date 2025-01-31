# System Design

## Class Diagram
This diagram shows the class diagram of a car rental system, which mainly consists of four classes: CarRentalSystem, User, Car, and Booking. The CarRentalSystem class is the core of the system. It is responsible for managing user, car, and booking information, and interacting with the DatabaseManager class for data. The User class represents the users in the system, the Car class contains detailed information about cars, and the Booking class records the relevant information of each car rental. The various classes are interconnected through one - to - many and one - to - one relationships, forming a complete car rental management system.
![Class Diagram](./Diagram/Class%20Diagram.png)

## Use Case Diagram
This diagram shows the use case diagram of the car rental system, which mainly involves two types of users: customers and administrators. Customers can perform operations such as viewing available cars, booking cars, calculating rental fees, getting intelligent car recommendations, and registering. Administrators, on the other hand, have higher privileges. They can log in to the system, add, update, and delete car information, as well as manage bookings. Through these use cases, the system can meet the needs of different users and provide comprehensive car rental services.
![Use Case Diagram](./Diagram/Use%20Case%20Diagram.png)

## Sequence Diagram
This diagram is the main sequence diagram of the car rental system, demonstrating the interaction process between users and the system. After logging in, users can select different menu options according to their roles (customers or administrators). Customers can view available vehicles, reserve vehicles, calculate rental fees, and get intelligent vehicle recommendations. Administrators can add, update, and delete vehicle information, as well as manage reservations. The system interacts with the database to process user requests and return results.
![Sequence Diagram](./Diagram/Sequence%20Diagram.png)

# Design Patterns

## Singleton Pattern

**Use Case:** To ensure that there is only one instance of the database connection manager in the system, avoiding the creation of duplicate database connections, the Singleton Pattern is employed. The `DatabaseManager` class provides a unified database connection and operation management throughout the application.

## Factory Method Pattern

**Use Case:** In the system, there is a need to create different types of objects such as `User`, `Car`, and `Booking`. The Factory Method Pattern encapsulates the object creation process, decoupling it from the rest of the system. This enhances the system's flexibility and scalability.

## Strategy Pattern

**Use Case:** Different rental fee calculation methods or vehicle recommendation strategies can be dynamically selected based on varying user input conditions. The Strategy Pattern encapsulates these algorithms or strategies, allowing for runtime selection, which improves the system's flexibility and extensibility.

## Observer Pattern

**Use Case:** When the booking status changes (e.g., booking confirmation or cancellation), the system needs to promptly update related information (e.g., vehicle availability). The Observer Pattern allows relevant modules in the system to automatically receive notifications when the state changes, ensuring data consistency and real-time updates.

## Template Method Pattern

**Use Case:** The system provides different operation menus for various user roles (e.g., admin and customer). Using the Template Method Pattern, a framework for the operation flow is defined, while the specific steps are implemented by subclasses (or user input). This simplifies the code logic and enhances scalability.

# Innovation

The innovation in this car rental system is primarily reflected in the "Smart Recommend Cars" feature. Traditional car rental systems typically offer only basic vehicle search and booking functionalities. However, this system introduces an intelligent recommendation algorithm that can suggest the most suitable vehicles based on user rental requirements (e.g., desired vehicle year, maximum mileage, rental dates, etc.).

Specifically, the system implements this feature through the `recommend_cars` method. When a user selects the "Smart Vehicle Recommendation" option, the system prompts the user to input their desired vehicle year, maximum mileage, and rental start and end dates. The system then filters the available vehicles based on these criteria and presents them to the user in a sorted manner (e.g., by price, model, etc.).

This innovation not only enhances the user experience by enabling users to find vehicles that meet their needs more quickly and accurately but also provides additional marketing opportunities for the car rental company. The system can recommend relevant vehicles based on user preferences, thereby increasing rental rates.

# Software Evolution

## Maintenance

After the development and deployment of this car rental system, the system may encounter various issues or require functional extensions based on user feedback. To ensure the continuous operation and optimization of the system, regular maintenance work must be carried out. Here are some key points for maintaining this system:

- **Bug Fixing**: During system operation, some errors or defects (bugs) may be found. These issues can affect system stability or user experience. Therefore, we need to periodically review the system's log files, fix known bugs, and conduct tests to ensure that the repaired functions are working correctly.

- **Feature Enhancement**: Based on user needs or market changes, it may be necessary to add new features. For example, more intelligent recommendation algorithms could be added in the future, or customers could be allowed to choose different payment methods. Whenever new features are added, we will ensure that the code for the new features is compatible with existing functions and conduct necessary regression testing.

- **Performance Optimization**: As the amount of system data grows, it may be necessary to optimize the performance of database queries, vehicle recommendations, and other operations. This may include optimizing database indexes or improving the efficiency of certain algorithms.

- **System Security**: Regularly check and update the system's security to ensure the security of user data and prevent potential cyberattacks. Conduct regular audits and updates on password management and data encryption.

## Versioning

This project uses Git for version control to ensure that code is effectively managed and tracked during development. Git version control can help the team avoid code conflicts during development, record changes for each commit, and easily roll back to previous versions.

- **Version Release**: Whenever an important functional module is completed or a major bug is fixed, we will create a new Git tag to mark the current version. Version naming follows the Semantic Versioning (SemVer) rules, with the format `vX.Y.Z`, where:
    - `X` represents the major version number, which increases when there are major changes that are not compatible with the old version.
    - `Y` represents the minor version number, which increases when new backward-compatible features are added.
    - `Z` represents the patch version number, which increases when backward-compatible bug fixes are made.

- **Branch Management**: We use the Git Flow workflow for branch management. The main branches are:
    - `main`: Used to release stable production versions. All released code is merged into this branch.
    - `develop`: Used for code under development. All new features are first merged into this branch.
    - `feature/`: Used for temporary branches for developing new features. A new feature branch is created from the `develop` branch for each feature development, and after development is completed, it is merged back into `develop`.
    - `bugfix/`: Used for temporary branches for fixing bugs. After the fix is completed, it is merged back into `develop`.
    - `release/`: Used for branches preparing for release. Usually, final testing and fixes are performed, and then it is merged into `main` and `develop`.
    - `hotfix/`: Used for fixing urgent issues in the production environment. After the fix is completed, it is merged into `main` and `develop`.

- **Commit Conventions**: Each commit should clearly and concisely state the purpose of the commit, following a format similar to the following:
    - `feat: Add vehicle booking feature`
    - `fix: Fixed a bug in the vehicle recommendation algorithm`
    - `docs: Update README file`
    - `chore: Update dependency packages`

## Compatibility

Over time, the system may encounter compatibility issues with operating systems, databases, or other external tools. To ensure the availability and stability of the system in different environments, the following aspects need to be considered:

- **Operating System Compatibility**: Currently, this system supports Windows, macOS, and Linux operating systems. We ensure that the system runs normally under these operating systems, especially in terms of file paths, permission management, and environment variable compatibility.

- **Database Compatibility**: This system uses SQLite as the database. SQLite is a lightweight database engine that can run on most operating systems. We ensure that data operation functions remain consistent across different versions of SQLite. At the same time, we may consider migrating to other database systems (such as MySQL or PostgreSQL) in the future to support higher concurrent data access.

- **Python Version Compatibility**: This system requires Python 3.6 or higher. We ensure the compatibility of the system in different Python versions, avoiding code incompatibility issues caused by language version updates. If it is necessary to support lower versions of Python, it may be necessary to downgrade some new features (such as f-strings, asynchronous operations, etc.).

- **Third-Party Library Compatibility**: Currently, this system does not depend on third-party libraries and only uses the Python standard library. In the future, if it is necessary to use other libraries or frameworks (such as Flask or Django), we need to ensure their compatibility with the current system to avoid unnecessary dependency conflicts.

Through these measures, we ensure the long-term stability and cross-platform compatibility of the system, providing reliable services to users.
