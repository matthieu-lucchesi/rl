import os
import random
import time

import numpy as np
import streamlit as st
import torch
from tqdm import tqdm
from Agent import Agent


def train_agent(env, agent, ennemy=None, player_input=-1, episodes=1000, save_path="toto"):
    results = []
    players = []
    times = []
    losses= []
    evolutions = []
    for ep in tqdm(range(1, episodes + 1)):
        start_time = time.time()
        state, terminated = env.reset()
        agent_state = None
        rewards = []
        player = player_input
        if player_input == -1:
            player = random.choice([1,2])
        players.append(player)
        opponent = player % 2 + 1
        while not terminated:
            if env.get_turn() == player:  # Agent to play
                agent_state = state.copy()
                action = agent.get_action(state, p=False)
                next_state, reward, terminated = env.step(player, action)
                agent_next_state = next_state.copy()
                if terminated: 
                    agent.store_exp(agent_state, action, reward, agent_next_state, terminated)  # Store exp Agent ending the game
                    rewards.append(reward)
                state = next_state.copy()
            else:  # Opponent to play
                opponent_action = random.choice([i for i in range(len(env.grid)) if env.grid[i] == 0])
                if ennemy is not None:  # and random.random() < 0.5:
                    with torch.no_grad():
                        opponent_action = ennemy.get_action(state)
                    if state[opponent_action] != 0:
                        opponent_action = np.random.choice([i for i in range(9) if state[i] == 0])
                    
                opponent_next_state, opponent_reward, terminated = env.step(opponent, opponent_action)
                state = opponent_next_state.copy()
                if agent_state is not None:
                    if terminated and opponent_reward == 1:  # Opponent won
                        reward = -1 
                    else:  # Agent didn't loose so he played a regular moove
                        reward = 0.1
                    agent.store_exp(agent_state, action, reward, agent_next_state, terminated)  
                    rewards.append(reward)
        times.append(round(time.time() - start_time, 2))
        results.append(reward)
        if len(agent.memory) > agent.batch_size and ep % agent.update_rate == 0:  # Train every update_rate episodes
            loss = agent.train_()  
            losses.append(loss) 
            agent.update_eps()
            if ep % (4 * agent.update_rate) == 0:
                agent.target_model.load_state_dict(agent.model.state_dict())
                agent.target_model.eval()
                if ep % (1000 * agent.update_rate) == 0:
                    print(f"{ep=}")
                    new_ennemy = agent.evolution(ennemy, save_path=save_path)
                    if new_ennemy is not ennemy:  # Si l'adversaire change, on stocke l'évolution
                        ennemy = new_ennemy
                        evolutions.append(ep)

    return players, results, agent, times, losses


def compare_2_agent(env, device, bs, update_rate, agent1_title: str, agent2_title: str | None, games: int = 100):
    agent1 = Agent(device=device, batch_size=bs, update_rate=update_rate, eps=0)
    agent1.model.load_state_dict(torch.load(agent1_title, weights_only=True))
    agent1.model.eval()
    if agent2_title is None:
        agent2 = Agent(device=device, batch_size=bs, update_rate=update_rate, eps=1)  # Random with eps = 1
        agent2.model.load_state_dict(torch.load(agent1_title, weights_only=True))
        agent2.model.eval()
        agent2_title = "RandomAgent"
    else:
        agent2 = Agent(device=device, batch_size=bs, update_rate=update_rate, eps=0)
        agent2.model.load_state_dict(torch.load(agent2_title, weights_only=True))
        agent2.model.eval()
    results = []
    players = []
    for _ in range(1, games + 1):
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
    print(f"Results of {os.path.basename(agent1_title)} VS {agent2_title} over {games} games:")
    print(f"Played X {sum([1 for p in players if p == 1]) / games * 100:.2f}% of the time")
    print(f"Wins : {wins / len(results) * 100:.2f}%")
    print(f"Draws : {draws / len(results) * 100:.2f}%")
    print(f"Loss : {defeats / len(results) * 100:.2f}%")


def init_st(player:int = 1):
    """Init the session_state values."""
    st.title("Morpion avec Streamlit")

    if "board" not in st.session_state:
        st.session_state.board = np.array([' ' for _ in range (9)])

    if "game_ended" not in st.session_state:
        st.session_state.game_ended = False

    if "player" not in st.session_state:
        st.session_state.player = player 

    if "agent_score" not in st.session_state:
        st.session_state.agent_score = 0

    if "player_score" not in st.session_state:
        st.session_state.player_score = 0


def css_st():
    return st.markdown(
        """
        <style> 
        [class*="grid"] {
            display: flex;
            flex-wrap: wrap; 
            justify-content: center; 
            width: 100%; 
            max-width: 500px; 
            margin: 0; 
            opacity: 0.4;
            background-color: lightgreen !important;
            padding: 1%; /* left and right */
            gap: 0%;
        }
        [class*="grid"] > [class*="HorizontalBlock"] {
            gap: 0% !important;
            margin: 0 !important;
            padding: 0 !important;
        }


        [class*="cell"] {
            flex: 1 1 calc(33.33% - 1%); 
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 2%  /* top and bottom*/;
        }

        [class*="cell"] button {
            width: 100%;
            aspect-ratio: 1 / 1;
            background-color: #4CAF50 !important; 
            line-height: 1 !important;   
            border-radius: 5px;
            border: 3px solid black !important;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.2) !important;
            transition: 0.2s;
            display: flex !important;
        }


        [class*="cell"] button:not(:disabled):hover {
            background-color: darkgreen !important; 
            transform: scale(1.05); 
        }

        [class*="cell"] button:disabled{  /*After clicked*/
            color: black !important;
            font-size-adjust: 3 !important;
            font-weight: bold !important;
        }
        

        [class*="buttons"] {
            display: flex;
            justify-content: center; 
            align-items: center; 
        }

        [class*="_button"] button {
            background-color: grey !important;
            color: white !important; 
            font-size: 24px !important;
            padding: 10px 20px !important;
            border-radius: 5px; 
            border: 2px solid black !important; 
            transition: 0.2s;
            min-width: 150px !important;  
            height: 60px !important;      
            white-space: nowrap !important;
        }

        [class*="_button"] button:not(:disabled):hover {
            background-color: darkgrey !important; 
            transform: scale(1.1); 
        }

        </style>
        """,
        unsafe_allow_html=True
    )


def launch_agent(agent_path):
    """Load agent from path."""
    agent = Agent(eps=0)
    if "tictactoe" not in os.getcwd() and "app" not in os.getcwd():
        agent_path = os.path.join("tictactoe", agent_path)
    agent.model.load_state_dict(torch.load(agent_path, weights_only=True))
    agent.model.eval()
    return agent


def play_agent(agent, grid):
    """Play a move and random if can't predict."""
    chars = {'O': -1, ' ': 0, 'X': 1}
    grid = torch.FloatTensor([chars[ele] for ele in grid ], device=agent.device)
    action = agent.get_action(grid)
    if grid[action] != ' ':
        action = random.choice([i for i in range(len(grid)) if grid[i] == 0])
    return action


def check_winner(grid):
    indices = [[0,1,2], [3,4,5], [6,7,8], [0,3,6], [1,4,7], [2,5,8], [0, 4, 8], [2,4,6]]
    res = 0
    if any(np.array_equal(grid[vals], ['X','X','X']) for vals in indices):
        res = 1
    if any(np.array_equal(grid[vals], ['O','O','O']) for vals in indices):
        res = 2
    if res == 0 and all(cell != ' ' for cell in grid):
        res = 3  # Tie
    return res


def check_winner_st():
    """Check if there is a winner"""
    winner = check_winner(st.session_state.board)
    if winner and not st.session_state.game_ended:
        if winner == 3:
            st.session_state.winner_message = "Well played, it's a tie !"
        elif winner == st.session_state.player:
            st.session_state.player_score += 1
            st.session_state.winner_message = "Player won !"
        else:
            st.session_state.agent_score += 1
            st.session_state.winner_message = "Agent won !"
        st.session_state.game_ended = True


def board_st(agent: Agent):

    if st.session_state.game_ended:
        st.success(st.session_state.winner_message)
    col1, col2 = st.columns([3, 1], vertical_alignment="center")
    with st.container():
        with col1:
            with st.container(key="grid"):
                for r in range(3):
                    col = st.columns(3)
                    for c in range(3):
                        index = c + 3 * r
                        with col[c]:
                            disabled = st.session_state.board[index] != ' ' or st.session_state.game_ended
                            if st.session_state.player == 2 and all(cell == ' ' for cell in st.session_state.board):
                                action = play_agent(agent, st.session_state.board)
                                st.session_state.board[action] = 'X'

                            if st.button(st.session_state.board[index], key=f"cell-{index}", disabled=disabled):
                                if st.session_state.board[index] == ' ' and not st.session_state.game_ended:
                                    st.session_state.board[index] = 'X' if st.session_state.player == 1 else 'O'
                                    check_winner_st()
                                if not st.session_state.game_ended:
                                    action = play_agent(agent, st.session_state.board)
                                    st.session_state.board[action] = 'O' if st.session_state.player == 1 else 'X'
                                    check_winner_st()
                                st.rerun()
        with col2:
            st.subheader("Agent", divider="grey")
            st.markdown(f"<h1 style='text-align: center; font-size: 36px;'>{st.session_state.agent_score}</h1>", unsafe_allow_html=True)
            st.subheader("Player", divider="grey")
            st.markdown(f"<h1 style='text-align: center; font-size: 36px;'>{st.session_state.player_score}</h1>", unsafe_allow_html=True)


def play_reset_st():
    col1, col2 = st.columns([3, 1], vertical_alignment="center")
    with col1:
        with st.container(key="buttons"):
            col1, col2 = st.columns(2, gap="large")
            with col1:
                if st.button("Play", key="Play_button"):
                    st.session_state.board = np.array([' ' for _ in range(9)])
                    st.session_state.player = 3 - st.session_state.player
                    st.session_state.game_ended = False
                    st.rerun()  
            with col2:
                if st.button("Reset", key="Reset_button"):
                    st.session_state.agent_score = 0
                    st.session_state.player_score = 0
                    st.rerun()  