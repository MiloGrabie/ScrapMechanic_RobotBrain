from numpy import array, dot
from numpy.linalg import norm
from shapely import geometry


class Brain:

    def __init__(self, body):
        self.body = body

    def setArms(self, objective):
        for arm in self.body.arms:
            arm.move(objective)

