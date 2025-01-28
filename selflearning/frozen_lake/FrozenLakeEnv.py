import gymnasium as gym
import time

env = gym.make('FrozenLake-v1', desc=None, map_name="4x4", is_slippery=True, render_mode="human")

observation, info = env.reset(seed=42)
time.sleep(5)
env.close()


