import time
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # allow running this file directly

from xarm.wrapper import XArmAPI
import cv2
# import the opencv library
import keyboard  # load keyboard package
from libraries.vision.markers_detection import *
from libraries.vision.usbCamera import usbCamera
from libraries.xarm_support.xarm_support import *
from libraries.vision.enums import *

robot_ip = '192.168.1.193'  # Replace with your robot's IP address

camera_index = 0
# The pose from where the image processing happens

def initialize_camera():
    global camera
    camera = usbCamera(camera_index)
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


def printMenu():
    print("Commands: ")
    print(" q --> Quit")
    print(" o --> Goto to observation-pose")
    print(" r --> Goto resting-pose")
    print(" p --> Take Photo")
    print(" s --> Save Image")

def main():

    initialize_camera()

    robot = XArmAPI(robot_ip)
    robot.connect()

    robot.clean_error()
    robot.motion_enable(True)
    robot.set_mode(0)
    robot.set_state(0)

    print("To home pose")
    moveToJointAngles(robot, home_joint_angles)

    print("To observation")
    moveToPose(robot, observation_pose)

    print("Take photo")
    takePhoto()

    print("To home pose")
    moveToJointAngles(robot, home_joint_angles)

    print("Ready")

    while True:
        printMenu()
        ans = input("Enter Choice: ")
        ans = ans.lower()
        if ans == "q":  # returns True if "q" is pressed
            moveToJointAngles(robot, home_joint_angles)
            camera.end();
            robot.disconnect()
            time.sleep(0.5)
            break
        if ans == "o":  # returns True if "o" is pressed
            print("To observation")
            moveToPose(robot, observation_pose)
            camera.enable_crosshair(True)
            time.sleep(0.5)
        if ans == "r":  # returns True if "o" is pressed
            print("To resting pose")
            moveToPose(robot, home_pose)
            time.sleep(0.5)
        if ans == "p":  # returns True if "o" is pressed
            print("Take photo")
            takePhoto()
            time.sleep(0.5)

if __name__ == "__main__":
    main()