import json
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from ikpy.chain import Chain
from ikpy.link import OriginLink, URDFLink

# Ensure 3D plotting works correctly
plt.rcParams['figure.figsize'] = [12, 8]

def parse_robot_json(json_data):
    """
    Parse the robot JSON data and extract joint information.
    
    The JSON structure shows 4 main joints (indices 260, 251, 252, 259)
    which represent the 4 legs, each with nested joints.
    """
    
    # If json_data is a string, parse it
    if isinstance(json_data, str):
        data = json.loads(json_data)
    else:
        data = json_data
    
    legs_data = []
    
    # Extract the 4 main leg joints
    for joint in data['joints']:
        leg_info = {
            'index': joint['index'],
            'angle': joint['angle'],
            'direction': joint['direction'],
            'position': joint.get('localPosition', {}),
            'joints': []
        }
        
        # Parse nested joints (shoulder2, knee, foot)
        for sub_joint in joint.get('joints', []):
            sub_info = {
                'index': sub_joint['index'],
                'angle': sub_joint['angle'],
                'direction': sub_joint['direction'],
                'position': sub_joint.get('localPosition', {})
            }
            
            # Get knee joint
            if 'joints' in sub_joint:
                for knee_joint in sub_joint['joints']:
                    knee_info = {
                        'index': knee_joint['index'],
                        'angle': knee_joint['angle'],
                        'direction': knee_joint['direction'],
                        'position': knee_joint.get('localPosition', {})
                    }
                    
                    # Get foot joint
                    if 'joints' in knee_joint:
                        for foot_joint in knee_joint['joints']:
                            foot_info = {
                                'index': foot_joint['index'],
                                'angle': foot_joint['angle'],
                                'position': foot_joint.get('localPosition', {})
                            }
                            knee_info['foot'] = foot_info
                    
                    sub_info['knee'] = knee_info
            
            leg_info['joints'].append(sub_info)
        
        legs_data.append(leg_info)
    
    return legs_data

def create_leg_from_json(leg_data, leg_name, robot_center):
    """
    Create an ikpy chain from parsed JSON leg data using position.
    
    This function maps the JSON structure to ikpy links.
    Chain starts at the shoulder joint.
    """
    
    # Build the chain starting at the shoulder
    links = [
        # Base link (shoulder position)
        OriginLink(),
        
        # First shoulder joint (from main joint data)
        URDFLink(
            name=f"{leg_name}_shoulder1",
            origin_translation=np.array([0, 0, 0]),
            origin_orientation=np.array([0, 0, 0]),
            rotation=np.array([
                leg_data['direction']['x'],
                leg_data['direction']['y'],
                leg_data['direction']['z']
            ]),
            bounds=(-np.pi/2, np.pi/2)
        ),
    ]
    
    # Add subsequent joints
    if leg_data['joints']:
        shoulder2_data = leg_data['joints'][0]
        
        # Get position for second shoulder joint (relative to first shoulder)
        shoulder2_pos = shoulder2_data.get('position', {})
        shoulder2_global = np.array([
            shoulder2_pos.get('x', 0),
            shoulder2_pos.get('y', 0),
            shoulder2_pos.get('z', 0)
        ])
        
        # Get first shoulder position for reference
        shoulder1_pos = leg_data.get('position', {})
        shoulder1_global = np.array([
            shoulder1_pos.get('x', 0),
            shoulder1_pos.get('y', 0),
            shoulder1_pos.get('z', 0)
        ])
        
        # Calculate offset from first shoulder to second shoulder
        shoulder2_offset = shoulder2_global - shoulder1_global
        
        # Translation to second shoulder
        links.append(URDFLink(
            name=f"{leg_name}_to_shoulder2",
            origin_translation=shoulder2_offset,
            origin_orientation=np.array([0, 0, 0]),
            rotation=np.array([0, 0, 0]),
        ))
        
        # Second shoulder joint
        links.append(URDFLink(
            name=f"{leg_name}_shoulder2",
            origin_translation=np.array([0, 0, 0]),
            origin_orientation=np.array([0, 0, 0]),
            rotation=np.array([
                shoulder2_data['direction']['x'],
                shoulder2_data['direction']['y'],
                shoulder2_data['direction']['z']
            ]),
            bounds=(-np.pi/2, np.pi/2)
        ))
        
        # Knee joint
        if 'knee' in shoulder2_data:
            knee_data = shoulder2_data['knee']
            
            # Get position for knee
            knee_pos = knee_data.get('position', {})
            knee_global = np.array([
                knee_pos.get('x', 0),
                knee_pos.get('y', 0),
                knee_pos.get('z', 0)
            ])
            knee_offset = knee_global - shoulder2_global
            
            # Translation to knee
            links.append(URDFLink(
                name=f"{leg_name}_to_knee",
                origin_translation=knee_offset,
                origin_orientation=np.array([0, 0, 0]),
                rotation=np.array([0, 0, 0]),
            ))
            
            # Knee joint
            links.append(URDFLink(
                name=f"{leg_name}_knee",
                origin_translation=np.array([0, 0, 0]),
                origin_orientation=np.array([0, 0, 0]),
                rotation=np.array([
                    knee_data['direction']['x'],
                    knee_data['direction']['y'],
                    knee_data['direction']['z']
                ]),
                bounds=(-np.pi/2, np.pi)  # Allow negative knee angles
            ))
            
            # Foot (fixed joint)
            if 'foot' in knee_data:
                foot_data = knee_data['foot']
                
                # Get position for foot
                foot_pos = foot_data.get('position', {})
                foot_global = np.array([
                    foot_pos.get('x', 0),
                    foot_pos.get('y', 0),
                    foot_pos.get('z', 0)
                ])
                foot_offset = foot_global - knee_global
                
                # Translation to foot
                links.append(URDFLink(
                    name=f"{leg_name}_to_foot",
                    origin_translation=foot_offset,
                    origin_orientation=np.array([0, 0, 0]),
                    rotation=np.array([0, 0, 0]),
                ))
                
                # Foot end effector
                links.append(URDFLink(
                    name=f"{leg_name}_foot",
                    origin_translation=np.array([0, 0, 0]),
                    origin_orientation=np.array([0, 0, 0]),
                    rotation=np.array([0, 0, 0]),  # Fixed joint
                ))
    
    return Chain(name=f"{leg_name}_chain", links=links)

class RobotDogFromJSON:
    def __init__(self, json_data):
        # Ensure json_data is a dictionary, not a string
        if isinstance(json_data, str):
            self.json_data = json.loads(json_data)
        else:
            self.json_data = json_data
        self.legs_data = parse_robot_json(self.json_data)
        
        # Map joint indices to leg names based on typical quadruped layout
        # You might need to adjust this mapping based on your specific robot
        self.index_to_leg = {
            260: 'front_right',
            251: 'rear_right',
            252: 'rear_left',
            259: 'front_left'
        }
        
        # Calculate robot center from shoulder positions
        self.robot_center = self.calculate_robot_center_from_shoulders()
        
        # Create chains for each leg
        self.legs = {}
        self.current_angles = {}
        for leg_data in self.legs_data:
            leg_index = leg_data['index']
            if leg_index in self.index_to_leg:
                leg_name = self.index_to_leg[leg_index]
                self.legs[leg_name] = create_leg_from_json(leg_data, leg_name, self.robot_center)
                
                # Store current angles from JSON
                self.current_angles[leg_name] = self.extract_angles_from_json(leg_data)
    
    def calculate_robot_center_from_shoulders(self):
        """
        Calculate the robot center as the center of the square formed by the four shoulder joints.
        This uses the relative positions from the JSON data.
        """
        shoulder_positions = []
        shoulder_info = []
        
        # Collect all shoulder positions
        for leg_data in self.legs_data:
            leg_index = leg_data['index']
            if leg_index in self.index_to_leg:
                leg_name = self.index_to_leg[leg_index]
                shoulder_pos = leg_data.get('position', {})
                pos = np.array([
                    shoulder_pos.get('x', 0),
                    shoulder_pos.get('y', 0),
                    shoulder_pos.get('z', 0)
                ])
                shoulder_positions.append(pos)
                shoulder_info.append((leg_name, pos))
        
        if len(shoulder_positions) == 0:
            # Fallback to origin if no shoulders found
            return np.array([0.0, 0.0, 0.0])
        
        # Calculate the center as the mean of all shoulder positions
        shoulder_positions = np.array(shoulder_positions)
        robot_center = np.mean(shoulder_positions, axis=0)
        
        # Print debug information
        print(f"\nShoulder positions used for robot center calculation:")
        for leg_name, pos in shoulder_info:
            print(f"  {leg_name}: [{pos[0]:.3f}, {pos[1]:.3f}, {pos[2]:.3f}]")
        print(f"Calculated robot center: [{robot_center[0]:.3f}, {robot_center[1]:.3f}, {robot_center[2]:.3f}]")
        
        return robot_center
    
    def extract_angles_from_json(self, leg_data):
        """Extract current joint angles from JSON data."""
        angles = {
            'shoulder1': leg_data['angle'],
            'shoulder2': 0,
            'knee': 0
        }
        
        if leg_data['joints']:
            angles['shoulder2'] = leg_data['joints'][0]['angle']
            if 'knee' in leg_data['joints'][0]:
                angles['knee'] = leg_data['joints'][0]['knee']['angle']
        
        return angles
    
    def get_current_foot_positions(self):
        """Get current foot positions from JSON data (global positions)."""
        foot_positions = {}
        
        for leg_data in self.legs_data:
            leg_index = leg_data['index']
            if leg_index in self.index_to_leg:
                leg_name = self.index_to_leg[leg_index]
                
                # Navigate to foot position in JSON structure
                if leg_data['joints'] and 'knee' in leg_data['joints'][0]:
                    knee_data = leg_data['joints'][0]['knee']
                    if 'foot' in knee_data:
                        foot_pos = knee_data['foot'].get('position', {})
                        foot_positions[leg_name] = [
                            foot_pos.get('x', 0),
                            foot_pos.get('y', 0),
                            foot_pos.get('z', 0)
                        ]
        
        return foot_positions
    
    def compute_forward_kinematics(self, leg_name):
        """Compute joint positions using forward kinematics with current angles."""
        if leg_name not in self.legs:
            return None
        
        chain = self.legs[leg_name]
        angles = self.current_angles[leg_name]
        
        # Build full angle array for ikpy (includes fixed joints)
        # The order depends on how we built the chain (now starting at shoulder)
        full_angles = [0]  # Origin link (shoulder)
        full_angles.append(angles['shoulder1'])  # Shoulder1 joint
        full_angles.append(0)  # Translation to shoulder2
        full_angles.append(angles['shoulder2'])  # Shoulder2 joint
        full_angles.append(0)  # Translation to knee
        full_angles.append(angles['knee'])  # Knee joint
        full_angles.append(0)  # Translation to foot
        full_angles.append(0)  # Foot (fixed)
        
        # Get shoulder position for offset
        leg_data = None
        for ld in self.legs_data:
            if self.index_to_leg.get(ld['index']) == leg_name:
                leg_data = ld
                break
        
        if not leg_data:
            return None
            
        shoulder_pos = leg_data.get('position', {})
        shoulder_global = np.array([
            shoulder_pos.get('x', 0),
            shoulder_pos.get('y', 0),
            shoulder_pos.get('z', 0)
        ])
        
        # Compute forward kinematics for each link
        positions = []
        for i in range(len(chain.links)):
            transform = chain.forward_kinematics(full_angles)
            pos = transform[:3, 3] + shoulder_global
            positions.append(pos)
        
        return positions
    
    def plot_robot(self, ax=None):
        """Plot the robot in 3D using current positions from JSON data."""
        if ax is None:
            fig = plt.figure(figsize=(12, 10))
            ax = fig.add_subplot(111, projection='3d')
        
        # Define colors for each leg
        leg_colors = {
            'front_left': 'red',
            'front_right': 'blue',
            'rear_left': 'green',
            'rear_right': 'purple'
        }
        
        # Plot robot body as square between shoulders
        shoulder_positions = []
        shoulder_names = []
        
        # Collect shoulder positions in order
        for leg_data in self.legs_data:
            leg_index = leg_data['index']
            if leg_index in self.index_to_leg:
                leg_name = self.index_to_leg[leg_index]
                shoulder_pos = leg_data.get('position', {})
                shoulder_positions.append(np.array([
                    shoulder_pos.get('x', 0),
                    shoulder_pos.get('y', 0),
                    shoulder_pos.get('z', 0)
                ]))
                shoulder_names.append(leg_name)
        
        # Draw the square/quadrilateral between shoulders
        if len(shoulder_positions) >= 4:
            # Create a closed polygon by connecting shoulders in order
            # Assuming the order is: front_right, rear_right, rear_left, front_left
            shoulder_order = ['front_right', 'rear_right', 'rear_left', 'front_left']
            ordered_positions = []
            
            for name in shoulder_order:
                if name in shoulder_names:
                    idx = shoulder_names.index(name)
                    ordered_positions.append(shoulder_positions[idx])
            
            # Close the polygon by adding the first point at the end
            if len(ordered_positions) >= 4:
                ordered_positions.append(ordered_positions[0])
                ordered_positions = np.array(ordered_positions)
                
                # Plot the shoulder square
                ax.plot(ordered_positions[:, 0], ordered_positions[:, 1], ordered_positions[:, 2], 
                       'k-', linewidth=3, label='Shoulder Square')
                
                # Plot shoulder points
                ax.scatter(ordered_positions[:-1, 0], ordered_positions[:-1, 1], ordered_positions[:-1, 2], 
                          color='black', marker='o', zorder=5)
        
        # Plot robot center point
        ax.scatter(self.robot_center[0], self.robot_center[1], self.robot_center[2], 
                  color='red', marker='x', s=200, label='Robot Center', zorder=6)
        
        # Plot each leg using actual positions from JSON
        for leg_data in self.legs_data:
            leg_index = leg_data['index']
            if leg_index in self.index_to_leg:
                leg_name = self.index_to_leg[leg_index]
                color = leg_colors.get(leg_name, 'black')
                
                # Collect joint positions from JSON data
                joint_positions = []
                
                # Shoulder position
                shoulder_pos = leg_data.get('position', {})
                shoulder_global = np.array([
                    shoulder_pos.get('x', 0),
                    shoulder_pos.get('y', 0),
                    shoulder_pos.get('z', 0)
                ])
                joint_positions.append(shoulder_global)
                
                # Subsequent joints
                if leg_data['joints']:
                    shoulder2_data = leg_data['joints'][0]
                    shoulder2_pos = shoulder2_data.get('position', {})
                    shoulder2_global = np.array([
                        shoulder2_pos.get('x', 0),
                        shoulder2_pos.get('y', 0),
                        shoulder2_pos.get('z', 0)
                    ])
                    joint_positions.append(shoulder2_global)
                    
                    # Knee joint
                    if 'knee' in shoulder2_data:
                        knee_data = shoulder2_data['knee']
                        knee_pos = knee_data.get('position', {})
                        knee_global = np.array([
                            knee_pos.get('x', 0),
                            knee_pos.get('y', 0),
                            knee_pos.get('z', 0)
                        ])
                        joint_positions.append(knee_global)
                        
                        # Foot position
                        if 'foot' in knee_data:
                            foot_data = knee_data['foot']
                            foot_pos = foot_data.get('position', {})
                            foot_global = np.array([
                                foot_pos.get('x', 0),
                                foot_pos.get('y', 0),
                                foot_pos.get('z', 0)
                            ])
                            joint_positions.append(foot_global)
                
                joint_positions = np.array(joint_positions)
                
                # Plot leg segments
                if len(joint_positions) > 1:
                    ax.plot(joint_positions[:, 0], joint_positions[:, 1], joint_positions[:, 2], 
                           color=color, linewidth=2, marker='o', markersize=6,
                           label=leg_name)
                    
                    # Highlight foot position
                    if len(joint_positions) > 0:
                        ax.scatter(joint_positions[-1, 0], joint_positions[-1, 1], joint_positions[-1, 2], 
                                 color=color, marker='s', edgecolors='black', zorder=5)
        
        # Plot ground plane (simplified as a grid)
        ground_size = 1.0
        x_ground = np.linspace(self.robot_center[0] - ground_size, self.robot_center[0] + ground_size, 10)
        y_ground = np.linspace(self.robot_center[1] - ground_size, self.robot_center[1] + ground_size, 10)
        z_ground = self.robot_center[2] - 0.5
        
        # Plot ground grid lines
        for x in x_ground:
            ax.plot([x, x], [y_ground[0], y_ground[-1]], [z_ground, z_ground], 'gray', alpha=0.3, linewidth=0.5)
        for y in y_ground:
            ax.plot([x_ground[0], x_ground[-1]], [y, y], [z_ground, z_ground], 'gray', alpha=0.3, linewidth=0.5)
        
        # Set labels and title
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title('Robot Dog Configuration (Using Position Data)')
        ax.legend(loc='upper right')
        
        # Set equal aspect ratio
        # max_range = 0.8
        # ax.set_xlim(self.robot_center[0] - max_range, self.robot_center[0] + max_range)
        # ax.set_ylim(self.robot_center[1] - max_range, self.robot_center[1] + max_range)
        # ax.set_zlim(self.robot_center[2] - 0.6, self.robot_center[2] + 0.4)
        
        return ax
    
    def plot_leg_details(self, leg_name):
        """Plot detailed view of a specific leg."""
        fig = plt.figure(figsize=(15, 5))
        
        # Find leg data
        leg_data = None
        for ld in self.legs_data:
            if self.index_to_leg.get(ld['index']) == leg_name:
                leg_data = ld
                break
        
        if not leg_data:
            print(f"Leg {leg_name} not found")
            return
        
        # Plot 1: Joint angles
        ax1 = fig.add_subplot(131)
        angles = self.extract_angles_from_json(leg_data)
        joint_names = list(angles.keys())
        joint_angles_deg = [np.rad2deg(angles[j]) for j in joint_names]
        
        bars = ax1.bar(joint_names, joint_angles_deg)
        ax1.set_ylabel('Angle (degrees)')
        ax1.set_title(f'{leg_name} Joint Angles')
        ax1.grid(True, alpha=0.3)
        
        # Add value labels on bars
        for bar, angle in zip(bars, joint_angles_deg):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{angle:.1f}°', ha='center', va='bottom' if height >= 0 else 'top')
        
        # Get positions using forward kinematics
        positions = self.compute_forward_kinematics(leg_name)
        
        if positions:
            # Filter joint positions
            joint_positions = []
            for i, link in enumerate(self.legs[leg_name].links):
                if 'shoulder' in link.name or 'knee' in link.name or 'foot' in link.name:
                    joint_positions.append(positions[i])
            
            joint_positions = np.array(joint_positions)
            
            # Plot 2: 2D side view (X-Z plane)
            ax2 = fig.add_subplot(132)
            if len(joint_positions) > 0:
                ax2.plot(joint_positions[:, 0], joint_positions[:, 2], 'bo-', linewidth=2, markersize=8)
                ax2.scatter(joint_positions[-1, 0], joint_positions[-1, 2], color='red', s=100, 
                           marker='s', label='Foot')
            
            ax2.set_xlabel('X')
            ax2.set_ylabel('Z')
            ax2.set_title(f'{leg_name} Side View')
            ax2.grid(True, alpha=0.3)
            ax2.legend()
            ax2.axis('equal')
            
            # Plot 3: 2D top view (X-Y plane)
            ax3 = fig.add_subplot(133)
            if len(joint_positions) > 0:
                ax3.plot(joint_positions[:, 0], joint_positions[:, 1], 'go-', linewidth=2, markersize=8)
                ax3.scatter(joint_positions[-1, 0], joint_positions[-1, 1], color='red', s=100, 
                           marker='s', label='Foot')
            
            ax3.set_xlabel('X')
            ax3.set_ylabel('Y')
            ax3.set_title(f'{leg_name} Top View')
            ax3.grid(True, alpha=0.3)
            ax3.legend()
            ax3.axis('equal')
        
        plt.tight_layout()
        return fig
    
    def get_leg_ik_angles(self, leg_name, offset):
        """
        For a given leg, compute the joint angles needed to keep the foot in the same place
        when the robot center is moved to offset.
        """
        if leg_name not in self.legs:
            return None
        chain = self.legs[leg_name]
        
        # Get the original foot position (global)
        foot_positions = self.get_current_foot_positions()
        foot_pos = np.array(foot_positions[leg_name])
        
        # Get the shoulder position (global)
        leg_data = None
        for ld in self.legs_data:
            if self.index_to_leg.get(ld['index']) == leg_name:
                leg_data = ld
                break
        
        if not leg_data:
            return None
            
        shoulder_pos = leg_data.get('position', {})
        shoulder_global = np.array([
            shoulder_pos.get('x', 0),
            shoulder_pos.get('y', 0),
            shoulder_pos.get('z', 0)
        ])
        
        # The target for IK is the foot position relative to the shoulder
        # Since the shoulder moves with the robot center, we need to account for the offset
        new_shoulder_pos = shoulder_global + offset
        target = foot_pos - new_shoulder_pos
        
        # Debug: Print target information
        print(f"\n{leg_name} IK Debug:")
        print(f"  Original shoulder: {shoulder_global}")
        print(f"  New shoulder: {new_shoulder_pos}")
        print(f"  Foot position: {foot_pos}")
        print(f"  Original foot relative to shoulder: {foot_pos - shoulder_global}")
        print(f"  Target (relative to new shoulder): {target}")
        print(f"  Target distance: {np.linalg.norm(target):.3f}")
        
        # Calculate leg segment lengths for reachability check
        if leg_data['joints']:
            shoulder2_data = leg_data['joints'][0]
            shoulder2_pos = shoulder2_data.get('position', {})
            shoulder2_global = np.array([
                shoulder2_pos.get('x', 0),
                shoulder2_pos.get('y', 0),
                shoulder2_pos.get('z', 0)
            ])
            
            if 'knee' in shoulder2_data:
                knee_data = shoulder2_data['knee']
                knee_pos = knee_data.get('position', {})
                knee_global = np.array([
                    knee_pos.get('x', 0),
                    knee_pos.get('y', 0),
                    knee_pos.get('z', 0)
                ])
                
                if 'foot' in knee_data:
                    foot_data = knee_data['foot']
                    foot_pos_actual = foot_data.get('position', {})
                    foot_global = np.array([
                        foot_pos_actual.get('x', 0),
                        foot_pos_actual.get('y', 0),
                        foot_pos_actual.get('z', 0)
                    ])
                    
                    # Calculate segment lengths
                    upper_leg_length = np.linalg.norm(shoulder2_global - shoulder_global)
                    lower_leg_length = np.linalg.norm(knee_global - shoulder2_global)
                    foot_length = np.linalg.norm(foot_global - knee_global)
                    total_leg_length = upper_leg_length + lower_leg_length + foot_length
                    
                    print(f"  Leg segment lengths:")
                    print(f"    Upper leg: {upper_leg_length:.3f}")
                    print(f"    Lower leg: {lower_leg_length:.3f}")
                    print(f"    Foot: {foot_length:.3f}")
                    print(f"    Total leg length: {total_leg_length:.3f}")
                    print(f"    Max reach: {total_leg_length:.3f}")
                    print(f"    Target reachable: {np.linalg.norm(target) <= total_leg_length}")
        
        # Get current angles as initial guess for IK
        current_angles = self.current_angles[leg_name]
        
        # Build full angle array for ikpy (includes fixed joints)
        # The order depends on how we built the chain (now starting at shoulder)
        initial_angles = [0]  # Origin link (shoulder)
        initial_angles.append(current_angles['shoulder1'])  # Shoulder1 joint
        initial_angles.append(0)  # Translation to shoulder2
        initial_angles.append(current_angles['shoulder2'])  # Shoulder2 joint
        initial_angles.append(0)  # Translation to knee
        initial_angles.append(current_angles['knee'])  # Knee joint
        initial_angles.append(0)  # Translation to foot
        initial_angles.append(0)  # Foot (fixed)
        
        # Use ikpy to solve for the new angles
        try:
            ik_angles = chain.inverse_kinematics(target, initial_position=initial_angles)
            return ik_angles
        except Exception as e:
            print(f"IK failed for {leg_name}: {e}")
            print(f"Target: {target}")
            print(f"Initial angles: {initial_angles}")
            return initial_angles  # Return current angles if IK fails

    def plot_robot_with_body_offset_ik(self, offset, ax=None):
        """
        Plot the robot with the body moved by offset, using IK to keep the feet fixed.
        """
        if ax is None:
            fig = plt.figure(figsize=(12, 10))
            ax = fig.add_subplot(111, projection='3d')
        leg_colors = {
            'front_left': 'red',
            'front_right': 'blue',
            'rear_left': 'green',
            'rear_right': 'purple'
        }
        new_center = self.robot_center + offset
        # Plot robot body as square between shoulders (moved)
        shoulder_positions = []
        shoulder_names = []
        for leg_data in self.legs_data:
            leg_index = leg_data['index']
            if leg_index in self.index_to_leg:
                leg_name = self.index_to_leg[leg_index]
                shoulder_pos = leg_data.get('position', {})
                shoulder_positions.append(np.array([
                    shoulder_pos.get('x', 0),
                    shoulder_pos.get('y', 0),
                    shoulder_pos.get('z', 0)
                ]) + offset)
                shoulder_names.append(leg_name)
        if len(shoulder_positions) >= 4:
            shoulder_order = ['front_right', 'rear_right', 'rear_left', 'front_left']
            ordered_positions = []
            for name in shoulder_order:
                if name in shoulder_names:
                    idx = shoulder_names.index(name)
                    ordered_positions.append(shoulder_positions[idx])
            if len(ordered_positions) >= 4:
                ordered_positions.append(ordered_positions[0])
                ordered_positions = np.array(ordered_positions)
                ax.plot(ordered_positions[:, 0], ordered_positions[:, 1], ordered_positions[:, 2], 
                        'k--', linewidth=3, label='Shoulder Square (Moved)')
                ax.scatter(ordered_positions[:-1, 0], ordered_positions[:-1, 1], ordered_positions[:-1, 2], 
                           color='black', marker='o', zorder=5)
        # Plot new robot center
        ax.scatter(new_center[0], new_center[1], new_center[2], 
                   color='orange', marker='x', label='Robot Center (Moved)', zorder=6)
        
        # Plot each leg (shoulders moved, feet fixed, joints from IK)
        for leg_name in self.legs:
            color = leg_colors.get(leg_name, 'black')
            ik_angles = self.get_leg_ik_angles(leg_name, offset)
            
            if ik_angles is not None:
                # Round angles very close to 0 to exactly 0 for numerical stability
                ik_angles = np.array([0.0 if abs(a) < 1e-8 else a for a in ik_angles])
                chain = self.legs[leg_name]
                
                # Get shoulder position for offset
                leg_data = None
                for ld in self.legs_data:
                    if self.index_to_leg.get(ld['index']) == leg_name:
                        leg_data = ld
                        break
                
                if leg_data:
                    shoulder_pos = leg_data.get('position', {})
                    shoulder_global = np.array([
                        shoulder_pos.get('x', 0),
                        shoulder_pos.get('y', 0),
                        shoulder_pos.get('z', 0)
                    ])
                    new_shoulder_pos = shoulder_global + offset
                    
                    # Compute forward kinematics for each link
                    positions = []
                    for i in range(4):
                        transform = chain.forward_kinematics(ik_angles)
                        pos = transform[:3, i] + new_shoulder_pos
                        positions.append(pos)
                    joint_positions = np.array(positions)
                    # joint_positions = chain.forward_kinematics(ik_angles)
                    # Plot leg segments
                    ax.plot(joint_positions[:, 0], joint_positions[:, 1], joint_positions[:, 2],
                            color=color, linewidth=2, marker='o', markersize=6,
                            label=leg_name + ' (IK)')
                    # Highlight foot position
                    ax.scatter(joint_positions[-1, 0], joint_positions[-1, 1], joint_positions[-1, 2], 
                               color=color, marker='s', edgecolors='black', zorder=5)
            else:
                print(f"Warning: No IK solution found for {leg_name}")
        # Plot ground plane (same as before)
        ground_size = 1.0
        x_ground = np.linspace(new_center[0] - ground_size, new_center[0] + ground_size, 10)
        y_ground = np.linspace(new_center[1] - ground_size, new_center[1] + ground_size, 10)
        z_ground = new_center[2] - 0.5
        for x in x_ground:
            ax.plot([x, x], [y_ground[0], y_ground[-1]], [z_ground, z_ground], 'gray', alpha=0.3, linewidth=0.5)
        for y in y_ground:
            ax.plot([x_ground[0], x_ground[-1]], [y, y], [z_ground, z_ground], 'gray', alpha=0.3, linewidth=0.5)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title('Robot Dog (Body Moved Forward, IK)')
        ax.legend(loc='upper right')
        return ax
    
    def update_json_with_ik_angles(self, offset):
        """
        Update the JSON data with new angles calculated from inverse kinematics
        when the robot body is moved by the given offset.
        
        Args:
            offset: The offset to move the robot body
            
        Returns:
            updated_json: The updated JSON data with new angles
        """
        # Create a deep copy of the original JSON data
        import copy
        updated_json = copy.deepcopy(self.json_data)
        
        # Update angles for each leg
        for leg_data in updated_json['joints']:
            leg_index = leg_data['index']
            if leg_index in self.index_to_leg:
                leg_name = self.index_to_leg[leg_index]
                
                # Get IK angles for this leg
                ik_angles = self.get_leg_ik_angles(leg_name, offset)
                
                if ik_angles is not None:
                    # Update the main joint angle (shoulder1)
                    leg_data['angle'] = ik_angles[1]  # shoulder1 angle
                    
                    # Update nested joints
                    if leg_data['joints']:
                        # Update shoulder2 angle
                        leg_data['joints'][0]['angle'] = ik_angles[3]  # shoulder2 angle
                        
                        # Update knee angle
                        if 'knee' in leg_data['joints'][0]:
                            leg_data['joints'][0]['knee']['angle'] = ik_angles[5]  # knee angle
                            
                            # Update foot angle (if it exists)
                            if 'foot' in leg_data['joints'][0]['knee']:
                                leg_data['joints'][0]['knee']['foot']['angle'] = ik_angles[7]  # foot angle
        
        return updated_json
    
    def save_updated_json(self, updated_json, filename='Scripts/JSON/interface_out_updated.json'):
        """
        Save the updated JSON data to a file.
        
        Args:
            updated_json: The updated JSON data
            filename: The filename to save to
        """
        with open(filename, 'w') as f:
            json.dump(updated_json, f, indent=2)
        print(f"Updated JSON saved to {filename}")
    
    def create_robot_from_updated_json(self, updated_json):
        """
        Create a new RobotDogFromJSON instance from updated JSON data.
        
        Args:
            updated_json: The updated JSON data
            
        Returns:
            robot: New RobotDogFromJSON instance
        """
        return RobotDogFromJSON(updated_json)
    
    def plot_robot_classic_verification(self, original_robot, updated_robot, offset, ax=None):
        """
        Create a classic plot to verify that the robot URDF was properly updated
        with the new angles from inverse kinematics.
        
        Args:
            original_robot: The original RobotDogFromJSON instance
            updated_robot: The updated RobotDogFromJSON instance
            offset: The offset that was applied
            ax: Matplotlib axis (optional)
        """
        if ax is None:
            fig = plt.figure(figsize=(15, 10))
            ax = fig.add_subplot(111, projection='3d')
        
        # Define colors for comparison
        original_color = 'blue'
        updated_color = 'red'
        offset_color = 'orange'
        
        # Plot original robot (blue)
        print("Plotting original robot configuration...")
        original_robot.plot_robot(ax=ax)
        
        # Change colors for updated robot
        leg_colors = {
            'front_left': updated_color,
            'front_right': updated_color,
            'rear_left': updated_color,
            'rear_right': updated_color
        }
        
        # Plot updated robot (red) - overlay on same plot
        print("Plotting updated robot configuration...")
        for leg_data in updated_robot.legs_data:
            leg_index = leg_data['index']
            if leg_index in updated_robot.index_to_leg:
                leg_name = updated_robot.index_to_leg[leg_index]
                color = leg_colors.get(leg_name, 'black')
                
                # Collect joint positions from updated JSON data
                joint_positions = []
                
                # Shoulder position (moved by offset)
                shoulder_pos = leg_data.get('position', {})
                shoulder_global = np.array([
                    shoulder_pos.get('x', 0),
                    shoulder_pos.get('y', 0),
                    shoulder_pos.get('z', 0)
                ]) + offset  # Apply offset to show moved position
                joint_positions.append(shoulder_global)
                
                # Subsequent joints
                if leg_data['joints']:
                    shoulder2_data = leg_data['joints'][0]
                    shoulder2_pos = shoulder2_data.get('position', {})
                    shoulder2_global = np.array([
                        shoulder2_pos.get('x', 0),
                        shoulder2_pos.get('y', 0),
                        shoulder2_pos.get('z', 0)
                    ]) + offset  # Apply offset
                    joint_positions.append(shoulder2_global)
                    
                    # Knee joint
                    if 'knee' in shoulder2_data:
                        knee_data = shoulder2_data['knee']
                        knee_pos = knee_data.get('position', {})
                        knee_global = np.array([
                            knee_pos.get('x', 0),
                            knee_pos.get('y', 0),
                            knee_pos.get('z', 0)
                        ]) + offset  # Apply offset
                        joint_positions.append(knee_global)
                        
                        # Foot position
                        if 'foot' in knee_data:
                            foot_data = knee_data['foot']
                            foot_pos = foot_data.get('position', {})
                            foot_global = np.array([
                                foot_pos.get('x', 0),
                                foot_pos.get('y', 0),
                                foot_pos.get('z', 0)
                            ]) + offset  # Apply offset
                            joint_positions.append(foot_global)
                
                joint_positions = np.array(joint_positions)
                
                # Plot updated leg segments with different style
                if len(joint_positions) > 1:
                    ax.plot(joint_positions[:, 0], joint_positions[:, 1], joint_positions[:, 2], 
                           color=color, linewidth=3, marker='s', markersize=8,
                           linestyle='--', label=f'{leg_name} (Updated)')
                    
                    # Highlight updated foot position
                    if len(joint_positions) > 0:
                        ax.scatter(joint_positions[-1, 0], joint_positions[-1, 1], joint_positions[-1, 2], 
                                 color=color, marker='*', s=200, edgecolors='black', zorder=5)
        
        # Plot offset vector
        ax.quiver(original_robot.robot_center[0], original_robot.robot_center[1], original_robot.robot_center[2],
                 offset[0], offset[1], offset[2], color=offset_color, arrow_length_ratio=0.1,
                 linewidth=3, label=f'Offset: {offset}')
        
        # Set labels and title
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title('Robot URDF Update Verification\nBlue: Original, Red: Updated with IK, Orange: Offset Vector')
        ax.legend(loc='upper right')
        
        return ax
    
    def compare_angles_before_after(self, original_robot, updated_robot):
        """
        Compare joint angles before and after IK update.
        
        Args:
            original_robot: The original RobotDogFromJSON instance
            updated_robot: The updated RobotDogFromJSON instance
        """
        print("\n" + "="*60)
        print("JOINT ANGLE COMPARISON: BEFORE vs AFTER IK UPDATE")
        print("="*60)
        
        for leg_name in original_robot.legs:
            print(f"\n{leg_name.upper()} LEG:")
            print("-" * 30)
            
            original_angles = original_robot.current_angles[leg_name]
            updated_angles = updated_robot.current_angles[leg_name]
            
            joints = ['shoulder1', 'shoulder2', 'knee']
            
            for joint in joints:
                orig_deg = np.rad2deg(original_angles[joint])
                upd_deg = np.rad2deg(updated_angles[joint])
                diff_deg = upd_deg - orig_deg
                
                print(f"  {joint:10s}: {orig_deg:8.2f}° → {upd_deg:8.2f}° (Δ: {diff_deg:+6.2f}°)")
        
        print("\n" + "="*60)
    
    def print_positions(self):
        """Print all positions from the JSON for debugging."""
        print("\nPositions from JSON:")
        for leg_data in self.legs_data:
            leg_index = leg_data['index']
            if leg_index in self.index_to_leg:
                leg_name = self.index_to_leg[leg_index]
                print(f"\n{leg_name} (index {leg_index}):")
                
                # Shoulder position
                pos = leg_data.get('position', {})
                print(f"  Shoulder: x={pos.get('x', 0):.3f}, y={pos.get('y', 0):.3f}, z={pos.get('z', 0):.3f}")
                
                # Other joints
                if leg_data['joints']:
                    shoulder2_data = leg_data['joints'][0]
                    pos = shoulder2_data.get('position', {})
                    print(f"  Shoulder2: x={pos.get('x', 0):.3f}, y={pos.get('y', 0):.3f}, z={pos.get('z', 0):.3f}")
                    
                    if 'knee' in shoulder2_data:
                        knee_data = shoulder2_data['knee']
                        pos = knee_data.get('position', {})
                        print(f"  Knee: x={pos.get('x', 0):.3f}, y={pos.get('y', 0):.3f}, z={pos.get('z', 0):.3f}")
                        
                        if 'foot' in knee_data:
                            foot_data = knee_data['foot']
                            pos = foot_data.get('position', {})
                            print(f"  Foot: x={pos.get('x', 0):.3f}, y={pos.get('y', 0):.3f}, z={pos.get('z', 0):.3f}")

# Example usage
if __name__ == "__main__":
    # Load your JSON data
    with open('Scripts/JSON/interface_out.json', 'r') as f:
        json_data = json.load(f)
    # Create robot from JSON
    robot = RobotDogFromJSON(json_data)
    # Print positions
    robot.print_positions()
    # Print current angles
    print("\nCurrent joint angles from JSON:")
    for leg_name, angles in robot.current_angles.items():
        print(f"\n{leg_name}:")
        print(f"  Shoulder 1: {np.rad2deg(angles['shoulder1']):.2f}°")
        print(f"  Shoulder 2: {np.rad2deg(angles['shoulder2']):.2f}°")
        print(f"  Knee: {np.rad2deg(angles['knee']):.2f}°")
    # Get foot positions
    foot_positions = robot.get_current_foot_positions()
    print("\nCurrent foot positions (global):")
    for leg_name, pos in foot_positions.items():
        print(f"{leg_name}: {pos}")
    # Plot the robot (current position)
    print("\nPlotting robot configuration (current position)...")
    fig = plt.figure(figsize=(12, 10))
    ax1 = fig.add_subplot(121, projection='3d')
    robot.plot_robot(ax=ax1)
    # Plot the robot with body moved forward by 0.5 units in X using IK
    print("Plotting robot configuration (body moved forward, IK)...")
    ax2 = fig.add_subplot(122, projection='3d')
    robot.plot_robot_with_body_offset_ik(np.array([0.5, 0, 0]), ax=ax2)  # Larger offset to test
    plt.tight_layout()
    plt.show()
    print("Done")