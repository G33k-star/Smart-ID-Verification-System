import tkinter as tk
from .base_screen import BaseScreen

class Screen4(BaseScreen):
    def __init__(self, parent, controller):
        BaseScreen.__init__(self, parent, controller)

        top_bar = tk.Frame(self, bg="white")
        top_bar.pack(fill="x", padx=20, pady=20)

        tk.Label(
            top_bar,
            text="Admin Dashboard",
            font=("Arial", 22, "bold"),
            bg="white"
        ).pack(side="left")

        tk.Button(
            top_bar,
            text="Exit Admin",
            width=12,
            command=lambda: controller.show_frame("Screen1")
        ).pack(side="right")

        center = tk.Frame(self, bg="white")
        center.pack(expand=True)

        tk.Button(
            center,
            text="Access CSV Files",
            width=24,
            height=2,
            command=controller.open_csv_folder
        ).pack(pady=10)

        tk.Button(
            center,
            text="Access Database Folder",
            width=24,
            height=2,
            command=controller.open_database_folder
        ).pack(pady=10)

        tk.Button(
            center,
            text="Quit Program",
            width=24,
            height=2,
            command=controller.safe_quit_program
        ).pack(pady=10)