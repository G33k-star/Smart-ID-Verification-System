# ID Check-In System

A lightweight Python-based ID card scanning system designed to log daily check-ins automatically. The system records user information and stores attendance data in organized CSV files for each day.

This project is designed to run on systems such as a Raspberry Pi or Linux workstation connected to an ID card scanner.

---

## Features

- Scan ID cards to register check-ins
- Automatically logs data into a CSV file
- Creates a new CSV file each day
- Stores the following information:
  - Name (from ID card)
  - Card ID
  - Student ID
  - Phone Number
  - Timestamp
- Automatically resets at 3:00 AM and begins a new daily log
- Designed for lightweight operation on Debian-based systems
- Compatible with Python 3.5 environments

---

## How It Works

1. User scans their ID card.
2. The system reads the card ID.
3. The system prompts the user to enter:
   - Student ID
   - Phone number
4. The program logs the check-in information to a CSV file.
5. The CSV file is automatically saved in a **data folder**.

Each day creates a new CSV file for easier organization and record keeping.

---

## Example CSV Output

| Name | Card ID | Student ID | Phone Number | Timestamp |
| :-------- | :---------- | :-------: | :-------: | :-------: |
| John Doe | 1234 4568 9012 3456 | 1234567890 | 1234567890 | 2026-03-10 14:32:11 |

---

## Requirements

- Python 3.5+
- Debian / Raspberry Pi OS recommended
- USB ID card scanner or compatible input device

---

## System Architecture

The system operates as a simple input-processing pipeline:

1. **Card Scanner Input**  
   The ID scanner acts as a keyboard input device and sends the card ID to the system.

2. **Python Processing Script**  
   The Python program captures the scanned card data and prompts the user for additional information.

3. **Data Logging Module**  
   The system formats the collected information and appends it to a CSV file.

4. **Daily File Management**  
   The program checks the current date and automatically creates a new CSV file when the date changes.

---

## Project Structure

```
id-checkin-system/
│
├── main.py
├── checkin_logs/
│   ├── 2026-03-10.csv
├── database.csv
├── LICENSE
└── README.md
```

**main.py**  
Primary script responsible for handling input, prompting users, and logging data.

**checkin_logs/**  
Directory where daily checkin CSV log files are stored.

**database.csv/**  
File where all known user information are stored.

---

## Deployment (Raspberry Pi Example)

1. Clone the repository

```
git clone https://github.com/yourusername/id-checkin-system.git
```

2. Navigate into the project directory

```
cd id-checkin-system
```

3. Run the program

```
python3 main.py
```

Optional: Configure the script to run automatically on system startup using `cron` or a system service.
