# xArm API Documentation

Documentation for the UFACTORY xArm Python SDK, used to control the Lite 6 robot arm in the Vision Workshop.

## Installation

```bash
pip install xarm-python-sdk
```

## Getting Started

### Connecting to the Robot

```python
from xarm.wrapper import XArmAPI

arm = XArmAPI('192.168.1.123')  # Replace with the robot's IP address
```

### Disconnecting

```python
arm.disconnect()
```

## Motion

### Set Position

```python
arm.set_position(x=300, y=0, z=200, roll=180, pitch=0, yaw=0, speed=100, wait=True)
```

| Parameter | Description              | Unit  |
|-----------|--------------------------|-------|
| `x`       | X coordinate             | mm    |
| `y`       | Y coordinate             | mm    |
| `z`       | Z coordinate             | mm    |
| `roll`    | Rotation around X axis   | deg   |
| `pitch`   | Rotation around Y axis   | deg   |
| `yaw`     | Rotation around Z axis   | deg   |
| `speed`   | Movement speed           | mm/s  |
| `wait`    | Block until move is done | bool  |

### Set Joint Angles

```python
arm.set_servo_angle(angle=[0, 0, 0, 0, 0, 0], speed=50, wait=True)
```

### Get Current Position

```python
code, pose = arm.get_position()  # [x, y, z, roll, pitch, yaw]
```

### Get Joint Angles

```python
code, angles = arm.get_servo_angle()
```

## Gripper

```python
arm.set_gripper_enable(True)
arm.set_gripper_position(500, wait=True)  # 0 (open) to 850 (closed)
```

## Suction / Vacuum Gripper

```python
arm.set_suction_cup(True)   # Pick
arm.set_suction_cup(False)  # Release
```

## State Management

```python
arm.motion_enable(True)
arm.set_mode(0)      # Position control mode
arm.set_state(0)     # Sport state
arm.clean_warn()     # Clear warnings
arm.clean_error()    # Clear errors
```

## Common Workflow

```python
from xarm.wrapper import XArmAPI

arm = XArmAPI('192.168.1.123')
arm.motion_enable(True)
arm.set_mode(0)
arm.set_state(0)

# Home position
arm.set_servo_angle(angle=[0, 0, 0, 0, 0, 0], wait=True)

# Move to pick position
arm.set_position(x=250, y=0, z=150, roll=180, pitch=0, yaw=0, speed=100, wait=True)

# Grip
arm.set_suction_cup(True)

# Move to place position
arm.set_position(x=250, y=100, z=150, roll=180, pitch=0, yaw=0, speed=100, wait=True)

# Release
arm.set_suction_cup(False)

arm.disconnect()
```

## Return Codes

Most functions return a code where:

- `0` — success
- negative values — error (see SDK documentation for details)

## Reference

- Official SDK: https://github.com/xArm-Developer/xArm-Python-SDK
- User Manual: https://www.ufactory.cc/download/
