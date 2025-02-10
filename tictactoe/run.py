import time

from utils import click_img, get_position_from_img


click_img("opera")

print(f"selected_X at : {get_position_from_img("selected_X", confidence=0.999)}")
print(f"selected_O at : {get_position_from_img("selected_O", confidence=0.999)}")
print(f"unselected_X at : {get_position_from_img("unselected_X", confidence=.99)}")
print(f"unselected_O at : {get_position_from_img("unselected_O", confidence=.99)}")


click_img("opera", confidence=.5)
 
# grid = detect_grid()


# pyautogui.hotkey("alt", "tab")
