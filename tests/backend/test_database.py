import unittest
import sqlite3


class DatabaseTests(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(':memory:')
        self.cursor = self.conn.cursor()

        with open('../../database/database_setup.sql', 'r') as file:
            schema = file.read()

        self.cursor.executescript(schema)
        self.conn.commit()

    def tearDown(self):
        self.conn.close()

    def test_insert_organization(self):
        self.cursor.execute(
            "INSERT INTO Organization (Name) VALUES ('Test Organization')")
        self.conn.commit()

        self.cursor.execute("SELECT * FROM Organization")
        result = self.cursor.fetchone()
        self.assertEqual(result, (1, 'Test Organization'))

    def test_insert_employee(self):
        # Insert organization first, as OrganizationID is a foreign key in Employee table
        self.cursor.execute(
            "INSERT INTO Organization (Name) VALUES ('Test Organization')")
        self.conn.commit()

        self.cursor.execute(
            "INSERT INTO Employee (OrganizationID, FirstName, LastName, Email, PhoneNumber, Position, HireDate, IsActive) VALUES (1, 'John', 'Doe', 'john.doe@example.com', '+1234567890', 'Software Engineer', '2022-01-01', 1)")
        self.conn.commit()

        self.cursor.execute("SELECT * FROM Employee")
        result = self.cursor.fetchone()
        self.assertEqual(
            result,
            (1, 1, 'John', 'Doe', 'john.doe@example.com', '+1234567890',
             'Software Engineer', '2022-01-01', 1))

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

    def test_insert_position(self):
        self.cursor.execute("INSERT INTO Position (ExtraWageID) VALUES (NULL)")
        self.conn.commit()

        self.cursor.execute("SELECT * FROM Position")
        result = self.cursor.fetchone()
        self.assertEqual(result, (1, None))

    def test_insert_extrawages(self):
        self.cursor.execute("INSERT INTO Position (ExtraWageID) VALUES (NULL)")
        self.conn.commit()

        self.cursor.execute("INSERT INTO ExtraWages (PositionID, WageType, StartTime, EndTime, StartDate, EndDate, RecurrencePattern, RecurrenceDays, HourlyRate) VALUES (1, 'Overtime', '18:00', '20:00', '2022-01-01', '2022-01-31', 'Weekly', 'Monday,Wednesday', 25.00)")
        self.conn.commit()

        self.cursor.execute("SELECT * FROM ExtraWages")
        result = self.cursor.fetchone()
        self.assertEqual(
            result,
            (1, 1, 'Overtime', '18:00', '20:00', '2022-01-01', '2022-01-31',
             'Weekly', 'Monday,Wednesday', 25.00))

    def test_insert_user(self):
        self.cursor.execute("INSERT INTO Employee (OrganizationID, FirstName, LastName, Email, PhoneNumber, Position, HireDate, IsActive) VALUES (1, 'John', 'Doe', 'john.doe@example.com', '+1234567890', 'Software Engineer', '2022-01-01', 1)")
        self.conn.commit()

        self.cursor.execute(
            "INSERT INTO User (EmployeeID, Username, PasswordHash, Role) VALUES (1, 'johndoe', 'hashed_password', 'Admin')")
        self.conn.commit()

        self.cursor.execute("SELECT * FROM User")
        result = self.cursor.fetchone()
        self.assertEqual(result, (1, 1, 'johndoe', 'hashed_password', 'Admin'))

    def test_insert_workinghoursaudit(self):
        self.cursor.execute("INSERT INTO Employee (OrganizationID, FirstName, LastName, Email, PhoneNumber, Position, HireDate, IsActive) VALUES (1, 'John', 'Doe', 'john.doe@example.com', '+1234567890', 'Software Engineer', '2022-01-01', 1)")
        self.conn.commit()

        self.cursor.execute(
            "INSERT INTO WorkingHours (EmployeeID, StartTime, EndTime, CustomAmount) VALUES (1, '09:00', '17:00', 0)")
        self.conn.commit()

        self.cursor.execute(
            "INSERT INTO WorkingHoursAudit (WorkingHoursID, EmployeeID, StartTime, EndTime, ModificationType) VALUES (1, 1, '09:00', '17:00', 'Insert')")
        self.conn.commit()

        self.cursor.execute("SELECT * FROM WorkingHoursAudit")
        result = self.cursor.fetchone()
        self.assertEqual(result, (1, 1, 1, '09:00', '17:00', 'Insert'))


if __name__ == '__main__':
    unittest.main()
