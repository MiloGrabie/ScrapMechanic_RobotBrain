import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from numpy import array
from ikpy.chain import Chain
from ikpy.link import OriginLink, URDFLink
import time

class WholeRobotIK:
    """
    A class that creates a complete robot chain using ikpy and provides
    inverse kinematics and plotting for the entire robot.
    """
    
    def __init__(self, body):
        self.body = body
        self.robot_chain = None
        self.ax = None
        self.fig = None
        self.init_robot_chain()
        self.init_plot()
    
    def init_robot_chain(self):
        """
        Create a complete ikpy chain from all arms in the robot body.
        """
        links = []
        
        # Add base link (origin)
        links.append(
            URDFLink(
                name="base",
                origin_translation=array([0, 0, 0]),
                origin_orientation=array([0, 0, 0]),
                rotation=array([0, 0, 1]),  # Default z-axis rotation
            )
        )
        
        # Add all arms to the chain
        for arm_index, arm in enumerate(self.body.arms):
            # Add arm base link
            arm_base_position = arm.first_joint.localPosition
            links.append(
                URDFLink(
                    name=f"arm_{arm_index}_base",
                    origin_translation=arm_base_position,
                    origin_orientation=array([0, 0, 0]),
                    rotation=arm.first_joint.direction,
                )
            )
            
            # Add all joints in this arm
            for joint_index, joint in enumerate(arm.joints):
                if joint_index == len(arm.joints) - 1:  # Skip the last joint (end effector)
                    break
                    
                links.append(
                    URDFLink(
                        name=f"arm_{arm_index}_joint_{joint_index}",
                        origin_translation=joint.length,
                        origin_orientation=array([0, 0, 0]),
                        rotation=arm.joints[joint_index + 1].direction if joint_index + 1 < len(arm.joints) else array([0, 0, 0]),
                    )
                )
        
        # Create the complete robot chain
        self.robot_chain = Chain(name='complete_robot', links=links)
        
        # Set initial angles (all zeros)
        self.robot_chain.angles = np.zeros(len(links))
    
    def init_plot(self):
        """
        Initialize the matplotlib plot for visualization.
        """
        plt.ion()  # Turn on interactive mode
        self.fig = plt.figure(figsize=(12, 8))
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        self.ax.set_title('Complete Robot IK Visualization')
        
        # Set equal aspect ratio
        self.ax.set_box_aspect([1, 1, 1])
    
    def solve_ik_for_arm(self, arm_index, target_position):
        """
        Solve inverse kinematics for a specific arm.
        
        Args:
            arm_index: Index of the arm to control
            target_position: Target position for the arm's end effector
            
        Returns:
            angles: Joint angles for the entire robot chain
        """
        if self.robot_chain is None:
            raise ValueError("Robot chain not initialized")
        
        # Create a target matrix for the specific arm
        # We need to find the end effector position for this arm
        arm = self.body.arms[arm_index]
        
        # Set the target for the end effector of this arm
        target_matrix = np.eye(4)
        target_matrix[:3, 3] = target_position
        
        # Solve inverse kinematics
        angles = self.robot_chain.inverse_kinematics(target_matrix)
        
        return angles
    
    def solve_ik_for_multiple_arms(self, targets):
        """
        Solve inverse kinematics for multiple arms simultaneously.
        
        Args:
            targets: Dictionary mapping arm_index to target_position
            
        Returns:
            angles: Joint angles for the entire robot chain
        """
        if self.robot_chain is None:
            raise ValueError("Robot chain not initialized")
        
        # For multiple targets, we'll use a weighted approach
        # This is a simplified version - in practice you might want more sophisticated optimization
        
        # Start with current angles
        current_angles = self.robot_chain.angles.copy()
        
        # Solve for each target and average the results
        all_angles = []
        for arm_index, target_position in targets.items():
            if arm_index < len(self.body.arms):
                angles = self.solve_ik_for_arm(arm_index, target_position)
                all_angles.append(angles)
        
        if all_angles:
            # Average the angles (simple approach)
            avg_angles = np.mean(all_angles, axis=0)
            return avg_angles
        
        return current_angles
    
    def update_robot_angles(self, angles):
        """
        Update the robot chain with new joint angles.
        
        Args:
            angles: New joint angles for the robot chain
        """
        if self.robot_chain is None:
            raise ValueError("Robot chain not initialized")
        
        self.robot_chain.angles = angles
        
        # Update the actual robot joints
        self._update_robot_joints(angles)
    
    def _update_robot_joints(self, angles):
        """
        Update the actual robot joints with the calculated angles.
        This maps the chain angles back to individual arm joints.
        """
        angle_index = 1  # Skip the base link
        
        for arm_index, arm in enumerate(self.body.arms):
            # Skip the arm base link
            angle_index += 1
            
            # Update each joint in the arm
            for joint_index, joint in enumerate(arm.joints):
                if joint_index == len(arm.joints) - 1:  # Skip the last joint
                    break
                
                if angle_index < len(angles):
                    joint.targetAngle = angles[angle_index]
                    joint.move()
                    angle_index += 1
    
    def plot_robot(self, angles=None, target_positions=None):
        """
        Plot the complete robot using ikpy's Chain.plot method.
        
        Args:
            angles: Joint angles to plot (if None, uses current angles)
            target_positions: List of target positions to show as red dots
        """
        if self.robot_chain is None:
            raise ValueError("Robot chain not initialized")
        
        # Clear the plot
        self.ax.clear()
        
        # Set angles if provided
        if angles is not None:
            self.robot_chain.angles = angles
        
        # Use zeros or the current angles (if you have them)
        angles = np.zeros(len(self.robot_chain.links))
        self.robot_chain.plot(joints=angles, ax=self.ax, target=target_positions)
        
        # Add target positions if provided
        if target_positions is not None:
            for i, target in enumerate(target_positions):
                self.ax.scatter(target[0], target[1], target[2], 
                              color='red', s=100, marker='o', 
                              label=f'Target {i+1}')
        
        # Set labels and title
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        self.ax.set_title('Complete Robot IK Visualization')
        
        # Set equal aspect ratio
        self.ax.set_box_aspect([1, 1, 1])
        
        # Add legend if targets are shown
        if target_positions is not None:
            self.ax.legend()
        
        # Update the display
        plt.draw()
        plt.pause(0.001)
    
    def animate_robot(self, target_positions, duration=5.0, steps=100):
        """
        Animate the robot moving to target positions.
        
        Args:
            target_positions: List of target positions for each arm
            duration: Animation duration in seconds
            steps: Number of animation steps
        """
        if self.robot_chain is None:
            raise ValueError("Robot chain not initialized")
        
        # Convert targets to dictionary format
        targets = {i: pos for i, pos in enumerate(target_positions) if i < len(self.body.arms)}
        
        # Calculate angles for the target
        target_angles = self.solve_ik_for_multiple_arms(targets)
        
        # Get current angles
        current_angles = self.robot_chain.angles.copy()
        
        # Animate
        for step in range(steps + 1):
            # Interpolate between current and target angles
            t = step / steps
            interpolated_angles = current_angles + t * (target_angles - current_angles)
            
            # Update robot
            self.update_robot_angles(interpolated_angles)
            
            # Plot
            self.plot_robot(interpolated_angles, target_positions)
            
            # Sleep
            time.sleep(duration / steps)
    
    def get_forward_kinematics(self, angles=None):
        """
        Get forward kinematics for the complete robot.
        
        Args:
            angles: Joint angles (if None, uses current angles)
            
        Returns:
            positions: List of end effector positions for each arm
        """
        if self.robot_chain is None:
            raise ValueError("Robot chain not initialized")
        
        if angles is not None:
            self.robot_chain.angles = angles
        
        # Get forward kinematics for each arm
        positions = []
        for arm in self.body.arms:
            # Calculate the end effector position for this arm
            # This is a simplified calculation - you might need to adjust based on your robot structure
            end_position = arm.first_joint.position
            for joint in arm.joints:
                if joint.length is not None:
                    end_position += joint.length
            positions.append(end_position)
        
        return positions
    
    def get_robot_info(self):
        """
        Get information about the robot chain.
        
        Returns:
            info: Dictionary with robot information
        """
        if self.robot_chain is None:
            return {"error": "Robot chain not initialized"}
        
        info = {
            "total_links": len(self.robot_chain.links),
            "total_arms": len(self.body.arms),
            "current_angles": self.robot_chain.angles.tolist(),
            "arm_info": []
        }
        
        for i, arm in enumerate(self.body.arms):
            arm_info = {
                "arm_index": i,
                "joints": len(arm.joints),
                "first_joint_position": arm.first_joint.position.tolist(),
                "end_joint_position": arm.end_joint.position.tolist()
            }
            info["arm_info"].append(arm_info)
        
        return info
    
    def close_plot(self):
        """
        Close the matplotlib plot.
        """
        if self.fig is not None:
            plt.close(self.fig)
            self.fig = None
            self.ax = None 