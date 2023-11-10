import time

from threading import Thread
import multiprocessing as mp

from numpy.linalg import norm
from scipy.spatial.transform import Rotation as R

import matplotlib.pyplot as plt
import numpy as np
from numpy import array
from utils.toolbox import vectorize

from context import Context
from multi_legged.body_ml import Body_ML
from parts.body import Body
import trimesh

class PlotRobotRay:

    def __init__(self, context):
        self.ax = None
        self.context = context
        self.points = []
        self.init_trimesh()

    def init_trimesh(self):
        self.points = [vectorize(point) for point in self.context.data.raycasts[0:10]]
        self.points.append(vectorize(self.context.data.pos))
        pointsCloud = trimesh.PointCloud(self.points)
        axes = trimesh.creation.axis(axis_length=4)
        sphere = trimesh.creation.icosphere(radius=1)
        scene = trimesh.Scene([pointsCloud, axes, sphere]).show()
        # scene.show(callback=self.update_object)

    def update_object(self, scene):
        pass
        # self.context.refresh()
        # self.points.append(np.array([10,10,10 + scene.geometry['geometry_0'].shape[0] - 100]))
        # self.points = [vectorize(point) for point in self.context.data.raycasts]
        # print(len(self.points))
        # scene.geometry['geometry_0'] = trimesh.PointCloud(self.points)
        # print(scene.geometry['geometry_0'].shape)
        # scene.graph.update("", geometry='geometry_0')

    def refresh_plot(self):
        # print("test")
        # self.points.append(np.array([10,10,10]))
        pass



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
        arm = self.body.arms[0]
        arms = [arm.siblings[0], arm, arm.siblings[1]]
        other_arm = [a for a in self.body.arms if a not in arms][0]
        arms.append(other_arm)
        arms.insert(0, other_arm)
        # for arm in self.body.arms:
        #     points = [a.first_joint.position for a in [arm.siblings[0], arm, arm.siblings[1]]]
        self.plot3D([a.first_joint.position for a in arms])

        for arm in self.body.arms:
            self.plot3D([j.position for j in arm.joints])

        if self.body.gravity_center is not None:
            self.scatter3D(self.body.gravity_center)
            gc = self.body.gravity_center
            gc[2] = 0
            self.scatter3D(gc)
        # [self.scatter3D(a.default) for a in arms]

        # print(arms[0].first_joint.position - arms[1].end_joint.position)

        points = [a.end_joint.position for a in arms]
        x, y, z = zip(*points)
        self.ax.plot3D(x, y, [0] * len(points))

    def plot3D(self, points):
        x, y, z = zip(*points)
        self.ax.plot3D(x, y, z)

    def scatter3D(self, points):
        x, y, z = zip(points)
        self.ax.scatter(x, y, z)

