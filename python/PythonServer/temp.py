import math
import numpy as np
from numpy import array
from numpy.linalg import norm


a = [2, 3]
b = [1, 6]
c = [5, 3]
#d = [4, 6]
r = 4

ab = array([b[0] - a[0], b[1] - a[1]])
k = ab
print(ab)
x = np.random.randn(2)
x -= x.dot(k) * k / np.linalg.norm(k)**2
x /= norm(x)
x *= r
e = [c[0] + x[0], c[1] + x[1]]
print(x, norm(x))
print(e)

def getFarthestPoint(circle_center, radius, a, b):
    k = array([b[0] - a[0], b[1] - a[1]])   # vector distance of the two other arm
    x = np.random.randn(2)
    x -= x.dot(k) * k / np.linalg.norm(k) ** 2
    x /= norm(x)    # normalization
    x *= radius  # multiply by the radius
    e = [circle_center[0] + x[0], circle_center[1] + x[1]]  # result construction
    return array(e)


