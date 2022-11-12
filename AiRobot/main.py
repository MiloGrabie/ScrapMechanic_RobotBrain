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

from utils.plotRobot import PlotRobot


class Main:
    body = None

    def __init__(self):
        self.context = Context()
        self.body = None
        self.init_object()
        self.plotRobot = PlotRobot(self.context, self.body)
        self.run()

    def init_object(self):
        self.body = Body_ML(self.context)

    def run(self):
        self.context.refresh()
        self.plotRobot.refresh_plot()
        # self.context.clearAction()
        # time.sleep(1)
        # value = [-1.5, 0, -1]
        value = [0.75, 0.25, -1.25]
        objective = np.array(value)
        self.body.brain.setArms(objective)

        # self.body.brain.setArmsDefault()

        # time.sleep(1)
        # self.context.callback()
        cycle = 0
        while True:
            self.context.refresh()
            self.body.refresh()
            self.plotRobot.refresh_plot()

            # value[0] -= 0.01
            # value[1] += 0.01
            # value[1] += 0.01
            # for arm in self.body.arms:
            #     for joint in arm.joints:
            #         print(f"wp : {np.around(joint.worldPosition,2)} lp: {joint.localPosition} jl: {joint.length} jDir: {joint.direction}")
            #         # print(f"angle envoye : {joint.targetAngle} angle recu: {joint.angle}")
            # print("default", arm.shoulder_pos - arm.foot_pos)
            # print([norm(j.length) for j in arm.joints])
            # print([j.length for j in arm.joints])
            print(cycle % 30)
            if cycle % 30 == 0:
                value = [-0.75, 0.25, -1.25]
                objective = np.array(value)
                self.body.brain.setArms(objective)
            if cycle % 30 == 15:
                value = [0.75, 0.25, -1.25]
                objective = np.array(value)
                self.body.brain.setArms(objective)
            # self.body.brain.doMagic()
            # self.body.brain.move([1,0])
            cycle += 1
            time.sleep(0.1)


    # def callAction(self):
    #     for joint in self.body.getJoints():
    #         if (joint.index == 1):
    #             joint.angle = -1 if joint.angle < 0 else 1
    #             joint.move()


if __name__ == '__main__':
    Main()
