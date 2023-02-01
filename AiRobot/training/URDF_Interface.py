import xml.etree.cElementTree as treeService

import numpy as np
from numpy import ndarray, array

from context import Context


class URDF_Interface:

    def __init__(self, body):
        self.body = body
        self.robot = treeService.Element("robot", name="my_bot")

        self.robot_component = {
            "links": [],
            "joints": []
        }

        self.map_robot()
        self.generateXml()
        self.export_robot()

    def map_robot(self):
        for i_arm, arm in enumerate(self.body.arms):
            for i_joint, joint in enumerate(arm.joints):
                origin = {
                    "xyz": joint.localPosition,
                    "rpy": array([0, 0, 0])
                }
                # size = array([0.5, 0.5, 0.5]) + 1 * arm.joints[i_joint+1].localPosition - joint.localPosition if i_joint < len(arm.joints) - 1 else array([1, 1, 1])
                size = arm.joints[i_joint - 1].localPosition - joint.localPosition if i_joint > 0 else joint.localPosition
                geometry = {
                    "box": {
                        # "size": joint.length
                        "size": size
                    }
                }
                link = {
                    "name": "{}_{}".format(i_arm, i_joint),
                    # "inertial": {
                    #     "origin": origin,
                    #     "mass": {"value":10},
                    #     "inertia": {
                    #         "ixx": "0.0",
                    #         "ixy": "0.0",
                    #         "ixz": "0.0",
                    #         "iyy": "0.0",
                    #         "iyz": "0.0",
                    #         "izz": "0.0"
                    #     }
                    # },
                    "visual": {
                        "origin": origin,
                        "geometry": geometry,
                        "material": {
                            "name": "color_{}_{}".format(i_arm, i_joint),
                            "color": {
                                "rgba": "{r} {g} {b} {a}".format(r=(i_arm * 0.2) % 1, g=(i_joint * 0.2) % 1, b=0.5,
                                                                 a=1)}
                        }
                    }
                }
                self.robot_component["links"].append(link)
                xyz = arm.joints[i_joint - 1].localPosition - joint.localPosition if i_joint > 0 else joint.localPosition
                joint_u = {
                    "name": "{}_{}".format(i_arm, i_joint),
                    "type": "fixed" if i_joint == 0 else "revolute",
                    "parent": {"link": "base" if i_joint == 0 else "{}_{}".format(i_arm, i_joint - 1)},
                    "child": {"link": "{}_{}".format(i_arm, i_joint)},
                    "origin": {
                        "xyz": xyz,
                        "rpy": array([0, 0, 0])
                    },
                    "axis": {
                        "xyz": joint.direction
                    },
                    "limit": {
                        "lower": "-3.14",
                        "upper": "3.14",
                        "effort": "1.0",
                        "velocity": "1.0",
                    }
                }
                self.robot_component["joints"].append(joint_u)

        base = {
            "name": "base",
            "visual": {
                "origin": {
                    "xyz": array([0, 0, 0]),
                    "rpy": array([0, 0, 0])
                },
                "geometry": {
                    "box": {
                        "size": array([0.1, 0.1, 0.1])
                    }
                }
            }
        }
        self.robot_component["links"].append(base)

    def generateXml(self):
        for link in self.robot_component["links"]:
            self.addNode(self.robot, link, "link")
        for joint in self.robot_component["joints"]:
            self.addNode(self.robot, joint, "joint")

    def export_robot(self):
        tree = treeService.ElementTree(self.robot)
        tree.write(Context.root_path + r"\AiRobot\training\filename.urdf")

    def addNode(self, parent, dico, node_name=None):
        node = parent if node_name is None else treeService.SubElement(parent, node_name)
        for key, value in dico.items():
            if isinstance(value, dict):
                self.addNode(node, value, key)
            else:
                node.set(key, self.transformValue(value))

    def transformValue(self, value):
        if isinstance(value, ndarray) or isinstance(value, tuple):
            return "{} {} {}".format(value[0], value[1], value[2])
        return str(value)


"""self.robot_component = {
    "link": {
        "name": "base",
        "visual": {
            "origin": {
                "xyz": np.array([0, 0, 0]),
                "rpy": np.array([0, 0, 0])
            },
            "geometry": {
                "box": {
                    "size": np.array([0, 0, 0])
                }
            }
        }
    }
}"""
