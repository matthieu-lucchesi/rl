import time

from utils import click_img, start_game
from Grid import Grid


player = start_game()

print(player)
grid = Grid()
print(grid)
print(f"Player {grid.get_turn()} to play")
grid = grid.detect_gird()
print(grid)

click_img("opera", confidence=.5)
# grid = detect_grid()


# pyautogui.hotkey("alt", "tab")



