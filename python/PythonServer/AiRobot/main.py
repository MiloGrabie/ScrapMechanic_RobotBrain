import json
import re
from context import Context
from parts.body import Body
import time
import numpy as np
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
        time.sleep(2)
        value = [0, 4, 5]
        objective = np.array(value)
        for arm in self.body.arms:
            arm.move(objective)
        # objective = np.array(value)
        # self.body.arms[0].move(np.array([0., 0, 4]))   # [-1, -1, 1]
        # self.body.arms[1].move(objective)   # [1, 1, -1]
        # self.body.arms[2].move(np.array([0., 0, 4]))   # [1, -1, -1]
        # self.body.arms[3].move(objective)   # [-1, 1, 1]
        while True:
            self.context.refresh()
            self.body.refresh()
            self.body.brain.doMagic()
            self.body.brain.move([1,0])

            time.sleep(0.5)
            # value[1] -= 0.1d


    # def callAction(self):
    #     for joint in self.body.getJoints():
    #         if (joint.index == 1):
    #             joint.angle = -1 if joint.angle < 0 else 1
    #             joint.move()


if __name__ == '__main__':
    Main()
