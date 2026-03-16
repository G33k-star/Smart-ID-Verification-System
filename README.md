**Smart ID Verification and Check-In System**

A lightweight Python-based identity verification system that integrates an ID card scanner and computer vision to automatically log daily check-ins. The system records user information, captures a camera image for visual verification, and stores attendance data in organized CSV files for each day.

This project is designed to run on systems such as a Raspberry Pi or Linux workstation connected to an ID card scanner and camera.

---

**Features**

- Scan ID cards to register check-ins
- Computer vision capture for visual identity verification
- Automatically logs check-in data into a CSV file
- Creates a new CSV file each day
- Stores the following information:
  - Name (from ID card)
  - Card ID
  - Student ID
  - Phone Number
  - Timestamp
  - Image capture reference
- Automatically resets at 3:00 AM and begins a new daily log
- Prevents duplicate check-ins for the same user on the same day
- Designed for lightweight operation on Debian-based systems
- Compatible with Python 3.5+ environments

---

**How It Works**

1. User scans their ID card.
2. The system reads the card ID.
3. The system prompts the user to enter:
   - Student ID
   - Phone number
4. The camera captures an image for visual confirmation.
5. The program logs the check-in information to a CSV file.
6. The CSV file is automatically saved in a data folder.

Each day creates a new CSV file for easier organization and record keeping.

---

**Example CSV Output**

| Name | Card ID | Student ID | Phone Number | Timestamp |
| :-------- | :---------- | :-------: | :-------: | :-------: |
| John Doe | 1234 4568 9012 3456 | 1234567890 | 1234567890 | 2026-03-10 14:32:11 |

---

**Requirements**

- Python 3.5+
- Debian / Raspberry Pi OS recommended
- USB ID card scanner or compatible input device
- USB camera or Raspberry Pi camera module
- OpenCV (for computer vision functionality)

---

**System Architecture**

The system operates as a simple input-processing pipeline:

1. **Card Scanner Input**  
The ID scanner acts as a keyboard input device and sends the card ID to the system.

2. **Computer Vision Module**  
A camera captures an image during check-in to provide visual verification.

3. **Python Processing Script**  
The Python program captures the scanned card data and prompts the user for additional information.

4. **Data Logging Module**  
The system formats the collected information and appends it to a CSV file.

5. **Daily File Management**  
The program checks the current date and automatically creates a new CSV file when the date changes.

---
'''
smart-id-verification-system/
├── main.py
├── checkin_logs/
│   └── yyyy-mm-dd.csv
├── captured_images/
│   └── yyyy-mm-dd_14-32-11.jpg
├── database.csv
├── LICENSE
└── README.md
'''





**main.py**
Primary script responsible for handling input, camera capture, prompting users, and logging data.

**checkin_logs/**  
Directory where daily check-in CSV log files are stored.

**captured_images/**  
Directory where camera images taken during check-ins are stored.

**database.csv**  
File where all known user information is stored.
