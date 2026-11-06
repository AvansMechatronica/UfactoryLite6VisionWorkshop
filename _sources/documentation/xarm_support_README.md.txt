# xarm_support-bibliotheek

Kleine hulpbibliotheek voor het aansturen van de UFactory Lite 6 met de `xarm`-SDK (`XArmAPI`). Alle bewegingen worden uitgevoerd met `wait=True`, dus de functie keert pas terug als de beweging klaar is.

```python
from xarm.wrapper import XArmAPI
from libraries.xarm_support.xarm_support import *

robot = XArmAPI("192.168.1.193")
robot.connect()
robot.clean_error()
robot.motion_enable(True)
robot.set_mode(0)
robot.set_state(0)

moveToJointAngles(robot, home_joint_angles)
moveToPose(robot, observation_pose)

robot.disconnect()
```

Bestand: [xarm_support.py](./xarm_support.py)

---

## `xarm_pose(x=0, y=0, z=0, roll=0, pitch=0, yaw=0)`

Een positie en oriëntatie in het basiscoördinatensysteem van de robot. `x`, `y` en `z` zijn in millimeters, `roll`, `pitch` en `yaw` in graden.

| Onderdeel | Beschrijving |
|-----------|--------------|
| `pose()` | Geeft de waarden terug als tuple `(x, y, z, roll, pitch, yaw)` |
| `moveTo(robot)` | Beweegt de robot naar deze pose met `set_position` |
| `str(pose)` | Leesbare tekst, bijvoorbeeld voor `print` |

## `xarm_jointAngles(joint1=0, ..., joint6=0)`

De zes gewrichtshoeken in graden.

| Onderdeel | Beschrijving |
|-----------|--------------|
| `angles()` | Geeft de hoeken terug als tuple van zes waarden |
| `moveTo(robot)` | Beweegt de robot naar deze hoeken met `set_servo_angle` |
| `str(hoeken)` | Leesbare tekst |

## Functies

| Functie | Beschrijving |
|---------|--------------|
| `moveToPose(robot, pose)` | Beweegt naar een `xarm_pose`; doet hetzelfde als `pose.moveTo(robot)` |
| `moveToJointAngles(robot, joint_angles)` | Beweegt naar een `xarm_jointAngles`; doet hetzelfde als `joint_angles.moveTo(robot)` |

**Foutafhandeling:** geeft de SDK een foutcode terug, dan wordt er een melding geprint met `code`, `error_code` en `warn_code`. Daarna worden fouten en waarschuwingen gewist, wordt de motor weer ingeschakeld en gaat de robot terug naar mode 0, state 0. De beweging zelf wordt niet opnieuw geprobeerd; roep de functie dan zelf opnieuw aan.

## Vooraf gedefinieerde posities

| Naam | Type | Waarde |
|------|------|--------|
| `home_pose` | `xarm_pose` | x=250, y=0, z=400, roll=180, pitch=0, yaw=0 |
| `observation_pose` | `xarm_pose` | x=210, y=0, z=350, roll=180, pitch=0, yaw=0 (om foto's van het werkvlak te maken) |
| `left_pose` | `xarm_pose` | x=250, y=-200, z=400, roll=180, pitch=0, yaw=0 |
| `right_pose` | `xarm_pose` | x=250, y=200, z=400, roll=180, pitch=0, yaw=0 |
| `home_joint_angles` | `xarm_jointAngles` | 0°, 0°, 90°, 0°, 90°, 0° (veilige uitgangspositie) |

> Het voorbeeld `examples\UFactoryLite6Demo.py` definieert zelf poses met `yaw=180`, terwijl de poses in deze bibliotheek `yaw=0` gebruiken.

## Tips

- Zorg dat de robot in mode 0 en state 0 staat voor een beweging naar een positie. Mode 2 is bedoeld om de robot met de hand te verplaatsen (zoals in `tools\print_robot_position.py`).
- Gebruik `moveToJointAngles(robot, home_joint_angles)` als eerste beweging. Een gewrichtsbeweging is voorspelbaarder dan een rechtlijnige beweging naar een pose, die kan mislukken als de robot in een ongunstige stand staat.
- Controleer dat het werkgebied vrij is voordat je een script start.
