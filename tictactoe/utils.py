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
def get_position_from_img(img, confidence=.9, prnt=True):
    try:
        return pyautogui.locateOnScreen(get_path(img), confidence=confidence)
    except Exception as e:
        if print:
            print(f"Failed to locate {img} : {e}")
        return False 
def get_center_from_img(img, confidence=.9, prnt=True):
    try:
        return pyautogui.locateCenterOnScreen(get_path(img), confidence=confidence)
    except Exception as e:
        if print:
            print(f"Failed to locate {img} : {e}")
        return False 
def get_positions_from_img(img, confidence=.9, prnt=True):
    try:
        positions = pyautogui.locateAllOnScreen(get_path(img), confidence=confidence)
        return [pyautogui.center(position) for position in positions]
    except Exception as e:
        if print:
            print(f"Failed to locate {img} : {e}")
        return False 

def click_img(img, confidence=0.9, wait=0.2):
    pos_img = get_center_from_img(img, confidence=confidence)
    if pos_img:
        pyautogui.click(pos_img)
    time.sleep(wait)
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
    time.sleep(0.8)
    if player is None:
        player = random.random()
    else:
        player /= 2
    selected_X = get_center_from_img("selected_X", confidence=0.99, prnt=False)
    selected_O = get_center_from_img("selected_O", confidence=0.99, prnt=False)
    # unselected_X = get_position_from_img("unselected_X", confidence=.999)
    # unselected_O = get_position_from_img("unselected_O", confidence=.999)
    if player <= 0.5:
        if selected_O:
            click_img("unselected_X")
        return 1
    else:
        if selected_X:
            click_img("unselected_O")
        return 2
    
    
def start_game(player: int=None):
    click_img("opera")
    click_img("select_bot")
    player = pick_color(player)
    click_img("play_button")
    return player
