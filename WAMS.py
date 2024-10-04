import cv2
import sqlite3
import pytesseract

# Connect to the SQLite database
conn = sqlite3.connect('license_plates.db')
cursor = conn.cursor()

# Create the license plates and entry logs tables if they don't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS license_plates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        plate_number TEXT UNIQUE
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS entry_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        plate_number TEXT,
        entry_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS exit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        plate_number TEXT,
        exit_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

# Register a license plate
def register_license_plate(plate_number):
    cursor.execute('SELECT plate_number FROM license_plates WHERE plate_number = ?', (plate_number,))
    result = cursor.fetchone()
    if result:
        print('License plate already exists in the database.')
    else:
        cursor.execute('INSERT INTO license_plates (plate_number) VALUES (?)', (plate_number,))
        conn.commit()
        print('License plate registered successfully.')


# Define the functions to verify license plates at entry gate and exit gate
def verify_license_plate_at_entry_gate(plate_number):
    cursor.execute('SELECT plate_number FROM license_plates WHERE plate_number = ?', (plate_number,))
    result = cursor.fetchone()
    if result:
        print('Access granted. License plate is authorized:', plate_number)
        # Log entry in the database
        cursor.execute('INSERT INTO entry_logs (plate_number) VALUES (?)', (plate_number,))
        conn.commit()
        return True
    else:
        print('Access denied. License plate is not authorized.')
        return False

def verify_license_plate_at_exit_gate(plate_number):
    cursor.execute('SELECT plate_number FROM license_plates WHERE plate_number = ?', (plate_number,))
    result = cursor.fetchone()
    if result:
        print('Exit granted. License plate is authorized:', plate_number)
        # Log entry in the database
        cursor.execute('INSERT INTO exit_logs (plate_number) VALUES (?)', (plate_number,))
        conn.commit()
        return True
    else:
        print('Access denied. License plate is not authorized.')
        return False

# Delete a registered license plate
def delete_license_plate(plate_number):
    cursor.execute('DELETE FROM license_plates WHERE plate_number = ?', (plate_number,))
    conn.commit()
    if cursor.rowcount > 0:
        print('License plate deleted successfully.')
    else:
        print('License plate not found.')

# Modify a registered license plate
def modify_license_plate(old_plate_number, new_plate_number):
    try:
        cursor.execute('UPDATE license_plates SET plate_number = ? WHERE plate_number = ?', (new_plate_number, old_plate_number))
        conn.commit()
        if cursor.rowcount > 0:
            print('License plate modified successfully.')
        else:
            print('License plate not found.')
    except sqlite3.IntegrityError:
        print('License plate already exists in the database.')

# Clear the entire database
def clear_database():
    cursor.execute('DELETE FROM license_plates')
    cursor.execute('DELETE FROM entry_logs')
    cursor.execute('DELETE FROM exit_logs')
    conn.commit()
    print('Database cleared successfully.')

# Load image from file
def load_image(file_path):
    image = cv2.imread(file_path)
    return image

# Extract license plate number from image
def extract_license_plate_number():
    image_path = input('Enter the path to the image file: ')
    image = load_image(image_path)

    # License plate detection and recognition
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    canny_edge = cv2.Canny(gray_image, 170, 200)
    contours, new = cv2.findContours(canny_edge.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:30]

    license_plate = None

    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.01 * perimeter, True)
        if len(approx) == 4:
            contour_with_license_plate = approx
            x, y, w, h = cv2.boundingRect(contour)
            license_plate = gray_image[y:y + h, x:x + w]
            break

    (thresh, license_plate) = cv2.threshold(license_plate, 127, 255, cv2.THRESH_BINARY)
    license_plate = cv2.bilateralFilter(license_plate, 11, 17, 17)
    (thresh, license_plate) = cv2.threshold(license_plate, 150, 180, cv2.THRESH_BINARY)
    plate_number = pytesseract.image_to_string(license_plate)
    plate_number = plate_number.replace(' ', '')  # Remove spaces from the license plate number

    cv2.imshow("License Plate Detection", image)
    cv2.imshow("Detected License Plate", license_plate)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return plate_number.strip()

# View registered license plates
def view_registered_vehicles():
    cursor.execute('SELECT * FROM license_plates')
    results = cursor.fetchall()
    if results:
        print('Registered Vehicles:')
        for row in results:
            print(row[1])
    else:
        print('No registered vehicles.')

# View entry and exit logs
def view_entry_logs():
    cursor.execute('SELECT * FROM entry_logs')
    results = cursor.fetchall()
    if results:
        print('Entry Logs:')
        for row in results:
            print('Plate Number:', row[1])
            print('Entry Time:', row[2])
            print('------------')
    else:
        print('No entry logs.')

def view_exit_logs():
    cursor.execute('SELECT * FROM exit_logs')
    results = cursor.fetchall()
    if results:
        print('Exit Logs:')
        for row in results:
            print('Plate Number:', row[1])
            print('Exit Time:', row[2])
            print('------------')
    else:
        print('No exit logs.')

# Main loop
while True:
    option = input('1. Register license plate\n2. Verify license plate at entry gate\n3. Verify license plate at exit gate\n4. Delete license plate\n5. View registered vehicles\n6. View entry logs\n7. View exit logs\n8. Clear database\n9. Exit\nChoose an option: ')

    if option == '1':
        text = extract_license_plate_number()
        if text:
            print('Detected License Plate Number:', text)
            register_license_plate(text)
        else:
            print('No license plate detected in the image')

    elif option == '2':
        plate_number = extract_license_plate_number()
        verify_license_plate_at_entry_gate(plate_number)
    elif option == '3':
        plate_number = extract_license_plate_number()
        verify_license_plate_at_exit_gate(plate_number)
    elif option == '4':
        plate_number = input('Enter the license plate number to delete: ')
        delete_license_plate(plate_number)
    elif option == '5':
        view_registered_vehicles()
    elif option == '6':
        view_entry_logs()
    elif option == '7':
        view_exit_logs()
    elif option == '8':
        clear_database()
    elif option == '9':
        break
    else:
        print('Invalid option. Please try again.')

# Close the database connection
conn.close()
