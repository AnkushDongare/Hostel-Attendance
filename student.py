# student.py
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.simpledialog import askstring
import cv2 as cv
import os
import sqlite3
from sqlite3 import Error
import PIL.Image
import PIL.ImageTk
import numpy as np
import csv
from tkinter import filedialog

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('database/hostel_database.db')
        return conn
    except Error as e:
        print(e)

    return conn

def create_table(conn):
    query = '''
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
    );
    '''

    try:
        cursor = conn.cursor()
        cursor.execute(query)
    except Error as e:
        print(e)

def open_student_management_dashboard(root):
    student_window = tk.Toplevel(root)
    student_window.title("Student Registration Dashboard")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    student_window.geometry(f"{screen_width}x{screen_height}+0+0")

    student_frame = ttk.Frame(student_window, style="Accent.TFrame")
    student_frame.grid(row=0, column=0, sticky="nsew")
    student_frame.grid_rowconfigure(0, weight=1)
    student_frame.grid_columnconfigure(0, weight=1)

    right_frame = create_right_frame(student_frame)
    left_frame = create_left_frame(student_frame, student_window, right_frame)

    logout_button = ttk.Button(student_frame, text="Logout", command=student_window.destroy, style="Accent.TButton")
    logout_button.grid(row=1, column=0, pady=20)

def create_left_frame(parent, root, tree):
    frame = ttk.LabelFrame(parent, text="Student Details", padding=10)
    frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
    parent.grid_rowconfigure(0, weight=1)
    parent.grid_columnconfigure(0, weight=1)

    student_personal_frame = ttk.LabelFrame(frame, text="Student Personal", padding=10)
    student_personal_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    global name_entry, gender_combobox, age_entry, roll_no_entry, id_entry, email_entry, phone_entry, course_combobox, class_combobox, semester_combobox, year_entry, room_no_entry, sample_radio_var


    ttk.Label(student_personal_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    name_entry = ttk.Entry(student_personal_frame)
    name_entry.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(student_personal_frame, text="Gender:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    gender_combobox = ttk.Combobox(student_personal_frame, values=["Male", "Female", "Other"])
    gender_combobox.grid(row=1, column=1, padx=5, pady=5)
    gender_combobox.set("Male")

    ttk.Label(student_personal_frame, text="Age:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
    age_entry = ttk.Entry(student_personal_frame)
    age_entry.grid(row=2, column=1, padx=5, pady=5)

    ttk.Label(student_personal_frame, text="Roll No:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
    roll_no_entry = ttk.Entry(student_personal_frame)
    roll_no_entry.grid(row=3, column=1, padx=5, pady=5)

    ttk.Label(student_personal_frame, text="ID:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
    id_entry = ttk.Entry(student_personal_frame)
    id_entry.grid(row=4, column=1, padx=5, pady=5)

    ttk.Label(student_personal_frame, text="Email:").grid(row=5, column=0, padx=5, pady=5, sticky="w")
    email_entry = ttk.Entry(student_personal_frame)
    email_entry.grid(row=5, column=1, padx=5, pady=5)

    ttk.Label(student_personal_frame, text="Phone:").grid(row=6, column=0, padx=5, pady=5, sticky="w")
    phone_entry = ttk.Entry(student_personal_frame)
    phone_entry.grid(row=6, column=1, padx=5, pady=5)

    ttk.Label(student_personal_frame, text="Course:").grid(row=7, column=0, padx=5, pady=5, sticky="w")
    course_combobox = ttk.Combobox(student_personal_frame, values=["Course1", "Course2", "Course3"])
    course_combobox.grid(row=7, column=1, padx=5, pady=5)
    course_combobox.set("Course1")

    ttk.Label(student_personal_frame, text="Class:").grid(row=8, column=0, padx=5, pady=5, sticky="w")
    class_combobox = ttk.Combobox(student_personal_frame, values=["Class1", "Class2", "Class3"])
    class_combobox.grid(row=8, column=1, padx=5, pady=5)
    class_combobox.set("Class1")

    ttk.Label(student_personal_frame, text="Semester:").grid(row=9, column=0, padx=5, pady=5, sticky="w")
    semester_combobox = ttk.Combobox(student_personal_frame, values=[1, 2, 3, 4, 5, 6, 7, 8])
    semester_combobox.grid(row=9, column=1, padx=5, pady=5)
    semester_combobox.set(1)

    ttk.Label(student_personal_frame, text="Year:").grid(row=10, column=0, padx=5, pady=5, sticky="w")
    year_entry = ttk.Entry(student_personal_frame)
    year_entry.grid(row=10, column=1, padx=5, pady=5)

    ttk.Label(student_personal_frame, text="Room No:").grid(row=11, column=0, padx=5, pady=5, sticky="w")
    room_numbers = fetch_room_numbers()
    room_no_entry = ttk.Combobox(student_personal_frame, values=room_numbers)  # Define room_no_entry here
    room_no_entry.grid(row=11, column=1, padx=5, pady=5)

    ttk.Label(student_personal_frame, text="Sample Radio:").grid(row=14, column=0, padx=5, pady=5, sticky="w")
    sample_radio_var = tk.StringVar()
    add_images_radio = ttk.Radiobutton(student_personal_frame, text="Add images", variable=sample_radio_var, value="yes")
    add_images_radio.grid(row=14, column=1, padx=5, pady=5)

    dont_add_images_radio = ttk.Radiobutton(student_personal_frame, text="Don't add images", variable=sample_radio_var, value="no")
    dont_add_images_radio.grid(row=15, column=1, padx=5, pady=5)

    ttk.Button(student_personal_frame, text="Save", style="Accent.TButton", command=save_student_data).grid(row=17, column=0, columnspan=2, pady=10)
    ttk.Button(student_personal_frame, text="Reset", style="Accent.TButton", command=reset_student_data).grid(row=18, column=0, columnspan=2, pady=10)
    ttk.Button(student_personal_frame, text="Update", style="Accent.TButton", command=update_student_data).grid(row=19, column=0, columnspan=2, pady=10)
    ttk.Button(student_personal_frame, text="Delete", style="Accent.TButton", command=delete_selected_student).grid(row=20, column=0, columnspan=2, pady=10)
    ttk.Button(student_personal_frame, text="Take Image Sample", style="Accent.TButton", command=take_image_sample).grid(row=21, column=0, columnspan=2, pady=10)
    ttk.Button(student_personal_frame, text="Update Image", style="Accent.TButton", command=update_image_sample).grid(row=22, column=0, columnspan=2, pady=10)

    return frame

def create_right_frame(parent):
    frame = ttk.LabelFrame(parent, text="Search Details", padding=10)
    frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

    ttk.Label(frame, text="Search:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    global search_entry, search_criteria_combobox
    search_entry = ttk.Entry(frame)
    search_entry.grid(row=0, column=1, padx=5, pady=5, sticky="we")

    ttk.Label(frame, text="Search By:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    search_criteria_combobox = ttk.Combobox(frame, values=["Name", "ID", "All"], style="Accent.TCombobox")
    search_criteria_combobox.grid(row=1, column=1, padx=5, pady=5, sticky="we")
    search_criteria_combobox.set("Name")

    ttk.Button(frame, text="Search", style="Accent.TButton", command=search_student).grid(row=2, column=0, columnspan=2, padx=5, pady=10, sticky="we")

    # Create a canvas and treeview
    table_canvas = tk.Canvas(frame)
    table_canvas.grid(row=3, column=0, columnspan=2, padx=5, pady=10, sticky="nsew")

    columns = ("Sr No", "Name", "Gender", "Age", "Roll No", "ID", "Email", "Phone", "Course", "Class", "Semester", "Year", "Room No" , "Sample Radio")
    global tree
    tree = ttk.Treeview(table_canvas, columns=columns, show="headings")
    populate_treeview(tree)
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

    ttk.Button(frame, text="Export CSV", style="Accent.TButton", command=export_to_csv).grid(row=4, column=0, columnspan=2, pady=10)
    ttk.Button(frame, text="Import CSV", style="Accent.TButton", command=import_from_csv).grid(row=4, column=1, columnspan=2, pady=10)

    # Create a right-click menu
    right_click_menu = tk.Menu(frame, tearoff=0)
    right_click_menu.add_command(label="Delete", command=delete_selected_student)
    right_click_menu.add_separator()
    right_click_menu.add_command(label="Update", command=update_selected_student)

    def on_right_click(event):
        item = tree.identify_row(event.y)
        if item:
            right_click_menu.post(event.x_root, event.y_root)

    tree.bind("<Button-3>", on_right_click)

    return tree

def save_student_data():
    conn = create_connection()
    create_table(conn)

    name = name_entry.get()
    gender = gender_combobox.get()
    age = age_entry.get()
    roll_no = roll_no_entry.get()
    student_id = id_entry.get()
    email = email_entry.get()
    phone = phone_entry.get()
    course = course_combobox.get()
    class_ = class_combobox.get()
    semester = semester_combobox.get()
    year = year_entry.get()
    room_no = room_no_entry.get()
    sample_radio = sample_radio_var.get()

    query = '''
    INSERT INTO students (name, gender, age, roll_no, student_id, email, phone, course, class, semester, year, room_no, sample_radio)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    '''
    data = (name, gender, age, roll_no, student_id, email, phone, course, class_, semester, year, room_no, sample_radio)

    try:
        cursor = conn.cursor()
        cursor.execute(query, data)
        conn.commit()
        messagebox.showinfo("Success", "Student data saved successfully!")
        populate_treeview(tree)
        reset_student_data()
    except Error as e:
        conn.rollback()
        print(e)
        messagebox.showerror("Error", "Failed to save student data.")

    conn.close()

def fetch_room_numbers():
    # Function to fetch room numbers from the "rooms" table in the database
    conn = create_connection()
    create_table(conn)

    query = '''
    SELECT room_no FROM rooms;
    '''

    try:
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        room_numbers = [row[0] for row in rows]
        return room_numbers

    except Error as e:
        print(e)
        return []

    finally:
        conn.close()

def populate_treeview(tree):
    conn = create_connection()
    create_table(conn)

    query = '''
    SELECT * FROM students;
    '''

    try:
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()

        for item in tree.get_children():
            tree.delete(item)

        for row in rows:
            tree.insert("", "end", values=row)

    except Error as e:
        print(e)

    conn.close()
def search_student():
    conn = create_connection()
    create_table(conn)

    search_criteria = search_criteria_combobox.get()
    search_text = search_entry.get()

    if search_criteria == "Name":
        query = f'''
        SELECT * FROM students WHERE name LIKE ?;
        '''
        data = (f'%{search_text}%',)
    elif search_criteria == "ID":
        query = f'''
        SELECT * FROM students WHERE student_id LIKE ?;
        '''
        data = (f'%{search_text}%',)
    else:
        query = '''
        SELECT * FROM students;
        '''
        data = ()

    try:
        cursor = conn.cursor()
        cursor.execute(query, data)
        rows = cursor.fetchall()

        for item in tree.get_children():
            tree.delete(item)

        for row in rows:
            tree.insert("", "end", values=row)

    except Error as e:
        print(e)

    conn.close()

def delete_selected_student():
    selected_item = tree.selection()
    if selected_item:
        conn = create_connection()
        create_table(conn)

        student_id = tree.item(selected_item)['values'][5]
        query = '''
        DELETE FROM students WHERE student_id = ?;
        '''

        try:
            cursor = conn.cursor()
            cursor.execute(query, (student_id,))
            conn.commit()
            messagebox.showinfo("Success", "Student data deleted successfully!")
            populate_treeview(tree)
            reset_student_data()
        except Error as e:
            conn.rollback()
            print(e)
            messagebox.showerror("Error", "Failed to delete student data.")

        conn.close()

def update_selected_student():
    selected_item = tree.selection()
    if selected_item:
        data = tree.item(selected_item)['values']
        name_entry.delete(0, tk.END)
        name_entry.insert(0, data[1])
        gender_combobox.set(data[2])
        age_entry.delete(0, tk.END)
        age_entry.insert(0, data[3])
        roll_no_entry.delete(0, tk.END)
        roll_no_entry.insert(0, data[4])
        id_entry.delete(0, tk.END)
        id_entry.insert(0, data[5])
        email_entry.delete(0, tk.END)
        email_entry.insert(0, data[6])
        phone_entry.delete(0, tk.END)
        phone_entry.insert(0, data[7])
        course_combobox.set(data[8])
        class_combobox.set(data[9])
        semester_combobox.set(data[10])
        year_entry.delete(0, tk.END)
        year_entry.insert(0, data[11])
        room_no_entry.delete(0, tk.END)
        room_no_entry.insert(0, data[12])
        sample_radio_var.set(data[13])

def update_student_data():
    conn = create_connection()
    create_table(conn)

    name = name_entry.get()
    gender = gender_combobox.get()
    age = age_entry.get()
    roll_no = roll_no_entry.get()
    student_id = id_entry.get()
    email = email_entry.get()
    phone = phone_entry.get()
    course = course_combobox.get()
    class_ = class_combobox.get()
    semester = semester_combobox.get()
    year = year_entry.get()
    room_no = room_no_entry.get()
    sample_radio = sample_radio_var.get()

    query = '''
    UPDATE students
    SET name=?, gender=?, age=?, roll_no=?, student_id=?, email=?, phone=?, course=?, class=?, semester=?, year=?, room_no=?, sample_radio=?
    WHERE student_id=?;
    '''
    data = (name, gender, age, roll_no, student_id, email, phone, course, class_, semester, year, room_no, sample_radio, student_id)

    try:
        cursor = conn.cursor()
        cursor.execute(query, data)
        conn.commit()
        messagebox.showinfo("Success", "Student data updated successfully!")
        populate_treeview(tree)
        reset_student_data()
    except Error as e:
        conn.rollback()
        print(e)
        messagebox.showerror("Error", "Failed to update student data.")

    conn.close()



def reset_student_data():
    name_entry.delete(0, tk.END)
    gender_combobox.set("Male")
    age_entry.delete(0, tk.END)
    roll_no_entry.delete(0, tk.END)
    id_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    course_combobox.set("Course1")
    class_combobox.set("Class1")
    semester_combobox.set(1)
    year_entry.delete(0, tk.END)
    room_no_entry.delete(0, tk.END)
    sample_radio_var.set("")


import csv
from tkinter import filedialog, messagebox
from sqlite3 import Error

def export_to_csv():
    try:
        # Connect to the database and create a table if it doesn't exist
        conn = create_connection()
        create_table(conn)

        # Fetch data from the 'students' table
        query = '''
        SELECT * FROM students;
        '''
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()

        # Check if there is data to export
        if not rows:
            messagebox.showwarning("Warning", "No data to export.")
            return

        # Ask the user to choose a file for saving
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        
        # Check if the user canceled the file dialog
        if not file_path:
            return

        # Write data to the CSV file
        with open(file_path, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            header = [desc[0] for desc in cursor.description]
            csv_writer.writerow(header)
            csv_writer.writerows(rows)

        messagebox.showinfo("Success", f"Data exported to {file_path}")

    except Error as e:
        print(e)
        messagebox.showerror("Error", "Failed to export data.")

    finally:
        # Close the database connection
        conn.close()


def import_from_csv():
    # Ask the user to choose a file for importing
    file_path = filedialog.askopenfilename(title="Select CSV file", filetypes=[("CSV files", "*.csv")])
    if not file_path:
        return

    try:
        with open(file_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)  # Skip the header row
            data_to_insert = [tuple(row) for row in csv_reader]

        conn = create_connection()
        create_table(conn)

        query = f'''
    INSERT INTO students (name, gender, age, roll_no, student_id, email, phone, course, class, semester, year, room_no, sample_radio,clock_in_status)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
'''

        try:
            cursor = conn.cursor()
            cursor.executemany(query, data_to_insert)
            conn.commit()
            messagebox.showinfo("Success", f"Data imported from {file_path}")
            populate_treeview(tree)

        except Error as e:
            conn.rollback()
            print(e)
            messagebox.showerror("Error", "Failed to import data.")

        conn.close()

    except FileNotFoundError:
        messagebox.showerror("Error", "File not found.")
    except Exception as e:
        print(e)
        messagebox.showerror("Error", "An error occurred during import.")

def take_image_sample():
    # Get the student ID for naming images (you may adjust this based on your data structure)
    student_id = id_entry.get()  # Assuming id_entry is the entry widget for student ID

    if not student_id:
        messagebox.showwarning("Warning", "Please enter a student ID before capturing images.")
        return

    # Connect to the camera (assuming the default camera index, you can change it accordingly)
    cap = cv.VideoCapture(0)

    # Create a folder for image samples if it doesn't exist
    sample_folder = "image_samples"
    os.makedirs(sample_folder, exist_ok=True)

    # Create a face cascade using the haarcascade_frontalface_default.xml file
    cascade_path = 'haarcascade_frontalface_default.xml'  # Replace with your actual path
    face_cascade = cv.CascadeClassifier(cascade_path)

    # Capture 100 image samples
    for i in range(100):
        ret, frame = cap.read()

        # Convert the frame to grayscale for face detection
        gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

        # Save the cropped face as a grayscale image
        for (x, y, w, h) in faces:
            # Crop the face from the grayscale frame
            face_roi = gray_frame[y:y + h, x:x + w]

            # Save the cropped face as an image with a unique name based on student ID
            image_path = os.path.join(sample_folder, f"{student_id}_sample_{i}.png")
            cv.imwrite(image_path, face_roi)

        # Display the captured frame with face detection
        cv.imshow("Image Sample", frame)
        cv.waitKey(1)

    # Release the camera and close the OpenCV window
    cap.release()
    cv.destroyAllWindows()

def update_image_sample():
    # Get the student ID from the selected item in the tree
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Warning", "Please select a student from the tree to update the image.")
        return

    student_id = tree.item(selected_item)['values'][5]  # Assuming student ID is in the 6th column

    # Connect to the camera (assuming the default camera index, you can change it accordingly)
    cap = cv.VideoCapture(0)

    # Create a folder for image samples if it doesn't exist
    sample_folder = "image_samples"
    os.makedirs(sample_folder, exist_ok=True)

    # Create a face cascade using the haarcascade_frontalface_default.xml file
    cascade_path = 'haarcascade_frontalface_default.xml'  # Replace with your actual path
    face_cascade = cv.CascadeClassifier(cascade_path)

    # Capture 100 image samples
    for i in range(100):
        ret, frame = cap.read()

        # Convert the frame to grayscale for face detection
        gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

        # Save the cropped face as a grayscale image
        for (x, y, w, h) in faces:
            # Crop the face from the grayscale frame
            face_roi = gray_frame[y:y + h, x:x + w]

            # Save the cropped face as an image with a unique name based on student ID
            image_path = os.path.join(sample_folder, f"{student_id}_sample_{i}.png")
            cv.imwrite(image_path, face_roi)

        # Display the captured frame with face detection
        cv.imshow("Image Sample", frame)
        cv.waitKey(1)

    # Release the camera and close the OpenCV window
    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    root = tk.Tk()

    style = ttk.Style()
    style.configure("Accent.TLabel", font=("Helvetica", 12))
    style.configure("Accent.TEntry", font=("Helvetica", 12))
    style.configure("Accent.TButton", font=("Helvetica", 12))
    style.configure("Accent.TCombobox", font=("Helvetica", 12))
    style.configure("Accent.TFrame", background="#f2f2f2")

    open_student_management_dashboard(root)

    root.mainloop()


