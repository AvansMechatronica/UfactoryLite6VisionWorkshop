import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # allow running this file directly

from xarm.wrapper import XArmAPI
from libraries.xarm_support.xarm_support import moveToJointAngles, home_joint_angles

robot_ip = '192.168.1.193'  # Replace with your robot's IP address

SPEED = 50  # mm/s, keep low for a demo


def check(code, action):
    if code != 0:
        raise RuntimeError(f"{action} failed, code: {code}, error_code: {robot.error_code}, warn_code: {robot.warn_code}")


def print_position():
    code, position = robot.get_position()
    check(code, "Reading position")
    print("   Position:", [round(value, 1) for value in position])


def main():
    global robot
    robot = XArmAPI(robot_ip)
    robot.connect()

    try:
        robot.clean_error()
        robot.motion_enable(True)
        robot.set_mode(0)
        robot.set_state(0)

        print("Start: joint angles to home")
        moveToJointAngles(robot, home_joint_angles)

        print("1. Absolute pose: x, y, z in mm, roll, pitch, yaw in degrees")
        check(robot.set_position(x=250, y=0, z=400, roll=180, pitch=0, yaw=0, speed=SPEED, wait=True), "Absolute move")
        print_position()

        print("2. Only change some values: x=300 (the rest stays the same)")
        check(robot.set_position(x=300, speed=SPEED, wait=True), "Move x only")
        print_position()

        print("3. Relative move: 50 mm to the left (y + 50)")
        check(robot.set_position(y=50, relative=True, speed=SPEED, wait=True), "Relative move y")
        print_position()

        print("4. Relative move: 100 mm down (z - 100)")
        check(robot.set_position(z=-100, relative=True, speed=SPEED, wait=True), "Relative move z")
        print_position()

        print("5. Rotate the tool: yaw + 45 degrees (relative)")
        check(robot.set_position(yaw=45, relative=True, speed=SPEED, wait=True), "Relative yaw")
        print_position()

        print("6. Back to the start pose")
        check(robot.set_position(x=250, y=0, z=400, roll=180, pitch=0, yaw=0, speed=SPEED, wait=True), "Back to start")
        print_position()

        moveToJointAngles(robot, home_joint_angles)
    finally:
        robot.disconnect()


if __name__ == "__main__":
    main()
