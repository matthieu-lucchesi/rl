import json
import gymnasium as gym
from Agent_lake import AgentQ
from tqdm import tqdm
from utils import custom_step, plots, save_results, score

max_length = 100
decay = 0.95
env = gym.make(
    "FrozenLake-v1",
    desc=None,
    map_name="4x4",
    is_slippery=False,
    max_episode_steps=max_length,
    # render_mode="human",
)

with open("test.json", "r") as file:
    agents_test = json.load(file)

score_agents = []
allrecord_results = []
print(f"Training of {len(agents_test)} agents.")
for agent_test in tqdm(agents_test):
    agent = AgentQ(env=env, **agent_test)
    agent_test["Title"] = "_".join(f"{k}-{v}" for k, v in agent_test.items())

    for _ in range(agent.n_episode):
        (observation, info), episode_over = agent.new_episode(env)
        while not episode_over:
            action = agent.get_action(observation)
            # 0: Move left --- 1: Move down --- 2: Move right --- 3: Move up
            new_observation, reward, terminated, truncated, info = custom_step(
                env, agent, action, observation
            )

            best_action = agent.get_action(new_observation, exploit_only=True)
            agent.update(observation, action, reward, new_observation, best_action)

            observation = new_observation
            episode_over = terminated or truncated
        agent.end_episode()
    allrecord_result = score(agent.episodes)
    allrecord_result["Agent"] = agent_test["Title"]
    allrecord_results.append(allrecord_result)
    score_agents.append(plots(allrecord_result.copy(), agent_test["Title"], save=True))

env.close()
print("Plots saved in frozen_lake/results/")
print(f"Results saved at {save_results(score_agents, allrecord_results)}")
