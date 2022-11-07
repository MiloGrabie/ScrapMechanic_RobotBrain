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
        self.callAction()
        value = [7, 5, 5]
        while True:
            time.sleep(0.1)
            self.context.refresh()
            self.body.refresh()
            # print(self.body.parts[0].localPosition)
            objective = np.array(value)
            print(objective)
            self.body.arms[0].move(objective * [-1, -1, 1]) # -1 -1 1
            self.body.arms[1].move(objective * [1, 1, -1])
            self.body.arms[2].move(objective * [1, -1, -1])
            self.body.arms[3].move(objective * [-1, 1, 1])
            value[1] -= 0.1

            # self.context.callback()

    def callAction(self):
        for joint in self.body.getJoints():
            if (joint.index == 1):
                joint.angle = -1 if joint.angle < 0 else 1
                joint.move()


if __name__ == '__main__':
    Main()
