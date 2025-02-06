import gymnasium as gym
from Agent_lake import AgentQ
env = gym.make('FrozenLake-v1', desc=None, map_name="4x4", is_slippery=False, 
            #    render_mode="human"
               )

n_episode = 100
agent = AgentQ(env, eps=0.8, T=1, c=1, lr= 0.1, gamma=0.9, n_episode=n_episode)
decay = .95
policy = "softmax"
policy = "ucb"
policy = "epsilon_greedy"

def custom_step(env, agent, action, observation):
    obs, r, terminated, truncated, info = env.step(action)
    agent.add_record(observation, action)
    if r == 0:
        if terminated:
            r = -1 #Lac
        elif obs == observation:
            r = -0.1 #Don't move (hitting the wall)
        # else:
        #     r = -0.01 #Don-t loop
        #     # r=0
    return obs, r, terminated, truncated, info


for _ in range(n_episode):
    observation, info = env.reset(seed=42)
    # Observation: id of where agent is.
    episode_over = False
    while not episode_over:
        action = agent.get_action(observation, policy)
        # 0: Move left --- 1: Move down --- 2: Move right --- 3: Move up
        new_observation, reward, terminated, truncated, info = custom_step(env, agent, action, observation)
       
        best_action = agent.get_action(new_observation, exploit_only=True)
        agent.update(observation, action, reward, new_observation, best_action)
        
        observation = new_observation
        episode_over = terminated or truncated
    agent.eps = max(agent.eps * decay, 0.1)
    agent.T = max(agent.T * decay, 0.1)
env.close()
agent.print_table(agent.q)
agent.print_table(agent.record)
