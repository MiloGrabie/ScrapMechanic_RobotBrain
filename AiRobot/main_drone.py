import json
import re

from numpy import array
from numpy.linalg import norm
from drone.drone_body import DroneBody

from context import Context
import time
import numpy as np
from math import pi
from scipy.spatial.transform import Rotation as R
from controller import XboxController

class MainDrone:
    body: DroneBody | None = None
    controller: XboxController

    def __init__(self):
        self.context = Context()
        self.body = None
        self.controller = XboxController()
        self.init_object()
        self.run()

    def init_object(self):
        self.body = DroneBody(self.context)

    def run(self):
        self.context.refresh()
        
        while True:
            self.context.refresh()
            self.body.refresh()

            right_joystick = self.controller.get_right_joystick()
            left_joystick = self.controller.get_left_joystick()
            triggers = self.controller.get_triggers()
            #print(triggers)

            multiplier = self.body.mass

            roll = -triggers['left'] + triggers['right']
            #print(roll)

            order_vector = [
                left_joystick["y"] * multiplier,
                left_joystick["x"] * multiplier,
                roll * multiplier
            ]
            shape_dir = array(order_vector)
            #print(shape_dir)

            self.body.apply_impulse(order_vector)


            direction_multiplier = self.body.mass / 10

            direction_vector = [0, 0, -right_joystick['x'] * direction_multiplier]
            #self.body.apply_torque(direction_vector)
            self.body.stabilize_pitch_and_roll(-right_joystick['x'] * direction_multiplier)

            time.sleep(0.1)

if __name__ == '__main__':
    MainDrone()
