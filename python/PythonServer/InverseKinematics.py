from math import acos, pi, sin, cos, sqrt, atan2


# https://www.youtube.com/watch?v=nW5FUVzYCKM
class InverseKinemactis:

    def __init__(self, body):
        self.body = body

    def calc(self):
        x = 10
        y = 10
        a1 = 10  # length_first
        a2 = 5  # length_second
        r = 12  # length_objective
        alpha = acos((a1 ** 2) + (a2 ** 2) - (x ** 2) - (y ** 2) / (2 * a1 * a2))
        q2 = pi - alpha  # angle_second

        a2_sin_q2 = sqrt(1 - cos(q2**2))
        a2_cos_q2 = a2 * sin(q2)
        side_length = a1 + a2_cos_q2
        beta = atan2(a2_sin_q2, side_length)  # angle_first from r
        q1 = atan2(y,x) - atan2(a2_sin_q2, (a1 + a2_cos_q2))  # angle_first from horizontal
