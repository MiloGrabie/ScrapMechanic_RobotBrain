import json
import pickle
import time

from threading import Thread
import multiprocessing as mp

from numpy.linalg import norm
from scipy.spatial.transform import Rotation as R

import matplotlib.pyplot as plt
import numpy as np
from numpy import array

from context import Context
from multi_legged.body_ml import Body_ML
from parts.body import Body
from training.URDF_Interface import URDF_Interface
from utils.plotRobot import PlotRobot


def get_orientation(xAxis, yAxis, zAxis):
    indexes = [(1, 2, 0), (0, 2, 1), (0, 1, 2)]
    return_data = [0, 0, 0]
    for i, index in enumerate(indexes):
        if sum([abs(xAxis[index[0]]), abs(yAxis[index[1]]), abs(zAxis[index[2]])]) == 3:
            return_data[i] = 1
            return return_data


class MainPlot:

    def __init__(self):
        self.ax = None
        self.context = Context(read_only=True)
        self.body = Body(self.context)
        self.plotRobot = PlotRobot(self.context, self.body)
        self.URDF_Interface = URDF_Interface(self.body)
        self.run()

    def run(self):
        while True:
            self.context.refresh()
            self.body.refresh()
            self.plotRobot.refresh_plot()


if __name__ == '__main__':
    plotRobot = MainPlot()
