
import numpy as np
from multi_legged.brain_ml import Brain_ML


class DogBrain(Brain_ML):

    def __init__(self, body):
        super().__init__(body)

    def forward(self):
        self.getFrontArm()

    def getFrontArm(self):
        for index, arm in enumerate(self.body.arms):
            arm = self.body.arms[0]
            print(index, arm.end_joint.relativePosition)
        # print(index, arm.end_joint.localPosition)
        # print(self.body.arms[0].end_joint.relativePosition)
        # print(arm.end_joint.worldPosition)
        print(np.linalg.norm(self.body.arms[0].end_joint.relativePosition))
        self.body.arms[0].move(np.array([1, 1, 1]))