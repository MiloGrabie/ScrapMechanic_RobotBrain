from numpy import array
from numpy.linalg import norm

from AiRobot.parts.arm import Arm
from AiRobot.parts.brain import Brain
from AiRobot.parts.joint import Joint
from AiRobot.utils.toolbox import vectorize, vectorize_quat
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
        self.direction = array(R.from_quat(self.rot).as_rotvec())
        self.shape = Shape(self.context.data.shape)
        self.gravity_center = None
        self.setBrain()

    def setBrain(self):
        self.brain = Brain(self)

    def refresh(self):
        if self.context.data.joints is not None:
            for input_joint in self.context.data.joints:
                [arm.refreshData(input_joint) for arm in self.arms if arm.first_joint.index == input_joint.index]

        self.pos = vectorize(self.context.data.pos)
        self.gravity_center = vectorize(self.context.data.mass_center)
        self.shape.refresh(self.context.data.shape)

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
