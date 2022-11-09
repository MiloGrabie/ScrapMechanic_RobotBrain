import numpy as np
from numpy import array
from numpy.linalg import norm


def vectorize(dico):
    return np.array([
        dico.x,
        dico.y,
        dico.z,
    ])


def vectorize_quat(dico):
    return np.array([
        dico.x,
        dico.y,
        dico.z,
        dico.w,
    ])


def getFarthestPoint(circle_center, radius, a, b):
    k = array([b[0] - a[0], b[1] - a[1]])   # vector distance of the two other arm
    x = np.random.randn(2)
    x -= x.dot(k) * k / np.linalg.norm(k) ** 2
    x /= norm(x)    # normalization
    x *= radius  # multiply by the radius
    x = abs(x)
    midpoint = [(a[0] + b[0])/2, (a[1] + b[1])/2]
    x *= [1 if circle_center[0] < midpoint[0] else -1, 1 if circle_center[1] < midpoint[1] else -1]
    e = [circle_center[0] + x[0], circle_center[1] + x[1]]  # result construction
    return array(e)