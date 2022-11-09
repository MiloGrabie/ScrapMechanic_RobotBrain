from parts.part import Part

from utils.actions import Actions
from utils.toolbox import vectorize, vectorize_quat

from python.PythonServer.AiRobot.parts.shape import Shape


class Joint(Part):

    def __init__(self, context, part):
        self.shapeB = Shape(part.shapeB)
        self.length = None
        self.context = context
        self.index = part.index
        self.targetAngle = None
        self.angle = part.angle
        self.localRotation = vectorize_quat(part.localRotation)
        self.localPosition = vectorize(part.localPosition)
        self.xAxis = vectorize(part.xAxis)
        self.yAxis = vectorize(part.yAxis)
        self.zAxis = vectorize(part.zAxis)
        self.position = vectorize(part.position)
        self.angularVelocity = 1
        self.maxImpulse = 350
        self.joints = []
        self.getChildJoint(part)

    def getChildJoint(self, part):
        self.length = 0
        if 'joints' in part:
            for joint in part.joints:
                local_joint = Joint(self.context, joint)
                self.joints.append(local_joint)
                self.length = local_joint.localPosition - self.localPosition

    def refresh_data(self, part):
        self.angle = part.angle
        self.localRotation = vectorize_quat(part.localRotation)
        self.localPosition = vectorize(part.localPosition)
        if 'joints' in part:
            for input_joint in part.joints:
                [joint.refresh_data(input_joint) for joint in self.joints if joint.index == input_joint.index]
        self.shapeB.refresh(part.shapeB)

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

