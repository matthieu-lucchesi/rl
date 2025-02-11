import cv2
import numpy as np
import pyautogui
from utils import get_positions_from_img, go_to_img, get_center_from_img, get_path, get_position_from_img

class Grid:
    def __init__(self):
        self.values = np.zeros((9), dtype=int)
        self.winner = 0

    def check_winner(self):
        indices = [[0,1,2], [3,4,5], [6,7,8], [0,3,6], [1,4,7], [2,5,8], [0, 4, 8], [2,4,6]]
        res = 0
        if any(self.values[vals] == [1,1,1] for vals in indices):
            res = 1
        if any(self.values[vals] == [-1,-1,-1] for vals in indices):
            res = 2
        self.winner = res
        return res
    
    def check_full(self):
        return np.count_nonzero(self.values) == 9
    
    def get_turn(self):
        return np.count_nonzero(self.values) // 2 + 1
    
    # def detect_grid(self):
    #     """Return the cell coordinates"""
    #     go_to_img("border")
    #     empty_cells = get_positions_from_img("empty_cell", confidence=0.8)
    #     print(f"{empty_cells=}")
    #     for pos in empty_cells:
    #         pyautogui.moveTo(pos, duration=.5)
    #     cells_O = get_positions_from_img("cell_O", confidence=0.9)
    #     print(f"{cells_O=}")
    #     cells_X = get_positions_from_img("cell_X", confidence=0.9)
    #     print(f"{cells_X=}")

    # def detect_grid(self):
    #     """Détecte la grille du morpion dans une capture d'écran."""
    #     img = pyautogui.screenshot()
    #     img = np.array(img)  # Convertir en tableau NumPy
    #     img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    #     # 📌 1. Charger l'image
    #     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #     blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    #     # 📌 2. Détection des bords avec Canny
    #     edges = cv2.Canny(blurred, 50, 150)

    #     # 📌 3. Détection des lignes avec HoughLinesP
    #     lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi/180, threshold=100, minLineLength=200, maxLineGap=20)

    #     if lines is None:
    #         print("❌ Aucune ligne détectée, vérifie l’image.")
    #         return None

    #     # 📌 4. Trouver les lignes verticales et horizontales
    #     vertical_lines = []
    #     horizontal_lines = []

    #     for line in lines:
    #         x1, y1, x2, y2 = line[0]
    #         if abs(x1 - x2) < 10:  # Lignes verticales
    #             vertical_lines.append((x1, y1, x2, y2))
    #         elif abs(y1 - y2) < 10:  # Lignes horizontales
    #             horizontal_lines.append((x1, y1, x2, y2))

    #     # 📌 5. Trouver les intersections des lignes (coins de la grille)
    #     vertical_lines = sorted(vertical_lines, key=lambda x: x[0])
    #     horizontal_lines = sorted(horizontal_lines, key=lambda x: x[1])

    #     if len(vertical_lines) < 3 or len(horizontal_lines) < 3:
    #         print("❌ Pas assez de lignes pour former une grille complète.")
    #         return None

    #     # 📌 6. Déterminer les coordonnées de la grille
    #     x_min = vertical_lines[0][0]
    #     x_max = vertical_lines[-1][0]
    #     y_min = horizontal_lines[0][1]
    #     y_max = horizontal_lines[-1][1]

    #     width = x_max - x_min
    #     height = y_max - y_min

    #     print(f"✅ Grille détectée : {x_min}, {y_min}, {width}x{height}")
    #     return (x_min, y_min, width, height)

    # def detect_grid_and_symbols(self, confidence=0.8):

        grid_position = self.detect_grid()
        if not grid_position:
            print("❌ Grille non trouvée.")
            return None

        x, y, w, h = grid_position  # Position et taille de la grille
        pyautogui.moveTo(x,y)
        import time
        time.sleep(1)
        print(f"✅ Grille détectée à {x}, {y}, {w}x{h}")

        cell_size = int(w) // 3  # Supposons une grille carrée
        grid = np.zeros((3, 3), dtype=int)

        for row in range(3):
            for col in range(3):
                cx, cy = x + col * cell_size, y + row * cell_size  # Coordonnées de la case

                # Capturer une image de la case avec PyAutoGUI
                region = (cx, cy, cell_size, cell_size)
                print(region)
                cell_img = pyautogui.screenshot(region=(int(cx), int(cy), cell_size, cell_size))

                # Convertir en image OpenCV (grayscale)
                cell_img = cv2.cvtColor(np.array(cell_img), cv2.COLOR_RGB2GRAY)

                # 📌 4. DÉTECTION DES "X" ET "O"
                def match_template(template, threshold=0.8):
                    template_img = cv2.imread(template, cv2.IMREAD_GRAYSCALE)
                    res = cv2.matchTemplate(cell_img, template_img, cv2.TM_CCOEFF_NORMED)
                    return np.max(res) >= threshold  # Retourne True si correspondance

                if match_template(get_path("cell_X")):
                    grid[row, col] = 1  # X détecté
                elif match_template(get_path("cell_O")):
                    grid[row, col] = -1  # O détecté
                else:
                    grid[row, col] = 0  # Case vide

        return grid
    
    def detect_gird(self):
        left_ = get_position_from_img("left_grid", confidence=0.99)
        right_ = get_position_from_img("right_grid", confidence=0.99)
        print(left_, right_)
        top = int(left_[1] + right_[1]) // 2
        left = int(left_[0] + left_[2] / 2)
        width = int(pyautogui.center(right_)[0] - pyautogui.center(left_)[0])
        height = int(left_[3] + right_[3]) // 2
        grid = left, top, width, height
        # pyautogui.moveTo(left, top, duration=1)
        # pyautogui.moveTo(left + width, top, duration=1)
        # pyautogui.moveTo(left + width, top + height, duration=1)
        # pyautogui.moveTo(left, top + height, duration=1)
        return grid

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