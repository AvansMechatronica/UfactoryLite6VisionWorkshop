import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # allow running this file directly

from libraries.xarm_support.xarm_support import moveToJointAngles, moveToPose

import cv2
# import the opencv library
import keyboard  # load keyboard package
from xarm.wrapper import XArmAPI

from libraries.vision.usbCamera import usbCamera
from libraries.vision.markers_detection import *
from libraries.vision.ObjectDetector import ObjectDetector
from libraries.vision.enums import *
from libraries.xarm_support.xarm_support import *

import time

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
    camera.set_brightness(2.0)
    camera.set_contrast(1.0)
    camera.set_saturation(1.0)

    while True:
        printMenu()
        ans = input("Enter Choice: ")
        ans = ans.lower()

        if ans == 'q':  # returns True if "q" is pressed
            moveToJointAngles(robot, home_joint_angles)
            camera.end();
            robot.disconnect()
            time.sleep(0.5)
            camera.end();
            break

        if ans == 'p':  # returns True if "q" is pressed
            print("To observation")
            moveToPose(robot, observation_pose)

            image = camera.take_photo()

            print("Back to home pose")
            moveToJointAngles(robot, home_joint_angles)
            
            detector = ObjectDetector(
                obj_type=ObjectType.ANY, obj_color=ColorHSVPrime.RED,
                workspace_ratio=1.0,
                ret_image_bool=True,
            )
            all = False
            if all:
                status, cx_rel_list, cy_rel_list, list_size, angle_list, color_list, object_type_list = detector.extract_all_object_with_hsv(image)
            else:
                status, result_pose, obj_type, obj_color, im_draw = detector.extract_object_with_hsv(image)
                if status:
                    print(result_pose)
                    print(obj_type)
                    print(obj_color)
                    cv2.imshow("Result", im_draw)
                    
                    #realword_pose = workspace.get_pose(result_pose.x, result_pose.y, result_pose.yaw)
                    #print(realword_pose)
            
            cv2.waitKey(1)
            time.sleep(1)


if __name__ == "__main__":
    main()