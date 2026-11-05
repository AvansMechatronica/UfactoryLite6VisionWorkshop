"""
Sort objects into bins left of the workspace.

Order: red, green, blue; for each color: square, circle, any.
Bins are 40 mm apart (center to center); their positions are defined at the top (BIN_*).

Steps per object:
 1. Go to the observation pose and take a photo
 2. Detect the workspace markers
 3. Detect the object (HSV color/shape detection)
 4. Calculate the absolute position relative to the robot using workspace.json
 5. Move 10 mm above the object, open the gripper, move down to the object, close the gripper
 6. Move the object to its bin and release it
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

# Bins left of the workspace, in a row along the workspace x-axis (robot coordinates in mm)
BIN_FIRST_X = 190.0      # x of the first bin (red, square)
BIN_Y = -200.0           # y of all bin centers
BIN_Z = 150.0            # z to release the object above a bin
BIN_PITCH = 40.0         # center-to-center distance between bins

MAX_OBJECTS_PER_CLASS = 10  # safety limit

# Sorting order: color first (red, green, blue), then shape (square, circle, any)
COLORS = [("red", ColorHSV.RED), ("green", ColorHSV.GREEN), ("blue", ColorHSV.BLUE)]
SHAPES = [("square", ObjectType.SQUARE), ("circle", ObjectType.CIRCLE), ("any", ObjectType.ANY)]

# (color name, color, shape name, shape) -> bin position
BINS = {}
for _ci, (_cn, _c) in enumerate(COLORS):
    for _si, (_sn, _s) in enumerate(SHAPES):
        BINS[(_cn, _sn)] = (BIN_FIRST_X + (_ci * len(SHAPES) + _si) * BIN_PITCH, BIN_Y, BIN_Z)


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


def sort_one(robot, camera, workspace, color, shape, bin_pos):
    """Pick one object of the given color/shape and put it in its bin. Returns False if none is found."""
    # 1. Take photo
    observation_pose.moveTo(robot)
    image = camera.take_photo()
    moveToJointAngles(robot, home_joint_angles)

    # 2. Detect markers
    found, im_markers = draw_markers(image, workspace_ratio=1.0)
    cv2.imshow("Markers", im_markers)
    cv2.waitKey(1)
    if not found:
        print("Workspace markers not found")
        return False

    # 3. Detect object
    detector = ObjectDetector(obj_type=shape, obj_color=color, workspace_ratio=1.0, ret_image_bool=True)
    status, result_pose, obj_type, obj_color, im_draw = detector.extract_object_with_hsv(image)
    if not status:
        return False
    print("Object", obj_type, obj_color, "relative position:", result_pose)
    cv2.imshow("Object", im_draw)
    cv2.waitKey(1)

    # 4. Absolute position relative to the robot
    obj_x, obj_y, obj_z = workspace_to_robot(workspace, result_pose.x, result_pose.y)
    obj_z += GRASP_Z_OFFSET

    # 5. Pick: object angle (rad, workspace frame) + workspace rotation (rad) -> gripper yaw (deg)
    yaw = -math.degrees(workspace.orgin.yaw + result_pose.yaw) + GRIPPER_YAW_OFFSET
    yaw = (yaw + 180.0) % 360.0 - 180.0
    above = xarm_pose(obj_x, obj_y, obj_z + APPROACH_HEIGHT, GRIPPER_ROLL, GRIPPER_PITCH, yaw)
    grasp = xarm_pose(obj_x, obj_y, obj_z, GRIPPER_ROLL, GRIPPER_PITCH, yaw)
    above.moveTo(robot)
    open_gripper(robot)
    grasp.moveTo(robot)
    close_gripper(robot)
    above.moveTo(robot)

    # 6. Place in the bin
    bx, by, bz = bin_pos
    xarm_pose(bx, by, bz, GRIPPER_ROLL, GRIPPER_PITCH, 0).moveTo(robot)
    open_gripper(robot)
    moveToJointAngles(robot, home_joint_angles)
    return True


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

        for color_name, color in COLORS:
            for shape_name, shape in SHAPES:
                bin_pos = BINS[(color_name, shape_name)]
                for _ in range(MAX_OBJECTS_PER_CLASS):
                    if not sort_one(robot, camera, workspace, color, shape, bin_pos):
                        break
                else:
                    print(f"Limit reached for {color_name} {shape_name}")
                print(f"Done: {color_name} {shape_name}")

        robot.stop_lite6_gripper()
        print("Sorting finished")

        print("Press any key in an image window to finish")
        cv2.waitKey(0)
    finally:
        if camera is not None:
            camera.end()
        cv2.destroyAllWindows()
        robot.disconnect()


if __name__ == "__main__":
    main()
