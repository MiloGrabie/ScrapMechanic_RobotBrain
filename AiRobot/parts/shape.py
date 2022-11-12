from numpy import array

from AiRobot.utils.toolbox import vectorize, vectorize_quat

from scipy.spatial.transform import Rotation as R

class Shape:

    def __init__(self, shape):
        self.direction = None
        self.at = None
        self.rot = None
        self.pos = None
        self.up = None
        self.refresh(shape)

    def refresh(self, shape):
        self.pos = vectorize(shape.pos)
        self.rot = vectorize_quat(shape.rot)
        self.at = vectorize(shape.at)
        self.up = vectorize(shape.up)
        self.direction = array(R.from_quat(self.rot).as_rotvec())
