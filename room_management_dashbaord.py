import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.simpledialog import askstring
import sqlite3
from sqlite3 import Error

def create_rooms_management_dashboard(root):
    rooms_window = tk.Toplevel(root)
    rooms_window.title("Rooms Management Dashboard")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    rooms_window.geometry(f"{screen_width}x{screen_height}+0+0")

    rooms_frame = ttk.Frame(rooms_window, style="Accent.TFrame")
    rooms_frame.grid(row=0, column=0, sticky="nsew")
    rooms_frame.grid_rowconfigure(0, weight=1)
    rooms_frame.grid_columnconfigure(0, weight=1)

    right_frame = create_rooms_right_frame(rooms_frame)
    left_frame = create_rooms_left_frame(rooms_frame, rooms_window, right_frame)

    logout_button = ttk.Button(rooms_frame, text="Logout", command=rooms_window.destroy, style="Accent.TButton")
    logout_button.grid(row=1, column=0, pady=20)

def create_rooms_left_frame(parent, root, tree):
    frame = ttk.LabelFrame(parent, text="Room Details", padding=10)
    frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
    parent.grid_rowconfigure(0, weight=1)
    parent.grid_columnconfigure(0, weight=1)

    room_info_frame = ttk.LabelFrame(frame, text="Room Information", padding=10)
    room_info_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    global room_no_entry, capacity_entry

    ttk.Label(room_info_frame, text="Room No:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    room_no_entry = ttk.Entry(room_info_frame)
    room_no_entry.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(room_info_frame, text="Capacity:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    capacity_entry = ttk.Entry(room_info_frame)
    capacity_entry.grid(row=1, column=1, padx=5, pady=5)

    ttk.Button(room_info_frame, text="Save", style="Accent.TButton", command=save_room_data).grid(row=2, column=0, columnspan=2, pady=10)
    ttk.Button(room_info_frame, text="Reset", style="Accent.TButton", command=reset_room_data).grid(row=3, column=0, columnspan=2, pady=10)
    ttk.Button(room_info_frame, text="Update", style="Accent.TButton", command=update_room_data).grid(row=4, column=0, columnspan=2, pady=10)
    ttk.Button(room_info_frame, text="Delete", style="Accent.TButton", command=delete_selected_room).grid(row=5, column=0, columnspan=2, pady=10)

    return frame

def create_rooms_right_frame(parent):
    frame = ttk.LabelFrame(parent, text="Search Details", padding=10)
    frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

    ttk.Label(frame, text="Search:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    global search_entry, search_criteria_combobox
    search_entry = ttk.Entry(frame)
    search_entry.grid(row=0, column=1, padx=5, pady=5, sticky="we")

    ttk.Label(frame, text="Search By:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    search_criteria_combobox = ttk.Combobox(frame, values=["Room No", "Capacity", "All"], style="Accent.TCombobox")
    search_criteria_combobox.grid(row=1, column=1, padx=5, pady=5, sticky="we")
    search_criteria_combobox.set("Room No")

    ttk.Button(frame, text="Search", style="Accent.TButton", command=search_room).grid(row=2, column=0, columnspan=2, padx=5, pady=10, sticky="we")

    # Create a canvas and treeview
    table_canvas = tk.Canvas(frame)
    table_canvas.grid(row=3, column=0, columnspan=2, padx=5, pady=10, sticky="nsew")

    columns = ("Room No", "Capacity")
    global tree
    tree = ttk.Treeview(table_canvas, columns=columns, show="headings")
    populate_rooms_treeview(tree)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)

    tree.grid(row=0, column=0, sticky="nsew")

    v_scrollbar = ttk.Scrollbar(table_canvas, orient="vertical", command=tree.yview)
    h_scrollbar = ttk.Scrollbar(table_canvas, orient="horizontal", command=tree.xview)

    tree.configure(yscrollcommand=v_scrollbar.set)
    tree.configure(xscrollcommand=h_scrollbar.set)

    v_scrollbar.grid(row=0, column=1, sticky="ns")
    h_scrollbar.grid(row=1, column=0, sticky="we")

    return tree

def save_room_data():
    conn = create_connection()
    create_rooms_table(conn)

    room_no = room_no_entry.get()
    capacity = capacity_entry.get()

    query = '''
    INSERT INTO rooms (room_no, room_vac)
    VALUES (?, ?);
    '''
    data = (room_no, capacity)

    try:
        cursor = conn.cursor()
        cursor.execute(query, data)
        conn.commit()
        messagebox.showinfo("Success", "Room data saved successfully!")
        
        tree.delete(*tree.get_children())

        populate_rooms_treeview(tree)
        reset_room_data()
    except Error as e:
        conn.rollback()
        print(e)
        messagebox.showerror("Error", "Failed to save room data.")

    conn.close()

def populate_rooms_treeview(tree):
    conn = create_connection()
    create_rooms_table(conn)

    query = '''
    SELECT room_no, room_vac FROM rooms;
    '''

    try:
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()

        for row in rows:
            tree.insert("", "end", values=row)

    except Error as e:
        print(e)

    conn.close()

def reset_room_data():
    room_no_entry.delete(0, "end")
    capacity_entry.delete(0, "end")

def update_room_data():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Warning", "Please select a room to update.")
        return

    room_no = room_no_entry.get()
    capacity = capacity_entry.get()

    conn = create_connection()
    create_rooms_table(conn)

    query = '''
    UPDATE rooms
    SET room_vac = ?
    WHERE room_no = ?;
    '''
    data = (capacity, room_no)

    try:
        cursor = conn.cursor()
        cursor.execute(query, data)
        conn.commit()
        messagebox.showinfo("Success", "Room data updated successfully!")
        tree.delete(*tree.get_children())

        populate_rooms_treeview(tree)
        reset_room_data()
    except Error as e:
        conn.rollback()
        print(e)
        messagebox.showerror("Error", "Failed to update room data.")

    conn.close()

def delete_selected_room():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Warning", "Please select a room to delete.")
        return

    room_no = tree.item(selected_item, "values")[0]

    conn = create_connection()
    create_rooms_table(conn)

    query = '''
    DELETE FROM rooms
    WHERE room_no = ?;
    '''
    data = (room_no,)

    try:
        cursor = conn.cursor()
        cursor.execute(query, data)
        conn.commit()
        messagebox.showinfo("Success", "Room data deleted successfully!")
        tree.delete(*tree.get_children())

        populate_rooms_treeview(tree)
        reset_room_data()
    except Error as e:
        conn.rollback()
        print(e)
        messagebox.showerror("Error", "Failed to delete room data.")

    conn.close()

def search_room():
    conn = create_connection()
    create_rooms_table(conn)

    search_text = search_entry.get()
    search_criteria = search_criteria_combobox.get()

    query = '''
    SELECT room_no, room_vac FROM rooms
    WHERE {} LIKE ?;
    '''.format(search_criteria.lower())

    data = ('%' + search_text + '%',)

    try:
        cursor = conn.cursor()
        cursor.execute(query, data)
        rows = cursor.fetchall()

        # Clear existing items in the treeview
        tree.delete(*tree.get_children())

        # Insert search results into the treeview
        for row in rows:
            tree.insert("", "end", values=row)

    except Error as e:
        print(e)

    conn.close()

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect("database/hostel_database.db")
        return conn
    except Error as e:
        print(e)

    return conn

def create_rooms_table(conn):
    query = '''
    CREATE TABLE IF NOT EXISTS rooms (
        room_no TEXT PRIMARY KEY,
        room_vac INTEGER
    );
    '''
    try:
        cursor = conn.cursor()
        cursor.execute(query)
    except Error as e:
        print(e)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Student Management System")

    # Create a style to use for buttons and frames
    style = ttk.Style()
    style.configure("Accent.TButton", foreground="white", background="#4CAF50", font=("Arial", 12))
    style.configure("Accent.TFrame", background="#4CAF50")

    create_rooms_management_dashboard(root)

    root.mainloop()
