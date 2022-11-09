from numpy import array
from numpy.linalg import norm

from python.PythonServer.AiRobot.utils.toolbox import getFarthestPoint


class Brain:

    def __init__(self, body):
        self.body = body

    def control_gravity(self):
        gv = self.body.gravity_center
        dist_gv_pos = gv - self.body.pos
        print("distance centre machine", dist_gv_pos)

        closest_arm = self.closest_arm()
        # closest_arm = self.body.arms[0]

        shoulder = closest_arm.first_joint
        center_influ = shoulder.position
        sib_a = closest_arm.siblings[0].end_joint.position
        sib_b = closest_arm.siblings[1].end_joint.position
        farthest_point = getFarthestPoint(
            [center_influ[0], center_influ[1]],
            closest_arm.max_length - 5,
            [sib_a[0], sib_a[1]],
            [sib_b[0], sib_b[1]]
        )
        farthest_point = array([farthest_point[0], farthest_point[1], 0])
        farthest_point -= center_influ
        farthest_point -= 1
        farthest_point = farthest_point
        farthest_point[2] = 5
        print(farthest_point)
        # farthest_point = [5, 5, 5]
        # objective = array(farthest_point)
        # objective[2] = 5
        print(farthest_point)
        closest_arm.move(farthest_point)
        print(closest_arm.max_length)
        # print(norm(objective))

    def closest_arm(self):
        gv = self.body.gravity_center
        pos_list = [[norm(gv - arm.end_joint.shapeB.pos), arm] for arm in self.body.arms]
        if pos_list[0][0] == 0.0 : return pos_list[0][1]
        return min(pos_list)[1]