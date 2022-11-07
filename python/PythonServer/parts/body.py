from numpy.linalg import norm
from parts.joint import Joint
import json

import numpy as np

from python.PythonServer.parts.arm import Arm
from python.PythonServer.utils.toolbox import vectorize


class Body:

    parts = []
    arms = []

    def __init__(self, context):
        self.centroid = None
        self.context = context
        self.init_joints()
        self.calcCentroid() # center of shoulders
        self.init_kinematics()
        self.pos = vectorize(self.context.data.pos)
        self.gravity_center = None

    def control_gravity(self):
        gv = self.gravity_center
        pos_list = [[norm(gv - arm.end_joint.shapeB.pos), arm] for arm in self.arms]
        # print([(pos[0], pos[1]) for pos in pos_list])
        dist_gv_pos = gv - self.pos
        normalized = np.array([dist_gv_pos[0] / abs(dist_gv_pos[0]), dist_gv_pos[1] / abs(dist_gv_pos[1]), dist_gv_pos[2] / abs(dist_gv_pos[2])])
        print("distance centre machine", dist_gv_pos)
        # print(pos_list)
        # print(min(pos_list))
        closest_arm = min(pos_list)[1]
        farthest_point = [5, 5, 5]
        objective = np.array(farthest_point) * normalized
        objective[2] = 5
        print(objective)
        closest_arm.move(objective)
        print(closest_arm.max_length)
        print(norm(objective))
        # print(nearest_point, gv)
        # print("distance", norm(gv - nearest_point))

    def refresh(self):
        for input_joint in self.context.data.joints:
            [arm.refreshData(input_joint) for arm in self.arms if arm.first_joint.index == input_joint.index]

        self.pos = vectorize(self.context.data.pos)
        self.gravity_center = vectorize(self.context.data.mass_center)

    def init_joints(self):
        for parts in self.context.data.joints:
            joint = Joint(self.context, parts)
            self.arms.append(Arm(joint, self))
            self.parts.append(joint)

    def getJoints(self) -> list:
        return [joint for joint in self.parts if isinstance(joint, Joint)]

    def calcCentroid(self):
        list_shoulder = [arm.first_joint for arm in self.arms]
        list_x = [joint.localPosition[0] for joint in list_shoulder]
        list_y = [joint.localPosition[1] for joint in list_shoulder]
        self.centroid = (sum(list_x) / len(list_shoulder), sum(list_y) / len(list_shoulder))

    def init_kinematics(self):
        [arm.init_kinematics() for arm in self.arms]




