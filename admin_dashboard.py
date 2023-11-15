# admin_dashboard.py
import tkinter as tk
from tkinter import ttk, messagebox
from database_manager import DatabaseManager
from student import open_student_management_dashboard
from room_management_dashbaord import create_rooms_management_dashboard
import os

def open_admin_dashboard(root):
    admin_window = tk.Toplevel(root)
    admin_window.title("Admin Dashboard")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    admin_window.geometry(f"{screen_width}x{screen_height}+0+0")

    # Main Frame
    main_frame = ttk.Frame(admin_window, style="Accent.TFrame")
    main_frame.pack(fill=tk.BOTH, expand=True)

    title_label = ttk.Label(main_frame, text="Admin Dashboard", font=("Helvetica", 24, "bold"))
    title_label.pack(pady=20)

    # Statistics Frame
    stats_frame = ttk.Frame(main_frame, style="Accent.TFrame")
    stats_frame.pack(pady=20)

    current_warden_name = DatabaseManager.get_current_warden_name()
    total_students = DatabaseManager.get_total_students()
    total_wardens = DatabaseManager.get_total_wardens()
    total_present_students = DatabaseManager.get_total_present_students()
    present_students_per_room = DatabaseManager.get_present_students_per_room()
    get_total_rooms = DatabaseManager.get_total_rooms()
    total_absent_students = total_students - total_present_students

    total_student_text = ttk.Label(stats_frame, text="Total Students", font=("Helvetica", 16))
    total_student_text.grid(row=0, column=0, padx=10, pady=5, sticky="w")

    total_student_number = ttk.Label(stats_frame, text=total_students, font=("Helvetica", 16, "bold"))
    total_student_number.grid(row=1, column=0, padx=10, pady=5, sticky="w")

    total_present_student_text = ttk.Label(stats_frame, text="Present Students", font=("Helvetica", 16))
    total_present_student_text.grid(row=0, column=1, padx=10, pady=5, sticky="w")

    total_present_student_number = ttk.Label(stats_frame, text=total_present_students, font=("Helvetica", 16, "bold"))
    total_present_student_number.grid(row=1, column=1, padx=10, pady=5, sticky="w")

    total_absent_student_text = ttk.Label(stats_frame, text="Absent Students", font=("Helvetica", 16))
    total_absent_student_text.grid(row=0, column=2, padx=10, pady=5, sticky="w")

    total_absent_student_number = ttk.Label(stats_frame, text=total_absent_students, font=("Helvetica", 16, "bold"))
    total_absent_student_number.grid(row=1, column=2, padx=10, pady=5, sticky="w")

    total_warden_text = ttk.Label(stats_frame, text="Total Warden", font=("Helvetica", 16))
    total_warden_text.grid(row=0, column=3, padx=10, pady=5, sticky="w")

    total_absent_warden_number = ttk.Label(stats_frame, text=total_wardens, font=("Helvetica", 16, "bold"))
    total_absent_warden_number.grid(row=1, column=3, padx=10, pady=5, sticky="w")

    total_warden_name_text = ttk.Label(stats_frame, text="Current Warden Name", font=("Helvetica", 16))
    total_warden_name_text.grid(row=0, column=4, padx=10, pady=5, sticky="w")

    total_warden_name_number = ttk.Label(stats_frame, text=current_warden_name, font=("Helvetica", 16, "bold"))
    total_warden_name_number.grid(row=1, column=4, padx=10, pady=5, sticky="w")

    total_room_text = ttk.Label(stats_frame, text="Total Rooms:", font=("Helvetica", 16))  # Fixed label variable name
    total_room_text.grid(row=3, column=0, padx=10, pady=5, sticky="w")

    total_room_number = ttk.Label(stats_frame, text=get_total_rooms, font=("Helvetica", 16, "bold"))  # Fixed label variable name
    total_room_number.grid(row=3, column=1, padx=10, pady=5, sticky="w")

    students_per_room = ttk.Label(stats_frame, text="Students per Room", font=("Helvetica", 16))  # Fixed label variable name
    students_per_room.grid(row=4, column=0, padx=10, pady=5, sticky="w")

    row_num = 5
    col_num = 0
    total_availability = 5
    for room, present_count in present_students_per_room.items():
        
        if (total_availability - present_count) <= 0:
            color = "red"
        else:
            color= "green"
        students_per_room_number = ttk.Label(stats_frame, text=f"{room}: {present_count} / vacancy {total_availability - present_count}", font=("Helvetica", 16, "bold"), foreground=color)
        students_per_room_number.grid(row=row_num, column=col_num, padx=10, pady=5, sticky="w")
        col_num += 1
        if col_num >= 5:
            col_num = 0
            row_num += 1

    # Buttons
    buttons_frame = ttk.Frame(main_frame, style="Accent.TFrame")
    buttons_frame.pack(pady=20)

    student_button = ttk.Button(buttons_frame, text="Manage Students", command=lambda: open_student_management_dashboard(root))
    student_button.pack(side=tk.LEFT, padx=10)

    image_button = ttk.Button(buttons_frame, text="View Image Samples", command=lambda: open_image_folder(root))
    image_button.pack(side=tk.LEFT, padx=10)

    room_button = ttk.Button(buttons_frame, text="Room Management", command=lambda: create_rooms_management_dashboard(root))
    room_button.pack(side=tk.LEFT, padx=10)

    #TODO button to destroy this screen not the root
    logout_button = ttk.Button(buttons_frame, text="Logout", command=admin_window.destroy)
    logout_button.pack(side=tk.LEFT, padx=20)

def open_image_folder(root):
    os.startfile("image_samples")

if __name__ == "__main__":
    root = tk.Tk()

    style = ttk.Style()
    style.configure("Accent.TLabel", font=("Helvetica", 12))
    style.configure("Accent.TButton", font=("Helvetica", 12))
    style.configure("Accent.TFrame", background="#f2f2f2")

    open_admin_dashboard(root)
    root.mainloop()
