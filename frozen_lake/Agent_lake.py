import random
from matplotlib import cm
import numpy as np
import matplotlib.pyplot as plt
import time


class AgentQ:
    def __init__(self, env, eps=0.8, T=1, lr=0.1, gamma=0.9, n_episode=100):
        self.env = env
        self.eps = eps
        self.T = T
        self.learning_rate = lr
        self.gamma = gamma
        self.n_episode = n_episode

        self.q = np.zeros(
            (int(env.observation_space.n), int(env.action_space.n)), dtype=np.float64
        )


    
    def get_action(self, obs, policy="epsilon_greedy", exploit_only=False):
        action = np.argmax(self.q[obs])
        if exploit_only:
            return action
        if policy is "epsilon_greedy" and random.random() < self.eps:  # Explore
            action = self.env.action_space.sample()
        elif policy is "softmax":
            state_values = self.q[obs]
            probabilities = softmax(state_values)
            action = np.random.choice(len(state_values), p=probabilities)

        return action

    def update(self, state, action, reward, new_state, new_action):
        print(f"{state=} {action=} {reward=} {new_state=} {new_action=}")
        print(self.q[state, action])
        self.q[state, action] = self.q[state, action] + self.learning_rate * (
            reward + self.gamma * self.q[new_state, new_action] - self.q[state, action]
        )
        print(self.q[state, action])

    def print_table(self):

        grid_size = int(np.sqrt(self.env.observation_space.n))
        fig, ax = plt.subplots(figsize=(6, 6))

        # Dessiner la grille
        for i in range(grid_size + 1):
            ax.plot([i, i], [0, grid_size], "k", lw=2)  # Lignes verticales
            ax.plot([0, grid_size], [i, i], "k", lw=2)  # Lignes horizontales

        # Ajouter les valeurs au centre de chaque côté
        for i in range(grid_size):
            for j in range(grid_size):
                left, bottom, right, top = self.q[i * grid_size + j]

                # Center cell (i, j)
                x, y = j + 0.5, grid_size - i - 0.5  # Top and bottom reversed

                cmap = cm.get_cmap("RdYlGn")  # Couleurs du rouge au vert
                norm = plt.Normalize(vmin=-1, vmax=1)  # Normalisation des valeurs

                left_color = cmap(norm(left))
                bottom_color = cmap(norm(bottom))
                right_color = cmap(norm(right))
                top_color = cmap(norm(top))

                fontsize = 8
                ax.text(
                    x - 0.3,
                    y,
                    f"{left:0.5f}",
                    ha="center",
                    va="center",
                    fontsize=fontsize,
                    color=left_color,
                    bbox=dict(facecolor="k", alpha=0.8, boxstyle="round,pad=0.1"),
                )  # left
                ax.text(
                    x,
                    y - 0.3,
                    f"{bottom:0.5f}",
                    ha="center",
                    va="center",
                    fontsize=fontsize,
                    color=bottom_color,
                    bbox=dict(facecolor="k", alpha=0.8, boxstyle="round,pad=0.1"),
                )  # bottom
                ax.text(
                    x + 0.3,
                    y,
                    f"{right:0.5f}",
                    ha="center",
                    va="center",
                    fontsize=fontsize,
                    color=right_color,
                    bbox=dict(facecolor="k", alpha=0.8, boxstyle="round,pad=0.1"),
                )  # right
                ax.text(
                    x,
                    y + 0.3,
                    f"{top:0.5f}",
                    ha="center",
                    va="center",
                    fontsize=fontsize,
                    color=top_color,
                    bbox=dict(facecolor="k", alpha=0.8, boxstyle="round,pad=0.1"),
                )  # top

        # Désactiver les axes
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xlim(0, grid_size)
        ax.set_ylim(0, grid_size)

        plt.title("Q table")
        manager = plt.get_current_fig_manager()
        try:
            manager.window.move(100, 100)  # Position (x=100, y=100)
        except AttributeError:
            pass  # Ignore si move() ne fonctionne pas

        plt.show(block=True)
        # plt.pause(0.75)
        # plt.close()
    
def softmax(values, t):
    exp_values = np.exp(values / t)
    return exp_values / np.sum(exp_values)