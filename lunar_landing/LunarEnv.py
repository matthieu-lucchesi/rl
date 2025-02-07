import gymnasium as gym
import time


env = gym.make(
    "LunarLander-v3",
    render_mode="human",
    max_episode_steps=2000,
    continuous=False,
    gravity=-9.81,
    enable_wind=False,
)
observation, info = env.reset(seed=42)
episode_over = False
while not episode_over:
    action = env.action_space.sample()
    # action = 2 if i % 3 == 0 else 0  # agent policy that uses the observation and info
    observation, reward, terminated, truncated, info = env.step(action)
    # Observation[8]: [coordinates x, y, linear velocities x, y,
    # angle, angular velocity, 2 booleans leg in contact with ground]
    episode_over = terminated or truncated

env.close()
