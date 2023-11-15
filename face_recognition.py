import cv2
import numpy as np
import sqlite3
from datetime import datetime

def fetch_student_data(student_id):
    # Connect to the database
    conn = sqlite3.connect("database/hostel_database.db")  # Replace with the path to your database file

    # Query to fetch student information based on student_id
    query = '''
    SELECT * FROM students WHERE student_id = ?;
    '''

    try:
        cursor = conn.cursor()
        cursor.execute(query, (student_id,))
        student_data = cursor.fetchone()
        return student_data

    except sqlite3.Error as e:
        print(f"Error fetching student data: {e}")
        return None

    finally:
        conn.close()

def update_attendance(student_id, clock_in_status):
    # Connect to the database
    conn = sqlite3.connect("database/hostel_database.db")  # Replace with the path to your database file

    # Update the attendance table based on clock_in_status
    if clock_in_status == 1:
        # Clock-in
        query = '''
        INSERT INTO attendance (student_id, clock_in_time, status_code)
        VALUES (?, ?, ?);
        '''
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        values = (student_id, timestamp, clock_in_status)
    else:
        # Clock-out
        query = '''
        UPDATE attendance
        SET clock_out_time = ?, status_code = ?
        WHERE student_id = ? AND status_code = 1;
        '''
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        values = (timestamp, clock_in_status, student_id)

    try:
        cursor = conn.cursor()
        cursor.execute(query, values)
        conn.commit()
        print("Attendance updated successfully.")

    except sqlite3.Error as e:
        print(f"Error updating attendance: {e}")

    finally:
        conn.close()

def verify_face():
    # Load the pre-trained LBPH Face Recognizer
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("classifier.xml")  # Replace with the path to your trained classifier.xml file

    # Load the face cascade
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Open a connection to the webcam (0 indicates the default camera)
    cap = cv2.VideoCapture(0)

    try:
        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()

            # Convert the frame to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Detect faces in the frame
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in faces:
                # Extract the face region from the frame
                face_roi = gray[y:y+h, x:x+w]

                # Perform face recognition
                label, confidence = recognizer.predict(face_roi)

                # Fetch student data from the database based on the recognized label
                student_data = fetch_student_data(label)

                # Display the recognized face and student data
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                if student_data:
                    student_info_text = f"Label: {label}\nStudent ID: {student_data[5]}\nName: {student_data[1]}\nRoll No: {student_data[4]}\nEmail: {student_data[6]}"
                    cv2.putText(frame, student_info_text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                    # Check if the 'c' key is pressed to clock-in or clock-out
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord('c'):
                        if student_data[14] == 0:  # Clock-in
                            update_attendance(student_data[5], 1)
                        else:  # Clock-out
                            update_attendance(student_data[5], 0)

                else:
                    cv2.putText(frame, f"Label: {label} (Unknown)", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            # Display the resulting frame
            cv2.imshow('Face Verification', frame)

            # Break the loop when 'q' key is pressed
            if key == ord('q'):
                break

    finally:
        # Release the webcam and close all windows
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    verify_face()
