

import cv2
import time
from pyzbar.pyzbar import decode
from pydobot import Dobot

CAMERA_INDEX = 0
SCAN_DURATION = 3  # seconds

def scan_book_name(duration=SCAN_DURATION):
    cap = cv2.VideoCapture(CAMERA_INDEX)
    if not cap.isOpened():
        print(f"ERROR: Could not open camera index {CAMERA_INDEX}")
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
            detected_name = barcode.data.decode("utf-8").strip()
            print(f"Detected Book Name: {detected_name}")
            break

        cv2.imshow("Book Scan", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if detected_name:
            break

    cap.release()
    cv2.destroyAllWindows()
    return detected_name

def pick_book_with_dobot(expected_name):
    port = "COM3"
    device = Dobot(port=port, verbose=True)

    try:
        device.speed(velocity=100, acceleration=100)

        # Enable linear rail
        device._set_device_with_l(0x80, [1, 0, 0, 0])  # Enable rail V1

        # Define rail positions (step scan)
        rail_positions = [0, 100, 200, 300]

        found = False
        for rail_pos in rail_positions:
            print(f"Moving rail to {rail_pos}mm")
            device._set_l(rail_pos, isQueued=1)
            device._set_queued_cmd_start_exec()
            time.sleep(2)  # wait for rail move

            # Move arm to scanning position
            device.move_to(31.91, -259.38, 7.4, -37.89, wait=True)

            # Scan book
            detected_name = scan_book_name()
            if detected_name and detected_name.lower() == expected_name.lower():
                print("Book matched! Picking up...")
                device.grip(True)
                time.sleep(2)
                device.move_to(243.69, 12.62, 0.98, 48.05, wait=True)
                device.grip(False)
                print("Book placed in bin.")
                found = True
                break
            else:
                print("No match at this rail position, moving forward...")

        # --- Always return rail to home (0) ---
        print("Returning rail to home (0mm)")
        device._set_l(0, isQueued=1)
        device._set_queued_cmd_start_exec()
        time.sleep(2)

        if not found:
            print("Book not found along rail path.")

        return found

    finally:
        device.close()

if __name__ == "__main__":
    user_input = input("Enter expected book name: ").strip()
    pick_book_with_dobot(user_input)
