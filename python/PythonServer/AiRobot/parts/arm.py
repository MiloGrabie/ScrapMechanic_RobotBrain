from numpy.linalg import norm

from python.PythonServer.AiRobot.inverseKinematics import InverseKinematics


class Arm:

    def __init__(self, joint, body):
        self.objective = None
        self.inverseKinematics = None
        self.first_joint = joint
        self.end_joint = self.init_end_joint()
        self.body = body
        self.joints = self.init_joints()
        self.position_correction = [1, 1, 1]  # relative position correction
        self.max_length = sum([norm(j.length) for j in self.joints])

    def init_kinematics(self):
        self.calcCorrection()
        # for joint in self.joints:
        #     joint.length *= self.position_correction
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

    def calcCorrection(self):
        joint = self.first_joint
        center_x, center_y = self.body.centroid[0], self.body.centroid[1]
        x, y = joint.position[0], joint.position[1]
        correction = [1, 1 if y > center_y else -1, -1 if x < center_x else 1]
        self.position_correction = correction

    def move(self, objective=None):
        if objective is not None:
            self.objective = objective
        angles = self.inverseKinematics.getAngle(self.objective * self.position_correction)
        for index, angle in enumerate(angles):
            self.joints[index].angle = angle
            self.joints[index].move()

    @property
    def shoulder_pos(self):
        return self.first_joint.position

    @property
    def foot_pos(self):
        return self.end_joint.position