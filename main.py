import csv
import os
from datetime import datetime
import sys
import tkinter as tk

# settings
DATABASE_FOLDER = "database_folder"
DATABASE_FILE = os.path.join(DATABASE_FOLDER, "database.csv")
CHECKIN_FOLDER = "checkin_logs"
DISCLAIMER = "By scanning your ID, you agree to the terms and conditions."
EXIT_CODE = "adminexit"

# create folders
os.makedirs(CHECKIN_FOLDER, exist_ok=True)
os.makedirs(DATABASE_FOLDER, exist_ok=True)


def create_database_if_needed():
    if not os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Card ID", "Student ID", "Phone Number"])


def get_today_checkin_file():
    today = datetime.now().strftime("%Y-%m-%d")
    filename = "checkin_{0}.csv".format(today)
    return os.path.join(CHECKIN_FOLDER, filename)


def create_checkin_file_if_needed(filename):
    if not os.path.exists(filename):
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Card ID", "Student ID", "Phone Number", "Timestamp"])


def parse_swipe(swipe):
    swipe = swipe.strip()

    if "^" not in swipe:
        raise ValueError("Swipe data missing '^' separators")

    parts = swipe.split("^")

    card_part = parts[0].strip()

    if not card_part.startswith("%B"):
        raise ValueError("Swipe data missing Track 1 start")

    card_id = card_part.replace("%B", "").strip()

    name_raw = parts[1].strip()

    if "/" not in name_raw:
        raise ValueError("Name format invalid")

    last, first = name_raw.split("/")[0:2]

    first = " ".join(first.split())
    last = " ".join(last.split())

    formatted_name = "{0} {1}".format(first, last)

    return formatted_name, card_id


def valid_student_id(student_id):
    return student_id.isdigit() and len(student_id) == 10


def valid_phone_number(phone):
    digits_only = "".join(ch for ch in phone if ch.isdigit())
    return len(digits_only) == 10


def normalize_phone_number(phone):
    return "".join(ch for ch in phone if ch.isdigit())


def find_student_in_database(card_id):
    if not os.path.exists(DATABASE_FILE):
        return None

    with open(DATABASE_FILE, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["Card ID"] == card_id:
                return row

    return None


def add_student_to_database(name, card_id, student_id, phone_number):
    with open(DATABASE_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([name, card_id, student_id, phone_number])


def already_checked_in_today(filename, card_id):
    if not os.path.exists(filename):
        return False

    with open(filename, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["Card ID"] == card_id:
                return True

    return False


def save_checkin(filename, name, card_id, student_id, phone_number):
    timestamp = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")

    with open(filename, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([name, card_id, student_id, phone_number, timestamp])


class CheckInApp:

    def __init__(self, root):
        self.root = root
        self.root.title("ID Check-In System")
        self.root.geometry("520x380")

        create_database_if_needed()

        self.swipe_var = tk.StringVar()
        self.student_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.exit_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Waiting for card swipe...")

        self.pending_name = None
        self.pending_card_id = None

        tk.Label(root, text="ID Check-In System", font=("Arial", 16, "bold")).pack(pady=10)
        tk.Label(root, text=DISCLAIMER, wraplength=450).pack(pady=5)

        frame = tk.Frame(root)
        frame.pack(pady=10)

        tk.Label(frame, text="Swipe Card").grid(row=0, column=0, pady=5)
        self.swipe_entry = tk.Entry(frame, textvariable=self.swipe_var, show="*", width=35)
        self.swipe_entry.grid(row=0, column=1)
        self.swipe_entry.bind("<Return>", lambda event: self.process_swipe())

        tk.Label(frame, text="Student ID").grid(row=1, column=0, pady=5)
        self.student_entry = tk.Entry(frame, textvariable=self.student_var, state="disabled", width=35)
        self.student_entry.grid(row=1, column=1)

        tk.Label(frame, text="Phone Number").grid(row=2, column=0, pady=5)
        self.phone_entry = tk.Entry(frame, textvariable=self.phone_var, state="disabled", width=35)
        self.phone_entry.grid(row=2, column=1)

        tk.Label(frame, text="Admin").grid(row=3, column=0, pady=10)
        self.exit_entry = tk.Entry(frame, textvariable=self.exit_var, show="*", width=35)
        self.exit_entry.grid(row=3, column=1)

        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Process Swipe", command=self.process_swipe).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Save New Student", command=self.save_new_student).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Check Admin", command=self.check_admin_exit).grid(row=0, column=2, padx=5)

        tk.Label(root, text="Status:", font=("Arial", 11, "bold")).pack()
        tk.Label(root, textvariable=self.status_var, wraplength=450).pack()

    def check_admin_exit(self):
        if self.exit_var.get().strip().lower() == EXIT_CODE:
            self.root.destroy()

    def process_swipe(self):
        swipe = self.swipe_var.get().strip()

        if swipe == "":
            self.status_var.set("No swipe detected.")
            return

        try:
            name, card_id = parse_swipe(swipe)
        except Exception as e:
            self.status_var.set("Invalid swipe format.")
            return

        checkin_file = get_today_checkin_file()
        create_checkin_file_if_needed(checkin_file)

        if already_checked_in_today(checkin_file, card_id):
            self.status_var.set(f"{name} already checked in today.")
            return

        student = find_student_in_database(card_id)

        if student:
            save_checkin(
                checkin_file,
                student["Name"],
                student["Card ID"],
                student["Student ID"],
                student["Phone Number"]
            )

            self.status_var.set(f"Check-in saved for {student['Name']}")
            self.swipe_var.set("")
            return

        self.pending_name = name
        self.pending_card_id = card_id

        self.student_entry.config(state="normal")
        self.phone_entry.config(state="normal")

        self.status_var.set(f"New student detected: {name}")

    def save_new_student(self):

        student_id = self.student_var.get().strip()
        phone = self.phone_var.get().strip()

        if not valid_student_id(student_id):
            self.status_var.set("Invalid Student ID.")
            return

        if not valid_phone_number(phone):
            self.status_var.set("Invalid phone number.")
            return

        phone = normalize_phone_number(phone)

        checkin_file = get_today_checkin_file()
        create_checkin_file_if_needed(checkin_file)

        add_student_to_database(self.pending_name, self.pending_card_id, student_id, phone)
        save_checkin(checkin_file, self.pending_name, self.pending_card_id, student_id, phone)

        self.status_var.set("New student added and checked in.")

        self.student_var.set("")
        self.phone_var.set("")
        self.swipe_var.set("")

        self.student_entry.config(state="disabled")
        self.phone_entry.config(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    app = CheckInApp(root)
    root.mainloop()
