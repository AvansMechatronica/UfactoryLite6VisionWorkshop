# Importeren benodigde libraries en functions in omgeving
import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from pytransform3d import rotations as pr
from pytransform3d import transformations as pt
from pytransform3d.transform_manager import TransformManager

# transformatie padestrain t.o.v. wereld(nul punt)
roll = 0
pitch = 0
yaw = -math.pi/2
rotation_euler = [roll, pitch, yaw]

x = 0.6
y = 0.3
z = 0.0
translation = [x, y, z]

padestrain2world = pt.transform_from(pr.active_matrix_from_intrinsic_euler_xyz(np.array(rotation_euler)), np.array(translation))

# transformatie robot t.o.v. padestrain
roll = 0
pitch = 0
yaw = -math.pi/2
rotation_euler = [roll, pitch, yaw]

x = 0.0
y = 0.0
z = 0.3
translation = [x, y, z]

robot2padestrain = pt.transform_from(pr.active_matrix_from_intrinsic_euler_xyz(np.array(rotation_euler)), np.array(translation))

# transformatie camera t.o.v world
cam2world = pt.transform_from(pr.active_matrix_from_intrinsic_euler_xyz(np.array([0, math.pi/2, 0])), np.array([0.6,0.6,0.9]))

# values from webots simulation
transform_translation = [0.5769463353425253, 4.0588195919510905e-07, 0.16400028704225772]
transform_rotation = [0.7071142074291583, -9.165782968693809e-07, -0.7070993548653495, 3.1415907339407982]

# transformatie object t.o.v. camera

quaternion = pr.quaternion_from_axis_angle(transform_rotation)
box2cam = pt.transform_from(pr.matrix_from_quaternion(quaternion), np.array(transform_translation))

# registreer transformaties in TransformManager
tm = TransformManager()
tm.add_transform("padestrain", "world", padestrain2world)
tm.add_transform("robot", "padestrain", robot2padestrain)
tm.add_transform("camera", "world", cam2world)
tm.add_transform("box", "camera", box2cam)

# plot alle bestaande transformaties
ax = tm.plot_frames_in("world", s=0.1)
ax = tm.plot_connections_in("world")
plt.show()

# vraag de transformatie van de box naar de robot uit de TransformManager tm
box2robot = tm.get_transform("box", "robot")

translation = pt.pq_from_transform(box2robot)[0:3]
rotation_quaternion = pt.pq_from_transform(box2robot)[3:7]
rotation = pr.euler_from_quaternion(rotation_quaternion,0,1,2, False)

print("Transform van robot naar box:")
print("  translation: x = %g, y = %g, z = %g" % (translation[0], translation[1], translation[2]))
print("  rotation: roll = %g, pitch = %g, yaw = %g" % (rotation[0], rotation[1], rotation[2]))

"""# Deel 2: Inverse Kinematica"""

# Importeren benodigde libraries en functions in omgeving
import ikpy
from ikpy.chain import Chain
from ikpy.link import OriginLink, URDFLink

# definitie van de joint namen van de niryoNED robot
joint_names = ['joint_1', 'joint_2', 'joint_3', 'joint_4', 'joint_5', 'joint_6', 'gripper::left', 'gripper::right']

# kinematic chain van het model laden
filename = "Ned.urdf"
armChain = Chain.from_urdf_file(filename, active_links_mask = [False, True, True, True, True, True, True, False, False])
#print(armChain)

# bereken de joint_values van de NiryoNED robot a.h. van de transformatie uit het voorbeeld van Transformaties
joint_values = armChain.inverse_kinematics(translation, rotation, orientation_mode = "Z", max_iter=4)

i = 0
for joint in joint_names:
  i = i + 1
  print("%s = %g" % (joint, joint_values[i]))

# plot alle robot-joints and links
ax = plt.figure().add_subplot(111, projection='3d')
armChain.plot(joint_values, ax)
plt.show()

"""Resultaat van de aansturing met de joint_values
Filmpje van simualtie in webots: https://youtu.be/JEYSEGsAdU8 (Openen in nieuw tabblad !!!)
"""