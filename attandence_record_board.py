import tkinter as tk
from tkinter import ttk
import sqlite3
from datetime import datetime

DATABASE_FILE = "database/hostel_database.db"

class AttendanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Attendance Record System")

        # Create a notebook (tabbed interface)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Create tabs
        self.create_student_tab()
        self.create_leave_tab()

    def create_student_tab(self):
        student_tab = ttk.Frame(self.notebook)
        self.notebook.add(student_tab, text="Students")

        # Create widgets for the Students tab
        self.student_tree = ttk.Treeview(student_tab, columns=("ID", "Name", "Roll No", "Status"))
        self.student_tree.heading("#0", text="ID")
        self.student_tree.column("#0", width=50, anchor=tk.CENTER)
        self.student_tree.heading("ID", text="ID")
        self.student_tree.heading("Name", text="Name")
        self.student_tree.heading("Roll No", text="Roll No")
        self.student_tree.heading("Status", text="Status")

        self.student_tree.pack(fill=tk.BOTH, expand=True)

        # Buttons for marking attendance, displaying details, editing data, and adding leave
        mark_attendance_button = tk.Button(student_tab, text="Mark Attendance", command=self.mark_attendance)
        mark_attendance_button.pack(pady=5)
        
        display_details_button = tk.Button(student_tab, text="Display Details", command=self.display_student_details)
        display_details_button.pack(pady=5)

        edit_data_button = tk.Button(student_tab, text="Edit Data", command=self.edit_student_data)
        edit_data_button.pack(pady=5)

        add_leave_button = tk.Button(student_tab, text="Add Leave", command=self.add_leave)
        add_leave_button.pack(pady=5)

        resume_attendance_button = tk.Button(student_tab, text="Resume Attendance", command=self.resume_attendance)
        resume_attendance_button.pack(pady=5)

        # Connect to the database and populate the treeview
        self.populate_student_tree()

    def create_leave_tab(self):
        leave_tab = ttk.Frame(self.notebook)
        self.notebook.add(leave_tab, text="Leave Requests")

        # Create widgets for the Leave Requests tab
        self.leave_tree = ttk.Treeview(leave_tab, columns=("ID", "Student ID", "Start Time", "End Time", "Reason"))
        self.leave_tree.heading("#0", text="ID")
        self.leave_tree.column("#0", width=50, anchor=tk.CENTER)
        self.leave_tree.heading("ID", text="ID")
        self.leave_tree.heading("Student ID", text="Student ID")
        self.leave_tree.heading("Start Time", text="Start Time")
        self.leave_tree.heading("End Time", text="End Time")
        self.leave_tree.heading("Reason", text="Reason")

        self.leave_tree.pack(fill=tk.BOTH, expand=True)

        # Button for handling leave requests
        handle_leave_button = tk.Button(leave_tab, text="Handle Leave Request", command=self.handle_leave_request)
        handle_leave_button.pack(pady=5)

        # Connect to the database and populate the treeview
        self.populate_leave_tree()

    def populate_student_tree(self):
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()

        cursor.execute("SELECT id, name, roll_no, clock_in_status FROM students")
        for row in cursor.fetchall():
            status = "Present" if row[3] == 1 else "Absent"
            self.student_tree.insert("", "end", values=(row[0], row[1], row[2], status))

        conn.close()

    def populate_leave_tree(self):
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()

        cursor.execute("SELECT id, student_id, leave_start_time, leave_end_time, reason FROM leave_record")
        for row in cursor.fetchall():
            self.leave_tree.insert("", "end", values=(row[0], row[1], row[2], row[3], row[4]))

        conn.close()

    def mark_attendance(self):
        selected_item = self.student_tree.selection()
        if selected_item:
            student_id = self.student_tree.item(selected_item, "values")[0]
            conn = sqlite3.connect(DATABASE_FILE)
            cursor = conn.cursor()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            try:
                cursor.execute("INSERT INTO attendance (student_id, clock_in_time, status_code) VALUES (?, ?, ?);",
                               (student_id, timestamp, 1))
                conn.commit()
                self.populate_student_tree()  # Refresh the treeview
            except sqlite3.Error as e:
                print(f"Error marking attendance: {e}")
            finally:
                conn.close()

    def display_student_details(self):
        selected_item = self.student_tree.selection()
        if selected_item:
            student_id = self.student_tree.item(selected_item, "values")[0]
            conn = sqlite3.connect(DATABASE_FILE)
            cursor = conn.cursor()

            try:
                cursor.execute("SELECT * FROM students WHERE id = ?;", (student_id,))
                student_data = cursor.fetchone()
                if student_data:
                    details_window = tk.Toplevel(self.root)
                    details_window.title("Student Details")

                    # Display student details in a new window
                    for i, field in enumerate(student_data):
                        label = tk.Label(details_window, text=f"{self.student_tree.heading(i)['text']}: {field}")
                        label.pack()

            except sqlite3.Error as e:
                print(f"Error fetching student details: {e}")
            finally:
                conn.close()

    def edit_student_data(self):
        selected_item = self.student_tree.selection()
        if selected_item:
            student_id = self.student_tree.item(selected_item, "values")[0]
            conn = sqlite3.connect(DATABASE_FILE)
            cursor = conn.cursor()

            try:
                cursor.execute("SELECT * FROM students WHERE id = ?;", (student_id,))
                student_data = cursor.fetchone()
                if student_data:
                    edit_window = tk.Toplevel(self.root)
                    edit_window.title("Edit Student Data")

                    # Create entry fields to edit data
                    entries = []
                    for i, field in enumerate(student_data[1:]):  # Exclude the ID field
                        label = tk.Label(edit_window, text=f"{self.student_tree.heading(i+1)['text']}:")
                        label.grid(row=i, column=0, pady=5, padx=5, sticky=tk.E)

                        entry_var = tk.StringVar()
                        entry_var.set(field)
                        entry = tk.Entry(edit_window, textvariable=entry_var)
                        entry.grid(row=i, column=1, pady=5, padx=5, sticky=tk.W)
                        entries.append(entry_var)

                    # Button to save changes
                    save_button = tk.Button(edit_window, text="Save Changes", command=lambda: self.save_student_changes(student_id, entries, edit_window))
                    save_button.grid(row=len(student_data)-1, columnspan=2, pady=10)

            except sqlite3.Error as e:
                print(f"Error fetching student details: {e}")
            finally:
                conn.close()

    def save_student_changes(self, student_id, entries, edit_window):
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()

        try:
            # Update the student data in the database
            cursor.execute("UPDATE students SET name=?, gender=?, age=?, roll_no=?, email=?, phone=?, course=?, class=?, semester=?, year=?, room_no=?, sample_radio=? WHERE id=?;",
                           (*[entry.get() for entry in entries], student_id))
            conn.commit()
            edit_window.destroy()
            self.populate_student_tree()  # Refresh the treeview
        except sqlite3.Error as e:
            print(f"Error updating student data: {e}")
        finally:
            conn.close()

    def add_leave(self):
        selected_item = self.student_tree.selection()
        if selected_item:
            student_id = self.student_tree.item(selected_item, "values")[0]
            start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            end_time = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")  # Example: leave for one day

            conn = sqlite3.connect(DATABASE_FILE)
            cursor = conn.cursor()

            try:
                cursor.execute("INSERT INTO leave_record (student_id, leave_start_time, leave_end_time, reason) VALUES (?, ?, ?, ?);",
                               (student_id, start_time, end_time, "Vacation"))
                conn.commit()
                self.populate_leave_tree()  # Refresh the treeview
            except sqlite3.Error as e:
                print(f"Error adding leave: {e}")
            finally:
                conn.close()

    def resume_attendance(self):
        selected_item = self.student_tree.selection()
        if selected_item:
            student_id = self.student_tree.item(selected_item, "values")[0]
            conn = sqlite3.connect(DATABASE_FILE)
            cursor = conn.cursor()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            try:
                cursor.execute("INSERT INTO attendance (student_id, clock_in_time, status_code) VALUES (?, ?, ?);",
                               (student_id, timestamp, 1))
                conn.commit()
                self.populate_student_tree()  # Refresh the treeview
            except sqlite3.Error as e:
                print(f"Error resuming attendance: {e}")
            finally:
                conn.close()

    def handle_leave_request(self):
        selected_item = self.leave_tree.selection()
        if selected_item:
            leave_id = self.leave_tree.item(selected_item, "values")[0]
            conn = sqlite3.connect(DATABASE_FILE)
            cursor = conn.cursor()

            try:
                cursor.execute("DELETE FROM leave_record WHERE id = ?;", (leave_id,))
                conn.commit()
                self.populate_leave_tree()  # Refresh the treeview
            except sqlite3.Error as e:
                print(f"Error handling leave request: {e}")
            finally:
                conn.close()


if __name__ == "__main__":
    root = tk.Tk()
    app = AttendanceApp(root)
    root.geometry("800x600")
    root.mainloop()
