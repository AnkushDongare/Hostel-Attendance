import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime

# Constants
DATABASE_FILE = "hostel_database.db"

class LeaveRequestGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Leave Request System")
        self.root.geometry("400x300")

        # Student Leave Request Frame
        self.student_frame = tk.Frame(root)
        self.student_frame.pack(pady=10)
        self.create_student_widgets()

        # Admin Interface Frame
        self.admin_frame = tk.Frame(root)
        self.admin_frame.pack(pady=10)
        self.create_admin_widgets()

    def create_student_widgets(self):
        # Student Leave Request Heading
        self.label_heading_student = tk.Label(self.student_frame, text="Student Leave Request")
        self.label_heading_student.pack(pady=5)

        # Student ID Label and Entry
        self.label_student_id = tk.Label(self.student_frame, text="Student ID:")
        self.label_student_id.pack(pady=5)
        self.entry_student_id = tk.Entry(self.student_frame)
        self.entry_student_id.pack(pady=5)

        # Leave Start Time Label and Entry
        self.label_leave_start = tk.Label(self.student_frame, text="Leave Start Time (YYYY-MM-DD HH:mm):")
        self.label_leave_start.pack(pady=5)
        self.entry_leave_start = tk.Entry(self.student_frame)
        self.entry_leave_start.pack(pady=5)

        # Leave End Time Label and Entry
        self.label_leave_end = tk.Label(self.student_frame, text="Leave End Time (YYYY-MM-DD HH:mm):")
        self.label_leave_end.pack(pady=5)
        self.entry_leave_end = tk.Entry(self.student_frame)
        self.entry_leave_end.pack(pady=5)

        # Reason Label and Entry
        self.label_reason = tk.Label(self.student_frame, text="Reason:")
        self.label_reason.pack(pady=5)
        self.entry_reason = tk.Entry(self.student_frame)
        self.entry_reason.pack(pady=5)

        # Submit Button
        self.submit_button = tk.Button(self.student_frame, text="Submit", command=self.submit_leave_request)
        self.submit_button.pack(pady=10)

    def create_admin_widgets(self):
        # Admin Interface Heading
        self.label_heading_admin = tk.Label(self.admin_frame, text="Admin Interface")
        self.label_heading_admin.pack(pady=5)

        # Listbox to display leave requests
        self.leave_requests_listbox = tk.Listbox(self.admin_frame, selectmode=tk.SINGLE, height=5, width=50)
        self.leave_requests_listbox.pack(pady=5)

        # Accept and Reject Buttons
        self.accept_button = tk.Button(self.admin_frame, text="Accept", command=self.accept_leave_request)
        self.accept_button.pack(pady=5)
        self.reject_button = tk.Button(self.admin_frame, text="Reject", command=self.reject_leave_request)
        self.reject_button.pack(pady=5)

        # Load leave requests
        self.load_leave_requests()

    def submit_leave_request(self):
        student_id = self.entry_student_id.get()
        leave_start = self.entry_leave_start.get()
        leave_end = self.entry_leave_end.get()
        reason = self.entry_reason.get()

        try:
            # Connect to the SQLite database
            conn = sqlite3.connect(DATABASE_FILE)
            cursor = conn.cursor()

            # Insert leave request into the database
            cursor.execute("INSERT INTO leave_requests (student_id, leave_start_time, leave_end_time, reason) VALUES (?, ?, ?, ?)",
                           (student_id, leave_start, leave_end, reason))

            # Commit the changes
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Leave request submitted successfully.")
            self.clear_entries()

            # Reload leave requests for admin interface
            self.load_leave_requests()

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Database error: {e}")

    def load_leave_requests(self):
        try:
            # Connect to the SQLite database
            conn = sqlite3.connect(DATABASE_FILE)
            cursor = conn.cursor()

            # Fetch leave requests from the database
            cursor.execute("SELECT id, student_id, leave_start_time, leave_end_time, reason, status FROM leave_requests")
            leave_requests = cursor.fetchall()

            # Clear existing items in the listbox
            self.leave_requests_listbox.delete(0, tk.END)

            # Populate the listbox with leave requests
            for leave_request in leave_requests:
                status = "Pending" if leave_request[5] == "pending" else leave_request[5].capitalize()
                item = f"ID: {leave_request[0]}, Student ID: {leave_request[1]}, Start: {leave_request[2]}, End: {leave_request[3]}, Reason: {leave_request[4]}, Status: {status}"
                self.leave_requests_listbox.insert(tk.END, item)

            conn.close()

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Database error: {e}")

    def accept_leave_request(self):
        selected_index = self.leave_requests_listbox.curselection()
        if selected_index:
            leave_request_id = self.leave_requests_listbox.get(selected_index).split(",")[0].split(":")[1].strip()

            try:
                # Connect to the SQLite database
                conn = sqlite3.connect(DATABASE_FILE)
                cursor = conn.cursor()

                # Update leave request status to "approved"
                cursor.execute("UPDATE leave_requests SET status = 'approved' WHERE id = ?", (leave_request_id,))

                # Commit the changes
                conn.commit()
                conn.close()

                messagebox.showinfo("Success", "Leave request approved.")
                self.load_leave_requests()

            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Database error: {e}")

    def reject_leave_request(self):
        selected_index = self.leave_requests_listbox.curselection()
        if selected_index:
            leave_request_id = self.leave_requests_listbox.get(selected_index).split(",")[0].split(":")[1].strip()

            try:
                # Connect to the SQLite database
                conn = sqlite3.connect(DATABASE_FILE)
                cursor = conn.cursor()

                # Update leave request status to "rejected"
                cursor.execute("UPDATE leave_requests SET status = 'rejected' WHERE id = ?", (leave_request_id,))

                # Commit the changes
                conn.commit()
                conn.close()

                messagebox.showinfo("Success", "Leave request rejected.")
                self.load_leave_requests()

            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Database error: {e}")

    def clear_entries(self):
        self.entry_student_id.delete(0, tk.END)
        self.entry_leave_start.delete(0, tk.END)
        self.entry_leave_end.delete(0, tk.END)
        self.entry_reason.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = LeaveRequestGUI(root)
    root.mainloop()
