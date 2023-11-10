import trimesh
import numpy as np

from context import Context
from utils.toolbox import vectorize

# # Sample point cloud data
# points = np.random.random((100, 3))

# # Optional: Create colors for each point
# colors = np.random.randint(0, 255, size=(points.shape[0], 4))

# Create a PointCloud object
# cloud = trimesh.points.PointCloud(points, colors=colors).show()
context = Context(read_only=True)

points = [vectorize(point) for point in context.data.raycasts]
# points = [point for point in points if point[0] <= -50 and point[1] != 0 and point[2] != 0]
# points = generate_sphere_points(10, [0, 0, 0], 100)
# points.append(vectorize(context.data.pos))
print(len(points))
colors = np.random.randint(100, 255, size=(len(points), 4))

cloud = trimesh.PointCloud(points, colors=colors)
axes = trimesh.creation.axis(axis_length=2000)
sphere = trimesh.creation.icosphere(radius=1)
# scene = trimesh.Scene([cloud, axes, sphere]).show()

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Create a new matplotlib figure and 3D axis
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Scatter plot
sc = ax.scatter(
    cloud.vertices[:, 0],  # X coordinates
    cloud.vertices[:, 1],  # Y coordinates
    cloud.vertices[:, 2],  # Z coordinates
    s=10,                  # Point size, you can also pass an array to set individual sizes
    c=cloud.colors[:, :3] / 255,  # Point colors, assuming colors are in [0, 255]
    depthshade=False
)

# Setting the aspect ratio to equal for x, y, z
ax.set_box_aspect([np.ptp(i) for i in cloud.vertices.T])


pos = vectorize(context.data.pos)
dir = vectorize(context.data.dir)
point_at = [pos, (pos + dir)*2]

def plot3D(ax, points):
    x, y, z = zip(*points)
    ax.plot3D(x, y, z)

x, y, z = zip(pos)
ax.scatter(x, y, z)

# plot3D(ax, point_at)

# Show the plot
plt.show()

# print(mesh.vertices.shape, mesh.faces.shape, mesh.triangles.shape, mesh.bounds)