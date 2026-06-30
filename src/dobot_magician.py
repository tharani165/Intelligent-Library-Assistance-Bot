import time
import DobotDllType as dType

def main():
    api = dType.load()

    # Connect to Dobot
    state = dType.ConnectDobot(api, "COM3", 115200)[0]
    if state != dType.DobotConnect.DobotConnect_NoError:
        print("Connect failed:", state)
        return
    print("Connected to Dobot")

    # Clear command queue
    dType.SetQueuedCmdClear(api)

    # Enable rail (V1)
    dType.SetDeviceWithL(api, 1, 0, 0)

    # Set motion params
    dType.SetPTPJointParams(api, 100, 100, 100, 100, 100, 100, 100, 100)
    dType.SetPTPCommonParams(api, 100, 100)

    # Move to (200,0,50)
    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 200, 0, 50, 0, 1)

    # Move rail (example: 50 mm forward)
    # convert mm → pulses: adjust conversion constants to your rail
    pulses_per_mm = 100  # calibrate this!
    dType.SetEMotorS(api, 0, 1, 2000, 50 * pulses_per_mm, 1)

    # Open gripper
    dType.SetEndEffectorGripper(api, 1, 0, 1)

    # Close gripper
    time.sleep(1)
    dType.SetEndEffectorGripper(api, 1, 1, 1)

    # Move to (245,0,35)
    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 245, 0, 35, 0, 1)

    # Release gripper
    dType.SetEndEffectorGripper(api, 1, 0, 1)

    # Start execution
    dType.SetQueuedCmdStartExec(api)
    time.sleep(10)
    dType.SetQueuedCmdStopExec(api)

    # Disconnect
    dType.DisconnectDobot(api)

if __name__ == "__main__":
    main()
