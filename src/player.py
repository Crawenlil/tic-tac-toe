import game_engine
from utils import *
import random
import numpy as np
import copy

class Player(object):
    def __init__(self, name):
        self.name = name

    def make_move(self, state):
        game_engine.end_move(state)

    def set_commands_getter(self, commands_getter):
        pass

    def __str__(self):
        return self.name

class HumanPlayer(Player):
    def set_commands_getter(self, commands_getter):
        self.get_command = commands_getter

    def make_move(self, state):
        actions = game_engine.actions(state)
        command = self.get_command()
        if command:
            for action in actions:
                if action.coords[0] == command[0] and action.coords[1] == command[1]:
                    game_engine.make_move(state, action)
                    super(HumanPlayer, self).make_move(state)

class RandomPlayer(Player):
    def make_move(self, state):
        actions = game_engine.actions(state)
        action = random.choice(actions)
        game_engine.make_move(state, action)
        super(RandomPlayer, self).make_move(state)

class SupervisedLearningPlayer(Player):
    def __init__(self, name, classifier):
        super(SupervisedLearningPlayer, self).__init__(name)
        self.classifier = classifier

    def make_move(self, state):
        actions = game_engine.actions(state)
        applied_actions = []
        for action in actions:
            tmp_state = copy.deepcopy(state)
            game_engine.make_move(tmp_state, action)
            applied_actions.append(tmp_state)
        action_scores = self.classifier.predict(applied_actions)
        if state.turn < 0:
            best_action_indexes = np.where(action_scores == action_scores.min())[0]
        else:
            best_action_indexes = np.where(action_scores == action_scores.max())[0]
        best_action_index = random.choice(best_action_indexes)
        action = actions[best_action_index]
        game_engine.make_move(state, action)
        super(SupervisedLearningPlayer, self).make_move(state)

class QPlayer(Player):
    def __init__(self, name, alpha, gamma):
        super(QPlayer, self).__init__(name)
        self.alpha = alpha
        self.gamma = gamma
        self.Xq = {}
        self.Oq = {}

    def make_move(self, state):
        q_table = self.Oq if state.turn == PLAYER_O else self.Xq 
        self.best_action = self.get_best_actoion(state, q_table)
        self.prev_state_dict = q_table[hash(state)] #store reference, so after changing state to new we can still update value
        game_engine.make_move(state, self.best_action)
        self.update_q(state, q_table)
        super(QPlayer, self).make_move(state)

    def get_best_actoion(self, state, q_table):
        '''If q[state] is empty, then inserts set of avaliable actions, else returns current best action'''
        best_action, best_value = None, -1
        hs = hash(state)
        if hs in q_table:
            state_q = q_table[hs] 
            for action, value in state_q.items():
                if value > best_value:
                    best_action = action
                    best_value = value
        else:
            actions = game_engine.actions(state)
            if actions:
                q_table[hs] = dict.fromkeys(actions, 0)
                best_action = random.choice(actions)
            else:
                best_action = None
        return best_action

    def update_q(self, state, q_table):
        next_best_action = self.get_best_actoion(state, turn)
        next_best_action_value = 0
        if next_best_action:
            next_best_action_value = q-table[hash(state)][next_best_action]
        self.prev_state_dict[self.action] = (1 - self.alpha) * self.prev_state_dict[self.action] + self.alpha * self.gamma * next_best_action_value

    def update_winner(self, reward):
        self.prev_state_dict[self.action] += self.alpha * reward
