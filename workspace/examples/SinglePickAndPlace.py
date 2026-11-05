"""
Single Pick and place example.

Steps:
 1. Go to the observation pose and take a photo
 2. Detect the workspace markers
 3. Detect the object (HSV color detection)
 4. Calculate the absolute position relative to the robot using workspace.json
 5. Move 10 mm above the object, open the gripper, move down to the object, close the gripper
 6. Move the object to another position and release it
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # allow running this file directly

import math
import time

import cv2
from xarm.wrapper import XArmAPI

from libraries.vision.usbCamera import usbCamera
from libraries.vision.markers_detection import draw_markers
from libraries.vision.ObjectDetector import ObjectDetector
from libraries.vision.Workspace import Workspace
from libraries.vision.enums import *
from libraries.xarm_support.xarm_support import *

camera_index = 0
CAMERA_BRIGHTNESS = 1.5
CAMERA_CONTRAST = 1.0
CAMERA_SATURATION = 1.0
robot_ip = '192.168.1.193'  # Replace with your robot's IP address

WORKSPACE_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'workspace.json')

APPROACH_HEIGHT = 10.0   # mm above the object
GRASP_Z_OFFSET = 0.0     # mm added to the workspace height when grasping, tune for object height
GRIPPER_TIME = 1.0       # seconds to wait for the gripper to open/close
GRIPPER_ROLL = 180       # gripper pointing down
GRIPPER_PITCH = 0
GRIPPER_YAW_OFFSET = 0.0 #90.0  # deg, correction between object angle and gripper orientation

# Place position (absolute, robot coordinates in mm)
place_x, place_y, place_z = 250.0, -200.0, 150.0


def workspace_to_robot(workspace, x_rel, y_rel):
    """Bilinear interpolation between the four workspace corner poses (x_rel: top->bottom, y_rel: left->right)."""
    ul, ur = workspace.UpperLeftPose, workspace.UpperRightPose
    ll, lr = workspace.LowerLeftPose, workspace.LowerRightPose

    def interp(attr):
        top = getattr(ul, attr) + (getattr(ur, attr) - getattr(ul, attr)) * y_rel
        bottom = getattr(ll, attr) + (getattr(lr, attr) - getattr(ll, attr)) * y_rel
        return top + (bottom - top) * x_rel

    return interp('x'), interp('y'), interp('z')


def open_gripper(robot):
    robot.close_lite6_gripper()
    time.sleep(GRIPPER_TIME)


def close_gripper(robot):
    robot.open_lite6_gripper()
    time.sleep(GRIPPER_TIME)


def main():
    workspace = Workspace()
    with open(WORKSPACE_FILE) as inputfile:
        if not workspace.from_json(inputfile.read()):
            raise SystemExit("Invalid workspace file: " + WORKSPACE_FILE)

    robot = XArmAPI(robot_ip)
    robot.connect()
    robot.clean_error()
    robot.motion_enable(True)
    robot.set_mode(0)
    robot.set_state(0)

    camera = None
    try:
        print("To home pose")
        moveToJointAngles(robot, home_joint_angles)

        camera = usbCamera(camera_index)
        camera.set_brightness(CAMERA_BRIGHTNESS)
        camera.set_contrast(CAMERA_CONTRAST)
        camera.set_saturation(CAMERA_SATURATION)

        # 1. Take photo
        print("To observation pose")
        observation_pose.moveTo(robot)
        image = camera.take_photo()
        print("Back to home pose")
        moveToJointAngles(robot, home_joint_angles)

        # 2. Detect markers
        found, im_markers = draw_markers(image, workspace_ratio=1.0)
        cv2.imshow("Markers", im_markers)
        cv2.waitKey(1)
        if not found:
            print("Workspace markers not found")
            return

        # 3. Detect object
        detector = ObjectDetector(
            obj_type=ObjectType.ANY, obj_color=ColorHSV.RED,
            workspace_ratio=1.0,
            ret_image_bool=True,
        )
        status, result_pose, obj_type, obj_color, im_draw = detector.extract_object_with_hsv(image)
        if not status:
            print("No object found")
            return
        print("Object", obj_type, obj_color, "relative position:", result_pose)
        cv2.imshow("Object", im_draw)
        cv2.waitKey(1)

        # 4. Absolute position relative to the robot
        obj_x, obj_y, obj_z = workspace_to_robot(workspace, result_pose.x, result_pose.y)
        obj_z += GRASP_Z_OFFSET
        print(f"Object absolute position: x={obj_x:.1f}, y={obj_y:.1f}, z={obj_z:.1f}")

        # 5. Pick
        # object angle (rad, in workspace frame) + workspace rotation (rad) -> gripper yaw (deg)
        yaw = -math.degrees(workspace.orgin.yaw + result_pose.yaw) + GRIPPER_YAW_OFFSET
        yaw = (yaw + 180.0) % 360.0 - 180.0
        print(f"Gripper yaw: {yaw:.1f} deg")
        above = xarm_pose(obj_x, obj_y, obj_z + APPROACH_HEIGHT, GRIPPER_ROLL, GRIPPER_PITCH, yaw)
        grasp = xarm_pose(obj_x, obj_y, obj_z, GRIPPER_ROLL, GRIPPER_PITCH, yaw)
        above.moveTo(robot)
        open_gripper(robot)
        grasp.moveTo(robot)
        close_gripper(robot)
        above.moveTo(robot)

        # 6. Place
        place_above = xarm_pose(place_x, place_y, place_z, GRIPPER_ROLL, GRIPPER_PITCH, 0)
        place_above.moveTo(robot)
        open_gripper(robot)
        time.sleep(0.5)
        robot.stop_lite6_gripper()

        print("Back to home pose")
        moveToJointAngles(robot, home_joint_angles)

        print("Press any key in an image window to finish")
        cv2.waitKey(0)
    finally:
        if camera is not None:
            camera.end()
        cv2.destroyAllWindows()
        robot.disconnect()


if __name__ == "__main__":
    main()
