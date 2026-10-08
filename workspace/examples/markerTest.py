import cv2
# import the opencv library
import keyboard  # load keyboard package
import time
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # allow running this file directly
from xarm.wrapper import XArmAPI
from libraries.vision.usbCamera import usbCamera
from libraries.vision.markers_detection import *
from libraries.vision.enums import *
from libraries.poseObject.poseObject import *

camera_index = 0
robot_ip = '192.168.1.193'  # Replace with your robot's IP address

def printMenu():
    print("Commands: ")
    print(" q --> Quit")
    print(" p --> Take Photo")

def main():

    robot = XArmAPI(robot_ip)
    robot.connect()

    robot.clean_error()
    robot.motion_enable(True)
    robot.set_mode(0)
    robot.set_state(0)

    print("To home pose")
    moveToJointAngles(robot, home_joint_angles)

    camera = usbCamera(camera_index)

    while True:
        printMenu()
        ans = input("Enter Choice: ")
        ans = ans.lower()

        if ans == 'q':  # returns True if "q" is pressed
            moveToJointAngles(robot, home_joint_angles)
            camera.end();
            robot.disconnect()
            time.sleep(0.5)
            break

        if ans == 'p':  # returns True if "q" is pressed
            print("To observation")
            moveToPose(robot, observation_pose)
            image = camera.take_photo(display_photo=False);
            print("Back to home pose")
            moveToJointAngles(robot, home_joint_angles)
            result = False
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
            time.sleep(1)

if __name__ == "__main__":
    main()