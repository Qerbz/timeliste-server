import unittest
import sqlite3


class ViewTests(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(':memory:')
        self.cursor = self.conn.cursor()

        with open('../../database/database_setup.sql', 'r') as file:
            schema = file.read()

        self.cursor.executescript(schema)
        self.conn.commit()

    def tearDown(self):
        self.conn.close()

    def test_workinghours_view_insert_audit(self):
        # Insert test data into Employee and WorkingHours tables
        self.cursor.execute("INSERT INTO Employee (OrganizationID, FirstName, LastName, Email, PhoneNumber, Position, HireDate, IsActive) VALUES (1, 'John', 'Doe', 'john.doe@example.com', '+1234567890', 'Software Engineer', '2022-01-01', 1)")
        self.conn.commit()

        # Test the INSTEAD OF INSERT trigger on WorkingHoursView
        self.cursor.execute(
            "INSERT INTO WorkingHoursView (EmployeeID, StartTime, EndTime, CustomAmount) VALUES (1, '09:00', '17:00', 0)")
        self.conn.commit()

        self.cursor.execute("SELECT * FROM WorkingHoursAudit")
        result = self.cursor.fetchone()
        self.assertEqual(result, (1, 1, 1, '09:00', '17:00', 'Insert'))

    def test_workinghours_view_update_audit(self):
        # Insert test data into Employee and WorkingHours tables
        self.cursor.execute("INSERT INTO Employee (OrganizationID, FirstName, LastName, Email, PhoneNumber, Position, HireDate, IsActive) VALUES (1, 'John', 'Doe', 'john.doe@example.com', '+1234567890', 'Software Engineer', '2022-01-01', 1)")
        self.conn.commit()

        self.cursor.execute(
            "INSERT INTO WorkingHours (EmployeeID, StartTime, EndTime, CustomAmount) VALUES (1, '09:00', '17:00', 0)")
        self.conn.commit()

        # Test the INSTEAD OF UPDATE trigger on WorkingHoursView
        self.cursor.execute(
            "UPDATE WorkingHoursView SET StartTime = '10:00' WHERE WorkingHoursID = 1")
        self.conn.commit()

        self.cursor.execute("SELECT * FROM WorkingHoursAudit")
        result = self.cursor.fetchone()
        self.assertEqual(result, (1, 1, 1, '10:00', '17:00', 'Update'))

    def test_workinghours_view_delete_audit(self):
        # Insert test data into Employee and WorkingHours tables
        self.cursor.execute("INSERT INTO Employee (OrganizationID, FirstName, LastName, Email, PhoneNumber, Position, HireDate, IsActive) VALUES (1, 'John', 'Doe', 'john.doe@example.com', '+1234567890', 'Software Engineer', '2022-01-01', 1)")
        self.conn.commit()

        self.cursor.execute(
            "INSERT INTO WorkingHours (EmployeeID, StartTime, EndTime, CustomAmount) VALUES (1, '09:00', '17:00', 0)")
        self.conn.commit()

        # Test the INSTEAD OF DELETE trigger on WorkingHoursView
        self.cursor.execute(
            "DELETE FROM WorkingHoursView WHERE WorkingHoursID = 1")
        self.conn.commit()

        self.cursor.execute("SELECT * FROM WorkingHoursAudit")
        result = self.cursor.fetchone()
        self.assertEqual(result, (1, 1, 1, '09:00', '17:00', 'Delete'))
