from numpy import array
from numpy.linalg import norm

from parts.arm import Arm
from parts.brain import Brain
from parts.joint import Joint
from utils.toolbox import vectorize, vectorize_quat
from scipy.spatial.transform import Rotation as R

from parts.shape import Shape


class Body:
    parts = []
    arms = []

    def __init__(self, context):
        self.brain = None
        self.centroid = None
        self.context = context
        self.init_joints()
        self.init_kinematics()
        self.pos = vectorize(self.context.data.pos)
        self.rot = vectorize_quat(self.context.data.rot)
        self.direction = vectorize(self.context.data.dir)
        self.shape = Shape(self.context.data.shape)
        self.velocity = vectorize(self.context.data.vel)
        self.local_velocity = vectorize(self.context.data.local_velocity)
        self.local_acceleration = vectorize(self.context.data.local_acceleration)
        self.gravity_center = None
        self.setBrain()

    def setBrain(self):
        self.brain = Brain(self)

    def refresh(self):
        if self.context.data.joints is not None:
            for input_joint in self.context.data.joints:
                [arm.refreshData(input_joint) for arm in self.arms if arm.first_joint.index == input_joint.index]

        for arm in self.arms:
            [joint.updateRelativePosition(self.pos) for joint in arm.joints]

        self.pos = vectorize(self.context.data.pos)
        self.gravity_center = vectorize(self.context.data.mass_center)
        self.direction = vectorize(self.context.data.dir)
        self.shape.refresh(self.context.data.shape)
        self.velocity = vectorize(self.context.data.vel)
        self.local_velocity = vectorize(self.context.data.local_velocity)
        self.local_acceleration = vectorize(self.context.data.local_acceleration)


    def init_joints(self):
        if self.context.data.joints is None: return
        for parts in self.context.data.joints:
            joint = Joint(self.context, parts)
            self.arms.append(Arm(joint, self))
            self.parts.append(joint)

        # self.calcSibling()

    @property
    def joints(self) -> list:
        return [joint for joint in self.parts if isinstance(joint, Joint)]

    def init_kinematics(self):
        [arm.init_kinematics() for arm in self.arms]
