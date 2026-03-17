import tkinter as tk
from .base_screen import BaseScreen

class Screen1(BaseScreen):
    def __init__(self, parent, controller):
        BaseScreen.__init__(self, parent, controller)

        top_bar = tk.Frame(self, bg="white")
        top_bar.pack(fill="x", padx=20, pady=20)

        tk.Label(
            top_bar,
            text="ID Check-In System",
            font=("Arial", 22, "bold"),
            bg="white"
        ).pack(side="left")

        tk.Button(
            top_bar,
            text="Admin",
            width=12,
            command=lambda: controller.show_frame("Screen3")
        ).pack(side="right")

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
            font=("Arial", 14)
        )
        self.swipe_entry.pack(pady=(0, 18))
        self.swipe_entry.bind("<Return>", lambda event: controller.process_swipe_from_screen1())

        disclaimer_frame = tk.Frame(center, bg="white")
        disclaimer_frame.pack(pady=(0, 25))

        tk.Label(
            disclaimer_frame,
            text="By scanning your ID, you agree to the ",
            bg="white",
            font=("Arial", 11)
        ).pack(side="left")

        terms_link = tk.Label(
            disclaimer_frame,
            text="terms and conditions.",
            fg="blue",
            cursor="hand2",
            bg="white",
            font=("Arial", 11, "underline")
        )
        terms_link.pack(side="left")
        terms_link.bind("<Button-1>", lambda event: controller.open_terms_window())

        self.message_label = tk.Label(
            center,
            text="Waiting for card swipe...",
            font=("Arial", 12),
            bg="white",
            fg="black"
        )
        self.message_label.pack(pady=10)

    def set_message(self, message, color="black", success=False):
        self.message_label.config(
            text=message,
            fg=color,
            font=("Arial", 16, "bold") if success else ("Arial", 12)
        )

    def focus_swipe(self):
        self.swipe_entry.focus_set()

    def reset_screen(self):
        self.set_message("Waiting for card swipe...", "black", success=False)
        self.controller.swipe_var.set("")
        self.focus_swipe()