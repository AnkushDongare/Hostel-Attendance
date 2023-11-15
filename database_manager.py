# database_manager.py
import sqlite3

DATABASE_FILE = "database/hostel_database.db"

QUERY_ADMIN_LOGIN = "SELECT username, password FROM admin_credentials WHERE username = ?"
QUERY_WARDEN_LOGIN = "SELECT username, password FROM warden_credentials WHERE username = ?"

class DatabaseManager:
    @staticmethod
    def check_login_credentials(query, username, password):
        with sqlite3.connect(DATABASE_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (username,))
            data = cursor.fetchone()
            if data:
                db_username, db_password = data
                return password == db_password
        return False

    @staticmethod
    def get_current_warden_name():
        with sqlite3.connect(DATABASE_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT username FROM warden_credentials WHERE id = 1")
            data = cursor.fetchone()
            if data:
                return data[0]
        return "Unknown"

    @staticmethod
    def get_total_wardens():
        with sqlite3.connect(DATABASE_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM warden_credentials")
            data = cursor.fetchone()
            if data:
                return data[0]
        return 0


    @staticmethod
    def get_total_students():
        with sqlite3.connect(DATABASE_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM students")
            data = cursor.fetchone()
            if data:
                return data[0]
        return 0

    @staticmethod
    def get_total_present_students():
        with sqlite3.connect(DATABASE_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM students WHERE clock_in_status = 1")
            data = cursor.fetchone()
            if data:
                return data[0]
        return 0

    @staticmethod
    def get_total_rooms():
        with sqlite3.connect(DATABASE_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT COUNT(DISTINCT room_no) FROM students")
            data = cursor.fetchall()
            if data:
                return data[0]
            return 0

    @staticmethod
    def get_present_students_per_room():
        present_students_per_room = {}
        with sqlite3.connect(DATABASE_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT room_no, COUNT(*) FROM students GROUP BY room_no")
            data = cursor.fetchall()
            for room, count in data:
                present_students_per_room[room] = count
        return present_students_per_room