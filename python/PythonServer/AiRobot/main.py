import json
import re

from numpy.linalg import norm

from context import Context
from parts.body import Body
import time
import numpy as np
from multi_legged.body_ml import Body_ML
from math import pi


class Main:
    body = None

    def __init__(self):
        self.context = Context()
        self.init_object()
        self.run()

    def init_object(self):
        self.body = Body(self.context)

    def run(self):
        self.context.refresh()
        self.context.clearAction()
        # time.sleep(2)
        value = [0, 12, 11]

        while True:
            self.context.refresh()
            self.body.refresh()
            # value[0] -= 0.1
            # value[1] -= 0.1
            # value[2] -= 0.1
            arm = self.body.arms[0]
            print("default", arm.shoulder_pos - arm.foot_pos)
            print([norm(j.length) for j in arm.joints])
            print([j.length for j in arm.joints])
            objective = np.array(value)
            self.body.brain.setArms(objective)
            # self.body.brain.doMagic()
            # self.body.brain.move([1,0])

            time.sleep(0.5)


    # def callAction(self):
    #     for joint in self.body.getJoints():
    #         if (joint.index == 1):
    #             joint.angle = -1 if joint.angle < 0 else 1
    #             joint.move()


if __name__ == '__main__':
    Main()
