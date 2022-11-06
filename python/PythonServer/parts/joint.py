from parts.part import Part
import json

from utils.actions import Actions


class Joint(Part):

    def __init__(self, context, part):
        self.context = context
        self.index = part.index
        self.targetAngle = part.angle
        self.angularVelocity = 1
        self.maxImpulse = 1

    # def setTargetAngle(self, targetAngle, targetVelocity, maxImpulse):
    #
    #     self.context.callback(self.toJson())

    def move(self):
        action = {
            "index": self.index,
            "targetAngle": self.targetAngle,
            "angularVelocity": self.angularVelocity,
            "maxImpulse": self.maxImpulse,
        }
        self.context.registerAction(Actions.setTargetAngle, action)