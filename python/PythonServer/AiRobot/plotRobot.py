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
        self.init_matplot()
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

    def refresh_plot(self):
        self.ax.cla()

        for arm in self.body.arms:
            points = [joint.position for joint in arm.joints]
            self.plot3D(points)

        # points = [arm.first_joint.position for arm in self.body.arms]
        # self.plot3D(points)
        # self.plot3D([arm.end_joint.position for arm in self.body.arms])

        arm = self.body.arms[0]
        arms = [arm.siblings[0], arm, arm.siblings[1]]
        other_arm = [a for a in self.body.arms if a not in arms][0]
        arms.append(other_arm)
        arms.insert(0, other_arm)
        # for arm in self.body.arms:
        #     points = [a.first_joint.position for a in [arm.siblings[0], arm, arm.siblings[1]]]
        self.plot3D([a.first_joint.position for a in arms])

        points = [a.end_joint.position for a in arms]
        x, y, z = zip(*points)
        self.ax.plot3D(x, y, [0]*len(points))

        # self.scatter3D(self.body.centroid)
        self.scatter3D(self.body.gravity_center)
        floor_gc = self.body.gravity_center
        floor_gc[2] = 0
        self.scatter3D(floor_gc)

        # ax.scatter(10,k,k)
        # ax.scatter(k,k,10)
        plt.draw()
        plt.pause(0.0001)

    def plot3D(self, points):
        x, y, z = zip(*points)
        self.ax.plot3D(x, y, z)

    def scatter3D(self, points):
        x, y, z = zip(points)
        self.ax.scatter(x, y, z)

if __name__ == '__main__':
    plotRobot = PlotRobot()