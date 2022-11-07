import json
import re
from context import Context
from parts.body import Body
import inverseKinematics
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
        while True:
            time.sleep(0.1)
            self.context.refresh()
            self.body.refresh()
            # print(self.body.parts[0].angle)
            # self.callAction()
            print(self.body.parts[0].localPosition)
            length_first = np.linalg.norm(self.body.parts[1].localPosition - self.body.parts[0].localPosition)
            length_second = np.linalg.norm(self.body.parts[2].localPosition - self.body.parts[1].localPosition)
            print(self.body.parts[2].localPosition)
            angles = inverseKinematics.calc(length_first + 1, length_second + 1)
            self.body.getJoints()[0].angle = angles[0]
            self.body.getJoints()[0].move()
            self.body.getJoints()[1].angle = angles[1]
            self.body.getJoints()[1].move()
            print(f"angles {angles}")
            # self.context.callback()

    def callAction(self):
        for joint in self.body.getJoints():
            if (joint.index == 1):
                joint.angle = -1 if joint.angle < 0 else 1;
                joint.move()



if __name__ == '__main__':
    Main()