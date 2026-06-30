import pydobot
from serial.tools import list_ports
port = "COM3"
device = pydobot.Dobot(port=port, verbose=True)
(x, y, z, r) = device.pose()
print("pose",x,y,z)
device.move_to(72.33,-294.68 ,34.59, -23.0558, wait=False)