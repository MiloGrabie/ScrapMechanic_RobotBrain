# Whole Robot Inverse Kinematics with ikpy

This implementation allows you to use ikpy to handle the entire robot as a single chain instead of individual arms, with built-in plotting capabilities.

## Overview

Instead of creating separate IK solvers for each arm, the `WholeRobotInverseKinematics` class creates a complete robot chain that includes all arms and their joints. This provides several advantages:

1. **Unified IK solving**: Solve IK for the entire robot at once
2. **Built-in plotting**: Use ikpy's `Chain.plot()` method for visualization
3. **Multi-arm coordination**: Solve IK for multiple arms simultaneously
4. **Better optimization**: Consider the entire robot structure when solving IK

## Files

- `inverseKinematics.py`: Contains the new `WholeRobotInverseKinematics` class
- `test_whole_robot_ik.py`: Simple test script to demonstrate usage
- `example_whole_robot.py`: More comprehensive example with animations

## Usage

### Basic Setup

```python
from context import Context
from multi_legged.body_ml import Body_ML
from inverseKinematics import WholeRobotInverseKinematics

# Initialize your robot
context = Context(read_only=True)
body = Body_ML(context)

# Create the whole robot IK solver
whole_robot_ik = WholeRobotInverseKinematics(body)
```

### Single Arm IK

```python
# Solve IK for a specific arm
target_position = np.array([2.0, 1.0, -1.0])
angles = whole_robot_ik.solve_ik_for_arm(0, target_position)

# Apply the angles to the robot
whole_robot_ik.update_robot_angles(angles)
```

### Multiple Arms IK

```python
# Solve IK for multiple arms simultaneously
targets = {
    0: np.array([2.0, 1.0, -1.0]),  # Arm 0 target
    1: np.array([-2.0, 1.0, -1.0]), # Arm 1 target
    2: np.array([0.0, 2.0, -1.0])   # Arm 2 target
}
angles = whole_robot_ik.solve_ik_for_multiple_arms(targets)

# Apply the angles
whole_robot_ik.update_robot_angles(angles)
```

### Plotting

```python
# Plot the robot with current angles
whole_robot_ik.plot_robot()

# Plot with specific angles and target positions
target_positions = [
    np.array([2.0, 1.0, -1.0]),
    np.array([-2.0, 1.0, -1.0])
]
whole_robot_ik.plot_robot(angles, target_positions)
```

### Getting Robot Information

```python
# Get information about the robot chain
info = whole_robot_ik.get_robot_info()
print(f"Robot has {info['total_links']} links")
print(f"Robot has {info['total_arms']} arms")
print(f"Current angles: {info['current_angles']}")
```

## Key Features

### 1. Complete Robot Chain
The class creates a single ikpy Chain that includes:
- Base link (origin)
- All arm base links
- All joints from all arms
- Proper joint connections and transformations

### 2. Multi-Arm IK Solving
- Solve IK for individual arms
- Solve IK for multiple arms simultaneously
- Weighted averaging for multi-target solutions

### 3. Built-in Plotting
- Uses ikpy's `Chain.plot()` method
- Shows the complete robot structure
- Can display target positions as red dots
- Interactive 3D visualization

### 4. Joint Mapping
- Automatically maps chain angles back to individual robot joints
- Updates the actual robot joints with calculated angles
- Maintains compatibility with existing robot control

## Advantages over Individual Arm IK

1. **Better Coordination**: Considers the entire robot structure
2. **Reduced Conflicts**: Minimizes interference between arms
3. **Unified Optimization**: Single optimization problem instead of multiple
4. **Built-in Visualization**: No need for custom plotting code
5. **Easier Multi-Arm Control**: Single interface for all arms

## Running the Examples

### Test Script
```bash
cd AiRobot
.\venv\Scripts\python.exe test_whole_robot_ik.py
```

### Full Example
```bash
cd AiRobot
.\venv\Scripts\python.exe example_whole_robot.py
```

## Integration with Existing Code

You can easily integrate this with your existing code by replacing individual arm IK calls:

**Before (individual arms):**
```python
for arm in body.arms:
    arm.inverseKinematics.getAngle(target)
```

**After (whole robot):**
```python
whole_robot_ik = WholeRobotInverseKinematics(body)
targets = {i: target for i, arm in enumerate(body.arms)}
angles = whole_robot_ik.solve_ik_for_multiple_arms(targets)
whole_robot_ik.update_robot_angles(angles)
```

## Notes

- The virtual environment at `./venv/` is used for all dependencies
- ikpy's `Chain.plot()` method provides the visualization
- The implementation maintains compatibility with your existing robot structure
- All plotting is done using matplotlib through ikpy's built-in plotting utilities 