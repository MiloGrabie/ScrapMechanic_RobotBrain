import numpy as np
import time
from context import Context
from multi_legged.body_ml import Body_ML
from wholeRobotIK import WholeRobotIK

def main():
    """
    Example demonstrating how to use the whole robot IK class
    instead of individual arm IK.
    """
    
    # Initialize context and body (same as your existing setup)
    context = Context(read_only=True)
    body = Body_ML(context)
    
    # Create the whole robot IK solver
    whole_robot_ik = WholeRobotIK(body)
    
    print("Whole Robot IK initialized!")
    print(f"Robot has {len(body.arms)} arms")
    
    # Get robot information
    info = whole_robot_ik.get_robot_info()
    print(f"Robot chain has {info['total_links']} links")
    
    # Example 1: Solve IK for a single arm
    print("\n--- Example 1: Single Arm IK ---")
    target_position = np.array([2.0, 1.0, -1.0])
    angles = whole_robot_ik.solve_ik_for_arm(0, target_position)
    print(f"Solved angles for arm 0: {angles}")
    
    # Plot the robot with the target
    whole_robot_ik.plot_robot(angles, [target_position])
    time.sleep(2)
    
    # Example 2: Solve IK for multiple arms simultaneously
    print("\n--- Example 2: Multiple Arms IK ---")
    targets = {
        0: np.array([2.0, 1.0, -1.0]),
        1: np.array([-2.0, 1.0, -1.0])
    }
    angles = whole_robot_ik.solve_ik_for_multiple_arms(targets)
    print(f"Solved angles for multiple arms: {angles}")
    
    # Plot the robot with multiple targets
    target_positions = list(targets.values())
    whole_robot_ik.plot_robot(angles, target_positions)
    time.sleep(2)
    
    # Example 3: Animate the robot
    print("\n--- Example 3: Robot Animation ---")
    animation_targets = [
        np.array([1.5, 0.5, -0.5]),
        np.array([-1.5, 0.5, -0.5])
    ]
    
    # Animate the robot moving to the targets
    whole_robot_ik.animate_robot(animation_targets, duration=3.0, steps=60)
    
    # Example 4: Get forward kinematics
    print("\n--- Example 4: Forward Kinematics ---")
    positions = whole_robot_ik.get_forward_kinematics()
    for i, pos in enumerate(positions):
        print(f"Arm {i} end effector position: {pos}")
    
    # Keep the plot open
    print("\nPress Ctrl+C to exit...")
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Closing...")
        whole_robot_ik.close_plot()

if __name__ == "__main__":
    main() 