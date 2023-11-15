# train.py
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image
import cv2
import os
import numpy as np

def train(root):
    print(cv2.__version__)

    admin_window = tk.Toplevel(root)
    admin_window.title("Train Dashboard")

    title_label = ttk.Label(admin_window, text="Train model Dashboard", font=("Helvetica", 24, "bold"))
    title_label.pack(pady=20)

    logout_button = ttk.Button(admin_window, text="Logout", command=root.destroy)
    logout_button.pack(pady=20)

    train_button = ttk.Button(admin_window, text="Train Model", command=train_classifier)
    train_button.pack(pady=20)

def train_classifier():
    data_dir = "image_samples"

    if not os.path.exists(data_dir):
        messagebox.showerror("Error", f"Directory '{data_dir}' not found.")
        return

    image_files = [f for f in os.listdir(data_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    if not image_files:
        messagebox.showinfo("Info", "No image samples found for training.")
        return

    faces = []
    ids = []

    for file in image_files:
        image_path = os.path.join(data_dir, file)
        image = Image.open(image_path).convert('L')
        image_np = np.array(image, 'uint8')
        # Extract ID from file name
        id = int(os.path.split(file)[1].split("_")[0].replace("subject", ""))
        ids.append(id)
        faces.append(image_np)

    ids = np.array(ids)

    # Use LBPHFaceRecognizer_create from cv2.face
    clf = cv2.face.LBPHFaceRecognizer_create()

    clf.train(faces, ids)

    # Confirm before overwriting existing classifier file
    if os.path.exists("classifier.xml"):
        response = messagebox.askyesno("Confirm", "The existing classifier file will be overwritten. Continue?")
        if not response:
            return

    clf.write("classifier.xml")
    messagebox.showinfo("Success", "Training completed successfully!")

if __name__ == "__main__":
    root = tk.Tk()

    style = ttk.Style()
    style.configure("Accent.TLabel", font=("Helvetica", 12))
    style.configure("Accent.TButton", font=("Helvetica", 12))
    style.configure("Accent.TFrame", background="#f2f2f2")

    train(root)
    root.mainloop()
