import time
from pydobot import Dobot

def main():
    port = "COM3"
    device = Dobot(port=port, verbose=True)
   
    try:
        device.speed(velocity=100, acceleration=100)
        device.move_to(243.6986846923828, 12.621055603027344, 0.9897842407226562, 48.053733825683594, wait=True)
        print("Moving linear rail to 0 -- implement this if supported")
        device.grip(False)
        print("Moving linear rail to 300 -- implement if supported")
        print("Moving joints to angles J1=-84, J2=0, J3=33 -- implement if supported")
        device.move_to(31.91568946838379, -259.38311767578125, 7.4087066650390625, -37.896263122558594, wait=True)
        device.move_to(31.91568946838379, -259.38311767578125, 7.4087066650390625, -37.896263122558594, wait=True)
        device.grip(True)
        time.sleep(1)
        device.move_to(243.6986846923828, 12.621055603027344, 0.9897842407226562, 48.053733825683594, wait=True)
        device.grip(False)
        device.suck(False)
        print("Moving linear rail back to 0 -- implement if supported")
        print("Sequence completed.")

    finally:
        device.close()

if __name__ == "__main__":
    main()
