from numpy import array
from numpy.linalg import norm

from AiRobot.inverseKinematics import InverseKinematics


class Arm:

    def __init__(self, joint, body):
        self.objective = array([3, 3, 3])
        self.inverseKinematics = None
        self.first_joint = joint
        self.end_joint = self.init_end_joint()
        self.body = body
        self.joints = self.init_joints()
        self.angles = array([0] * len(self.joints))
        #self.position_correction = [1, 1, 1]  # relative position correction
        self.max_length = sum([norm(j.length) for j in self.joints])

    def init_kinematics(self):
        #self.calcCorrection()
        self.inverseKinematics = InverseKinematics(self)

    def init_joints(self):
        joint = self.first_joint
        joints = []
        while True:
            joints.append(joint)
            if len(joint.joints) == 0: break
            joint = joint.joints[0]
        return joints

    def init_end_joint(self):
        joint = self.first_joint
        while True:
            if len(joint.joints) == 0:
                return joint
            joint = joint.joints[0]

    def refreshData(self, joint):
        self.first_joint.refresh_data(joint)

    def move(self, objective=None):
        if objective is not None:
            self.objective = objective
        self.angles = self.inverseKinematics.getAngle(self.objective)
        for index, joint in enumerate(self.joints):
            joint.targetAngle = self.angles[index]
            joint.move()

    @property
    def default(self):
        return self.first_joint.worldPosition - array([0, 0, 5])
        # return self.first_joint.position + array([0, 0, 5])

    @property
    def shoulder_pos(self):
        return self.first_joint.worldPosition

    @property
    def foot_pos(self):
        return self.end_joint.worldPosition