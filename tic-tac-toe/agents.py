import json
import pickle

import numpy as np

with open('settings.json') as settings_file:
    params = json.load(settings_file)['PARAMETERS']
    settings = json.load(settings_file)['GAME_SETTINGS']
    BOARD_ROWS = settings['BOARD_ROWS']
    BOARD_COLUMNS = settings['BOARD_COLUMNS']
    ROUNDS = settings['ROUNDS']


class ComputerPlayer:
    def __init__(self, name, exp_rate=params['EXP_RATE']):
        self.name = name
        self.states = []
        self.exp_rate = exp_rate
        self.lr = params['LEARNING_RATE']
        self.decay_gamma = params['DECAY_GAMMA']
        self.states_value = {}  # state -> value

    def get_hash(self, board):
        board_hash = str(board.reshape(BOARD_ROWS * BOARD_COLUMNS))
        return board_hash

    def choose_action(self, positions, current_board, symbol):
        if np.random.uniform(0, 1) <= self.exp_rate:
            idx = np.random.choice(len(positions))
            action = positions[idx]
        else:
            value_max = -999
            for p in positions:
                next_board = current_board.copy()
                next_board[p] = symbol
                next_board_hash = self.get_hash(next_board)
                value = 0 if self.states_value.get(next_board_hash) is None else self.states_value.get(next_board_hash)
                if value >= value_max:
                    value_max = value
                    action = p
        print(f"{self.name} takes action: {action}")
        return action

    def add_state(self, state):
        self.states.append(state)

    def feed_reward(self):
        for st in reversed(self.states):
            if self.states_value.get(st) is None:
                self.states_value[st] = 0
            self.states_value[st] += self.lr * (self.decay_gamma * reward - self.states_value[st])
            reward = self.states_value[st]

    def reset(self):
        self.states = []

    def save_policy(self):
        fw = open('policy_' + str(self.name), 'wb')
        pickle.dump(self.states_value, fw)
        fw.close()

    def load_policy(self, file):
        fr = open(file, 'rb')
        self.states_value = pickle.load(fr)
        fr.close()


# TODO: define human player
class HumanPlayer:
    pass
