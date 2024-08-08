from inputs import get_gamepad
import math
import threading

class XboxController:
    def __init__(self):
        self.left_joystick = {"x": 0.0, "y": 0.0}
        self.right_joystick = {"x": 0.0, "y": 0.0}
        self.triggers = {"left": 0.0, "right": 0.0}
        self.buttons = {
            "A": 0, "B": 0, "X": 0, "Y": 0,
            "LB": 0, "RB": 0,
            "BACK": 0, "START": 0,
            "LTHUMB": 0, "RTHUMB": 0
        }
        self._monitor_thread = threading.Thread(target=self._monitor_controller, daemon=True)
        self._monitor_thread.start()

    def _monitor_controller(self):
        while True:
            events = get_gamepad()
            for event in events:
                if event.code == "ABS_X":
                    self.left_joystick["x"] = self._normalize_joystick(event.state)
                elif event.code == "ABS_Y":
                    self.left_joystick["y"] = -self._normalize_joystick(event.state)  # Invert Y-axis
                elif event.code == "ABS_RX":
                    self.right_joystick["x"] = self._normalize_joystick(event.state)
                elif event.code == "ABS_RY":
                    self.right_joystick["y"] = -self._normalize_joystick(event.state)  # Invert Y-axis
                elif event.code == "ABS_Z":
                    self.triggers["left"] = event.state / 255.0
                elif event.code == "ABS_RZ":
                    self.triggers["right"] = event.state / 255.0
                elif event.code.startswith("BTN_"):
                    button_name = event.code[4:]
                    if button_name in self.buttons:
                        self.buttons[button_name] = event.state

    def _normalize_joystick(self, value):
        return value / 32768.0

    def get_left_joystick(self):
        return self.left_joystick

    def get_right_joystick(self):
        return self.right_joystick

    def get_triggers(self):
        return self.triggers

    def get_button(self, button_name):
        return self.buttons.get(button_name, 0)

    def get_all_buttons(self):
        return self.buttons