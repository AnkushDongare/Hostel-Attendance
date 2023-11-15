# main.py
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import PhotoImage
from PIL import Image, ImageTk
from database_manager import DatabaseManager, QUERY_ADMIN_LOGIN, QUERY_WARDEN_LOGIN
from ui_manager import UIManager
from admin_dashboard import open_admin_dashboard
from warden_dashboard import open_warden_dashboard
from face_recognition import verify_face

def main():
    root = UIManager.create_main_window("Hostel Face Recognition Attendance System")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{screen_width}x{screen_height}+0+0")

    frame = ttk.Frame(root, style="Accent.TFrame")
    frame.pack(fill="both", expand=True)

    # Load and display an image at the top of the application
    image = Image.open("./assets/1.jpg")
    image = image.resize((screen_width, 200))
    photo = ImageTk.PhotoImage(image)

    image_label = ttk.Label(frame, image=photo)
    image_label.image = photo
    image_label.pack()

    title_label = ttk.Label(frame, text="Hostel Face Recognition Attendance System", font=("Arial", 24, "bold"), style="Title.TLabel")
    title_label.pack(pady=(30, 30))

    button_frame = ttk.Frame(frame, style="Accent.TFrame")
    button_frame.pack()

    admin_button = UIManager.create_button_with_icon(button_frame, "Admin Login", "assets/admin_icon.png", lambda: show_login_popup(admin_login, "Admin", QUERY_ADMIN_LOGIN, root))
    warden_button = UIManager.create_button_with_icon(button_frame, "Warden Login", "assets/warden_icon.png", lambda: show_login_popup(warden_login, "Warden", QUERY_WARDEN_LOGIN, root))
    attendance_button = UIManager.create_button_with_icon(button_frame, "Attendance", "assets/attendance_icon.png", verify_face)

    admin_button.pack(side="left", padx=20)
    warden_button.pack(side="left", padx=20)
    attendance_button.pack(side="left", padx=20)

    root.mainloop()

def show_login_popup(login_func, login_type, query, root):
    login_popup = tk.Toplevel(root)
    login_popup.title(f"{login_type} Login")

    popup_width = 300
    popup_height = 200

    x = root.winfo_x() + (root.winfo_width() - popup_width) // 2
    y = root.winfo_y() + (root.winfo_height() - popup_height) // 2

    login_popup.geometry(f"{popup_width}x{popup_height}+{x}+{y}")

    username_label = ttk.Label(login_popup, text="Username:")
    username_label.pack(pady=(10, 5))

    username_entry = ttk.Entry(login_popup)
    username_entry.pack(pady=5)

    password_label = ttk.Label(login_popup, text="Password:")
    password_label.pack(pady=5)

    password_entry = ttk.Entry(login_popup, show="*")
    password_entry.pack(pady=5)

    login_button = ttk.Button(login_popup, text="Login", command=lambda ue=username_entry, pe=password_entry, lp=login_popup, q=query, r=root: login_func(ue.get(), pe.get(), lp, q, r))
    login_button.pack(pady=10)

    login_popup.mainloop()

def admin_login(username, password, login_popup, query, root):
    if DatabaseManager.check_login_credentials(query, username, password):
        login_popup.destroy()
        open_admin_dashboard(root)

def warden_login(username, password, login_popup, query, root):
    if DatabaseManager.check_login_credentials(query, username, password):
        login_popup.destroy()
        open_warden_dashboard(root)

if __name__ == "__main__":
    main()