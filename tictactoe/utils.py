import pyautogui 
import time
import os
import pyautogui
import subprocess

def get_path(wsl_path):
    wsl_path = "./tictactoe/images/" + wsl_path + ".png"
    return wsl_path
    # try:
    #     win_path = subprocess.check_output(["wslpath", "-w", wsl_path]).decode("utf-8").strip()
    #     return win_path
    # except Exception as e:
    #     print(f"Erreur lors de la conversion du chemin : {e}")
    #     return wsl_path  

def get_position_from_img(img, confidence=.9):
    try:
        return pyautogui.locateCenterOnScreen(get_path(img), confidence=confidence)
    except Exception as e:
        print(f"Failed to locate {img} : {e}")
        return False 

def click_img(img, confidence=0.9):
    pos_img = get_position_from_img(img, confidence=confidence)
    if pos_img:
        pyautogui.click(pos_img)
    return pos_img

def go_to_img(img, confidence=.9):
    pos_img = get_position_from_img(img, confidence=confidence)
    if pos_img:
        pyautogui.moveTo(pos_img)
    return pos_img

def pick_color():
    pyautogui

def start_game():
    click_img("opera")
    time.sleep(.5)
    click_img("select_bot")
    pick_color()
    click_img("play_button")

# def detect_grid():
#     """Return the grid coordinates"""

#     grid = list(pyautogui.locateAllOnScreen(win_image_path, confidence=0.8))
#     return grid

