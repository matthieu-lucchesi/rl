import utils
from TicTacToeEnv import TictactoeEnv
from Agent import Agent
import torch

import torch
from time import time

start = time()
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
device = "cpu"
print(f"Using device: {device}")
batch_size = 128
update_rate = 50


env = TictactoeEnv()
agent = Agent(device=device, batch_size=batch_size, update_rate=update_rate)
episodes = 100
players, results, agent, times = utils.train_agent(env, agent, player_input=-1, episodes=episodes)
print(sum([1 for player in players if player == 1 ]) / episodes *100, "% of the time playing X")
print(sum(results) / len(results) * 100, "% of the time winning")
# print(times)
agent.save(str(episodes))

env = TictactoeEnv()
agent = Agent(device=device, batch_size=batch_size, update_rate=update_rate)
episodes = 1000
players, results, agent, times = utils.train_agent(env, agent, player_input=-1, episodes=episodes)
print(sum([1 for player in players if player == 1 ]) / episodes *100, "% of the time playing X")
print(sum(results) / len(results) * 100, "% of the time winning")
# print(times)
agent.save(str(episodes))

env = TictactoeEnv()
agent = Agent(device=device, batch_size=batch_size, update_rate=update_rate)
episodes = 3000
players, results, agent, times = utils.train_agent(env, agent, player_input=-1, episodes=episodes)
print(sum([1 for player in players if player == 1 ]) / episodes *100, "% of the time playing X")
print(sum(results) / len(results) * 100, "% of the time winning")
# print(times)
agent.save(str(episodes))

print(f"Used {time()- start}s")