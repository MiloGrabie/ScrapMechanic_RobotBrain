import numpy as np
import tinyik
from math import pi

value = [3, 3, -5]


class InverseKinemactis:

    def __init__(self, body):
        self.body = body


def calc(length_first, length_second, length_third):
    arm = tinyik.Actuator(['z', length_first, 'x', length_second, 'x', length_third])
    # arm.angles = [pi, 1]
    # value[2] += 0.1
    arm.ee = value
    # tinyik.visualize(arm)
    result = [arm.angles[0], arm.angles[1], arm.angles[2]]
    print("result", result)
    return result
    # leg = tinyik.Actuator([[.3, .0, .0], 'z', [.3, .0, .0], 'x', [.0, -.5, .0], 'x', [.0, -.5, .0]])
    # leg.angles = np.deg2rad([30, 45, -90])
    # tinyik.visualize(leg)
