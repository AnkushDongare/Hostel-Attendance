# ui_manager.py
import tkinter as tk
from tkinter import ttk

class UIManager:
    @staticmethod
    def create_main_window(title):
        root = tk.Tk()
        root.title(title)

        window_width = root.winfo_screenwidth() // 2
        window_height = root.winfo_screenheight() // 2
        x = (root.winfo_screenwidth() // 2) - (window_width // 2)
        y = (root.winfo_screenheight() // 2) - (window_height // 2)
        root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        return root

    @staticmethod
    def create_button_with_icon(parent, text, icon_path, command):
        button = ttk.Button(parent, text=text, command=command, style="Accent.TButton")
        icon = tk.PhotoImage(file=icon_path)
        button.config(image=icon, compound="top")
        button.icon = icon
        return button
