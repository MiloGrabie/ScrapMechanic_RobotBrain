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


def get_orientation(xAxis, yAxis, zAxis):
    indexes = [(1, 2, 0), (0, 2, 1), (0, 1, 2)]
    return_data = [0, 0, 0]
    for i, index in enumerate(indexes):
        if sum([abs(xAxis[index[0]]), abs(yAxis[index[1]]), abs(zAxis[index[2]])]) == 3:
            return_data[i] = 1
            return return_data


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

        # self.scatter3D([32, -30, 0])
        # self.scatter3D([39, -20, 3])
        #
        # self.scatter3D([35, -25.25, 1.5])

        # for arm in self.body.arms:
        #     points = [joint.position for joint in arm.joints]
        #     # [self.scatter3D(joint.position) for joint in arm.joints]
        #     print(points)
        #     self.plot3D(points)
            # points = [joint. for joint in arm.joints]
            # self.plot3D(points)

        # points = []
        # points.append(self.body.arms[0].joints[0].position)
        # points.append([0,0,0])
        # for i, j in enumerate(self.body.arms[0].joints):
        #     p = points[-1] + j.length
        #     points.append(p)
        #     self.scatter3D(p)
        # points = [j.position + j.length for j in self.body.arms[0].joints]
        # points.insert(0, self.body.arms[0].joints[0].position)
        # self.plot3D(points)

        # self.body.arms[0].inverseKinematics.actuator.plot(self.body.arms[0].angles, self.ax)
        # self.body.arms[0].inverseKinematics.actuator.plot([j.targetAngle for j in self.body.arms[0].joints], self.ax)
        self.body.arms[0].inverseKinematics.actuator.plot([*[j.angle for j in self.body.arms[0].joints], 0], self.ax)

        # self.scatter3D(self.body.joints[-1].localPosition)
        # points = [arm.first_joint.position for arm in self.body.arms]
        # self.plot3D(points)
        # self.plot3D([arm.end_joint.position for arm in self.body.arms])

        # self.scatter3D(self.body.centroid)
        # self.scatter3D(self.body.gravity_center)
        # floor_gc = self.body.gravity_center
        # floor_gc[2] = 0
        # self.scatter3D(floor_gc)

        # ax.scatter(10,k,k)
        # ax.scatter(k,k,10)
        plt.draw()
        plt.pause(0.0001)

    def rpz_robot(self):
        arm = self.body.arms[0]
        arms = [arm.siblings[0], arm, arm.siblings[1]]
        other_arm = [a for a in self.body.arms if a not in arms][0]
        arms.append(other_arm)
        arms.insert(0, other_arm)
        # for arm in self.body.arms:
        #     points = [a.first_joint.position for a in [arm.siblings[0], arm, arm.siblings[1]]]
        self.plot3D([a.first_joint.position for a in arms])

        # [self.scatter3D(a.default) for a in arms]

        print(arms[0].first_joint.position - arms[1].end_joint.position)

        points = [a.end_joint.position for a in arms]
        x, y, z = zip(*points)
        self.ax.plot3D(x, y, [0] * len(points))

    def plot3D(self, points):
        x, y, z = zip(*points)
        self.ax.plot3D(x, y, z)

    def scatter3D(self, points):
        x, y, z = zip(points)
        self.ax.scatter(x, y, z)


if __name__ == '__main__':
    plotRobot = PlotRobot()
