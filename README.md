# ID Check-In System

A lightweight Python-based ID card scanning system designed to log daily check-ins automatically. The system records user information and stores attendance data in organized CSV files for each day.

This project is designed to run on systems such as a Raspberry Pi or Linux workstation connected to an ID card scanner.

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

## How It Works

1. User scans their ID card.
2. The system reads the card ID.
3. The system prompts the user to enter:
   - Student ID
   - Phone number
4. The program logs the check-in information to a CSV file.
5. The CSV file is automatically saved in a data folder.

Each day creates a new CSV file for easier organization and record keeping.

## Example CSV Output
| Name | Card ID | Student ID | Phone Number | Timestamp |
| :-------- | :---------- | :-------: | :-------: | :-------: |
| John Doe    | 1234 4568 9012 3456 | 1234567890 | 1234567890 | 2026-03-10 14:32:11 |

## Requirements

- Python 3.5+
- Debian / Raspberry Pi OS recommended
- USB ID card scanner or compatible input device
