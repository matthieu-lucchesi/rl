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
batch_size = 256
update_rate = 50


ennemy = None
ennemy = Agent(device=device, batch_size=batch_size, update_rate=update_rate, eps=0)
ennemy.model.load_state_dict(torch.load(os.path.join("tictactoe", "c.pth"), weights_only=True))
ennemy.model.eval()

env = TictactoeEnv()
# agent = Agent(device=device, batch_size=batch_size, update_rate=update_rate, eps_decay=0.999, eps_min=0.1, lr=0.0001)
# episodes = 2_000_000

# players, results, agent, times, losses = utils.train_agent(env, agent, ennemy, player_input=-1, episodes=episodes)
# print(times)
print(f"Used {time()- start}s")
# agent.save(os.path.join("tictactoe", "c"
#                         # + str(episodes)+"VS15000"
#                         ))
# plt.plot(losses)
# plt.xlabel("Training Steps")
# plt.ylabel("Loss")
# plt.title("Évolution de la perte")
# plt.show()
# agent = Agent(device=device, batch_size=batch_size, update_rate=update_rate, eps=0)
# agent.model.load_state_dict(torch.load(os.path.join("tictactoe", "b.pth"), weights_only=True))
with torch.no_grad():
    print(ennemy.get_action(torch.Tensor([
        -1,0,-1,
        1,1,0,
        0,0,1
        ])))



# print(agent.model(torch.Tensor([-1,0,-1,0,0,0,0,1,1])))

# agent.test(opponent_path=None,#os.path.join("tictactoe", "a.pth"),
#     games=1000,
#     p=True
# )

# env = TictactoeEnv()
# agent = Agent(device=device, batch_size=batch_size, update_rate=update_rate, eps_decay=0.995, eps_min=0.05, lr=0.0001)
# episodes = 20_000

# players, results, agent, times, losses = utils.train_agent(env, agent, ennemy, player_input=-1, episodes=episodes)
# # print(times)
# agent.save(os.path.join("tictactoe", "agentrandom"
#                         # + str(episodes)+"VS15000"
#                         ))
# utils.compare_2_agent(
#     TictactoeEnv(),
#     device,
#     batch_size,
#     update_rate,
#     os.path.join("tictactoe", "agentrandom.pth"),
#     # os.path.join("tictactoe", "agentVSrandom.pth"),
#     None,
#     games=10000
# )





# print(f"Épsilon final : {agent.eps}")
# print(f"Joué en X {sum([1 for p in players if p == 1]) / episodes * 100:.2f}% du temps")
# print(f"Taux de victoire : {sum(results) / len(results) * 100:.2f}%")




# utils.compare_2_agent(
#     TictactoeEnv(),
#     device,
#     batch_size,
#     update_rate,
#     os.path.join("tictactoe", "agentTEST2.pth"),
#     # os.path.join("tictactoe", "agentVSrandom.pth"),
#     None,
#     games=10000
# )


# agent = Agent(device=device, batch_size=batch_size, update_rate=update_rate, eps=0)
# agent.model.load_state_dict(
#     torch.load(os.path.join("tictactoe", "agent2.pth"), weights_only=True)
# )
# agent.model.eval()

# utils.play_website(Grid(), agent, 5)
