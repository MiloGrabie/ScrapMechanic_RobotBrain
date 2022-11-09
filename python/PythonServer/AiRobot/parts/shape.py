from python.PythonServer.AiRobot.utils.toolbox import vectorize


class Shape:

    def __init__(self, shape):
        self.refresh(shape)

    def refresh(self, shape):
        self.pos = vectorize(shape.pos)
