import numpy as np
import pyautogui 
import time
import os
import pyautogui
import subprocess
import random


def get_path(wsl_path):
    wsl_path = "./tictactoe/images/" + wsl_path + ".png"
    return wsl_path
    # try:
    #     win_path = subprocess.check_output(["wslpath", "-w", wsl_path]).decode("utf-8").strip()
    #     return win_path
    # except Exception as e:
    #     print(f"Erreur lors de la conversion du chemin : {e}")
    #     return wsl_path  

def get_position_from_img(img, confidence=.9, prnt=False):
    try:
        return pyautogui.locateOnScreen(get_path(img), confidence=confidence)
    except Exception as e:
        if prnt:
            print(f"Failed to locate {img} : {e}")
        return False 
    
def get_center_from_img(img, confidence=.9, prnt=False):
    try:
        center = pyautogui.locateCenterOnScreen(get_path(img), confidence=confidence)
        return int(center[0]), int(center[1])
    except Exception as e:
        if prnt:
            print(f"Failed to locate {img} : {e}")
        return False 

def get_positions_from_img(img, confidence=.9, prnt=False):
    try:
        positions = pyautogui.locateAllOnScreen(get_path(img), confidence=confidence)
        return list(positions)
        # return [pyautogui.center(position) for position in positions]
    except Exception as e:
        if prnt:
            print(f"Failed to locate {img} : {e}")
        return False 
    
def click_pos(pos, wait=0.2):
    """Go to pos in .25s then click then wait .2s."""
    if len(pos) == 4:
        pos = pyautogui.center(pos)
    pyautogui.moveTo(pos, duration=0.25)
    pyautogui.click()
    time.sleep(wait)

def click_img(img, confidence=0.9, wait=0.2):
    """Go to center of img in .25s then click then wait .2s."""
    pos_img = get_center_from_img(img, confidence=confidence)
    if pos_img:
        click_pos(pos_img, wait)
    return pos_img

def go_to_img(img, confidence=.9):
    pos_img = get_center_from_img(img, confidence=confidence)
    if pos_img:
        pyautogui.moveTo(pos_img)
    return pos_img

def pick_color(player: int=None):
    """Select player:
        - X is 1
        - O is 2
        - random"""
    if player is None:
        player = random.random()
    else:
        player /= 2

    # unselected_X = get_position_from_img("unselected_X", confidence=.999)
    # unselected_O = get_position_from_img("unselected_O", confidence=.999)
    if player <= 0.5:
        unselected_X = get_position_from_img("unselected_X", confidence=0.2, prnt=True)
        if unselected_X:
            click_img("unselected_X")
        return 1
    else:
        selected_X = get_center_from_img("selected_X", confidence=0.85, prnt=True)
        if selected_X:
            click_img("unselected_O")
        return 2
    
def group_cells(cells_pos: list):
    if not cells_pos:
        return []
    weight_test = cells_pos[0][2] // 2
    height_test = cells_pos[0][3] // 2
    grouped_cells_pos = []
    for pos in cells_pos:
        test = []
        for grouped_pos in grouped_cells_pos:
            test.append(abs(pos[0] - grouped_pos[0]) <= weight_test and abs(pos[1] - grouped_pos[1]) <= height_test)
        if any(test):
            continue
        grouped_cells_pos.append(pos)
    return grouped_cells_pos

def extract_cells():
    def detect_gird():
        left, top, _, height = get_position_from_img("top_grid", confidence=.9)
        top = top + height
        right, bottom = get_center_from_img("right_grid", confidence=0.99)
        width = right - left
        height = bottom - top
        grid = left, top, width, height
        return grid
    
    grid = detect_gird()
    cells = []
    width = grid[2] // 3
    height = grid[3] // 3
    for row in range(3):
        for col in range(3):
            left, top = grid[0] + col * width, grid[1] + row * height
            cells.append((left, top, width, height)) 
    
    return cells
    
def is_point_in_box(point, box):
    x, y = point
    x_min, y_min, w_max, h_max = box
    x_max = x_min + w_max
    y_max = y_min + h_max
    return x_min <= x <= x_max and y_min <= y <= y_max

def convert_cell_to_position(cells, positions):
    return [[is_point_in_box(pyautogui.center(cell), position) for position in positions].index(1) for cell in cells]


def detect_cells(positions):
    # print(f"{positions=}")
    empty_cells = group_cells(get_positions_from_img("empty_cell", confidence=0.8))
    # print(f"{empty_cells=}")
    empty_cells_index = convert_cell_to_position(empty_cells, positions)
    # print(f"{empty_cells_index=}")
    cells_X = group_cells(get_positions_from_img("cell_X", confidence=0.6))
    # print(f"{cells_X=}")
    cells_X_index = convert_cell_to_position(cells_X, positions)
    # print(f"{cells_X_index=}")
    cells_O = group_cells(get_positions_from_img("cell_O", confidence=0.6))
    # print(f"{cells_O=}")
    cells_O_index = convert_cell_to_position(cells_O, positions)
    # print(f"{cells_O_index=}")
    assert len(empty_cells_index + cells_X_index+ cells_O_index) == 9, "Unable to read the grid"
    new_grid = np.zeros((9), dtype=int)
    new_grid[cells_X_index] = 1
    new_grid[cells_O_index] = -1
    return new_grid
    

def start_game(player: int=None, first_init: bool=False):
    if first_init:
        click_img("opera", wait=0.5)
    click_img("select_bot", wait=1)
    player = pick_color(player)
    click_img("play_button")
    return player

def reset(player):
    click_img("reset_game", wait=1)
    return start_game(player)

def check_winner_after_cpu():
    res = False, 0
    if get_center_from_img("result_tie", confidence=.9, prnt=False):
        print("result_tie")
        res = True, 0
    if get_center_from_img("result_X", confidence=.9, prnt=False):
        assert not res[0], "Bad results to read"
        print("result_X")
        res = True, 1
    if get_center_from_img("result_O", confidence=.9, prnt=False):
        assert not res[0], "Bad results to read"
        print("result_O")
        res = True, 2
    return res