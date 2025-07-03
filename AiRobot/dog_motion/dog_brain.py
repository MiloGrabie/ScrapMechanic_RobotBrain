import time
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from collections import deque
import random
from multi_legged.brain_ml import Brain_ML

class DogBrainIQN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size, num_quantiles=32):
        super(DogBrainIQN, self).__init__()
        self.num_quantiles = num_quantiles
        self.input_size = input_size
        self.output_size = output_size
        self.hidden_size = hidden_size  # Add this line

        self.state_net = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU()
        )

        self.quantile_net = nn.Sequential(
            nn.Linear(1, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU()
        )

        self.merge_net = nn.Sequential(
            nn.Linear(hidden_size * 2, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, output_size)
        )

    def forward(self, state, tau):
        # Ensure state has the correct shape
        if state.numel() % self.input_size != 0:
            print(f"Skipping step due to shape mismatch: {state.shape}")
            return None
        
        state = state.view(-1, self.input_size)
        # Print shape for debugging
        print(f"State shape: {state.shape}, Tau shape: {tau.shape}")
        state_features = self.state_net(state)
        
        # Reshape tau to match the batch size of state
        batch_size = state.size(0)
        tau = tau.view(batch_size, -1, 1)
        tau_features = self.quantile_net(tau.view(-1, 1)).view(batch_size, -1, self.hidden_size)
        
        merged_features = torch.cat([state_features.unsqueeze(1).expand(-1, tau.size(1), -1), tau_features], dim=-1)
        return self.merge_net(merged_features.view(-1, merged_features.size(-1)))


class DogBrain(Brain_ML):
    def __init__(self, body, hidden_size=128, num_quantiles=32):
        super().__init__(body)
        self.state_size = self.calculate_state_size()
        self.action_size = self.calculate_action_size()
        self.num_quantiles = num_quantiles
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.model = DogBrainIQN(self.state_size, hidden_size, self.action_size, num_quantiles)
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.001)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def calculate_state_size(self):
        # Local velocity of the body (3)
        # Local velocity of joints (3 * number of joints)
        # Body world position (3)
        # Body acceleration (3)
        # Body velocity (3)
        # Two values for input order (2)
        # Joint positions (3 * number of joints)
        # return 3 + 3 * len(self.body.joints) + 3 + 3 + 3 + 2 + 3 * len(self.body.joints)
        return 24

    def calculate_action_size(self):
        # One angle for each joint
        return len(self.body.joints)

    def get_state(self):
        state = []
        # Local velocity of the body
        state.extend(self.body.local_velocity)
        # Local velocity of joints
        for joint in self.body.joints:
            state.extend(joint.shapeB.velocity)
        # Body world position
        state.extend(self.body.pos)
        # Body acceleration (you need to implement this in the Body class)
        state.extend(self.body.local_acceleration)
        # Body velocity
        state.extend(self.body.velocity)
        # Two values for input order (you need to implement this)
        state.extend(self.body.input_order)
        print(f"State size: {len(state)}")
        return np.array(state)

    def perform_action(self, action):
        for i, joint in enumerate(self.body.joints):
            joint.targetAngle = action[i]
            joint.move()

    def control_robot(self, state):
        if random.random() <= self.epsilon:
            return np.random.uniform(-np.pi, np.pi, self.action_size)
        state = torch.tensor(state, dtype=torch.float32).unsqueeze(0)
        tau = torch.rand(1, self.num_quantiles, 1)
        q_values = self.model(state.repeat(self.num_quantiles, 1), tau).mean(dim=0)
        return q_values.detach().numpy()
        
    def replay(self, batch_size):
        if len(self.memory) < batch_size:
            return
        
        batch = random.sample(self.memory, batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)
        
        states = torch.tensor(states, dtype=torch.float32)
        actions = torch.tensor(actions, dtype=torch.long)  # Ensure actions are of type long
        rewards = torch.tensor(rewards, dtype=torch.float32)
        next_states = torch.tensor(next_states, dtype=torch.float32)
        dones = torch.tensor(dones, dtype=torch.float32)

        print(f"States shape: {states.shape}")
        
        tau = torch.rand(batch_size, self.num_quantiles, 1)
        current_q = self.model(states, tau)
        print(f"Action shape: {actions.shape}, Num_quantiles: {self.num_quantiles}, current_q shape: {current_q.shape}")
        
        # Reshape actions to match the dimensions of current_q
        actions = actions.unsqueeze(1).expand(-1, self.num_quantiles, -1).reshape(-1, actions.size(-1))
        print(f'current_q shape: {current_q.shape}, actions shape: {actions.shape}')
        current_q = current_q.gather(1, actions)
        
        with torch.no_grad():
            next_q = self.model(next_states, tau).max(2)[0]
            target_q = rewards.unsqueeze(1) + self.gamma * next_q * (1 - dones.unsqueeze(1))
        
        loss = nn.functional.huber_loss(current_q, target_q)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
    
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)
        
    def train(self, num_episodes, max_steps_per_episode, batch_size):
        for episode in range(num_episodes):
            self.body.context.refresh()
            self.body.refresh()
            state = self.get_state()
            total_reward = 0
            done = False
            step = 0

            while not done and step < max_steps_per_episode:
                action = self.control_robot(state)
                self.perform_action(action)

                self.body.context.refresh()
                self.body.refresh()
                self.control_latitude()

                next_state = self.get_state()
                print("next_state", next_state)
                reward = self.calculate_reward(state, action, next_state)
                done = self.is_episode_done(next_state)

                self.remember(state, action, reward, next_state, done)
                state = next_state
                total_reward += reward
                step += 1

                self.replay(batch_size)

                #self.body.plotRobot.refresh_plot()
                time.sleep(0.01)  # Adjust this value to control the simulation speed

            print(f"Episode: {episode + 1}, Total Reward: {total_reward}, Steps: {step}, Epsilon: {self.epsilon}")

    def calculate_reward(self, state, action, next_state):
        # Implement reward calculation based on the dog's performance
        # For example, reward forward movement and penalize instability
        forward_movement = next_state[0] - state[0]  # Assuming the first state component represents forward position
        stability = -np.sum(np.abs(next_state[1::2]))  # Penalize high velocities in joints
        return forward_movement + 0.1 * stability

    def is_episode_done(self, state):
        # Implement logic to determine if the episode should end
        # For example, end if the dog falls (body height below a threshold) or reaches a goal
        body_height = state[2::6].mean()  # Assuming every 3rd component of each arm represents height
        return body_height < 0.5  # End episode if average body height is below 0.5

