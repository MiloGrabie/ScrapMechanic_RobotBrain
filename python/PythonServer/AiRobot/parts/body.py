from numpy.linalg import norm

from python.PythonServer.AiRobot.parts.arm import Arm
from python.PythonServer.AiRobot.parts.brain import Brain
from python.PythonServer.AiRobot.parts.joint import Joint
from python.PythonServer.AiRobot.utils.toolbox import vectorize


class Body:
    parts = []
    arms = []

    def __init__(self, context):
        self.brain = None
        self.centroid = None
        self.context = context
        self.init_joints()
        self.init_kinematics()
        self.pos = vectorize(self.context.data.pos)
        self.gravity_center = None
        self.setBrain()

    def setBrain(self):
        self.brain = Brain(self)

    def refresh(self):
        for input_joint in self.context.data.joints:
            [arm.refreshData(input_joint) for arm in self.arms if arm.first_joint.index == input_joint.index]

        self.pos = vectorize(self.context.data.pos)
        self.gravity_center = vectorize(self.context.data.mass_center)

    def init_joints(self):
        for parts in self.context.data.joints:
            joint = Joint(self.context, parts)
            self.arms.append(Arm(joint, self))
            self.parts.append(joint)

        # self.calcSibling()

    def getJoints(self) -> list:
        return [joint for joint in self.parts if isinstance(joint, Joint)]

    def init_kinematics(self):
        [arm.init_kinematics() for arm in self.arms]
