
from AiRobot.parts.arm import Arm


class Arm_ML(Arm):

    def __init__(self, joint, body):
        super().__init__(joint, body)
        self.position_correction = [1, 1, 1]  # relative position correction

    def calcCorrection(self):
        joint = self.first_joint
        center_x, center_y = self.body.centroid[0], self.body.centroid[1]
        x, y = joint.worldPosition[0], joint.worldPosition[1]
        correction = [1, 1 if y > center_y else -1, -1 if x < center_x else 1]
        self.position_correction = correction

    def move(self, objective=None):
        if objective is not None:
            self.objective = objective
        angles = self.inverseKinematics.getAngle(self.objective * self.position_correction)
        # angles = self.inverseKinematics.getAngle(self.objective)
        for index, angle in enumerate(angles):
            self.joints[index].targetAngle = angle
            self.joints[index].move()
