import json
import re

from numpy import array
from numpy.linalg import norm
from drone.drone_body import DroneBody

from context import Context
import time
import numpy as np
from math import pi
from scipy.spatial.transform import Rotation as R



class MainDrone:
    body = None

    def __init__(self):
        self.context = Context()
        self.body = None
        self.init_object()
        # self.plotRobot = PlotRobot(self.context, self.body)
        self.run()

    def init_object(self):
        self.body = DroneBody(self.context)

    def run(self):
        self.context.refresh()
        
        cycle = 0
        while True:
            self.context.refresh()
            self.body.refresh()

            # print(self.body.pos)
            # self.body.go_forward(10)
            self.body.set_height(-20)

            cycle += 1
            time.sleep(0.1)


if __name__ == '__main__':
    MainDrone()
