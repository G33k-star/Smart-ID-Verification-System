"""
ID Scanner Check-In System
Python 3.5 friendly
Debian / Raspberry Pi / Geany friendly

Logic:
- Swipe card
- Extract Name + Card ID from swipe
- Check if Card ID exists in database.csv
- If found:
    - Display student info
    - Save check-in to today's CSV if not already checked in today
- If not found:
    - Ask for Student ID and Phone Number
    - Save to database.csv
    - Save check-in to today's CSV
"""

import csv
import os
from datetime import datetime
from getpass import getpass

# =========================
# SETTINGS
# =========================
DATABASE_FILE = "database.csv"
CHECKIN_FOLDER = "checkin_logs"
DISCLAIMER = "By scanning your ID, you agree to the terms and conditions."

# Create folder if it does not exist
if not os.path.exists(CHECKIN_FOLDER):
    os.makedirs(CHECKIN_FOLDER)


# =========================
# FILE SETUP
# =========================
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


# =========================
# SWIPE PARSING
# =========================
def parse_swipe(swipe):
    """
    Example swipe:
    %B6029220033403492^SOUTER/JASON L            ^091212000000          000?;6029220033403492=09121200000000000000?
    """

    swipe = swipe.strip()

    # Must contain Track 1 separators
    if "^" not in swipe:
        raise ValueError("Swipe data missing '^' separators")

    parts = swipe.split("^")

    if len(parts) < 2:
        raise ValueError("Swipe data incomplete")

    # First part contains %B + card id
    card_part = parts[0].strip()

    if not card_part.startswith("%B"):
        raise ValueError("Swipe data missing Track 1 start")

    card_id = card_part.replace("%B", "").strip()

    # Name section
    name_raw = parts[1].strip()

    if "/" not in name_raw:
        raise ValueError("Name format invalid")

    name_parts = name_raw.split("/")

    if len(name_parts) < 2:
        raise ValueError("Name format incomplete")

    last = name_parts[0].strip()
    first = name_parts[1].strip()

    # Clean extra spaces inside first name
    first = " ".join(first.split())
    last = " ".join(last.split())

    formatted_name = "{0} {1}".format(first, last)

    return formatted_name, card_id


# =========================
# VALIDATION
# =========================
def valid_student_id(student_id):
    return student_id.isdigit() and len(student_id) == 10


def valid_phone_number(phone):
    digits_only = "".join(ch for ch in phone if ch.isdigit())
    return len(digits_only) == 10


def normalize_phone_number(phone):
    return "".join(ch for ch in phone if ch.isdigit())


# =========================
# DATABASE FUNCTIONS
# =========================
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


# =========================
# CHECK-IN FUNCTIONS
# =========================
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


# =========================
# MAIN PROGRAM
# =========================
def main():
    create_database_if_needed()

    while True:
        print("")
        print(DISCLAIMER)
        print("Please swipe your card.")
        print("")

        # Use input() for Debian/Geany reliability
        swipe = getpass("Swipe Card: ").strip()

        # Hidden testing exit command
        if swipe.lower() == "exit":
            print("Program ended.")
            break

        if swipe == "":
            print("No swipe detected. Please try again.")
            continue

        try:
            name, card_id = parse_swipe(swipe)
        except Exception as error:
            print("Invalid swipe format. Please try again.")
            print("Debug info:", error)
            continue

        checkin_file = get_today_checkin_file()
        create_checkin_file_if_needed(checkin_file)

        if already_checked_in_today(checkin_file, card_id):
            print("{0} has already checked in today. Entry ignored.".format(name))
            continue

        student = find_student_in_database(card_id)

        if student:
            print("")
            print("Student found in database:")
            print("Name: {0}".format(student["Name"]))
            print("Card ID: {0}".format(student["Card ID"]))
            print("Student ID: {0}".format(student["Student ID"]))
            print("Phone Number: {0}".format(student["Phone Number"]))

            save_checkin(
                checkin_file,
                student["Name"],
                student["Card ID"],
                student["Student ID"],
                student["Phone Number"]
            )

            print("Check-in saved successfully.")

        else:
            print("")
            print("Hello, {0}. You are not in the database yet.".format(name))
            print("Please enter your Student ID and Phone Number.")

            student_id = input("Student ID (10 digits): ").strip()
            while not valid_student_id(student_id):
                print("Invalid Student ID. It must be exactly 10 digits.")
                student_id = input("Student ID (10 digits): ").strip()

            phone_number = input("Phone Number (10 digits): ").strip()
            while not valid_phone_number(phone_number):
                print("Invalid phone number. It must contain exactly 10 digits.")
                phone_number = input("Phone Number (10 digits): ").strip()

            phone_number = normalize_phone_number(phone_number)

            add_student_to_database(name, card_id, student_id, phone_number)
            save_checkin(checkin_file, name, card_id, student_id, phone_number)

            print("New student added to database.")
            print("Check-in saved successfully.")


if __name__ == "__main__":
    main()
