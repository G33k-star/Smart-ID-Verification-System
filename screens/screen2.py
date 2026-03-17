import tkinter as tk
from .base_screen import BaseScreen

class Screen2(BaseScreen):
    def __init__(self, parent, controller):
        BaseScreen.__init__(self, parent, controller)

        top_bar = tk.Frame(self, bg="white")
        top_bar.pack(fill="x", padx=20, pady=20)

        tk.Label(
            top_bar,
            text="Add New User",
            font=("Arial", 22, "bold"),
            bg="white"
        ).pack(side="left")

        center = tk.Frame(self, bg="white")
        center.pack(expand=True)

        tk.Label(
            center,
            text="Swipe Card",
            font=("Arial", 14),
            bg="white"
        ).pack(pady=(10, 8))

        self.swipe_entry = tk.Entry(
            center,
            textvariable=controller.swipe_var,
            show="*",
            width=40,
            font=("Arial", 14),
            state="disabled"
        )
        self.swipe_entry.pack(pady=(0, 15))

        self.message_label = tk.Label(
            center,
            text="User not recognized. Add new user?",
            font=("Arial", 12),
            bg="white",
            fg="black"
        )
        self.message_label.pack(pady=10)

        yes_no_frame = tk.Frame(center, bg="white")
        yes_no_frame.pack(pady=10)

        self.yes_btn = tk.Button(
            yes_no_frame,
            text="Yes",
            width=12,
            command=self.show_add_user_fields
        )
        self.yes_btn.grid(row=0, column=0, padx=8)

        self.no_btn = tk.Button(
            yes_no_frame,
            text="No",
            width=12,
            command=self.back_to_screen1
        )
        self.no_btn.grid(row=0, column=1, padx=8)

        self.add_user_frame = tk.Frame(center, bg="white")

        tk.Label(self.add_user_frame, text="Student ID", bg="white", font=("Arial", 12)).pack(pady=(10, 5))
        self.student_entry = tk.Entry(
            self.add_user_frame,
            textvariable=controller.student_var,
            width=35,
            font=("Arial", 12)
        )
        self.student_entry.pack(pady=(0, 8))

        tk.Label(self.add_user_frame, text="Phone Number", bg="white", font=("Arial", 12)).pack(pady=(5, 5))
        self.phone_entry = tk.Entry(
            self.add_user_frame,
            textvariable=controller.phone_var,
            width=35,
            font=("Arial", 12)
        )
        self.phone_entry.pack(pady=(0, 8))

        tk.Label(self.add_user_frame, text="myMDC Username", bg="white", font=("Arial", 12)).pack(pady=(5, 5))
        self.username_entry = tk.Entry(
            self.add_user_frame,
            textvariable=controller.mymdc_username_var,
            width=35,
            font=("Arial", 12)
        )
        self.username_entry.pack(pady=(0, 12))

        self.add_user_btn = tk.Button(
            self.add_user_frame,
            text="Add User",
            width=18,
            command=controller.add_user_and_check_in
        )
        self.add_user_btn.pack(pady=(5, 8))

        self.fields_visible = False

    def set_message(self, message, color="black", success=False):
        self.message_label.config(
            text=message,
            fg=color,
            font=("Arial", 16, "bold") if success else ("Arial", 12)
        )

    def show_add_user_fields(self):
        if not self.fields_visible:
            self.add_user_frame.pack(pady=10)
            self.fields_visible = True
        self.student_entry.focus_set()

    def back_to_screen1(self):
        self.controller.pending_name = None
        self.controller.pending_card_id = None
        self.controller.swipe_var.set("")
        self.controller.student_var.set("")
        self.controller.phone_var.set("")
        self.controller.mymdc_username_var.set("")
        self.controller.email_var.set("")
        self.controller.show_frame("Screen1")

    def reset_screen(self):
        self.set_message("User not recognized. Add new user?", "black", success=False)
        self.controller.student_var.set("")
        self.controller.phone_var.set("")
        self.controller.mymdc_username_var.set("")
        self.controller.email_var.set("")

        if self.fields_visible:
            self.add_user_frame.pack_forget()
            self.fields_visible = False