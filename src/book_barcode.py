import cv2
import time
from pyzbar.pyzbar import decode
from pydobot import Dobot

# Camera and scan settings
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
        frame=cv2.rotate(frame,cv2.ROTATE_90_CLOCKWISE)
        barcodes = decode(frame)
        for barcode in barcodes:
            barcode_data = barcode.data.decode("utf-8")
            detected_name = barcode_data.strip()  # Treat barcode as book name
            print(f" Detected Book Name: {detected_name}")
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

def pick_book_with_dobot(expected_name, book_positions):
    """
    expected_name: string entered by user
    book_positions: list of dicts [{'x':..,'y':..,'z':..,'r':..}, ...]
    """
    port = "COM3"  # Set your Dobot COM port
    device = Dobot(port=port, verbose=True)

    try:
        # Set robot speed and acceleration
        device.speed(velocity=100, acceleration=100)

        for pos in book_positions:
            # Move to target book position
            device.move_to(pos['x'], pos['y'], pos['z'], pos.get('r', 0), wait=True)

            # Pause 3 seconds before gripping to scan barcode
            print("Pausing 3 seconds before gripping for barcode scan...")
            time.sleep(3)

            # Scan book name
            detected_name = scan_book_name()
            if detected_name and detected_name.lower() == expected_name.lower():
                print("Book matched! Picking up...")
                device.grip(True)  # Close gripper
                time.sleep(3)  # Ensure gripper holds book

                # Move to drop-off location
                device.move_to(243.6986846923828, 12.621055603027344, 0.9897842407226562, 48.053733825683594, wait=True)
                device.grip(False)  # Release book
                print("Book picked and placed successfully.")
                return True
            else:
                print("Book did not match. Moving to next position.")
                device.grip(False)  # Ensure gripper is open before next move

        print("No matching book found in all positions.")
        return False

    finally:
        device.close()

if __name__ == "__main__":
    # Get expected book name from user
    user_input = input("Enter the expected book name: ").strip()

    # List of book positions (replace with actual coordinates)
    positions = [
        {'x': 31.91568946838379, 'y': -259.38311767578125, 'z': 7.4087066650390625, 'r': -37.896263122558594},
        {'x': 35.0, 'y': -260.0, 'z': 7.4, 'r': -37.89},
        #{'x': 40.0, 'y': -255.0, 'z': 7.4, 'r': -37.89},
    ]

    pick_book_with_dobot(user_input, positions)
