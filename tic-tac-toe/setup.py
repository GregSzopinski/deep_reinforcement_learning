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

    def get_hash(self):
        self.board_hash = str(self.board.reshape(BOARD_COLUMNS * BOARD_ROWS))
        return self.board_hash

    def winner(self):
        for i in BOARD_ROWS:
            if sum(self.board[i, :]) == 3:
                self.is_end = True
                return 1
            if sum(self.board[i, :]) == -3:
                self.is_end = True
                return -1

        for i in BOARD_COLUMNS:
            if sum(self.board[:, i]) == 3:
                self.is_end = True
                return 1
            if sum(self.board[:, i]) == -3:
                self.is_end = True
                return -1
        # diagonal
        if np.trace(self.board) == 3 or np.trace(np.fliplr(self.board)) == 3:
            self.is_end = True
            return 1
        # anti-diagonal
        if np.trace(self.board) == -3 or np.trace(np.fliplr(self.board)) == -3:
            self.is_end = True
            return -1

        # tie - no available positions
        if len(self.available_positions()) == 0:
            self.is_end = True
            return 0
        self.is_end = False
        return None

    def available_positions(self):
        positions = []
        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLUMNS):
                if self.board[i, j] == 0:
                    positions.append((i, j))
        return positions

    def update_state(self, position):
        self.board[position] = self.player_symbol
        self.player_symbol = -1 if self.player_symbol == 1 else 1

    def give_reward(self):
        result = self.winner()
        if result == 1:
            self.player_one.feed_reward(1)
            self.player_two.feed_reward(0)
        elif result == -1:
            self.player_one.feed_reward(0)
            self.player_two.feed_reward(1)
        else:
            self.player_one.feed_reward(0.1)
            self.player_two.feed_reward(0.5)

    def reset(self):
        self.board = np.zeros((BOARD_ROWS, BOARD_COLUMNS))
        self.board_hash = None
        self.is_end = False
        self.player_symbol = 1

    # TODO:
    def play_with_cpu(self):
        pass

    # TODO:
    def play_with_human(self):
        pass


s = State("x", "y")
print(s.get_hash())


