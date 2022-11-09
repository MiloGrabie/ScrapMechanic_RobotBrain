from numpy.linalg import norm

from python.PythonServer.AiRobot.parts.arm import Arm
from python.PythonServer.AiRobot.parts.brain import Brain
from python.PythonServer.AiRobot.parts.joint import Joint
from python.PythonServer.AiRobot.utils.toolbox import vectorize


class Body:

    parts = []
    arms = []

    def __init__(self, context):
        self.centroid = None
        self.context = context
        self.init_joints()
        self.calcCentroid() # center of shoulders
        self.init_kinematics()
        self.pos = vectorize(self.context.data.pos)
        self.gravity_center = None
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

        self.calcSibling()

    def calcSibling(self):
        for arm in self.arms:
            pos_list = [[norm(arm.first_joint.position - arm_local.first_joint.position), arm_local] for arm_local in self.arms]
            closest_arm = sorted(pos_list, key=lambda tup: tup[0])[1:3]
            arm.siblings = [tup[1] for tup in closest_arm]


    def getJoints(self) -> list:
        return [joint for joint in self.parts if isinstance(joint, Joint)]

    def calcCentroid(self):
        list_shoulder = [arm.first_joint for arm in self.arms]
        list_x = [joint.localPosition[0] for joint in list_shoulder]
        list_y = [joint.localPosition[1] for joint in list_shoulder]
        list_z = [joint.localPosition[2] for joint in list_shoulder]
        self.centroid = (sum(list_x) / len(list_shoulder), sum(list_y) / len(list_shoulder), sum(list_z) / len(list_shoulder))

    def init_kinematics(self):
        [arm.init_kinematics() for arm in self.arms]




