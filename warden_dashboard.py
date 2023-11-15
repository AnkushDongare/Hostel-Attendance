# warden_dashboard.py
from tkinter import ttk
from database_manager import DatabaseManager
from ui_manager import UIManager

WELCOME_LABEL_FONT = ("Arial", 16, "bold")
CARD_TITLE_FONT = ("Arial", 12, "bold")
CARD_VALUE_FONT = ("Arial", 14)
ROOM_LABEL_FONT = ("Arial", 14, "bold")  # Increased font size for room label
LOGOUT_BUTTON_STYLE = "Accent.TButton"

def open_warden_dashboard(root):
    warden_dashboard = UIManager.create_main_window("Warden Dashboard")

    # Set the warden dashboard dimensions to match the screen resolution
    screen_width = warden_dashboard.winfo_screenwidth()
    screen_height = warden_dashboard.winfo_screenheight()
    warden_dashboard.geometry(f"{screen_width}x{screen_height}+0+0")

    warden_content_frame = ttk.Frame(warden_dashboard)
    warden_content_frame.pack(fill="both", expand=True, padx=20, pady=20)  # Added padding for better spacing

    welcome_label = ttk.Label(warden_content_frame, text="Welcome, Warden", font=WELCOME_LABEL_FONT, background="#3498db", foreground="white")
    welcome_label.grid(row=0, column=0, columnspan=2, pady=(20, 10))  # Used grid for consistent layout management

    def create_card(title, value, row, col):
        card_frame = ttk.Frame(warden_content_frame, style="Card.TFrame")
        card_frame.grid(row=row, column=col, padx=10, pady=10)  # Used grid for more control over layout

        title_label = ttk.Label(card_frame, text=title, font=CARD_TITLE_FONT, background="#3498db", foreground="white")
        title_label.grid(row=0, column=0, pady=(10, 5))

        value_label = ttk.Label(card_frame, text=value, font=CARD_VALUE_FONT, background="#3498db", foreground="white")
        value_label.grid(row=1, column=0, pady=5)

    current_warden_name = DatabaseManager.get_current_warden_name()
    total_students = DatabaseManager.get_total_students()
    total_present_students = DatabaseManager.get_total_present_students()
    present_students_per_room = DatabaseManager.get_present_students_per_room()
    total_absent_students = total_students - total_present_students

    create_card("Current Warden Name", current_warden_name, 1, 0)
    create_card("Total Students", total_students, 1, 1)
    create_card("Total Present Students", total_present_students, 2, 0)
    create_card("Total Absent Students", total_absent_students, 2, 1)

    room_label = ttk.Label(warden_content_frame, text="Present Students per Room:", font=ROOM_LABEL_FONT, background="#3498db", foreground="white")
    room_label.grid(row=3, column=0, columnspan=2, pady=(20, 10))

    row_num = 4
    col_num = 0

    for room, present_count in present_students_per_room.items():
        create_card(room, present_count, row_num, col_num)

        col_num += 1
        if col_num >= 2:
            col_num = 0
            row_num += 1

    logout_button = ttk.Button(warden_dashboard, text="Logout", command=warden_dashboard.destroy, style=LOGOUT_BUTTON_STYLE)
    logout_button.grid(row=row_num, column=col_num, columnspan=2, pady=10)  # Placed logout button in the next row

    style = ttk.Style()
    style.configure("Card.TFrame", background="#ecf0f1", borderwidth=2, relief="solid")  # Changed background color
    style.map("Card.TFrame", background=[("active", "#3498db")])

    warden_dashboard.mainloop()
