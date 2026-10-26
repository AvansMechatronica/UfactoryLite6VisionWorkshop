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

        print(
            "Robot position (X, Y, Z in mm; roll, pitch, yaw in degrees). "
            "Press any key to stop:"
        )
        while True:
            if msvcrt.kbhit():
                msvcrt.getwch()
                break

            code, position = robot.get_position()
            check_command(code, "Reading robot position")
            x, y, z, roll, pitch, yaw = position
            print(
                f"X={x:.2f}, Y={y:.2f}, Z={z:.2f}, "
                f"roll={roll:.2f}, pitch={pitch:.2f}, yaw={yaw:.2f}",
                flush=True,
            )
            time.sleep(POLL_INTERVAL_SECONDS)
    finally:
        robot.disconnect()


if __name__ == "__main__":
    main()
