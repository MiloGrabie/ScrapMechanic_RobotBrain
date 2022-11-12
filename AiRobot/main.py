import json
import re

from numpy.linalg import norm

from context import Context
from parts.body import Body
import time
import numpy as np
from multi_legged.body_ml import Body_ML
from math import pi
from scipy.spatial.transform import Rotation as R


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
        value = [-1.5, 0, 1]
        value = [1, 0, 1]
        value[0],value[1]=value[1],value[0]
        #
        # value[0] += 0
        # value[1] += 0.75
        # value[2] += -0.25


        # for joint in self.body.arms[0].joints:
        #     joint.angle = 0
        #     joint.maxImpulse = 500
        #     joint.move()
        # time.sleep(5)
        # self.context.callback()s

        while True:
            self.context.refresh()
            self.body.refresh()
            # value[0] -= 0.1
            # value[1] -= 0.1
            # value[2] -= 0.1
            # joint = self.body.joints[1]
            # r = R.from_quat(joint.localRotation)
            # print(joint.localRotation)
            # print(r.as_rotvec())
            # print(r.as_euler('xyz', degrees=True))
            print()

            for arm in self.body.arms:
                for joint in arm.joints:
                    print(f"wp : {np.around(joint.worldPosition,2)} lp: {joint.localPosition} jl: {joint.length} jDir: {joint.direction}")
            # print("default", arm.shoulder_pos - arm.foot_pos)
            # print([norm(j.length) for j in arm.joints])
            # print([j.length for j in arm.joints])
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
