from numpy import array, dot
from numpy.linalg import norm
from pyparsing import Optional
from shapely import geometry
from scipy.spatial.transform import Rotation as R
import copy


from utils.toolbox import getFarthestPoint
from parts.brain import Brain


class Brain_ML(Brain):

    def __init__(self, body):
        super().__init__(body)
        self.stored_arms = [copy.deepcopy(arm) for arm in body.arms]

    def move(self, direction):
        for arm in self.body.arms:
            if norm(arm.default) < 0.5 or 1 != 1:
                arm.objective += direction
                arm.move()

    def setArms(self, objective):
        for arm in self.body.arms:
            arm.objective = objective
            arm.move()
        
        self.stored_arms = [copy.deepcopy(arm) for arm in self.body.arms]
    

    def doMagic(self):
        pass
        # self.control_gravity()
        # self.control_latitude()

    def control_gravity(self):
        gc = self.body.gravity_center
        dist_gv_pos = gc - self.body.pos

        is_inside, distance = self.gravityCenterInside()
        print("distance gv arm", distance)
        if is_inside and distance > 0.08: return

        closest_arm = self.closest_arm()
        # closest_arm = self.body.arms[0]

        shoulder = closest_arm.first_joint
        center_influ = shoulder.worldPosition
        sib_a = closest_arm.siblings[0].end_joint.worldPosition
        sib_b = closest_arm.siblings[1].end_joint.worldPosition
        farthest_point = getFarthestPoint(
            [center_influ[0], center_influ[1]],
            closest_arm.max_length,
            [sib_a[0], sib_a[1]],
            [sib_b[0], sib_b[1]]
        )
        farthest_point = array([farthest_point[0], farthest_point[1], 0])
        farthest_point -= center_influ

        vect_centro = self.body.centroid - center_influ # Vecteur depuis le centroid vers l'épaule
        # if dot(vect_centro, farthest_point) < 0:
        #     farthest_point *= -1
        farthest_point[0] *= -1
        farthest_point[2] = closest_arm.objective[2]

        # print(farthest_point)
        closest_arm.move(farthest_point)
        # print(closest_arm.max_length)
        # print(norm(objective))

    def closest_arm(self):
        gc = self.body.gravity_center
        if gc is None: return
        pos_list = [[norm(gc - arm.end_joint.shapeB.pos), arm] for arm in self.body.arms]
        if pos_list[0][0] == 0.0 : return pos_list[0][1]
        return min(pos_list)[1]

    def control_latitude(self):
        height = -1.5
        #print(self.body.local_velocity)
        
        for index, arm in enumerate(self.body.arms):
            if index != 0: continue
            delta = arm.first_joint.position - arm.end_joint.position

            # Calculate horizontal and vertical distance
            horizontal_distance = abs(delta[0]) + abs(delta[1])
            vertical_distance = abs(delta[2])

            distance = 20
            #print(delta, horizontal_distance)

            if horizontal_distance > distance :
                # Move the arm behind the first_joint
                # new_objective = array([first_joint_pos[0], first_joint_pos[1], arm.objective[2]])
                new_objective = array([0,0,height])
                #print(new_objective)
                arm.move(new_objective)
                
                self.stored_arms[index] = copy.deepcopy(arm)
            else :
                delta_pos = arm.end_joint.position - self.stored_arms[index].end_joint.position
                # delta_vel = array([
                #     (self.body.local_velocity[0] / 4),
                #     (self.body.local_velocity[1] / 4),
                #     0
                # ])

                delta = (delta_pos) * [0, 0, 1]
                # Add the delta to the objective
                print(delta, "delta")
                new_objective = array(self.stored_arms[index].objective + delta)
                print(new_objective)
                #print(new_objective)
                arm.move(new_objective)

    def gravityCenterInside(self):
        points = [(a.foot_pos[0], a.foot_pos[1]) for a in self.body.arms]
        polygon = geometry.Polygon(points)

        gv = self.body.gravity_center
        point = geometry.Point(gv[0], gv[1])
        return polygon.contains(point), polygon.exterior.distance(point)
