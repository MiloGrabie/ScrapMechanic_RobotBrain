
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

def refresh_plot():
    ax.cla()
    y = np.random.random([4,3])*10
    vectors = [[0,0,0], [10,10,10], [15,15,15]]

    coord = [[v[i] for v in vectors] for i, _ in enumerate(vectors[0])]

    ax.plot3D(coord[0], coord[1], coord[2])
    # ax.scatter(10,k,k)
    # ax.scatter(k,k,10)
    plt.draw()
    plt.pause(0.02)

refresh_plot()
refresh_plot()
refresh_plot()
print("soleil")