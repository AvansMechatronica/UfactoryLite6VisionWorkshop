
class poseObject:

    def __init__(self, x=0, y=0, z=0, roll=0, pitch=0, yaw=0):
        self.x = x
        self.y = y
        self.z = z
        self.roll = roll
        self.pitch = pitch
        self.yaw = yaw
    def pose(self):
        return (self.x, self.y, self.z, self.roll, self.pitch, self.yaw)
    def __str__(self):
        return f"poseObject(x={self.x}, y={self.y}, z={self.z}, roll={self.roll}, pitch={self.pitch}, yaw={self.yaw})"


home_pose = poseObject(250, 0.0, 400, 180, 0, 0)
observation_pose = poseObject(150, 0.0, 300, 180, 0, 0)
left_pose = poseObject(250, -200, 400, 180, 0, 0)
right_pose = poseObject(250, 200, 400, 180, 0, 0)

class jointAngles:

    def __init__(self, joint1=0, joint2=0, joint3=0, joint4=0, joint5=0, joint6=0):
        self.joint1 = joint1
        self.joint2 = joint2
        self.joint3 = joint3
        self.joint4 = joint4
        self.joint5 = joint5
        self.joint6 = joint6

    def angles(self):
        return (self.joint1, self.joint2, self.joint3, self.joint4, self.joint5, self.joint6)

    def __str__(self):
        return f"jointAngles(joint1={self.joint1}, joint2={self.joint2}, joint3={self.joint3}, joint4={self.joint4}, joint5={self.joint5}, joint6={self.joint6})"   

home_joint_angles = jointAngles(0, 0, 90, 0, 90, 0)  # degrees, one value per joint

def moveToPose(robot, pose):
    code = robot.set_position(*pose.pose(), wait=True)
    if code != 0:
        print(f"Move failed, code: {code}, error_code: {robot.error_code}, warn_code: {robot.warn_code}")
        robot.clean_error()
        robot.clean_warn()
        robot.motion_enable(True)
        robot.set_mode(0)
        robot.set_state(0)

def moveToJointAngles(robot, joint_angles):
    code = robot.set_servo_angle(angle=joint_angles.angles(), wait=True)
    if code != 0:
        print(f"Move failed, code: {code}, error_code: {robot.error_code}, warn_code: {robot.warn_code}")
        robot.clean_error()
        robot.clean_warn()
        robot.motion_enable(True)
        robot.set_mode(0)
        robot.set_state(0)
