# Frozen Lake
## Action Space
* 0: Left
* 1: Down
* 2: Right
* 3: Up

## Observation Space
The state is an id of where we are on the 4x4 map.

## Rewards
The reward depends on where we are on the lake and where we decide to go.
Reward is:
* -1 if hitting a lake. Ending the episode
* -0.1 if Staying at the same place after action (wall hitting).
* +1 if hitting the present. Ending the episode

## Agents policies (Explore VS Exploit)
Varisous policies are tried here:
* ***$\epsilon$-greedy***: explore with a probability of $\epsilon$, otherwise exploit.
* ***$\epsilon$-greedy decaying***: explore with a probability of $\epsilon$, otherwise exploit. After each episode we reduce the value of $\epsilon$.
* ***SoftMax***: Apply softmax function to the q-table. High state action value => High probability of picking this action in this state.
$$
P(a) = \frac{e^{Q(s,a)/T}}{\sum_{a'} e^{Q(s,a')/T}}.
$$
* ***UCB*** *(Upper Confidence Bound)*: Reward new exploration.
$$
Q'(s, a) = Q(s, a) + c \sqrt{\frac{\log(N(s))}{N(s, a) + 1}}.
$$

## Results

We run the tests using a *json* file. Results are available in *results/*. We can see plots for each agent and two json files:
* The record of all episodes of every agent.
* The score of the agents we wanted to test, ordered by the first episode to reach a positive cumulative mean. We can also observe the mean of the ration episode reward / episode length.

## What comes next

Check repeatability of an agent.