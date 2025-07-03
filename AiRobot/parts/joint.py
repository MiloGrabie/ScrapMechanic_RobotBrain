import numpy as np
from numpy import array

from parts.part import Part

from utils.actions import Actions
from utils.toolbox import vectorize, vectorize_quat

from parts.shape import Shape
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
        self.relativePosition = None
        self.xAxis = vectorize(part.xAxis)
        self.yAxis = vectorize(part.yAxis)
        self.zAxis = vectorize(part.zAxis)
        self.worldPosition = vectorize(part.position)
        self.worldRotation = vectorize_quat(part.rotation)
        self.direction = -vectorize(part.direction)
        self.angularVelocity = 10
        self.maxImpulse = 1000
        self.joints = []
        self.updateChildrenJoints(part)

    def updateRelativePosition(self, body_position):
        self.relativePosition = self.position - body_position

    @property
    def position(self):
        return self.worldPosition
    
    @property
    def velocity(self):
        return self.shapeB.velocity

    def updateChildrenJoints(self, part):
        self.length = 0
        if 'joints' in part:
            for joint in part.joints: # normally, there's only one joint on the next shape
                next_joint = Joint(self.context, joint)
                self.joints.append(next_joint)
                # self.length = (next_joint.localPosition - self.localPosition)/4
                # next_joint.length = (self.localPosition - next_joint.localPosition)/4
                # print(self.length)
                # self.length = (self.localPosition-local_joint.localPosition)/4
                # self.length = local_joint.worldPosition - self.worldPosition

    def refresh_data(self, part):
        self.angle = part.angle
        self.localRotation = vectorize_quat(part.localRotation)
        self.localPosition = vectorize(part.localPosition)
        self.worldPosition = vectorize(part.position)
        self.worldRotation = vectorize_quat(part.rotation)
        # self.direction = vectorize(part.direction)
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

