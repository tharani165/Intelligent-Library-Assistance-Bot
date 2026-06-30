#!/usr/bin/env python3
"""
Realtime barcode/QR scanner using OpenCV + pyzbar.

Press 'q' to quit.
"""

import cv2
from pyzbar import pyzbar
import datetime

def decode_and_draw(frame):
    """
    Decode barcodes/QR codes in the frame, draw bounding boxes,
    and return a list of decoded (data, type, rect).
    """
    decoded_objects = pyzbar.decode(frame)
    results = []
    for obj in decoded_objects:
        (x, y, w, h) = obj.rect
        # rectangle
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # decode data
        barcode_data = obj.data.decode("utf-8", errors="replace")
        barcode_type = obj.type

        # put text above the rectangle (adjust y if too close to top)
        text = f"{barcode_type}: {barcode_data}"
        text_y = y - 10 if y - 10 > 10 else y + h + 20
        cv2.putText(frame, text, (x, text_y), cv2.FONT_HERSHEY_SIMPLEX,
                    0.6, (0, 0, 255), 2)

        results.append((barcode_data, barcode_type, obj.rect))
    return results

def main(camera_index=0, window_name="Barcode/QR Scanner"):
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print(f"ERROR: Could not open camera index {camera_index}")
        return

    print("Starting camera. Press 'q' to quit.")
    seen = set()  # optional: remember seen codes to avoid flooding prints
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        # Optional: resize for speed (uncomment if needed)
        # frame = cv2.resize(frame, (640, 480))
        frame=cv2.rotate(frame,cv2.ROTATE_90_CLOCKWISE)
        results = decode_and_draw(frame)

        # Print newly seen codes with timestamp
        for data, typ, rect in results:
            key = (data, typ)
            if key not in seen:
                seen.add(key)
                now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"[{now}] Detected {typ} -> {data}")

        cv2.imshow(window_name, frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    
    main()
