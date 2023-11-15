import sqlite3
from datetime import datetime

# Constants
DATABASE_FILE = "hostel_database.db"

def create_table(cursor, table_definition):
    cursor.execute(table_definition)

def insert_data(cursor, table_name, data):
    cursor.execute(f"INSERT INTO {table_name} VALUES ({', '.join(['?' for _ in data])})", data)

def initialize_database():
    # Connect to the SQLite database (it will be created if it doesn't exist)
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    # Create admin_credentials table
    create_table(cursor, '''
        CREATE TABLE IF NOT EXISTS admin_credentials (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # Insert sample data into admin_credentials
    insert_data(cursor, "admin_credentials", (1, "admin", "admin"))

    # Create warden_credentials table
    create_table(cursor, '''
        CREATE TABLE IF NOT EXISTS warden_credentials (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # Insert sample data into warden_credentials
    insert_data(cursor, "warden_credentials", (1, "warden", "pass"))

    # Create rooms table
    create_table(cursor, '''
        CREATE TABLE IF NOT EXISTS rooms (
            sr INTEGER PRIMARY KEY AUTOINCREMENT,
            room_id TEXT,
            room_no TEXT,
            room_vac INTEGER
        )
    ''')

    # Insert sample data into rooms
    insert_data(cursor, "rooms", (1, "R101", "101", 2))
    insert_data(cursor, "rooms", (2, "R102", "102", 1))

    # Create students table
    create_table(cursor, '''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            gender TEXT,
            age INTEGER,
            roll_no TEXT,
            student_id TEXT UNIQUE NOT NULL,
            email TEXT,
            phone TEXT,
            course TEXT,
            class TEXT,
            semester INTEGER,
            year INTEGER,
            room_no TEXT,
            sample_radio TEXT,
            clock_in_status INTEGER DEFAULT 1,
            FOREIGN KEY (room_no) REFERENCES rooms (room_no)
        )
    ''')

    # Insert sample data into students
    insert_data(cursor, "students", (1, "John Doe", "Male", 20, "RD001", "S001", "john@example.com", "1234567890", "Engineering", "A", 1, 2023, "101", "Sample Radio", 1))
    insert_data(cursor, "students", (2, "Jane Doe", "Female", 22, "RD002", "S002", "jane@example.com", "9876543210", "Business", "B", 1, 2023, "102", "Sample Radio", 1))

    # Create leave_requests table
    create_table(cursor, '''
        CREATE TABLE IF NOT EXISTS leave_record (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT,
            leave_start_time DATETIME,
            leave_end_time DATETIME,
            reason TEXT,
            FOREIGN KEY (student_id) REFERENCES students (student_id)
        )
    ''')

    # Insert sample data into leave_record
    insert_data(cursor, "leave_record", (1, "S001", "2023-11-01 08:00:00", "2023-11-05 18:00:00", "Family vacation"))
    insert_data(cursor, "leave_record", (2, "S002", "2023-12-10 12:00:00", "2023-12-15 20:00:00", "Personal reasons"))

    # Create attendance table
    create_table(cursor, '''
        CREATE TABLE IF NOT EXISTS attendance (
            sr INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT,
            clock_out_time DATETIME,
            clock_in_time DATETIME,
            status_code INTEGER DEFAULT 1,
            FOREIGN KEY (student_id) REFERENCES students (student_id)
        )
    ''')

    # Insert sample data into attendance
    insert_data(cursor, "attendance", (1, "S001", "2023-11-01 08:00:00", "2023-11-01 18:00:00", 1))
    insert_data(cursor, "attendance", (2, "S002", "2023-12-10 12:00:00", "2023-12-10 20:00:00", 1))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    print("Database and tables created, and sample data inserted.")

if __name__ == "__main__":
    initialize_database()
