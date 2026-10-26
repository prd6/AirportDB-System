-- Database Creation
CREATE DATABASE IF NOT EXISTS AirportDB;
USE AirportDB;

-- Tables
CREATE TABLE AIRPORT (
    Airport_ID INT PRIMARY KEY,
    AirportName VARCHAR(100) NOT NULL,
    Country VARCHAR(60),
    City VARCHAR(60)
);

CREATE TABLE AIRPLANE (
    Airplane_ID INT PRIMARY KEY,
    Capacity INT NOT NULL,
    Model VARCHAR(60),
    Manufacturer VARCHAR(100),
    CHECK (Capacity > 0)
);

CREATE TABLE EMPLOYEE (
    Employee_ID INT PRIMARY KEY,
    Address VARCHAR(200),
    Gender VARCHAR(20),
    FName VARCHAR(50) NOT NULL,
    MName VARCHAR(50),
    LName VARCHAR(50) NOT NULL,
    Salary DECIMAL(10,2),
    BDate DATE,
    Airport_ID INT,
    FOREIGN KEY (Airport_ID)
        REFERENCES AIRPORT(Airport_ID),
    CHECK (Salary IS NULL OR Salary >= 0)
);

CREATE TABLE FLIGHT_ATTENDANT (
    E_ID INT PRIMARY KEY,
    FA_Rank VARCHAR(50),
    FOREIGN KEY (E_ID)
        REFERENCES EMPLOYEE(Employee_ID)
        ON DELETE CASCADE
);

CREATE TABLE PILOT (
    E_ID INT PRIMARY KEY,
    PRank VARCHAR(50),
    License_Number VARCHAR(50) UNIQUE NOT NULL,
    FOREIGN KEY (E_ID)
        REFERENCES EMPLOYEE(Employee_ID)
        ON DELETE CASCADE
);

CREATE TABLE PASSENGER (
    Passenger_ID INT PRIMARY KEY,
    P_FName VARCHAR(50) NOT NULL,
    P_MName VARCHAR(50),
    P_LName VARCHAR(50) NOT NULL,
    PhoneNo VARCHAR(20),
    BDate DATE,
    P_Email VARCHAR(100) UNIQUE
);

CREATE TABLE FLIGHT (
    Flight_ID INT PRIMARY KEY,
    Duration INT,
    ALocation VARCHAR(100),
    ADate DATE,
    ATime TIME,
    DLocation VARCHAR(100),
    DDate DATE,
    DTime TIME,
    Airplane_ID INT NOT NULL,
    Airport_ID INT NOT NULL,
    FOREIGN KEY (Airplane_ID)
        REFERENCES AIRPLANE(Airplane_ID),
    FOREIGN KEY (Airport_ID)
        REFERENCES AIRPORT(Airport_ID),
    CHECK (Duration IS NULL OR Duration > 0)
);

CREATE TABLE LUGGAGE (
    Luggage_ID INT PRIMARY KEY,
    Weight DECIMAL(6,2) NOT NULL,
    Passenger_ID INT NOT NULL,
    FOREIGN KEY (Passenger_ID)
        REFERENCES PASSENGER(Passenger_ID)
        ON DELETE CASCADE,
    CHECK (Weight > 0)
);

CREATE TABLE BOOK (
    Flight_ID INT,
    Passenger_ID INT,
    Price DECIMAL(10,2) NOT NULL,
    Seat_Number VARCHAR(10) NOT NULL,
    PRIMARY KEY (Flight_ID, Passenger_ID),
    FOREIGN KEY (Flight_ID)
        REFERENCES FLIGHT(Flight_ID)
        ON DELETE CASCADE,
    FOREIGN KEY (Passenger_ID)
        REFERENCES PASSENGER(Passenger_ID)
        ON DELETE CASCADE,
    UNIQUE (Flight_ID, Seat_Number),
    CHECK (Price >= 0)
);
