import json
import re
from context import Context
from parts.body import Body
import time

class Main:

    body = None

    def __init__(self):
        self.context = Context()
        self.init_object()
        self.run()

    def init_object(self):
        self.body = Body(self.context)

    def run(self):
        self.context.refresh()
        self.callAction()
        while True:
            time.sleep(10)
            self.context.refresh()
            self.callAction()
            # self.context.callback()

    def callAction(self):
        for joint in self.body.getJoints():
            joint.targetAngle += 0.001
            joint.move()



if __name__ == '__main__':
    Main()