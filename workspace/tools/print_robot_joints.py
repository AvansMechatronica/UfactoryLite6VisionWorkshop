import msvcrt
import time

from xarm.wrapper import XArmAPI


ROBOT_IP = "192.168.1.193"
POLL_INTERVAL_SECONDS = 0.5


def check_command(code, command):
    if code != 0:
        raise RuntimeError(f"{command} failed with code {code}")


def main():
    robot = XArmAPI(ROBOT_IP)
    try:
        robot.connect()
        check_command(robot.clean_error(), "Clearing robot errors")
        check_command(robot.motion_enable(True), "Enabling robot motion")
        check_command(robot.set_mode(2), "Setting robot mode to 2")
        check_command(robot.set_state(0), "Setting robot state to 0")

        print("Robot joint angles (degrees). Press any key to stop:")
        while True:
            if msvcrt.kbhit():
                msvcrt.getwch()
                break

            code, angles = robot.get_servo_angle(is_radian=False)
            check_command(code, "Reading robot joint angles")
            print(
                ", ".join(
                    f"J{joint}={angle:.2f}" for joint, angle in enumerate(angles, 1)
                ),
                flush=True,
            )
            time.sleep(POLL_INTERVAL_SECONDS)
    finally:
        robot.disconnect()


if __name__ == "__main__":
    main()
