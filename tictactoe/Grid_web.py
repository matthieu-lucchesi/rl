import random
import numpy as np
from utils_web import click_img, click_pos, detect_cells, extract_cells, start_game

class Grid:
    def __init__(self):
        self.values = np.zeros(9, dtype=int)
        self.winner = 0
        self.pos = []

    def check_winner(self):
        indices = [[0,1,2], [3,4,5], [6,7,8], [0,3,6], [1,4,7], [2,5,8], [0, 4, 8], [2,4,6]]
        res = 0
        if any(np.array_equal(self.values[vals], [1,1,1]) for vals in indices):
            res = 1
        if any(np.array_equal(self.values[vals], [-1,-1,-1]) for vals in indices):
            res = 2
        self.winner = res
        return res
    
    def check_full(self):
        return np.count_nonzero(self.values) == 9
    
    def get_turn(self):
        return np.count_nonzero(self.values) % 2 + 1
    
    def update_grid(self):
        # ending, winner = check_winner_after_cpu()
        # if ending:
        #     print("ending after cpu")
        #     return ending, winner
        new_grid = detect_cells(self.pos)
        assert sum(new_grid**2) - sum(self.values**2) <= 1, "Too many values to update"
        self.values = new_grid
        if self.check_winner() or self.check_full():
            return True, self.winner
        else:  # Not ending
            return False, -1
    
    def play(self, player: int, index=-1):
        assert np.count_nonzero(self.values) < 9
        if index == -1:
            index = random.choice(list(zip(*np.where(self.values == 0))))[0]
        assert player == self.get_turn(), f"Player {self.get_turn()} to play."
        assert self.values[index] == 0, f"Cell {index} not empty"
        click_pos(self.pos[index])
        self.values[index] = (player - 1) * -2 + 1
        self.check_winner()
        return self.check_winner() or self.check_full(), self.winner
    
    def init_game(self, player: int = None, first_init: bool=False):
        player = start_game(player, first_init)
        self.pos = extract_cells()
        return player
    
    def reset(self, player:int = None):
        click_img("reset_game", confidence=0.8, wait=1)
        self.values = np.zeros(9, dtype=int)
        player = self.init_game(player)
        return player

    def __str__(self):
        ligne_sep = "\n" + "-" * 11 + "\n"
        new_vals = []
        for val in self.values:
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