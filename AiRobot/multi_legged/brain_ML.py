from numpy import array, dot
from numpy.linalg import norm
from shapely import geometry


from AiRobot.utils.toolbox import getFarthestPoint


class Brain_ML:

    def __init__(self, body):
        self.body = body

    def move(self, direction):
        for arm in self.body.arms:
            if norm(arm.default) < 0.5:
                arm.objective += direction
                arm.move()

    def setArms(self, objective):
        for arm in self.body.arms:
            arm.objective = objective
            arm.move()

    def doMagic(self):
        # self.control_gravity()
        self.control_latitude()

    def control_gravity(self):
        gc = self.body.gravity_center
        dist_gv_pos = gc - self.body.pos

        is_inside, distance = self.gravityCenterInside()
        if is_inside or distance > 0.3: return

        print("distance centre machine", dist_gv_pos)

        closest_arm = self.closest_arm()
        # closest_arm = self.body.arms[0]

        shoulder = closest_arm.first_joint
        center_influ = shoulder.worldPosition
        sib_a = closest_arm.siblings[0].end_joint.worldPosition
        sib_b = closest_arm.siblings[1].end_joint.worldPosition
        farthest_point = getFarthestPoint(
            [center_influ[0], center_influ[1]],
            closest_arm.max_length - 5,
            [sib_a[0], sib_a[1]],
            [sib_b[0], sib_b[1]]
        )
        farthest_point = array([farthest_point[0], farthest_point[1], 0])
        farthest_point -= center_influ

        vect_centro = self.body.centroid - center_influ # Vecteur depuis le centroid vers l'épaule
        if dot(vect_centro, farthest_point) < 0:
            farthest_point *= -1
        farthest_point[2] = 5

        print(farthest_point)
        closest_arm.move(farthest_point)
        print(closest_arm.max_length)
        # print(norm(objective))

    def closest_arm(self):
        gv = self.body.gravity_center
        pos_list = [[norm(gv - arm.end_joint.shapeB.pos), arm] for arm in self.body.arms]
        if pos_list[0][0] == 0.0 : return pos_list[0][1]
        return min(pos_list)[1]

    def control_latitude(self):
        for arm in self.body.arms:
            new_obj = arm.objective
            new_obj[2] = 5
            arm.move(new_obj)

    def gravityCenterInside(self):
        points = [(a.foot_pos[0], a.foot_pos[1]) for a in self.body.arms]
        polygon = geometry.Polygon(points)

        gv = self.body.gravity_center
        point = geometry.Point(gv[0], gv[1])
        print("p distance", polygon.exterior.distance(point))
        return polygon.contains(point), polygon.exterior.distance(point)
