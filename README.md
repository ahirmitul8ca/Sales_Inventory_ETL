Sales Inventory ETL is a high-performance ETL (Extract, Transform, Load) framework engineered to automate the synchronization of supply chain inventory and sales data. The project features a "self-healing" modular architecture, utilizing a dedicated file management layer to resolve directory dependencies and pathing logic automatically. This ensures seamless portability and zero-crash execution when transitioning between a Windows-based local development environment and a Linux-based containerized production environment.

The core engine integrates advanced data integrity logic by replacing standard inserts with T-SQL MERGE (Upsert) operations, allowing for intelligent, single-transaction updates to a SQL Server database. By centralizing orchestration in a "bootstrapping" main phase, the system validates environment readiness, initializes comprehensive logging for audit trails, and manages the entire lifecycle of data from extraction to daily CSV reporting and database synchronization.

Technical Stack:

    Language: Python 3.x

    Data Analysis: Pandas & NumPy

    Database: Microsoft SQL Server (MS SQL)

    Library Interface: SQLAlchemy & pyodbc

    DevOps & Deployment: Docker & Docker Compose

    Pathing: Pathlib for cross-platform OS compatibility
