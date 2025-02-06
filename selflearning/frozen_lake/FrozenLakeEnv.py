import gymnasium as gym
from Agent_lake import AgentQ
env = gym.make('FrozenLake-v1', desc=None, map_name="4x4", is_slippery=False, 
            #    render_mode="human"
               )

n_episode = 1000
agent = AgentQ(env, eps=0.2, lr= 0.1, gamma=0.9, n_episode=n_episode)
decay = 1

def custom_step(env, action, observation):
    obs, r, terminated, truncated, info = env.step(action)
    if r == 0:
        if terminated:
            r = -1 #Lac
        elif obs == observation:
            r = -0.01 #Don't move (hitting the wall)
        # else:
        #     r = -0.001 #Don-t loop
            # r=0
    return obs, r, terminated, truncated, info


for _ in range(n_episode):
    observation, info = env.reset(seed=42)
    # Observation: id of where agent is.
    episode_over = False
    while not episode_over:
        action = agent.get_action(observation)
        # 0: Move left --- 1: Move down --- 2: Move right --- 3: Move up
        new_observation, reward, terminated, truncated, info = custom_step(env, action, observation)
       
        best_action = agent.get_action(observation, exploit_only=True)
        agent.update(observation, action, reward, new_observation, best_action)
        
        observation = new_observation
        episode_over = terminated or truncated
        # if episode_over:
        #     print(f"Terminated: {terminated} --- Truncated: {truncated} --- Eps: {agent.eps}")
    agent.eps = agent.eps * decay
env.close()
agent.print_table()