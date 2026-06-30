import cv2
import time
from pyzbar.pyzbar import decode
from pydobot import Dobot
import pandas as pd

# -----------------------------
# Camera and scan settings
# -----------------------------
CAMERA_INDEX = 0
SCAN_DURATION = 3  # seconds to scan before gripping

def scan_book_name(duration=SCAN_DURATION):
    cap = cv2.VideoCapture(CAMERA_INDEX)
    if not cap.isOpened():
        print(f" ERROR: Could not open camera index {CAMERA_INDEX}")
        return None

    print("Scanning book for name...")
    start_time = time.time()
    detected_name = None

    while time.time() - start_time < duration:
        ret, frame = cap.read()
        if not ret:
            continue
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        barcodes = decode(frame)
        for barcode in barcodes:
            barcode_data = barcode.data.decode("utf-8")
            detected_name = barcode_data.strip()
            print(f"Detected Book Name: {detected_name}")
            break

        cv2.imshow("Book Scan", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Scan aborted by user")
            break
        if detected_name:
            break

    cap.release()
    cv2.destroyAllWindows()
    return detected_name

# -----------------------------
# Dobot book picking function
# -----------------------------
def pick_book_with_dobot(expected_name, book_positions):
    port = "COM3"  # Adjust your Dobot COM port
    device = Dobot(port=port, verbose=True)

    try:
        device.speed(velocity=100, acceleration=100)

        for pos in book_positions:
            print(f"Moving to position: {pos}")
            device.move_to(pos['x'], pos['y'], pos['z'], pos.get('r', 0), wait=True)

            # Pause before scanning
            print("Pausing 3 seconds before barcode scan...")
            time.sleep(3)

            # Scan book name
            detected_name = scan_book_name()
            if detected_name and detected_name.lower() == expected_name.lower():
                print("Book matched! Picking up...")
                device.grip(True)  # Close gripper
                time.sleep(3)

                # Move to drop-off bin
                bin_location = {'x': 243.6987, 'y': 12.6211, 'z': 0.9898, 'r': 48.0537}
                device.move_to(bin_location['x'], bin_location['y'], bin_location['z'], bin_location['r'], wait=True)
                device.grip(False)  # Release book
                print("Book placed in bin successfully!")
                return True
            else:
                print("Book did not match. Moving to next position...")
                device.grip(False)

        print("No matching book found in scanned positions.")
        return False

    finally:
        device.close()

# -----------------------------
# Excel Lookup + Robot Integration
# -----------------------------
def main():
    # Step 1: Load Excel file
    excel_file = r"Library_Books.xlsx"
    df = pd.read_excel(excel_file)
    df.columns = df.columns.str.strip()

    # User input
    requested_book_name = input("\nEnter the book name to search: ").strip().lower()

    df['Book Name Clean'] = df['Book Name'].astype(str).str.strip().str.lower()
    df['Author Name Clean'] = df['Author Name'].astype(str).str.strip().str.lower()

    # Find matching books
    matching_books = df[df['Book Name Clean'] == requested_book_name]
    if matching_books.empty:
        print("\nNo book found with that name in the Database.")
        return

    # List available authors
    authors = matching_books['Author Name'].tolist()
    print("\nAvailable authors for this book:")
    for i, author in enumerate(authors, 1):
        print(f"{i}. {author}")

    author_index = int(input("Select the correct author (enter number): "))
    selected_author = authors[author_index - 1].strip()

    # Match book with selected author
    book_match = matching_books[matching_books['Author Name'].str.strip() == selected_author]
    if not book_match.empty:
        aisle = book_match.iloc[0]['Aisle Number']
        rack = book_match.iloc[0]['Rack Number']
        print(f"\nBook found!")
        print(f"Book Name: {requested_book_name.title()}")
        print(f"Author: {selected_author}")
        print(f"Aisle Number: {aisle}")
        print(f"Rack Number: {rack}")

        # Step 2: Robot moves & scans
        # (Here you should map Aisle/Rack → Dobot coordinates)
        positions = [
            {'x': 31.9157, 'y': -259.3831, 'z': 7.4087, 'r': -37.8963},
            {'x': 35.0, 'y': -260.0, 'z': 7.4, 'r': -37.89},
        ]

        pick_book_with_dobot(requested_book_name, positions)

    else:
        print("\nBook not found in the Database with the selected author.")

if __name__ == "__main__":
    main()
