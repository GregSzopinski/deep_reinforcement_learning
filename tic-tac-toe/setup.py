import numpy as np
import pickle
from constants import BOARD_ROWS, BOARD_COLUMNS, ROUNDS


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

    def play_with_ai(self, rounds=ROUNDS):
        for i in range(rounds):
            if i % 1000 == 0:
                print(f"Rounds {i}")
            while not self.is_end:
                # Player One
                positions = self.available_positions()
                player_one_action = self.player_one.choose_action(positions, self.board, self.player_symbol)
                # action -> update (board) state
                self.update_state(player_one_action)
                board_hash = self.get_hash()
                self.player_one.add_state(board_hash)
                # check board status if it is an end

                win = self.winner()
                if win is not None:
                    self.show_board()
                    # if player one won the game or there was a draw
                    self.give_reward()
                    self.player_one.reset()
                    self.player_two.reset()
                    self.reset()
                    break

                else:
                    # Player Two
                    positions = self.available_positions()
                    player_two_action = self.player_two.choose_action(positions, self.board, self.player_symbol)
                    # same logic as above - update state in consequence of an action
                    self.update_state(player_two_action)
                    board_hash = self.get_hash()
                    self.player_two.add_state(board_hash)

                    win = self.winner()
                    if win is not None:
                        self.show_board()
                        self.give_reward()
                        self.player_one.reset()
                        self.player_two.reset()
                        self.reset()
                        break

    # TODO:
    def play_with_human(self):
        pass


s = State("x", "y")
print(s.get_hash())
