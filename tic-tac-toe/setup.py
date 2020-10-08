import numpy as np
import pickle
from constants import BOARD_ROWS, BOARD_COLUMNS


class State:
    def __init__(self, player_one, player_two):
        self.board = np.zeros((BOARD_ROWS, BOARD_COLUMNS))
        self.player_one = player_one
        self.player_two = player_two
        self.is_end = False
        self.board_hash = None
        self.player_symbol = 1

    def get_board(self):
        return self.board



