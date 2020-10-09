import json
import pickle
import numpy as np

with open('settings.json') as file:
    settings_file = json.load(file)
    params = settings_file['PARAMETERS']
    settings = settings_file['GAME_SETTINGS']
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
        # print(f"{self.name} takes action: {action}")
        return action

    def add_state(self, state):
        self.states.append(state)

    def feed_reward(self, reward):
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

    def load_policy(self, policy_file):
        fr = open(policy_file, 'rb')
        self.states_value = pickle.load(fr)
        fr.close()


class HumanPlayer:
    def __init__(self, name):
        self.name = name

    def choose_action(self, positions):
        while True:
            print("Your move.")
            row = int(input("Choose row: "))
            col = int(input("Choose column: "))
            action = (row, col)
            if action in positions:
                return action

    # append a hash state
    def add_state(self, state):
        pass

    # at the end of the game, backpropagate and update states value
    def feed_reward(self, reward):
        pass

    def reset(self):
        pass

