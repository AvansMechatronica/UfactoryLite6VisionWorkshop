import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # allow running this file directly

from xarm.wrapper import XArmAPI

robot_ip = '192.168.1.193'  # Replace with your robot's IP address

SPEED = 20  # deg/s, keep low for a demo

HOME = [0, 0, 90, 0, 90, 0]  # degrees, one value per joint


def check(code, action):
    if code != 0:
        raise RuntimeError(f"{action} failed, code: {code}, error_code: {robot.error_code}, warn_code: {robot.warn_code}")


def main():
    global robot
    robot = XArmAPI(robot_ip)
    robot.connect()

    try:
        robot.clean_error()
        robot.motion_enable(True)
        robot.set_mode(0)
        robot.set_state(0)

        print("1. All joints to home pose")
        check(robot.set_servo_angle(angle=HOME, speed=SPEED, wait=True), "Move to home")

        print("2. Joint 1 to +30 degrees (base turns left)")
        check(robot.set_servo_angle(servo_id=1, angle=30, speed=SPEED, wait=True), "Joint 1 to +30")

        print("3. Joint 1 to -30 degrees (base turns right)")
        check(robot.set_servo_angle(servo_id=1, angle=-30, speed=SPEED, wait=True), "Joint 1 to -30")

        print("4. Several joints at once: J1=0, J2=20, J6=45")
        check(robot.set_servo_angle(angle=[0, 20, 90, 0, 90, 45], speed=SPEED, wait=True), "Move several joints")

        print("5. Angles in radians (J1 = 0.5 rad = ~28.6 degrees)")
        check(robot.set_servo_angle(servo_id=1, angle=0.5, speed=SPEED * 3.14159 / 180, is_radian=True, wait=True),
              "Joint 1 in radians")

        code, angles = robot.get_servo_angle()
        check(code, "Reading joint angles")
        print("Current joint angles (degrees):", [round(a, 2) for a in angles])

        print("6. Back to home pose")
        check(robot.set_servo_angle(angle=HOME, speed=SPEED, wait=True), "Back to home")
    finally:
        robot.disconnect()


if __name__ == "__main__":
    main()
