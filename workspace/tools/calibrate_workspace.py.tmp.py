import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # allow running this file directly

# import the opencv library
import keyboard  # load keyboard package
from xarm.wrapper import XArmAPI

from libraries.vision.markers_detection import *
from libraries.vision.usbCamera import usbCamera
from libraries.poseObject.poseObject import *
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
        if 0:
            print("Select gripper to calibrate")
            print("1. Vacuum gripper(not supported yet), z-offset = 0.0 mm")
            print("2. Finger gripper(standard), z-offset = 85 mm")
            print("3. Adaptive gripper, z-offset = 121.5 mm")
            ans = input("What would you like to do?")
            try:
                select = int(ans)
            except ValueError:
                print("Invalid choise")
                continue
            if select == 1:
                offset = Niryo.NED.VACUUM_GRIPPER_TCP_OFFSET
                #break
            elif select == 2:
                offset = Niryo.NED.FINGER_GRIPPER_TCP_OFFSET
                break
            elif select == 3:
                offset = Niryo.NED.ADAPTIVE_GRIPPER_TCP_OFFSET
                break
            else:
                print("Invalid choise")
        offset = 0


        print("To observation")
        moveToJointAngles(robot, observation_pose)

        takePhoto()

    robot.tool.set_tcp(offset)
    robot.tool.set_tcp(offset)
    robot.tool.enable_tcp(True)

    #cv2.waitKey(0)

    robot.arm.move_to_home_pose()
    robot.arm.set_learning_mode(True)

    print("Move niryoNED calibration tool to marker 1 and press Enter(in stream/marker window)")
    cv2.waitKey(0)
    pose1 = robot.arm.get_pose()
    print(pose1)

    print("Move niryoNED calibration tool to marker 2 and press Enter(in stream/marker window)")
    cv2.waitKey(0)
    pose2 = robot.arm.get_pose()
    print(pose2)

    print("Move niryoNED calibration tool to marker 3 and press Enter(in stream/marker window)")
    cv2.waitKey(0)
    pose3 = robot.arm.get_pose()
    print(pose3)

    print("Move niryoNED calibration tool to marker 4 and press Enter(in stream/marker window)")
    cv2.waitKey(0)
    pose4 = robot.arm.get_pose()
    print(pose4)

    workspace.set(pose1, pose2, pose3, pose4)
    with open('../workspace.json', 'w') as outfile:
        outfile.write(workspace.to_json())
    wsp = workspace.to_json()
    print(wsp)

    robot.tool.enable_tcp(False)

    print("calibartion done")

    camera.end();
    robot.end()
    time.sleep(0.5)

if __name__ == "__main__":
    main()