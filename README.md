# Airport Database System

A MySQL and Flask project for managing airport operations, flight schedules, aircraft, employees, passengers, bookings, and luggage.

## 📐 Database Design

The system contains nine tables: `AIRPORT`, `AIRPLANE`, `FLIGHT`, `EMPLOYEE`, `PILOT`, `FLIGHT_ATTENDANT`, `PASSENGER`, `LUGGAGE`, and `BOOK`.

<img width="80%" alt="errDiagram" src="https://github.com/user-attachments/assets/98ce6bac-0df8-438a-8474-c28f2362d276" />
<img alt="RelationalSchema" src="https://github.com/user-attachments/assets/9715682c-1fd5-4bc0-8c77-7a709db0942a" />


### 📌 Main Relationships
- `AIRPORT` → `FLIGHT`: One-to-Many (1:N).
- `AIRPLANE` → `FLIGHT`: One-to-Many (1:N).
- `PASSENGER` → `LUGGAGE`: One-to-Many (1:N).
- `FLIGHT` ↔ `PASSENGER`: Many-to-Many (M:N), resolved by `BOOK`.
- `PILOT` and `FLIGHT_ATTENDANT` are employee subtypes.

## 🛠️ Technology Stack
- **Database:** MySQL
- **Backend:** Python and Flask
- **Frontend:** HTML and CSS
- **Database Connector:** `mysql-connector-python`

## How the UI Works

The browser sends a request to Flask (`app.py`). Flask executes SQL queries against MySQL and renders the results using templates in `templates/`. Styles are loaded from `static/`.

```text
Browser → Flask → MySQL Database → Flask Templates → Browser
```

The UI can display records and reports. Insert, update, and delete operations depend on the features implemented in the application.

## Setup and Installation

### 1. Create the database

```bash
mysql -u root -p
```

```sql
CREATE DATABASE AirportDB;
EXIT;
```

Skip the `CREATE DATABASE` command if the database already exists.

### 2. Import the schema and sample data

Run these commands from the project root folder:

```bash
mysql -u root -p AirportDB < Schema.sql
mysql -u root -p AirportDB < Data.sql
```

If `Schema.sql` contains `CREATE DATABASE AirportDB;`, remove that line before importing into an existing database. Avoid importing `Data.sql` repeatedly if it causes duplicate-key errors.

### 3. Install dependencies

```bash
cd airport_db_ui
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 4. Configure MySQL

```bash
export DB_HOST=localhost
export DB_USER=root
export DB_NAME=AirportDB
read -rsp "MySQL password: " DB_PASSWORD; echo
export DB_PASSWORD
```

### 5. Start the application

```bash
python app.py
```

Open **http://127.0.0.1:5000** in your browser.

## Testing
- Verify the MySQL connection.
- View existing records.
- Test insert, update, and delete features if implemented.
- Check foreign-key constraints and booking seat uniqueness.
- Compare UI reports with SQL query results.

## Project Files
- `Schema.sql` — database table definitions and constraints.
- `Data.sql` — sample data.
- `Images/errDiagram.png` — ER diagram.
- `Images/RelationalSchema.png` — relational schema.

## Objective

To apply relational database design, SQL queries, primary and foreign keys, relationships, and referential integrity to a practical airport-management system.
