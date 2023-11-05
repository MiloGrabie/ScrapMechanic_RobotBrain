


from dog_motion.dog_brain import DogBrain
from multi_legged.body_ml import Body_ML


class DogBody(Body_ML):

    def __init__(self, context):
        super().__init__(context)

    def setBrain(self):
        self.brain = DogBrain(self)

    def forward(self):
        self.getFrontArm()

    def getFrontArm(self):
        for arm in self.arms:
            pass