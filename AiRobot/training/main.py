import pybullet as p
import time

# Connect to the pybullet GUI (graphical user interface)
from context import Context
from multi_legged.body_ml import Body_ML
from parts.body import Body
from URDF_Interface import URDF_Interface

p.connect(p.GUI)

# Set the gravity
p.setGravity(0, 0, -9.8)

# Load the URDF file for the robot
# robot = p.loadURDF("URDF_examples/temp.urdf", useFixedBase=False)

context = Context(read_only=True)
body = Body_ML(context)
URDF_Interface = URDF_Interface(body)

robot = p.loadURDF("filename.urdf", useFixedBase=True)
# robot = p.loadURDF("URDF_examples/test_arm.urdf", useFixedBase=True)

# Set the time step for the simulation
p.setTimeStep(1.0 / 240)

while True:
    # Step the simulation
    p.stepSimulation()

    # Get the position and orientation of the base link
    base_position, base_orientation = p.getBasePositionAndOrientation(robot)

    t = p.getBodyInfo(robot)
    # p.resetDebugVisualizerCamera(cameraDistance=3, cameraYaw=30, cameraPitch=52, cameraTargetPosition=[0, 0, 0])

    # Print the base position and orientation
    # print(base_position, base_orientation)

    # Sleep for a bit
    time.sleep(1.0 / 240)

# Disconnect from the pybullet GUI
p.disconnect()
