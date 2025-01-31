# System Design

## Class Diagram
![Class Diagram](./Diagram/Class%20Diagram.png)

### Use Case Diagram
![Use Case Diagram](./Diagram/Use%20Case%20Diagram.png)

### Sequence Diagram
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
# 软件演化 (Software Evolution)

## 1. 维护 (Maintenance)

在开发和部署本汽车租赁系统后，系统可能会遇到各种问题或需要根据用户反馈进行功能扩展。为了保证系统的持续运行和优化，必须进行定期的维护工作。以下是本系统维护的几个关键点：

- **错误修复**：在系统运行过程中，可能会发现一些错误或缺陷（bug）。这些问题会影响系统的稳定性或用户体验。因此，我们需要定期审查系统的日志文件，修复已知的 bug，并进行测试以确保修复后的功能正常运行。
  
- **功能增强**：根据用户需求或市场变化，可能需要添加新的功能。例如，未来可以加入更多的智能推荐算法，或允许客户选择不同的支付方式。每当增加新功能时，我们会确保新功能的代码与现有功能兼容，并进行必要的回归测试。

- **性能优化**：随着系统数据量的增长，可能需要对数据库查询、车辆推荐等操作进行性能优化。这可能包括数据库索引的优化，或者改进某些算法的效率。

- **系统安全**：定期检查和更新系统的安全性，确保用户数据的安全性以及防止潜在的网络攻击。对密码管理、数据加密等方面进行定期审核和更新。

## 2. 版本控制 (Versioning)

本项目采用 Git 进行版本控制，确保代码在开发过程中得到有效管理和跟踪。Git 版本控制可以帮助团队在开发过程中避免代码冲突，记录每次提交的变更，并方便回滚到先前的版本。

- **版本发布**：每当完成一个重要的功能模块或修复一个重大 bug 时，我们会创建一个新的 Git 标签（tag），标记当前的版本。版本命名遵循语义化版本控制（SemVer）规则，格式为 `vX.Y.Z`，其中：
  - `X` 表示主版本号，增加时表示有重大变更，不兼容旧版本。
  - `Y` 表示次版本号，增加时表示向后兼容的新功能。
  - `Z` 表示修订号，增加时表示向后兼容的 bug 修复。

- **分支管理**：我们采用 Git Flow 工作流进行分支管理。主要分支有：
  - `main`：用于发布稳定的生产版本，所有发布的代码都会合并到此分支。
  - `develop`：用于开发中的代码，所有新特性都会先合并到此分支。
  - `feature/`：用于开发新特性的临时分支，每个功能开发时会从 `develop` 分支创建一个新的 feature 分支，开发完成后合并回 `develop`。
  - `bugfix/`：用于修复 bug 的临时分支，修复完成后合并回 `develop`。
  - `release/`：用于准备发布的分支，通常会进行最终的测试和修复，然后合并到 `main` 和 `develop`。
  - `hotfix/`：用于修复生产环境中的紧急问题，修复完成后会合并到 `main` 和 `develop`。

- **提交规范**：每次提交都应该简洁明了地说明此次提交的目的，遵循类似以下的格式：
  - `feat: 添加车辆预订功能`
  - `fix: 修复了车辆推荐算法的 bug`
  - `docs: 更新 README 文件`
  - `chore: 更新依赖包`

## 3. 兼容性 (Compatibility)

随着时间的推移，系统可能会遇到与操作系统、数据库或其他外部工具的兼容性问题。为了确保系统在不同环境下的可用性和稳定性，需要考虑以下几个方面：

- **操作系统兼容性**：目前本系统支持 Windows、macOS 和 Linux 操作系统。我们确保系统在这些操作系统下的运行正常，尤其是在文件路径、权限管理、环境变量等方面的兼容性。

- **数据库兼容性**：本系统使用 SQLite 作为数据库，SQLite 是一个轻量级的数据库引擎，能够在大多数操作系统中运行。我们确保在不同版本的 SQLite 中，数据操作功能保持一致。同时，未来可以考虑迁移到其他数据库系统（如 MySQL 或 PostgreSQL），以便支持更高并发的数据访问。

- **Python 版本兼容性**：本系统要求 Python 3.6 或更高版本。在不同的 Python 版本中，我们确保系统的兼容性，避免由于语言版本更新导致的代码不兼容问题。如果需要支持更低版本的 Python，可能需要对某些新特性（如 f-string、异步操作等）进行降级处理。

- **第三方库兼容性**：目前该系统没有依赖第三方库，只使用了 Python 标准库。将来，如果需要使用其他库或框架（例如 Flask 或 Django），我们需要确保其与当前系统的兼容性，避免产生不必要的依赖冲突。

通过这些措施，我们确保系统的长期稳定性和跨平台的兼容性，为用户提供可靠的服务。

