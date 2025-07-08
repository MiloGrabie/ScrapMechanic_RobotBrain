import numpy as np
import tinyik
from math import pi

from numpy import array
from ikpy.chain import Chain
from ikpy.link import OriginLink, URDFLink

value = [3, 3, -5]


class InverseKinematics:
    actuator_list = []

    def __init__(self, arm):
        self.arm = arm
        # actuator_parameter = []
        # for index, joint in enumerate(arm.joints):
        #     if index == len(arm.joints)-1: break
        #     actuator_parameter.append(self.getAxisLetter(joint.direction))
        #     # if index == 0:
        #     #     actuator_parameter.append('z')
        #     # else:
        #     #     actuator_parameter.append('x')
        #     actuator_parameter.append(joint.length)
        #
        # # actuator_parameter.insert(0, [0,0,-1])
        # self.actuator = tinyik.Actuator(actuator_parameter)

        links = [
            URDFLink(
                name="origin",
                origin_translation=array([0, 0, 0]),
                origin_orientation=array([0, 0, 0]),
                rotation=arm.first_joint.direction,
            )
        ]
        for index, joint in enumerate(arm.joints):
            # if index == len(arm.joints) - 1:  # last one
            if index == len(arm.joints) - 1:  # last one
                # links.append(
                #     URDFLink(
                #         name=joint.index,
                #         origin_translation=array([0, 0, 0]),
                #         origin_orientation=array([0, 0, 0]),
                #         rotation=array([0, 0, 0]),
                #     )
                # )
                break

            links.append(
                URDFLink(
                    name=joint.index,
                    origin_translation=joint.length,
                    origin_orientation=array([0, 0, 0]),
                    rotation=arm.joints[index + 1].direction,
                )
            )

        self.actuator = Chain(name='left_arm', links=links)
        # self.actuator = Chain(name='left_arm', links=links, active_links_mask=[True, True, True, False])

    def getAngle(self, objective):
        # self.actuator.inverse_kinematics(objective)
        # tinyik.visualize(self.actuator)
        angles = self.actuator.inverse_kinematics(objective)

        # return self.actuator.angles
        # print("deg", self.actuator.angles)
        return angles

    def getAxisLetter(self, vect):
        if vect == [1, 0, 0]: return "x"
        if vect == [0, 1, 0]: return "y"
        if vect == [0, 0, 1]: return "z"

    def visualize(self):
        tinyik.visualize(self.actuator)


class WholeRobotInverseKinematics:
    """
    A class that creates a complete robot chain using ikpy for the entire robot body.
    This allows solving IK for the whole robot instead of individual arms.
    """
    
    def __init__(self, body):
        self.body = body
        self.robot_chain = None
        self.init_robot_chain()
    
    def init_robot_chain(self):
        """
        Create a complete ikpy chain from all arms in the robot body.
        """
        print("DEBUG: Starting robot chain initialization...")
        links = []
        
        # Add base link (origin)
        print("DEBUG: Adding base link...")
        links.append(
            OriginLink()
        )
        
        # Add all arms to the chain
        print(f"DEBUG: Processing {len(self.body.arms)} arms...")
        for arm_index, arm in enumerate(self.body.arms):
            print(f"DEBUG: Processing arm {arm_index} with {len(arm.joints)} joints")
            
            # Add arm base link
            arm_base_position = arm.first_joint.localPosition
            print(f"DEBUG: Arm {arm_index} base position: {arm_base_position}")
            print(f"DEBUG: Arm {arm_index} first joint direction: {arm.first_joint.direction}")
            
            # Convert direction to axis format for ikpy
            direction = arm.first_joint.direction
            if np.array_equal(direction, [1, 0, 0]):
                axis = array([1, 0, 0])
            elif np.array_equal(direction, [0, 1, 0]):
                axis = array([0, 1, 0])
            elif np.array_equal(direction, [0, 0, 1]):
                axis = array([0, 0, 1])
            else:
                axis = array([0, 0, 1])  # Default to z-axis
            
            links.append(
                URDFLink(
                    name=f"arm_{arm_index}_base",
                    origin_translation=arm_base_position,
                    origin_orientation=array([0, 0, 0]),
                    rotation=axis,
                )
            )
            
            # Add all joints in this arm
            for joint_index, joint in enumerate(arm.joints):
                if joint_index == len(arm.joints) - 1:  # Skip the last joint (end effector)
                    print(f"DEBUG: Skipping last joint {joint_index} for arm {arm_index}")
                    break
                
                print(f"DEBUG: Adding joint {joint_index} for arm {arm_index}")
                print(f"DEBUG: Joint length: {joint.length}")
                print(f"DEBUG: Joint direction: {joint.direction}")
                
                # Convert direction to axis format for ikpy
                direction = joint.direction
                if np.array_equal(direction, [1, 0, 0]):
                    axis = array([1, 0, 0])
                elif np.array_equal(direction, [0, 1, 0]):
                    axis = array([0, 1, 0])
                elif np.array_equal(direction, [0, 0, 1]):
                    axis = array([0, 0, 1])
                else:
                    axis = array([0, 0, 1])  # Default to z-axis
                
                links.append(
                    URDFLink(
                        name=f"arm_{arm_index}_joint_{joint_index}",
                        origin_translation=joint.length,
                        origin_orientation=array([0, 0, 0]),
                        rotation=axis,
                    )
                )
        
        print(f"DEBUG: Created {len(links)} links total")
        print("DEBUG: Creating Chain...")
        
        # Create the complete robot chain
        self.robot_chain = Chain(name='complete_robot', links=links)
        
        print("DEBUG: Chain created successfully")
        print(f"DEBUG: Chain has {len(self.robot_chain.links)} links")
        
        # Set initial angles (all zeros)
        try:
            self.robot_chain.angles = np.zeros(len(links))
            print("DEBUG: Initial angles set successfully")
        except Exception as e:
            print(f"DEBUG: Error setting initial angles: {e}")
            # Try alternative approach
            try:
                self.robot_chain.angles = [0] * len(links)
                print("DEBUG: Initial angles set with list approach")
            except Exception as e2:
                print(f"DEBUG: Error with list approach: {e2}")
    
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
        print("DEBUG: Starting plot_robot...")
        if self.robot_chain is None:
            raise ValueError("Robot chain not initialized")
        
        print("DEBUG: Robot chain is initialized")
        
        # Set angles if provided
        if angles is not None:
            print(f"DEBUG: Setting angles: {angles}")
            try:
                self.robot_chain.angles = angles
                print("DEBUG: Angles set successfully")
            except Exception as e:
                print(f"DEBUG: Error setting angles: {e}")
        else:
            print("DEBUG: No angles provided, using current angles")
        
        # Create matplotlib figure and axis if not provided
        print("DEBUG: Creating matplotlib figure...")
        import matplotlib.pyplot as plt
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111, projection='3d')
        print("DEBUG: Matplotlib figure created")
        
        # Plot the robot chain using Chain.plot with required parameters
        print("DEBUG: About to call Chain.plot...")
        print(f"DEBUG: Number of links: {len(self.robot_chain.links)}")
        print(f"DEBUG: Link types: {[type(link) for link in self.robot_chain.links]}")
        
        try:
            # Create a list of joint indices (excluding the base link)
            joint_indices = list(range(0, len(self.robot_chain.links)))
            print(f"DEBUG: Joint indices: {joint_indices}")
            
            self.robot_chain.plot(joints=joint_indices, ax=ax, target=target_positions)
            print("DEBUG: Chain.plot called successfully")
        except Exception as e:
            print(f"DEBUG: Error in Chain.plot: {e}")
            print(f"DEBUG: Error type: {type(e)}")
            import traceback
            traceback.print_exc()
            return
        
        # Set labels and title
        print("DEBUG: Setting plot labels...")
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title('Complete Robot IK Visualization')
        
        # Set equal aspect ratio
        ax.set_box_aspect([1, 1, 1])
        
        # Show the plot
        print("DEBUG: Showing plot...")
        plt.show()
        print("DEBUG: Plot shown")
    
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


def calc(length_first, length_second, length_third):
    arm = tinyik.Actuator(['z', length_first, 'x', length_second, 'x', length_third])
    # arm.angles = [pi, 1]
    # value[2] += 0.1
    arm.ee = value
    tinyik.visualize(arm)
    result = [arm.angles[0], arm.angles[1], arm.angles[2]]
    print("result", result)
    return result
    # leg = tinyik.Actuator([[.3, .0, .0], 'z', [.3, .0, .0], 'x', [.0, -.5, .0], 'x', [.0, -.5, .0]])
    # leg.angles = np.deg2rad([30, 45, -90])
    # tinyik.visualize(leg)


if __name__ == '__main__':
    pass
