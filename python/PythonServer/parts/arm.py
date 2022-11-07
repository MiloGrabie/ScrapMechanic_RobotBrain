from python.PythonServer.inverseKinematics import InverseKinematics


class Arm:

    def __init__(self, joint):
        self.first_joint = joint
        self.joints = self.init_joints()
        self.inverseKinematics = InverseKinematics(self)

    def init_joints(self):
        joint = self.first_joint
        joints = []
        while True:
            joints.append(joint)
            if len(joint.joints) == 0: break
            joint = joint.joints[0]
        return joints

    def move(self, objective):
        angles = self.inverseKinematics.getAngle(objective)
        for index, angle in enumerate(angles):
            self.joints[index].angle = angle
            self.joints[index].move()