from serial.tools import list_ports
from pydobot import Dobot

port = list_ports.comports()[0].device
device = Dobot(port=port)

pose = device.pose()
print("Raw pose:", pose)

# unpack tuple
x, y, z, r, j1, j2, j3, j4 = pose
print(f"x={x}, y={y}, z={z}, r={r}")

# move back to current position (for example)
# device.move_to(x, y, z, r, wait=True)

device.close()
