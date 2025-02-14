import time
import random

import numpy as np
from utils import click_img, start_game, check_winner_after_cpu
from Grid import Grid
import pyautogui

# click_img("opera", confidence=.5)
# click_img("reset_game")
# # print(check_winner_cpu())


# print(1/0)
agent_wins = []
player_log = []

grid = Grid()
player = grid.init_game(player=None, first_init=True)

games = 3
for game_id in range(games):
    ending = False
    player_log.append(player)
    time.sleep(.5)
    grid.update_grid()
    print(grid)
    while not ending:
        ending, winner = grid.play(player, index=-1)  # Agent learning this index !
        print("played:")
        # time.sleep(.2)
        # grid.update_grid()
        print(grid, "\n")
        if ending or winner:
            break
        print("cpu played:")
        time.sleep(1)
        ending, winner = grid.update_grid()
        print(grid, "\n")
    print("WINNER ", winner)
    agent_wins.append(0 if winner == 0 else 1 if winner == player else -1)
    time.sleep(1)
    if game_id != games - 1:
        player = grid.reset()
    else:
        click_img("reset_game")

click_img("opera", confidence=.5)
print(player_log)
print(agent_wins)
# pyautogui.hotkey("alt", "tab")



