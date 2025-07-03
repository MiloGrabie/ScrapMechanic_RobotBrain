from dog_motion.dog_brain import DogBrain
from multi_legged.body_ml import Body_ML

class DogBody(Body_ML):

    def __init__(self, context):
        super().__init__(context)
        self.input_order = []  # Add this line to initialize the input_order attribute

    def setBrain(self):
        self.brain = DogBrain(self)

    def forward(self):
        self.getFrontArm()

    def getFrontArm(self):
        for arm in self.arms:
            pass

    # You might want to add a method to update the input_order
    def update_input_order(self, new_input):
        self.input_order.append(new_input)