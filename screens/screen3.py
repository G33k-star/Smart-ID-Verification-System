import tkinter as tk
from .base_screen import BaseScreen

class Screen3(BaseScreen):
    def __init__(self, parent, controller):
        BaseScreen.__init__(self, parent, controller)

        top_bar = tk.Frame(self, bg="white")
        top_bar.pack(fill="x", padx=20, pady=20)

        tk.Label(
            top_bar,
            text="Admin Login",
            font=("Arial", 22, "bold"),
            bg="white"
        ).pack(side="left")

        tk.Button(
            top_bar,
            text="Back",
            width=12,
            command=lambda: controller.show_frame("Screen1")
        ).pack(side="right")

        center = tk.Frame(self, bg="white")
        center.pack(expand=True)

        tk.Label(center, text="Username", font=("Arial", 12), bg="white").pack(pady=(10, 5))
        self.username_entry = tk.Entry(
            center,
            textvariable=controller.admin_user_var,
            width=35,
            font=("Arial", 12)
        )
        self.username_entry.pack(pady=(0, 12))

        tk.Label(center, text="Password", font=("Arial", 12), bg="white").pack(pady=(5, 5))
        self.password_entry = tk.Entry(
            center,
            textvariable=controller.admin_pass_var,
            show="*",
            width=35,
            font=("Arial", 12)
        )
        self.password_entry.pack(pady=(0, 15))

        tk.Button(
            center,
            text="Check Admin",
            width=18,
            command=controller.check_admin_credentials
        ).pack(pady=10)

        self.message_label = tk.Label(
            center,
            text="",
            font=("Arial", 12),
            bg="white",
            fg="red"
        )
        self.message_label.pack(pady=10)

    def set_message(self, message):
        self.message_label.config(text=message)

    def focus_username(self):
        self.username_entry.focus_set()

    def reset_screen(self):
        self.controller.admin_user_var.set("")
        self.controller.admin_pass_var.set("")
        self.set_message("")
        self.focus_username()