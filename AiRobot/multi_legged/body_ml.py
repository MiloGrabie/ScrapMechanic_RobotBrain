from numpy.linalg import norm

from multi_legged.arm_ml import Arm_ML
from multi_legged.brain_ml import Brain_ML
from parts.body import Body
from parts.joint import Joint


class Body_ML(Body):

    def __init__(self, context):
        super().__init__(context)
        self.calcCentroid()  # center of shoulders
        self.calc_corrections()

    def setBrain(self):
        self.brain = Brain_ML(self)

    def init_joints(self):
        if self.context.data.joints is None: return
        for parts in self.context.data.joints:
            joint = Joint(self.context, parts)
            self.arms.append(Arm_ML(joint, self))
            self.parts.append(joint)

        self.calcSibling()

    def refresh(self):
        super().refresh()
        self.calcCentroid()

    def calcSibling(self):
        for arm in self.arms:
            pos_list = [[norm(arm.first_joint.worldPosition - arm_local.first_joint.worldPosition), arm_local] for arm_local in
                        self.arms]
            closest_arm = sorted(pos_list, key=lambda tup: tup[0])[1:3]
            arm.siblings = [tup[1] for tup in closest_arm]

    def calcCentroid(self):
        if len(self.arms) == 0 : return
        list_shoulder = [arm.first_joint for arm in self.arms]
        x, y, z = zip(*[j.worldPosition for j in list_shoulder])
        self.centroid = (sum(x) / len(list_shoulder), sum(y) / len(list_shoulder), sum(z) / len(list_shoulder))

    def calc_corrections(self):
        [arm.calcCorrection() for arm in self.arms]
