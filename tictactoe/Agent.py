import copy
import random
# import os
from collections import deque

import numpy as np
import torch
import torch.nn as nn
from TicTacToeEnv import TictactoeEnv


class Brain(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(Brain, self).__init__()
        self.l1 = nn.Linear(input_size, hidden_size)
        self.l2 = nn.Linear(hidden_size, hidden_size)
        self.l3 = nn.Linear(hidden_size, hidden_size)
        self.l4 = nn.Linear(hidden_size, output_size)

    def forward(self, input):
        x = nn.functional.relu(self.l1(input))
        x = nn.functional.relu(self.l2(x))
        x = nn.functional.relu(self.l3(x))
        x = self.l4(x)
        return x


class Agent:
    def __init__(self, eps=1.0, eps_min=0.05, eps_decay=0.999, gamma=0.9, lr=0.001, batch_size=64, memory_size=4096, update_rate=500, device="cpu"):
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
        self.target_model = copy.deepcopy(self.model)
        self.target_model.eval()
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=lr)
        self.loss = nn.MSELoss()
        self.memory = deque(maxlen=memory_size)


    def get_action(self, state: np.array, p=False):
        if random.random() < self.eps:
            return random.randint(0,8)
        else:
            state_tensor = torch.tensor(state, dtype=torch.float32, device=self.device).unsqueeze(0)
            with torch.no_grad():
                q_values = self.model(state_tensor)
            # mask = torch.tensor([-100 if s != 0 else 0 for s in state], device=self.device)
            if p:
                print(state_tensor)
                print(q_values)
                
            return torch.argmax(q_values).item()

    def update_eps(self):
        self.eps = max(self.eps * self.eps_decay, self.eps_min)


    def store_exp(self, s, a, r, ns, terminated):
        self.memory.append((s, a, r, ns, terminated))
        # def pr(grid):
        #     ligne_sep = "\n" + "-" * 11 + "\n"
        #     new_vals = []
        #     for val in grid:
        #         if val == 1:
        #             char = 'X'
        #         elif val == -1:
        #             char = 'O'
        #         else:
        #             char = ' '
        #         new_vals.append(char)
        #     lignes = [
        #         f" {new_vals[0]} | {new_vals[1]} | {new_vals[2]} ",
        #         f" {new_vals[3]} | {new_vals[4]} | {new_vals[5]} ",
        #         f" {new_vals[6]} | {new_vals[7]} | {new_vals[8]} ",
        #     ]
        #     return ligne_sep.join(lignes)
        # print("STORING")
        # print(pr(s), a, r)
        # print(pr(ns), terminated, '\n\n\n')

    def train_(self):
        if len(self.memory) < self.batch_size:
            return  None

        self.model.train()
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
        with torch.no_grad():  # Ne pas backprop sur target_model
            next_q_values = -self.target_model(n_states).max(1)[0]  # Best action for the opponent 
        # next_q_values = self.target_model(n_states).min(1)[0]  # Select max value for next state values
        ytarget = rewards + (1 - terminateds) * self.gamma * next_q_values  # (1 - terminated) : no reward when episode is over
        loss = self.loss(ypred, ytarget.detach())

        # Backpropagation
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        return loss.item()

    def test_(self, opponent_path=None, opponent_model=None, games:int=100, p:bool = False):
        """
        Test the agent against opponent, can be a path to .pth model, default is random.
        returns : players, wins, draws, defeats, unplayed
        """
        self.model.eval()
        eps_before_test = self.eps
        self.eps = 0
        opponent = Agent(device=self.device, batch_size=self.batch_size, update_rate=self.update_rate, eps=0)
        
        if opponent_path is not None:
            opponent.model.load_state_dict(torch.load(opponent_path, weights_only=True))
        
        elif opponent_model is not None:
            opponent.model.load_state_dict(opponent_model.state_dict())
            opponent_path = "SavedAgent"

        else:
            opponent.eps=1  # Random with eps = 1
            opponent_path = "RandomAgent"
        opponent.model.eval()

        results = []
        players = []
        env = TictactoeEnv()
        for _ in range(games):
            state, terminated = env.reset()
            player = random.choice([1,2])
            players.append(player)
            opponent_id = player % 2 + 1
            while not terminated:
                if env.get_turn() == player:  # Agent to play
                    with torch.no_grad():
                        action = self.get_action(state)
                    next_state, reward, terminated = env.step(player, action)
                    state = next_state

                else:  # Opponent to play
                    with torch.no_grad():
                        action = opponent.get_action(state)
                    if state[action] != 0:
                        action = np.random.choice([i for i in range(9) if state[i] == 0])
                    next_state, opponent_reward, terminated = env.step(opponent_id, action)
                    reward = -opponent_reward 
                    state = next_state
                
            results.append(reward)
        wins = np.count_nonzero([result == 1 for result in results])
        draws = np.count_nonzero([abs(result) == 0.1 for result in results])
        defeats = np.count_nonzero([result == -1 for result in results])
        unplayed = np.count_nonzero([result == -5 for result in results])
        # print(results)
        assert wins + draws + defeats + unplayed == games, "Wrong number of games played"
        if p:
            print(f"Results of Agent VS {opponent_path} over {games} games:")
            print(f"Played X {sum([1 for p in players if p == 1]) / games * 100:.2f}% of the time")
            print(f"Wins : {wins / len(results) * 100:.2f}%")
            print(f"Draws : {draws / len(results) * 100:.2f}%")
            print(f"Loss : {defeats / len(results) * 100:.2f}%")
        self.eps = eps_before_test
        return players, wins, draws, defeats, unplayed

    def evolution(self, ennemy, save_path:str, games=100):
        _, wins, draws, defeats, unplayeds = self.test_(p=True, games=games)  # Against random
        if wins / games >= 0.25 and defeats / games <= 0.15 and unplayeds <= 0.05:
            _, wins, draws, defeats, unplayeds = self.test_(opponent_model=None if ennemy is None else ennemy.model, games=games)
            if defeats / games <= 0.15 and unplayeds / games <= 0.05:
                self.save(save_path)
                new_ennemy = copy.deepcopy(self)
                new_ennemy.model.load_state_dict(torch.load(save_path + ".pth", weights_only=True))  # Update ennemy
                new_ennemy.eps = max(self.eps_min * 3, self.eps * 0.5)
                print("\033[92m")
                print(
                    f"New evolution !\nAfter {games} games, Agent:"
                    f"\twins: {wins/games*100}%"
                    f"\tdraws: {draws/games*100}%"
                    f"\tdefeats: {defeats/games*100}%"
                    f"\tunplayeds: {unplayeds/games*100}%\n"
                    f"Agent will be now training against current agent with eps = {new_ennemy.eps}."
                    )
                print("\033[0m")
                return new_ennemy 
        return ennemy
    
    def save(self, name: str=None):
        title =  name if name is not None else "tictactoe_agent"
        title += ".pth"
        torch.save(self.model.state_dict(), title)
        print(f"Model saved '{title}'")

