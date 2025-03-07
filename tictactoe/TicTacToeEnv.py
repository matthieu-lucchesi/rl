"""Env to train faster than playing on the website"""
import numpy as np


class TictactoeEnv:
    def __init__(self):
        self.grid = np.zeros((9))
        self.terminated = False

    def get_turn(self):
        return sum(self.grid**2) %2 + 1
    
    def step(self, player, action):
        # X to play (player = 1 else player = 2)
        if self.grid[action] != 0:  # Played in bad position
            reward = -5
            terminated = True
        else:
            reward = .1
            terminated = False
            self.grid[action] = player if player == 1 else -1  # 1 for X and -1 for O
            indices = [[0,1,2], [3,4,5], [6,7,8], [0,3,6], [1,4,7], [2,5,8], [0, 4, 8], [2,4,6]]
            if any(np.abs(self.grid[vals].sum()) == 3 for vals in indices):
                terminated = True
                reward = 1  # player won !
            if sum(self.grid**2) == 9:  # Grid is full
                terminated = True
        return self.grid.copy(), reward, terminated

    
    def reset(self):
        self.grid = np.zeros((9))
        self.terminated = False
        return self.grid.copy(), self.terminated
    
    def __str__(self):
        ligne_sep = "\n" + "-" * 11 + "\n"
        new_vals = []
        for val in self.grid:
            if val == 1:
                char = 'X'
            elif val == -1:
                char = 'O'
            else:
                char = ' '
            new_vals.append(char)
        lignes = [
            f" {new_vals[0]} | {new_vals[1]} | {new_vals[2]} ",
            f" {new_vals[3]} | {new_vals[4]} | {new_vals[5]} ",
            f" {new_vals[6]} | {new_vals[7]} | {new_vals[8]} ",
        ]
        return ligne_sep.join(lignes)