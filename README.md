Warehouse Access Management System

Overview

The Warehouse Access Management System is designed to automate and secure the process of managing truck access at a warehouse. This system uses cameras to capture and identify truck license plates, allowing or denying access based on pre-registered plates in the database. The system also maintains logs of entry and exit times, providing a complete audit trail of warehouse access events.

Key Features

	•	License Plate Registration: Allows for registering truck license plates in the system’s database.
	•	Access Control at Entry and Exit: Verifies the license plate at entry and exit gates. If the plate is authorized, access is granted.
	•	Real-Time Logging: Records timestamps of entries and exits, creating a log for audit purposes.
	•	License Plate Detection: Utilizes OpenCV and Tesseract OCR to detect and extract license plate numbers from images.
	•	Database Management: Stores license plate data, entry logs, and exit logs in an SQLite database.
	•	Modifications and Deletions: Registered plates can be modified or deleted as required.
	•	View Logs: Enables viewing registered plates, entry logs, and exit logs.

Technologies Used

	•	Python: The core logic for handling user inputs, database operations, and image processing is written in Python.
	•	OpenCV: Used for image processing and detecting the license plate from the camera images.
	•	Tesseract OCR: For converting the detected license plate image into a string format.
	•	SQLite: A lightweight database used to store registered license plates and log access data.

How It Works

	1.	License Plate Registration: Users can capture and register truck license plates through camera images. The system detects the plate using OpenCV, extracts the number using Tesseract, and stores it in the database.
	2.	Access Verification:
	•	At Entry: The system captures the truck’s license plate as it approaches the entry gate. If the license plate is found in the database, access is granted, and the event is logged.
	•	At Exit: Similarly, at the exit gate, the system checks if the truck is authorized to leave and logs the event accordingly.
	3.	Data Management: Users can:
	•	View registered license plates.
	•	View entry and exit logs.
	•	Modify or delete license plates.
	•	Clear all database entries.

Installation

	1.	Clone this repository to your local machine.
	2.	Install the required Python libraries:
       - pip install opencv-python pytesseract sqlite3
Usage

	•	Register a License Plate: Capture the license plate image, and the system will extract and register it.
	•	Verify License Plate: At both entry and exit points, the system will check the license plate and allow or deny access.
	•	Manage Data: Use options to view, modify, delete, or clear data in the database.

Future Enhancements

	•	Integration with Security Cameras: Connect the system directly to live security camera feeds for real-time access management.
	•	Web Interface: Create a web-based dashboard for remote access to logs and management.
	•	Automatic Notifications: Send alerts when unauthorized access attempts are detected.

This system offers an efficient and secure solution to manage vehicle access in warehouses using license plate recognition. It minimizes human intervention while ensuring all access events are logged for security and auditing purposes.
