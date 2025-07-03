import numpy as np
import time
from context import Context
from dog_motion.dog_body import DogBody
from dog_motion.dog_brain import DogBrain
from utils.plotRobot import PlotRobot

class Main:
    def __init__(self):
        self.context = Context()
        self.body = DogBody(self.context)
        self.body.brain = DogBrain(self.body)
        #self.plotRobot = PlotRobot(self.context, self.body)
        self.run_training()

    def run_training(self):
        num_episodes = 1000
        max_steps_per_episode = 500
        batch_size = 32
        self.body.brain.train(num_episodes, max_steps_per_episode, batch_size)

if __name__ == '__main__':
    Main()