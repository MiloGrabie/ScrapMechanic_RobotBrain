import numpy as np
import tinyik
from math import pi

from numpy import array
from ikpy.chain import Chain
from ikpy.link import OriginLink, URDFLink

value = [3, 3, -5]


class InverseKinematics:

    actuator_list = []

    def __init__(self, arm):
        self.arm = arm
        # actuator_parameter = []
        # for index, joint in enumerate(arm.joints):
        #     if index == len(arm.joints)-1: break
        #     actuator_parameter.append(self.getAxisLetter(joint.direction))
        #     # if index == 0:
        #     #     actuator_parameter.append('z')
        #     # else:
        #     #     actuator_parameter.append('x')
        #     actuator_parameter.append(joint.length)
        #
        # # actuator_parameter.insert(0, [0,0,-1])
        # self.actuator = tinyik.Actuator(actuator_parameter)

        links = []
        links.append(
            URDFLink(
                name="origin",
                origin_translation=array([0,0,0]),
                origin_orientation=array([0, 0, 0]),
                rotation=arm.first_joint.direction,
            )
        )
        for index, joint in enumerate(arm.joints):
            if index == len(arm.joints)-1:
                links.append(
                    URDFLink(
                        name=joint.index,
                        origin_translation=array([0,0,0]),
                        origin_orientation=array([0, 0, 0]),
                        rotation=joint.direction,
                    )
                )
            else:
                links.append(
                    URDFLink(
                        name=joint.index,
                        origin_translation=joint.length,
                        origin_orientation=array([0, 0, 0]),
                        rotation=arm.joints[index+1].direction,
                    )
                )

        self.actuator = Chain(name='left_arm', links=links)

    def getAngle(self, objective):
        # self.actuator.inverse_kinematics(objective)
        # tinyik.visualize(self.actuator)
        angles = self.actuator.inverse_kinematics(objective)

        # return self.actuator.angles
        # print("deg", self.actuator.angles)
        return angles

    def getAxisLetter(self, vect):
        if vect == [1, 0, 0]: return "x"
        if vect == [0, 1, 0]: return "y"
        if vect == [0, 0, 1]: return "z"



def calc(length_first, length_second, length_third):
    arm = tinyik.Actuator(['z', length_first, 'x', length_second, 'x', length_third])
    # arm.angles = [pi, 1]
    # value[2] += 0.1
    arm.ee = value
    tinyik.visualize(arm)
    result = [arm.angles[0], arm.angles[1], arm.angles[2]]
    print("result", result)
    return result
    # leg = tinyik.Actuator([[.3, .0, .0], 'z', [.3, .0, .0], 'x', [.0, -.5, .0], 'x', [.0, -.5, .0]])
    # leg.angles = np.deg2rad([30, 45, -90])
    # tinyik.visualize(leg)

if __name__ == '__main__':
    pass