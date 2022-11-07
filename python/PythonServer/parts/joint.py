from parts.part import Part
import json

from utils.actions import Actions
from utils.toolbox import vectorize


class Joint(Part):

    def __init__(self, context, part):
        self.context = context
        self.index = part.index
        self.angle = part.angle
        self.targetAngle = None
        self.localRotation = part.localRotation
        self.localPosition = vectorize(part.localPosition)
        self.position = part.position
        self.angularVelocity = 3
        self.maxImpulse = 100

    def refresh_data(self, part):
        self.index = part.index
        self.angle = part.angle
        self.localRotation = part.localRotation
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