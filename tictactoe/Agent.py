from collections import deque
import torch.nn as nn 
import torch
import random
import numpy as np
import os

class Brain(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(Brain, self).__init__()
        self.l1 = nn.Linear(input_size, hidden_size)
        self.l2 = nn.Linear(hidden_size, hidden_size)
        self.l3 = nn.Linear(hidden_size, output_size)

    def forward(self, input):
        x = torch.relu(self.l1(input))
        x = torch.relu(self.l2(x))
        x = self.l3(x)
        return x


class Agent:
    def __init__(self, eps=1.0, eps_min=0.01, eps_decay=0.9, gamma=0.9, lr=0.001, batch_size=64, memory_size=512, update_rate=50, device="cpu"):
        # self.player = player  # 1 or 2; X or O
        self.eps = eps
        self.eps_decay = eps_decay
        self.eps_min = eps_min
        self.gamma = gamma
        self.batch_size = batch_size
        self.device = device
        self.update_rate = update_rate


        # Model parameters
        self.model = Brain(9, 128, 9).to(device)
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=lr)
        self.loss = nn.MSELoss()

        self.memory = deque(maxlen=memory_size)


    def get_action(self, state: np.array):
        if random.random() < self.eps:
            return random.choice([i for i in range(len(state)) if state[i] == 0])
        else:
            state_tensor = torch.tensor(state, dtype=torch.float32, device=self.device).unsqueeze(0)
            q_values = self.model(state_tensor)
            mask = torch.tensor([ele == 0 for ele in state], device=self.device)
            q_values = q_values * mask  # bad if cell already taken 
            print(q_values)
            return torch.argmax(q_values).item()

    def update_eps(self):
        self.eps = max(self.eps * self.eps_decay, self.eps_min)

    def store_exp(self, s, a, r, ns, terminated):
        self.memory.append((s, a, r, ns, terminated))

    def train(self):
        batch = random.sample(self.memory, self.batch_size)
        states, actions, rewards, n_states, terminateds = zip(*batch)

        # Tensors
        states = torch.tensor(np.array(states), dtype=torch.float32, device=self.device)
        actions = torch.tensor(actions, dtype=torch.int64, device=self.device)
        rewards = torch.tensor(rewards, dtype=torch.float32, device=self.device)
        n_states = torch.tensor(np.array(n_states), dtype=torch.float32, device=self.device)
        terminateds = torch.tensor(terminateds, dtype=torch.float32, device=self.device)

        #loss
        ypred = self.model(states).gather(1, actions.unsqueeze(1)).squeeze(1)  # Select only values for actions made
        next_q_values = self.model(n_states).max(1)[0]  # Select max value for next state values
        ytarget = rewards + (1 - terminateds) * self.gamma * next_q_values  # (1 - terminated) : no reward when episode is over
        loss = self.loss(ypred, ytarget.detach())

        # Backpropagation
        self.model.train()
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        return loss.item()

    def save(self, name: str=None):
        title =  name if name is not None else "tictactoe_agent"
        title += ".pth"
        torch.save(self.model.state_dict(), title)
        print(f"Model saved '{title}'")
