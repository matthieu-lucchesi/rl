


# Lunar Landing
## Action Space
* 0: do nothing
* 1: fire left orientation engine
* 2: fire main engine
* 3: fire right orientation engine

## Observation Space
The state is an 8-dimensional vector: the coordinates of the lander in x & y, its linear velocities in x & y, its angle, its angular velocity, and two booleans that represent whether each leg is in contact with the ground or not.

## Rewards
After every step a reward is granted. The total reward of an episode is the sum of the rewards for all the steps within that episode.

For each step, the reward:
* is increased/decreased the closer/further the lander is to the landing pad.
* is increased/decreased the slower/faster the lander is moving.
* is decreased the more the lander is tilted (angle not horizontal).
* is increased by 10 points for each leg that is in contact with the ground.
* is decreased by 0.03 points each frame a side engine is firing.
* is decreased by 0.3 points each frame the main engine is firing.

The episode receive an additional reward of -100 or +100 points for crashing or landing safely respectively.

An episode is considered a solution if it scores at least 200 points.

## Agents
Not yet...

# TicTacToe game

## Action  Space
Agent can play in nine cells

## Observation Space
The state is the grid, 9 digit with 0 for empty cell, -1 for 'O' and 1 for 'X'. 'X' begins.

## Rewards
We are testing two modes. In the first one, the agent needs to learn the rules and is free to play in every cell. When choosing a non-empty cell, it ends the game and get a reward of -5.
Reward of .1 if choosing a valid moove (empty cell). 1 if winning the game. If the agent loose after a moove, we store the previous moove and the agent gets reward of -1.

### Deep Q-learning Neural Network
The Agent is a DQN agent, model is 3 layers MLP. A target network is also used to predict the next q-values.

$$
y_{target} = r + (1 - terminated) * self.gamma * -max_{a'}(Q_{target}(s'))
$$
With $Q_{target}$ a copy of Q that represents the target model, updated each $n$ episodes with the weight of the $Q$ model.

$$
Loss = MSE(Q(s), y_{target})
$$