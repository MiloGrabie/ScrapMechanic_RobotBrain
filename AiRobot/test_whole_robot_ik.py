import numpy as np
import time
from context import Context
from multi_legged.body_ml import Body_ML
from inverseKinematics import WholeRobotInverseKinematics

def test_whole_robot_ik():
    """
    Test the whole robot inverse kinematics functionality.
    """
    
    # Initialize context and body
    context = Context(read_only=True)
    body = Body_ML(context)

    # print a json representation of the body
    
    print("Initializing whole robot IK...")
    
    # Create the whole robot IK solver
    whole_robot_ik = WholeRobotInverseKinematics(body)
    
    print(f"Robot has {len(body.arms)} arms")
    
    # Get robot information
    info = whole_robot_ik.get_robot_info()
    print(f"Robot chain has {info['total_links']} links")
    
    # Test single arm IK
    print("\nTesting single arm IK...")
    target_position = np.array([2.0, 1.0, -1.0])
    # angles = whole_robot_ik.solve_ik_for_arm(0, target_position)
    # print(f"Solved angles for arm 0: {angles}")
    
    # Test multiple arms IK
    print("\nTesting multiple arms IK...")
    targets = {
        0: np.array([2.0, 1.0, -1.0]),
        1: np.array([-2.0, 1.0, -1.0])
    }
    # angles = whole_robot_ik.solve_ik_for_multiple_arms(targets)
    # print(f"Solved angles for multiple arms: {angles}")
    
    # Test plotting (this will open a matplotlib window)
    print("\nTesting plotting...")
    try:
        whole_robot_ik.plot_robot(None, list(targets.values()))
        print("Plot should be displayed. Close the window to continue.")
        time.sleep(5)  # Keep plot open for 5 seconds
    except Exception as e:
        print(f"Plotting failed: {e}")
    
    print("Test completed!")

if __name__ == "__main__":
    test_whole_robot_ik() 