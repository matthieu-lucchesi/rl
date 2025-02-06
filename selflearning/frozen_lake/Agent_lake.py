import random
from matplotlib import cm
import numpy as np
import matplotlib.pyplot as plt


class AgentQ:
    def __init__(self, env, eps, lr, gamma, n_episode):
        self.env = env
        self.eps = eps
        self.learning_rate = lr
        self.gamma = gamma
        self.n_episode = n_episode

        self.q = np.zeros(
            (int(env.observation_space.n), int(env.action_space.n)), dtype=np.float64
        )

    def get_action(self, obs, exploit_only=False):
        action = np.argmax(self.q[obs])
        if not exploit_only and random.random() < self.eps:  # Explore
            action = self.env.action_space.sample()
        return action

    def update(self, state, action, reward, new_state, new_action):
        self.q[state, action] = self.q[state, action] + self.learning_rate * (
            reward + self.gamma * self.q[new_state, new_action] - self.q[state, action]
        )

    # def epsilon_decay(self):
    #     self.eps = self.eps - (2 * self.eps - 1) / (2 * self.n_episode)
    #     return self.eps

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
                    f"{left:0.3f}",
                    ha="center",
                    va="center",
                    fontsize=fontsize,
                    color=left_color,
                    bbox=dict(facecolor="k", alpha=0.8, boxstyle="round,pad=0.1"),
                )  # left
                ax.text(
                    x,
                    y - 0.3,
                    f"{bottom:0.3f}",
                    ha="center",
                    va="center",
                    fontsize=fontsize,
                    color=bottom_color,
                    bbox=dict(facecolor="k", alpha=0.8, boxstyle="round,pad=0.1"),
                )  # bottom
                ax.text(
                    x + 0.3,
                    y,
                    f"{right:0.3f}",
                    ha="center",
                    va="center",
                    fontsize=fontsize,
                    color=right_color,
                    bbox=dict(facecolor="k", alpha=0.8, boxstyle="round,pad=0.1"),
                )  # right
                ax.text(
                    x,
                    y + 0.3,
                    f"{top:0.3f}",
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
        plt.show()
