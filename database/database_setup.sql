CREATE TABLE Organization (
  OrganizationID INTEGER PRIMARY KEY AUTOINCREMENT,
  Name TEXT
);

CREATE TABLE Employee (
  EmployeeID INTEGER PRIMARY KEY AUTOINCREMENT,
  OrganizationID INTEGER,
  FirstName TEXT,
  LastName TEXT,
  Email TEXT,
  PhoneNumber TEXT,
  Position TEXT,
  HireDate TEXT,
  IsActive BOOLEAN,
  FOREIGN KEY (OrganizationID) REFERENCES Organization(OrganizationID)
);

-- Position and ExtraWages tables modified due to unsupported ENUM and SET
CREATE TABLE Position (
  PositionID INTEGER PRIMARY KEY AUTOINCREMENT,
  ExtraWageID INTEGER,
  FOREIGN KEY (ExtraWageID) REFERENCES ExtraWages(ExtraWageID)
);

CREATE TABLE ExtraWages (
  ExtraWageID INTEGER PRIMARY KEY AUTOINCREMENT,
  PositionID INTEGER,
  WageType TEXT,
  StartTime TEXT,
  EndTime TEXT,
  StartDate TEXT,
  EndDate TEXT,
  RecurrencePattern TEXT,
  RecurrenceDays TEXT,
  HourlyRate REAL,
  FOREIGN KEY (PositionID) REFERENCES Position(PositionID)
);

CREATE TABLE WorkingHours (
  WorkingHoursID INTEGER PRIMARY KEY AUTOINCREMENT,
  EmployeeID INTEGER,
  StartTime TEXT,
  EndTime TEXT,
  CustomAmount REAL,
  FOREIGN KEY (EmployeeID) REFERENCES Employee(EmployeeID)
);

CREATE TABLE User (
  UserID INTEGER PRIMARY KEY AUTOINCREMENT,
  EmployeeID INTEGER,
  Username TEXT,
  PasswordHash TEXT,
  Role TEXT,
  FOREIGN KEY (EmployeeID) REFERENCES Employee(EmployeeID)
);

-- Removed triggers and ModificationType ENUM from WorkingHoursAudit
CREATE TABLE WorkingHoursAudit (
  AuditID INTEGER PRIMARY KEY AUTOINCREMENT,
  WorkingHoursID INTEGER,
  EmployeeID INTEGER,
  StartTime TEXT,
  EndTime TEXT,
  ModificationType TEXT,
  FOREIGN KEY (WorkingHoursID) REFERENCES WorkingHours(WorkingHoursID),
  FOREIGN KEY (EmployeeID) REFERENCES Employee(EmployeeID)
);

-- Create a view for the WorkingHours table
CREATE VIEW WorkingHoursView AS
SELECT * FROM WorkingHours;

-- Create INSTEAD OF INSERT trigger
CREATE TRIGGER workinghours_insert_audit
INSTEAD OF INSERT ON WorkingHoursView
BEGIN
  -- Insert into WorkingHours table
  INSERT INTO WorkingHours (EmployeeID, StartTime, EndTime, CustomAmount)
  VALUES (NEW.EmployeeID, NEW.StartTime, NEW.EndTime, NEW.CustomAmount);

  -- Insert into WorkingHoursAudit table
  INSERT INTO WorkingHoursAudit (WorkingHoursID, EmployeeID, StartTime, EndTime, ModificationType)
  VALUES ((SELECT last_insert_rowid()), NEW.EmployeeID, NEW.StartTime, NEW.EndTime, 'Insert');
END;

-- Create INSTEAD OF UPDATE trigger
CREATE TRIGGER workinghours_update_audit
INSTEAD OF UPDATE ON WorkingHoursView
BEGIN
  -- Update the WorkingHours table
  UPDATE WorkingHours
  SET EmployeeID = NEW.EmployeeID, StartTime = NEW.StartTime, EndTime = NEW.EndTime, CustomAmount = NEW.CustomAmount
  WHERE WorkingHoursID = OLD.WorkingHoursID;

  -- Insert into WorkingHoursAudit table
  INSERT INTO WorkingHoursAudit (WorkingHoursID, EmployeeID, StartTime, EndTime, ModificationType)
  VALUES (OLD.WorkingHoursID, NEW.EmployeeID, NEW.StartTime, NEW.EndTime, 'Update');
END;

-- Create INSTEAD OF DELETE trigger
CREATE TRIGGER workinghours_delete_audit
INSTEAD OF DELETE ON WorkingHoursView
BEGIN
  -- Insert into WorkingHoursAudit table
  INSERT INTO WorkingHoursAudit (WorkingHoursID, EmployeeID, StartTime, EndTime, ModificationType)
  VALUES (OLD.WorkingHoursID, OLD.EmployeeID, OLD.StartTime, OLD.EndTime, 'Delete');

  -- Delete from WorkingHours table
  DELETE FROM WorkingHours
  WHERE WorkingHoursID = OLD.WorkingHoursID;
END;
