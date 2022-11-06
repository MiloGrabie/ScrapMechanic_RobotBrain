from parts.joint import Joint
import json

class Body:

    parts = []

    def __init__(self, context):
        self.context = context
        self.init_joints()

    def refresh(self):
        for parts in self.context.data.joints:
            [joint.refresh_data(parts) for joint in self.parts if joint.index == parts.index]

    def init_joints(self):
        for parts in self.context.data.joints:
            self.parts.append(Joint(self.context, parts))

    def getJoints(self) -> list:
        return [joint for joint in self.parts if isinstance(joint, Joint)] # TODO : only select joints



