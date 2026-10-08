import os
import sys
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

camera_index = 0

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
        input("Robot is in manual mode. Move it by hand, then press Enter to read the position...")
 
        ans = input("Move uFactory calibration tool to marker 1 and press Enter")

        code, position1 = robot.get_position()
        print("Robot position:", position1 if code == 0 else f"read failed, code {code}")
        pose1 = PoseObject(x=position1[0], y=position1[1], z=position1[2], roll=position1[3], pitch=position1[4], yaw=position1[5])
    
        ans = input("Move uFactory calibration tool to marker 2 and press Enter")

        code, position2 = robot.get_position()
        print("Robot position:", position2 if code == 0 else f"read failed, code {code}")
        pose2 = PoseObject(x=position2[0], y=position2[1], z=position2[2], roll=position2[3], pitch=position2[4], yaw=position2[5])

        ans = input("Move uFactory calibration tool to marker 3 and press Enter")

        code, position3 = robot.get_position()
        print("Robot position:", position3 if code == 0 else f"read failed, code {code}")
        pose3 = PoseObject(x=position3[0], y=position3[1], z=position3[2], roll=position3[3], pitch=position3[4], yaw=position3[5])

        ans = input("Move uFactory calibration tool to marker 4 and press Enter")

        code, position4 = robot.get_position()
        print("Robot position:", position4 if code == 0 else f"read failed, code {code}")
        pose4 = PoseObject(x=position4[0], y=position4[1], z=position4[2], roll=position4[3], pitch=position4[4], yaw=position4[5])

        print("Calibration positions:")
        print("Marker 1:", position1)
        print("Marker 2:", position2)
        print("Marker 3:", position3)
        print("Marker 4:", position4)

        workspace.set(pose1, pose2, pose3, pose4)
        with open('../workspace.json', 'w') as outfile:
            outfile.write(workspace.to_json())
        wsp = workspace.to_json()
        print(wsp)

if __name__ == "__main__":
    main()