import utils
import streamlit as st
import numpy as np


utils.init_st(player=1)
utils.css_st()
utils.check_winner_st()
agent = utils.launch_agent("c.pth")

utils.board_st(agent)
utils.play_reset_st()

