from parts.joint import Joint
import json

from python.PythonServer.parts.arm import Arm


class Body:

    parts = []
    arms = []

    def __init__(self, context):
        self.context = context
        self.init_joints()

    def refresh(self):
        for parts in self.context.data.joints:
            [joint.refresh_data(parts) for joint in self.parts if joint.index == parts.index]


    def init_joints(self):
        for parts in self.context.data.joints:
            joint = Joint(self.context, parts)
            self.arms.append(Arm(joint))
            self.parts.append(joint)

    def getJoints(self) -> list:
        return [joint for joint in self.parts if isinstance(joint, Joint)] # TODO : only select joints



