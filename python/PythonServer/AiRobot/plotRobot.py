import json
import pickle
import time

from threading import Thread
import multiprocessing as mp

import matplotlib.pyplot as plt
import numpy as np

from context import Context
from parts.body import Body


class PlotRobot:

    def __init__(self):
        self.ax = None
        self.context = Context(read_only=True)
        self.body = Body(self.context)
        self.run()

    def init_matplot(self):
        plt.ion()
        fig = plt.figure()
        self.ax = fig.add_subplot(111, projection='3d')

    def run(self):
        while True:
            self.context.refresh()
            self.body.refresh()
            self.refresh_plot()
            time.sleep(1)

    def refresh_plot(self):
        self.ax.cla()

        for arm in self.body.arms:
            points = [joint.position for joint in arm.joints]
            coord = [[v[i] for v in points] for i, _ in enumerate(points[0])]
            self.ax.plot3D(coord[0], coord[1], coord[2])

        # ax.scatter(10,k,k)
        # ax.scatter(k,k,10)
        plt.draw()
        plt.pause(0.02)


if __name__ == '__main__':
    plotRobot = PlotRobot()

    for i in range(20):
        plotRobot.refresh_plot()