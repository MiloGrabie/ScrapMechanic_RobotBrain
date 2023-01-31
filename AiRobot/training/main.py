import pybullet as p
import time

# Connect to the pybullet GUI (graphical user interface)
p.connect(p.GUI)

# Set the gravity
p.setGravity(0, 0, -9.8)

# Load the URDF file for the robot
robot = p.loadURDF("path/to/dog_robot.urdf", useFixedBase=False)

# Set the time step for the simulation
p.setTimeStep(1.0 / 240)

while True:
    # Step the simulation
    p.stepSimulation()

    # Get the position and orientation of the base link
    base_position, base_orientation = p.getBasePositionAndOrientation(robot)

    # Print the base position and orientation
    print(base_position, base_orientation)

    # Sleep for a bit
    time.sleep(1.0 / 240)

# Disconnect from the pybullet GUI
p.disconnect()
