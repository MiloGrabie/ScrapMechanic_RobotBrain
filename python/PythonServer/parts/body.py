from parts.joint import Joint
import json

class Body:

    parts = []

    def __init__(self, context):
        self.context = context
        self.init_joints()

    def init_joints(self):
        for parts in self.context.data.joints:
            self.parts.append(Joint(self.context, parts))

    def getJoints(self) -> list:
        return self.parts # TODO : only select joints



