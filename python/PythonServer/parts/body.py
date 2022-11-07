from parts.joint import Joint
import json

from python.PythonServer.parts.arm import Arm


class Body:

    parts = []
    arms = []

    def __init__(self, context):
        self.centroid = None
        self.context = context
        self.init_joints()
        self.calcCentroid() # center of shoulders

    def refresh(self):
        for parts in self.context.data.joints:
            [joint.refresh_data(parts) for joint in self.parts if joint.index == parts.index]


    def init_joints(self):
        for parts in self.context.data.joints:
            joint = Joint(self.context, parts)
            self.arms.append(Arm(joint))
            self.parts.append(joint)

    def getJoints(self) -> list:
        return [joint for joint in self.parts if isinstance(joint, Joint)]

    def calcCentroid(self):
        list_shoulder = [arm.first_joint for arm in self.arms]
        list_x = [joint.localPosition[0] for joint in list_shoulder]
        list_y = [joint.localPosition[1] for joint in list_shoulder]
        self.centroid = (sum(list_x) / len(list_shoulder), sum(list_y) / len(list_shoulder))
        center_x, center_y = self.centroid[0], self.centroid[1]
        for arm in self.arms:
            joint = arm.first_joint
            x, y = joint.localPosition[0], joint.localPosition[1]
            correction = [1 if x > center_x else -1, 1 if y > center_y else -1, 1]
            arm.position_correction = correction



