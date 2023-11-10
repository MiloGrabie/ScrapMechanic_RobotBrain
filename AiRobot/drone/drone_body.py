from numpy import array
from numpy.linalg import norm

from utils.toolbox import vectorize, vectorize_quat
from scipy.spatial.transform import Rotation as R

from utils.actions import Actions
from parts.shape import Shape
from simple_pid import PID

class DroneBody:

    def __init__(self, context):
        self.context = context
        
        self.index = self.context.data.index
        self.pos = vectorize(self.context.data.pos)
        self.vel = vectorize(self.context.data.vel)
        self.rot = vectorize_quat(self.context.data.rot)
        self.direction = vectorize(self.context.data.dir)
        self.shape = Shape(self.context.data.shape)
        self.mass = self.context.data.mass
        self.apply_impulse()
        self.height_pid = PID(0.5, 0.1, 0.01)
        self.front_speed = PID(0.5, 0.1, 0.01)

    def apply_impulse(self, impulse = 0):        
        action = {
            "index": self.index,
            "impulse_vector": [0,0,impulse],
        }
        self.context.registerAction(Actions.ApplyImpulse, action)

    def set_height(self, height):
        actual_height = self.context.data.pos['z']
        order = height - actual_height
        self.height_pid.setpoint = order
        input = self.vel[2]
        input = 100 if input > 100 else input
        input = 0 if input < 0 else input
        impulse = self.height_pid(input) * self.mass / 10
        impulse = 200 if impulse > 200 else impulse
        impulse = -200 if impulse < -200 else impulse
        # print("order", order, "response", impulse, "actual_height", actual_height, "input", input, "vel", self.vel)
        self.apply_impulse(impulse)

    def go_forward(self, speed):
        actual_speed = self.vel[2]
        order = speed - actual_speed
        self.height_pid.setpoint = order
        input = self.acceleration[2]
        input = 100 if input > 100 else input
        input = 0 if input < 0 else input
        impulse = self.height_pid(input) * self.mass / 10
        print("order", order, "response", impulse, "actual_speed", actual_speed, "input", input, "acceleration", self.context.acceleration)
        self.apply_impulse(impulse)

    
    def refresh(self):
        self.pos = vectorize(self.context.data.pos)
        self.vel = vectorize(self.context.data.vel)
        self.rot = vectorize_quat(self.context.data.rot)
        self.direction = vectorize(self.context.data.dir)
        self.gravity_center = vectorize(self.context.data.mass_center)
        self.acceleration = vectorize(self.context.acceleration) if self.context.acceleration is not None else None
        self.shape.refresh(self.context.data.shape)