from parts.part import Part
import json

from utils.actions import Actions
from utils.toolbox import vectorize, vectorize_quat


class Joint(Part):

    def __init__(self, context, part):
        self.context = context
        self.index = part.index
        self.targetAngle = None
        self.refresh_data(part)
        self.xAxis = vectorize(part.xAxis)
        self.yAxis = vectorize(part.yAxis)
        self.zAxis = vectorize(part.zAxis)
        self.position = part.position
        self.angularVelocity = 3
        self.maxImpulse = 1000
        self.joints = []
        self.length = 0
        if 'joints' in part:
            for joint in part.joints:
                local_joint = Joint(context, joint)
                self.joints.append(local_joint)
                self.length = local_joint.localPosition - self.localPosition


    def refresh_data(self, part):
        self.angle = part.angle
        self.localRotation = vectorize_quat(part.localRotation)
        self.localPosition = vectorize(part.localPosition)

    # def setTargetAngle(self, targetAngle, targetVelocity, maxImpulse):
    #
    #     self.context.callback(self.toJson())

    def move(self):
        action = {
            "index": self.index,
            "targetAngle": self.angle,
            "angularVelocity": self.angularVelocity,
            "maxImpulse": self.maxImpulse,
        }
        self.context.registerAction(Actions.setTargetAngle, action)