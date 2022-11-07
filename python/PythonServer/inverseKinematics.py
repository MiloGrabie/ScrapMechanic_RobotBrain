
import numpy as np
import tinyik
from math import pi

value = [10, -2, 0.]

class InverseKinemactis:

    def __init__(self, body):
        self.body = body

def calc(length_first, length_second):
    arm = tinyik.Actuator(['z', [length_first, 0., 0.], 'z', [length_second, 0., 0.]])
    # arm.angles = [pi, 1]
    value[0] -= 0.1
    arm.ee = value
    # tinyik.visualize(arm)
    result = [ - arm.angles[0], -arm.angles[1]]
    return result
    # leg = tinyik.Actuator([[.3, .0, .0], 'z', [.3, .0, .0], 'x', [.0, -.5, .0], 'x', [.0, -.5, .0]])
    # leg.angles = np.deg2rad([30, 45, -90])
    # tinyik.visualize(leg)
