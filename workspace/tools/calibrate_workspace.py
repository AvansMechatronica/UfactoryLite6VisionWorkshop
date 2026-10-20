import os
import sys
import threading
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # allow running this file directly

# import the opencv library
import keyboard  # load keyboard package
from xarm.wrapper import XArmAPI


from libraries.vision.markers_detection import *
from libraries.vision.usbCamera import usbCamera
from libraries.xarm_support.xarm_support import *
import cv2
import time
from libraries.vision.Workspace import Workspace
from libraries.vision.enums import *

robot_ip = '192.168.1.193'  # Replace with your robot's IP address

camera_index = 1

def initialize_camera():
    global camera
    camera = usbCamera(camera_index )
    camera.set_brightness(1.5)
    camera.set_contrast(1.0)
    camera.set_saturation(1.0)


def takePhoto():
    image = camera.take_photo()
    result, crop_image = extract_img_markers(image, workspace_ratio=1.0)
    if result:
        cv2.imshow("Crop", crop_image)
    else:
        print("Unable to extract image markers")

    result, marker_image = draw_markers(image, workspace_ratio=1.0)
    if result:
        cv2.imshow("Marker", marker_image)
    else:
        print("Unable to draw image markers")
    cv2.waitKey(1)


def orientation_warning(position):
    warnings = []
    roll_deviation = abs((position[3] - 180 + 180) % 360 - 180)
    pitch_deviation = abs((position[4] + 180) % 360 - 180)

    if roll_deviation > 2:
        warnings.append(f"roll={position[3]:.2f} deg (expected 180 +/- 2 deg)")
    if pitch_deviation > 2:
        warnings.append(f"pitch={position[4]:.2f} deg (expected 0 +/- 2 deg)")

    return f" WARNING: {', '.join(warnings)}" if warnings else ""


def read_marker_position(robot, marker_number):
    stop_event = threading.Event()

    def show_position():
        while not stop_event.is_set():
            code, position = robot.get_position()
            if code == 0:
                if 0:
                    print(
                        f"Current robot position: {position}{orientation_warning(position)}",
                        flush=True,
                    )
                else:
                    warning = orientation_warning(position)
                    if warning:
                        print(warning.strip(), flush=True)
            else:
                print(f"Could not read robot position, code {code}", flush=True)
            stop_event.wait(0.5)

    monitor = threading.Thread(target=show_position)
    monitor.start()
    try:
        input(
            f"Move the calibration tool to marker {marker_number}.\n"
            "Press Enter to record the current position:\n"
        )
    finally:
        stop_event.set()
        monitor.join()

    code, position = robot.get_position()
    if code != 0:
        raise RuntimeError(f"Could not record marker {marker_number}, code {code}")
    print(f"Recorded marker {marker_number}: {position}")
    warning = orientation_warning(position)
    if warning:
        print(warning.strip())
    return position


def main():

    robot = XArmAPI(robot_ip)
    robot.connect()

    robot.clean_error()
    robot.motion_enable(True)
    robot.set_mode(0)
    robot.set_state(0)

    print("To home pose")
    moveToJointAngles(robot, home_joint_angles)

    initialize_camera()

    workspace = Workspace()

    while True:
        ans = input("Start calibration? (y/n): ")
        if ans.lower() != 'y':
            robot.set_mode(0)
            robot.set_state(0)
            moveToJointAngles(robot, home_joint_angles)
            camera.end()  # stops the camera thread, which would otherwise keep the process alive
            robot.disconnect()
            return
        print("To observation")
        
        moveToPose(robot, observation_pose)
        takePhoto()
        moveToJointAngles(robot, home_joint_angles)
        robot.set_mode(2)
        robot.set_state(0)

        position1 = read_marker_position(robot, 1)
        pose1 = xarm_pose(x=position1[0], y=position1[1], z=position1[2], roll=position1[3], pitch=position1[4], yaw=position1[5])

        position2 = read_marker_position(robot, 2)
        pose2 = xarm_pose(x=position2[0], y=position2[1], z=position2[2], roll=position2[3], pitch=position2[4], yaw=position2[5])

        position3 = read_marker_position(robot, 3)
        pose3 = xarm_pose(x=position3[0], y=position3[1], z=position3[2], roll=position3[3], pitch=position3[4], yaw=position3[5])

        position4 = read_marker_position(robot, 4)
        pose4 = xarm_pose(x=position4[0], y=position4[1], z=position4[2], roll=position4[3], pitch=position4[4], yaw=position4[5])

        print("Calibration positions:")
        print("Marker 1:", position1)
        print("Marker 2:", position2)
        print("Marker 3:", position3)
        print("Marker 4:", position4)

        workspace.set(pose1, pose2, pose3, pose4)
        wsp = workspace.to_json()
        try:
            with open('workspace.json', 'w') as outfile:
                outfile.write(wsp)
        except Exception as e:
            print(f"Failed to write workspace to file: {e}")
        # with open('../workspace.json', 'w') as outfile:
        #     outfile.write(wsp)
        
        print(wsp)

if __name__ == "__main__":
    main()