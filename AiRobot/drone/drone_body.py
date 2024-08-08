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
        self.height_pid = PID(2, 0.01, 0.1)
        self.front_speed = PID(2, 0.01, 0.01)
        self.pitch_pid = PID(1, 0.01, 0.8)
        self.pitch_pid = PID(1, 0.05, 0.8)
        self.order_vector = array([0.0, 0.0, 0.0])

    def apply_impulse(self, impulse_vector=[0, 0, 0]):
        action = {
            "index": self.index,
            "impulse_vector": impulse_vector,
        }
        self.context.registerAction(Actions.ApplyImpulse, action)

    def apply_torque(self, torque_vector=[0, 0, 0]):
        action = {
            "index": self.index,
            "torque_vector": torque_vector,
        }
        self.context.registerAction(Actions.ApplyTorque, action)

    def add_order_vector(self, order_vector):
        new_order_vector = array(order_vector)
        max_value = 300.0
        self.order_vector = array([
            self.order_vector[0] if new_order_vector[0] == 0 else max(-max_value, min(max_value, new_order_vector[0])),
            self.order_vector[1] if new_order_vector[1] == 0 else max(-max_value, min(max_value, new_order_vector[1])),
            self.order_vector[2] if new_order_vector[2] == 0 else max(-max_value, min(max_value, new_order_vector[2]))
        ])
        #print(self.order_vector)
        self.apply_impulse([float(self.order_vector[0]), float(self.order_vector[1]), float(self.order_vector[2])])

    def set_height(self, height):
        actual_height = self.context.data.pos['z']
        order = height - actual_height
        self.height_pid.setpoint = order
        input = self.vel[2]
        input = 200 if input > 200 else input
        input = 0 if input < 0 else input
        impulse = self.height_pid(input) * self.mass / 10
        impulse = max(-200, min(200, impulse))
        # print("order", order, "response", impulse, "actual_height", actual_height, "input", input, "vel", self.vel)
        self.add_order_vector([0, 0, impulse])

    def go_forward(self, speed):
        actual_speed = self.vel[1]
        order = speed - actual_speed
        self.front_speed.setpoint = order
        input = self.context.acceleration[2] if self.context.acceleration is not None else 0
        input = 100 if input > 100 else input
        input = 0 if input < 0 else input
        impulse = self.front_speed(input) * self.mass / 10
        impulse = max(-1000, min(1000, impulse))
        #print("order", order, "response", impulse, "actual_speed", actual_speed, "input", input, "acceleration", self.context.acceleration)
        self.add_order_vector([0, impulse, 0])

    def stabilize_pitch_and_roll(self, yaw):
        rotation = R.from_quat(self.rot)
        current_row = rotation.as_euler('xyz')[0]
        current_pitch = -rotation.as_euler('xyz')[1]
        print('current', current_row, current_pitch)
        
        row_correction = self.pitch_pid(current_row) * self.mass / 10
        pitch_correction = self.pitch_pid(current_pitch) * self.mass / 10
        
        #print('correction', pitch_correction, pitch_correction)
        self.apply_torque([pitch_correction, row_correction, yaw])

    
    def refresh(self):
        self.pos = vectorize(self.context.data.pos)
        self.vel = vectorize(self.context.data.vel)
        self.rot = vectorize_quat(self.context.data.rot)
        self.direction = vectorize(self.context.data.dir)
        self.gravity_center = vectorize(self.context.data.mass_center)
        self.acceleration = vectorize(self.context.acceleration) if self.context.acceleration is not None else None
        self.shape.refresh(self.context.data.shape)