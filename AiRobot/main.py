import json
import re

from numpy import array
from numpy.linalg import norm

from context import Context
from parts.body import Body
import time
import numpy as np
from multi_legged.body_ml import Body_ML
from math import pi
from scipy.spatial.transform import Rotation as R

from utils.plotRobot import PlotRobot
from utils.xbox_controller import XboxController


class Main:
    body = None

    def __init__(self):
        self.context = Context()
        self.body = None
        self.init_object()
        # self.plotRobot = PlotRobot(self.context, self.body)
        self.xbox_controller = XboxController()
        self.run()

    def init_object(self):
        self.body = Body(self.context)

    def run(self):
        self.context.refresh()
        # self.plotRobot.refresh_plot()
        # self.context.clearAction()
        # time.sleep(1)
        # value = [-1.5, 0, -1]
        value = [0.75, 0.25, -1.5]
        objective = np.array(value)

        self.body.brain.setArms(objective)

        # self.body.brain.setArmsDefault()

        # time.sleep(1)
        # self.context.callback()
        cycle = 0
        while True:
            self.context.refresh()
            self.body.refresh()
            # self.plotRobot.refresh_plot()

            # value[0] -= 0.01
            # value[1] += 0.01
            # value[1] += 0.01

            # self.body.brain.move([1, 1, 1])

            arm = self.body.arms[0]

            delta = array([self.xbox_controller.LeftJoystickY, -self.xbox_controller.LeftJoystickX, self.xbox_controller.RightJoystickY])
            delta = np.round(delta, 1)
            print(delta)
            value += delta / 10
            objective = np.array(value)
            arm.move(objective)

            # print(self.body.arms[0].default)
            # if cycle % 80 == 0:
            #     value = [-0.75, 0.25, -1.5]
            #     objective = np.array(value)
            #     self.body.brain.setArms(objective)
            # if cycle % 80 == 40:
            #     value = [0.75, 0.25, -1.5]
            #     objective = np.array(value)
            #     self.body.brain.setArms(objective)
            # self.body.brain.doMagic()
            # self.body.brain.move([1,0])
            cycle += 1
            time.sleep(0.1)


if __name__ == '__main__':
    Main()
