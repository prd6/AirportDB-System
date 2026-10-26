# Airport Database System

A database management project built using **MySQL, Python, and Flask** to manage airport operations, flight schedules, aircraft, employees, passengers, bookings, and luggage.

## 📐 Database Design

The system contains nine tables: `AIRPORT`, `AIRPLANE`, `FLIGHT`, `EMPLOYEE`, `PILOT`, `FLIGHT_ATTENDANT`, `PASSENGER`, `LUGGAGE`, and `BOOK`.

### ER Diagram
<img width="80%" alt="ER Diagram" src="https://github.com/user-attachments/assets/98ce6bac-0df8-438a-8474-c28f2362d276" />

### Relational Schema
<img width="80%" alt="Relational Schema" src="https://github.com/user-attachments/assets/9715682c-1fd5-4bc0-8c77-7a709db0942a" />

### Main Relationships
- `AIRPORT` → `FLIGHT`: One-to-Many (1:N).
- `AIRPLANE` → `FLIGHT`: One-to-Many (1:N).
- `PASSENGER` → `LUGGAGE`: One-to-Many (1:N).
- `FLIGHT` ↔ `PASSENGER`: Many-to-Many (M:N), resolved through `BOOK`.
- `PILOT` and `FLIGHT_ATTENDANT` are employee subtypes.

## 🛠️ Technology Stack

- **Database:** MySQL
- **Backend:** Python and Flask
- **Frontend:** HTML and CSS
- **Database Connector:** `mysql-connector-python`
- **Version Control:** Git and GitHub

## ⚙️ How the Application Works

The browser sends requests to the Flask application. Flask executes SQL queries against MySQL and returns the results through HTML templates.

```text
Browser → Flask → MySQL Database
   ↑                    |
   └── HTML Response ←──┘
```

The available features depend on the routes and templates implemented in the application.

## 🚀 Setup and Installation

### Prerequisites

Install the following software:

- Python 3
- MySQL Server 8.0 or compatible version
- Git

### 1. Clone the Repository

```powershell
git clone https://github.com/prd6/AirportDB-System.git
cd AirportDB-System
```

### 2. Create the Database

Open PowerShell and run:

```powershell
mysql -u root -p
```

Enter your MySQL root password. At the MySQL prompt, execute:

```sql
CREATE DATABASE IF NOT EXISTS AirportDB;
EXIT;
```

If the `mysql` command is not recognized, use the full path to `mysql.exe`, for example:

```powershell
& "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -p
```

Adjust the path if MySQL is installed elsewhere.

### 3. Import the Schema and Sample Data

Run these commands from the repository root directory in PowerShell.

**Import the schema:**

```powershell
Get-Content .\Schema.sql -Raw | & "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -p AirportDB
```

**Import the sample data:**

```powershell
Get-Content .\Data.sql -Raw | & "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -p AirportDB
```

These commands use PowerShell-compatible input piping instead of the `<` redirection syntax used in Command Prompt.

If `mysql` is already available in your PATH, you can replace the full executable path with `mysql`.

**Note:** If the SQL files create the database themselves, ensure they do not conflict with the existing database. Import the sample data only after the schema has been created successfully. Avoid importing the data repeatedly if it produces duplicate-key errors.

### 4. Verify the Database

Run:

```powershell
& "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -p -e "USE AirportDB; SHOW TABLES;"
```

The command should display the tables created by the schema.

### 5. Set Up the Flask Application

Navigate to the application directory:

```powershell
cd airport_db_ui
```

Create a virtual environment:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can use the virtual environment's Python executable directly instead.

Install the required dependencies:

```powershell
python -m pip install -r requirements.txt
```

### 6. Configure MySQL Connection

Set the database connection environment variables in PowerShell:

```powershell
$env:DB_HOST = "localhost"
$env:DB_USER = "root"
$env:DB_NAME = "AirportDB"
$env:DB_PASSWORD = Read-Host "Enter MySQL password"
```

Use your actual MySQL password. These environment variables apply to the current PowerShell session.

### 7. Run the Application

Start the Flask application:

```powershell
python app.py
```

Open your browser and visit:

**http://127.0.0.1:5000**

Keep the terminal open while using the application.

## 🧪 Testing

- Verify the MySQL connection.
- Confirm that the nine tables are created.
- Check that sample records are available.
- View database records and reports through the UI.
- Test insert, update, and delete operations where implemented.
- Verify foreign-key constraints and booking seat uniqueness.

## 📁 Project Structure

```text
AirportDB-System/
├── Schema.sql
├── Data.sql
├── Images/
│   ├── errDiagram.png
│   └── RelationalSchema.png
├── airport_db_ui/
│   ├── app.py
│   ├── requirements.txt
│   ├── templates/
│   └── static/
└── README.md
```

The structure above represents the intended layout; filenames and folders should match the actual repository.

## 🎯 Project Objective

To apply relational database design concepts, SQL queries, primary and foreign keys, entity relationships, and referential integrity to a practical airport-management system with a Flask-based web interface.

## 👨‍💻 Author

**Priyangshu Das**

