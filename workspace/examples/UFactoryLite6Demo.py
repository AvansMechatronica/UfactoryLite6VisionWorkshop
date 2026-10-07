from xarm.wrapper import XArmAPI
import time
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # allow running this file directly
from libraries.poseObject import poseObject

robot_ip = '192.168.1.193'  # Replace with your robot's IP address


#define poses
home_pose = poseObject.poseObject(250, 0.0, 400, 180, 0, 180)
left_pose = poseObject.poseObject(250, -200, 400, 180, 0, 180)
right_pose = poseObject.poseObject(250, 200, 400, 180, 0, 180)
poses = [home_pose, left_pose, right_pose, home_pose]

arm = XArmAPI(robot_ip)  # Replace with your robot's IP address
arm.connect()

arm.clean_error()
arm.motion_enable(True)
arm.set_mode(0)
arm.set_state(0)

for pose in poses:
    print(f"Moving to pose: {pose}")
    #input("Press Enter to continue...")
    code = arm.set_position(*pose.pose(), wait=True)
    if code != 0:
        print(f"Move failed, code: {code}, error_code: {arm.error_code}, warn_code: {arm.warn_code}")
        arm.clean_error()
        arm.clean_warn()
        arm.motion_enable(True)
        arm.set_mode(0)
        arm.set_state(0)



arm.get_state()
print(arm.get_state())

result = arm.set_vacuum_gripper(True)   # Pick
print(f"Vacuum gripper set result: {result}")
time.sleep(2)
result = arm.set_vacuum_gripper(False)  # Release
print(f"Vacuum gripper set result: {result}")

arm.disconnect()