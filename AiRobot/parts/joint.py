import numpy as np
from numpy import array

from parts.part import Part

from utils.actions import Actions
from utils.toolbox import vectorize, vectorize_quat

from AiRobot.parts.shape import Shape
from scipy.spatial.transform import Rotation as R


class Joint(Part):

    def __init__(self, context, part):
        self.shapeB = Shape(part.shapeB) if part.shapeB is not None else None
        self.length = None
        self.context = context
        self.index = part.index
        self.angle = part.angle
        self.targetAngle = 0
        self.localRotation = vectorize_quat(part.localRotation)
        self.localPosition = vectorize(part.localPosition)
        self.xAxis = vectorize(part.xAxis)
        self.yAxis = vectorize(part.yAxis)
        self.zAxis = vectorize(part.zAxis)
        self.worldPosition = vectorize(part.position)
        self.worldRotation = vectorize_quat(part.rotation)
        self.direction = self.getDirection()
        self.angularVelocity = 1.5
        self.maxImpulse = 350
        self.joints = []
        self.getChildJoint(part)

    @property
    def position(self):
        return self.worldPosition

    def getChildJoint(self, part):
        self.length = 0
        if 'joints' in part:
            for joint in part.joints:
                local_joint = Joint(self.context, joint)
                self.joints.append(local_joint)
                self.length = (local_joint.localPosition - self.localPosition)/4
                # self.length = (self.localPosition-local_joint.localPosition)/4
                # self.length = local_joint.worldPosition - self.worldPosition

    def refresh_data(self, part):
        self.angle = part.angle
        self.localRotation = vectorize_quat(part.localRotation)
        self.localPosition = vectorize(part.localPosition)
        self.worldPosition = vectorize(part.position)
        self.worldRotation = vectorize_quat(part.rotation)
        if 'joints' in part:
            for input_joint in part.joints:
                [joint.refresh_data(input_joint) for joint in self.joints if joint.index == input_joint.index]
        if self.shapeB: self.shapeB.refresh(part.shapeB)

    # def setTargetAngle(self, targetAngle, targetVelocity, maxImpulse):
    #
    #     self.context.callback(self.toJson())

    def move(self):
        action = {
            "index": self.index,
            "targetAngle": np.round(self.targetAngle, 3),
            "angularVelocity": self.angularVelocity,
            "maxImpulse": self.maxImpulse,
        }
        self.context.registerAction(Actions.setTargetAngle, action)

    def getDirection(self):
        return self.zAxis
        indexes = [(1, 2, 0), (0, 2, 1), (0, 1, 2)]
        return_data = [0, 0, 0]
        for i, index in enumerate(indexes):
            if sum([abs(self.xAxis[index[0]]), abs(self.yAxis[index[1]]), abs(self.zAxis[index[2]])]) == 3:
                return_data[i] = 1
                return return_data

