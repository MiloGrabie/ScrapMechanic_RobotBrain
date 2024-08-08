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

class PlotRobot:

    def __init__(self, context, body):
        self.ax = None
        self.context = context
        self.body = body
        self.init_matplot()

    def init_matplot(self):
        plt.ion()
        fig = plt.figure()
        self.ax = fig.add_subplot(111, projection='3d')

    def refresh_plot(self):
        self.ax.cla()

        # for arm in self.body.arms:
        #     self.scatter3D(arm.foot_pos + arm.default * self.body.direction)
        #     self.scatter3D(arm.foot_pos)
            # self.plot3D([j.position for j in arm.joints])
        print("centroid", self.body.direction)
        # self.plot3D([self.body.centroid, self.body.centroid + self.body.direction])
        self.rpz_robot()

        plt.draw()
        plt.pause(0.00001)

    def draw_length(self):
        arm = self.body.arms[0]
        points = []
        points.append(array([0, 0, 0]))
        for i, j in enumerate(arm.joints):
            p = points[-1] + j.length
            self.plot3D([points[-1], points[-1] + j.direction])
            # print(j.position - (j.position + p))
            points.append(p)
            # self.scatter3D(p)
        # points = [j.position + j.length for j in arm.joints[:-1]]
        self.plot3D(points)

    def rpz_robot(self):
        # arm = self.body.arms[0]
        # arms = [arm.siblings[0], arm, arm.siblings[1]]
        # other_arm = [a for a in self.body.arms if a not in arms][0]
        # arms.append(other_arm)
        # arms.insert(0, other_arm)
        # for arm in self.body.arms:
        #     points = [a.first_joint.position for a in [arm.siblings[0], arm, arm.siblings[1]]]
        # self.plot3D([a.first_joint.position for a in self.body.arms])

        # for arm in self.body.arms:
        #     self.plot3D([j.position for j in arm.joints])
        #     #self.scatter3D(arm.first_joint.position + arm.objective)

        # velocity_vector = self.body.velocity
        # start_point = self.body.centroid
        # end_point = start_point + velocity_vector
        # self.plot3D([start_point, end_point])

        for arm in self.body.arms:
            length = [0,0,0]
            for j in arm.joints:
                # self.scatter3D(j.localPosition)
                length += j.length
                self.scatter3D(length)
            

        # if self.body.gravity_center is not None:
        #     self.scatter3D(self.body.gravity_center)
        #     gc = self.body.gravity_center
        #     gc[2] = 0
        #     self.scatter3D(gc)
        # [self.scatter3D(a.default) for a in arms]

        # print(arms[0].first_joint.position - arms[1].end_joint.position)

        points = [a.end_joint.position for a in self.body.arms]
        x, y, z = zip(*points)
        self.ax.plot3D(x, y, [0] * len(points))

    def plot3D(self, points):
        x, y, z = zip(*points)
        self.ax.plot3D(x, y, z)

    def scatter3D(self, point):
        x, y, z = zip(point)
        self.ax.scatter(x, y, z)

