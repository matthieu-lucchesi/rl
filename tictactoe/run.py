import matplotlib.pyplot as plt
import utils
from TicTacToeEnv import TictactoeEnv
from Agent import Agent
import torch
from Agent import Brain
import torch
from time import time
import os
from Grid import Grid

start = time()
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
device = "cpu"
print(f"Using device: {device}")
batch_size = 32
update_rate = 10


ennemy = None
# ennemy = Agent(device=device, batch_size=batch_size, update_rate=update_rate, eps=0)
# ennemy.model.load_state_dict(torch.load(os.path.join("tictactoe", "agent4.pth"), weights_only=True))
# ennemy.model.eval()

# env = TictactoeEnv()
# agent = Agent(device=device, batch_size=batch_size, update_rate=update_rate, eps_decay=0.995, eps_min=0.05, lr=0.0001)
# episodes = 8000


# players, results, agent, times, losses = utils.train_agent(env, agent, ennemy, player_input=-1, episodes=episodes)
# print(sum([1 for player in players if player == 1 ]) / episodes *100, "% of the time playing X")
# print(sum(results) / len(results) * 100, "% of the time winning")
# # print(times)
# agent.save(os.path.join("tictactoe", "agent1"
#                         # + str(episodes)+"VS15000"
#                         ))

# print(f"Used {time()- start}s")

# plt.plot(losses)
# plt.xlabel("Training Steps")
# plt.ylabel("Loss")
# plt.show()

agent1 = Agent(device=device, batch_size=batch_size, update_rate=update_rate, eps=0)
agent1.model.load_state_dict(torch.load(os.path.join("tictactoe", "agent1.pth"), weights_only=True))
agent1.model.eval()

# agent2 = Agent(device=device, batch_size=batch_size, update_rate=update_rate, eps=0)
# agent2.model.load_state_dict(torch.load(os.path.join("tictactoe", "agent2.pth"), weights_only=True))
# agent2.model.eval()

# agent3 = Agent(device=device, batch_size=batch_size, update_rate=update_rate, eps=0)
# agent3.model.load_state_dict(torch.load(os.path.join("tictactoe", "agent3.pth"), weights_only=True))
# agent3.model.eval()

# agent4 = Agent(device=device, batch_size=batch_size, update_rate=update_rate, eps=0)
# agent4.model.load_state_dict(torch.load(os.path.join("tictactoe", "agent4.pth"), weights_only=True))
# agent4.model.eval()

# agent5 = Agent(device=device, batch_size=batch_size, update_rate=update_rate, eps=0)
# agent5.model.load_state_dict(torch.load(os.path.join("tictactoe", "agent5.pth"), weights_only=True))
# agent5.model.eval()
grid = [
    1,0,1,
    -1,0,0,
    0,0,0
    ]

print(
    agent1.get_action(grid),
#     agent2.get_action(grid),
#     agent3.get_action(grid),
#     agent4.get_action(grid),
#     agent5.get_action(grid),
    )
utils.play_website(Grid(), agent1, 10)      