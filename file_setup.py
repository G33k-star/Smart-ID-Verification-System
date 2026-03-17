import csv
import os
from datetime import datetime, timedelta
from config import DATABASE_FOLDER, DATABASE_FILE, CHECKIN_FOLDER, TERMS_FILE, PHOTO_FOLDER

os.makedirs(CHECKIN_FOLDER, exist_ok=True)
os.makedirs(DATABASE_FOLDER, exist_ok=True)

def create_database_if_needed():
    if not os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([
                "Name",
                "Card ID",
                "Student ID",
                "Phone Number",
                "myMDC Username",
                "Email"
            ])

def create_terms_file_if_needed():
    if not os.path.exists(TERMS_FILE):
        with open(TERMS_FILE, mode="w", encoding="utf-8") as file:
            file.write("")

def get_terms_text():
    create_terms_file_if_needed()
    with open(TERMS_FILE, mode="r", encoding="utf-8") as file:
        return file.read()

def get_today_photo_folder():
    folder = os.path.join(PHOTO_FOLDER, get_system_day())
    os.makedirs(folder, exist_ok=True)
    return folder

def get_today_checkin_file():
    today = datetime.now().strftime("%Y-%m-%d")
    filename = "checkin_{0}.csv".format(today)
    return os.path.join(CHECKIN_FOLDER, filename)

def create_checkin_file_if_needed(filename):
    if not os.path.exists(filename):
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([
                "Name",
                "Card ID",
                "Student ID",
                "Phone Number",
                "Timestamp"
            ])
            
def get_system_day():
    now = datetime.now()

    # If current time is before 3:00 AM,
    # treat it as part of the previous day
    if now.hour < 3:
        now = now - timedelta(days=1)

    return now.strftime("%Y-%m-%d")