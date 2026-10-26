-- Airports
INSERT INTO AIRPORT VALUES
(1, 'Netaji Subhas Chandra Bose Airport', 'India', 'Kolkata'),
(2, 'Indira Gandhi International Airport', 'India', 'Delhi');

-- Airplanes
INSERT INTO AIRPLANE VALUES
(101, 180, 'A320', 'Airbus'),
(102, 220, 'B737', 'Boeing');

-- Employees
INSERT INTO EMPLOYEE VALUES
(201, 'Kolkata', 'Male', 'Rahul', NULL, 'Das',
 55000, '1990-05-10', 1),
(202, 'Kolkata', 'Female', 'Priya', 'S', 'Roy',
 48000, '1995-08-12', 1);

-- Pilot
INSERT INTO PILOT VALUES
(201, 'Senior Pilot', 'LIC1001');

-- Flight attendant
INSERT INTO FLIGHT_ATTENDANT VALUES
(202, 'Senior Attendant');

-- Passengers
INSERT INTO PASSENGER VALUES
(301, 'Amit', NULL, 'Sharma', '9876543210',
 '2000-01-15', 'amit@example.com'),
(302, 'Neha', 'K', 'Sen', '9876501234',
 '2001-06-20', 'neha@example.com');

-- Flights
INSERT INTO FLIGHT VALUES
(401, 120, 'Delhi', '2026-11-01', '10:00:00',
 'Kolkata', '2026-11-01', '12:00:00', 101, 1),
(402, 135, 'Kolkata', '2026-11-02', '14:00:00',
 'Delhi', '2026-11-02', '16:15:00', 102, 2);

-- Luggage
INSERT INTO LUGGAGE VALUES
(501, 18.50, 301),
(502, 12.00, 301),
(503, 15.25, 302);

-- Bookings
INSERT INTO BOOK VALUES
(401, 301, 4500.00, '12A'),
(401, 302, 4500.00, '12B'),
(402, 301, 5200.00, '14C');
