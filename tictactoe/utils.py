import numpy as np
import pyautogui 
import time
import pyautogui
import random
import torch
from tqdm import tqdm
import copy

from Agent import Agent

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


def train_agent(env, agent, ennemy=None, player_input=-1, episodes=1000):
    results = []
    players = []
    times = []
    losses= []
    for ep in range(1, episodes + 1):
        start_time = time.time()
        state, terminated = env.reset()
        agent_state = None
        rewards = []
        player = player_input
        if player_input == -1:
            player = random.choice([1,2])
        players.append(player)
        opponent = player % 2 + 1
        # print("Agent is player: ", player)
        while not terminated:
            if env.get_turn() == player:  # Agent to play
                agent_state = state.copy()
                # print(state)
                action = agent.get_action(state)
                # print("Agent Choice is :", action)
                next_state, reward, terminated = env.step(player, action)
                agent_next_state = next_state.copy()
                if terminated: 
                    agent.store_exp(agent_state, action, reward, next_state, terminated)  # Store exp Agent ending the game
                state = next_state

            else:  # Opponent to play
                opponent_action = random.choice([i for i in range(len(env.grid)) if env.grid[i] == 0])
                if ennemy is not None:
                    opponent_action = ennemy.get_action(state)
                opponent_next_state, opponent_reward, opponent_terminated = env.step(opponent, opponent_action)
                reward = -opponent_reward  # Negative reward when agent is loosing
                if agent_state is not None:
                    agent.store_exp(agent_state, action, reward, agent_next_state, terminated)  # Store exp after opponent played to check reward
                state = opponent_next_state
                terminated = opponent_terminated
            
            rewards.append(reward)
            # print(env)
        times.append(round(time.time() - start_time, 2))
        results.append(reward)
        if ep > 25 and ep % agent.update_rate == 0:  # Train every update_rate episodes
            loss = agent.train()  
            losses.append(loss) 
            agent.update_eps()
            print(f"After ep {ep}: rewards of {sum(results[-agent.update_rate:]) / len(results[-agent.update_rate:]) * 100}%")
            # print(results[-agent.update_rate:])
            print(agent.eps)
    return players, results, agent, times, losses


def play_website(env, agent, games = 3):
    agent_wins = []
    player_log = []
    grid = env
    player = grid.init_game(player=None, first_init=True)
    for game_id in range(games):
        ending = False
        player_log.append(player)
        time.sleep(.5)
        grid.update_grid()
        print(grid)
        while not ending:
            print(grid.values)
            index = agent.get_action(grid.values)
            ending, winner = grid.play(player, index=index)  # Agent learning this index !
            print("played:")
            print(grid, "\n")
            if ending or winner:
                break
            time.sleep(1)
            print("cpu played:")
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


def compare_2_agent(env, device, bs, update_rate, agent1_title: str, agent2_title: str, games: int = 100):
    agent1 = Agent(device=device, batch_size=bs, update_rate=update_rate, eps=0)
    agent1.model.load_state_dict(torch.load(agent1_title, weights_only=True))
    agent1.model.eval()

    agent2 = Agent(device=device, batch_size=bs, update_rate=update_rate, eps=0)
    agent2.model.load_state_dict(torch.load(agent2_title, weights_only=True))
    agent2.model.eval()

    results = []
    players = []
    for ep in range(1, games + 1):
        state, terminated = env.reset()
        player = random.choice([1,2])
        players.append(player)
        opponent = player % 2 + 1
        while not terminated:
            if env.get_turn() == player:  # Agent to play
                # print(state)
                action = agent1.get_action(state)
                # print("Agent Choice is :", action)
                next_state, reward, terminated = env.step(player, action)
                state = next_state

            else:  # Opponent to play
                action = agent2.get_action(state)
                next_state, opponent_reward, terminated = env.step(opponent, action)
                reward = -opponent_reward 
                state = next_state
        results.append(reward)
    wins = np.count_nonzero([result == 1 for result in results])
    draws = np.count_nonzero([result == 0 for result in results])
    defeats = np.count_nonzero([result == -1 for result in results])
    assert wins + draws + defeats == games, "Wrong number of games played"
    print(f"After {games}, {agent1_title} won {wins} times, lost {defeats} times and made {draws} draws against {agent2_title}.")
    print(results)
