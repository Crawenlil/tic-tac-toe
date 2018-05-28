import game_engine
from utils import *
import random
import copy

class Player(object):
    def __init__(self, name, which_player):
        self.name = name
        self.which_player = which_player

    def make_move(self, state):
        game_engine.end_move(state)

    def set_commands_getter(self, commands_getter):
        self.get_command = commands_getter

    def __str__(self):
        return self.name

class HumanPlayer(Player):
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
    def __init__(self, name, which_player, classifier):
        super(SupervisedLearningPlayer, self).__init__(name, which_player)
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
            best_action_index = action_scores.argmin()
        else:
            best_action_index = action_scores.argmax()
        action = actions[best_action_index]
        game_engine.make_move(state, action)
        super(SupervisedLearningPlayer, self).make_move(state)

class QPlayer(Player):
    def __init__(self, name, which_player, alpha, gamma):
        super(QPlayer, self).__init__(name, which_player)
        self.alpha = alpha
        self.gamma = gamma
        self.q = self.init_q()

    def init_q(self):
        return {}

    def make_move(self, state):
        best_action = self.get_best_actoion(state)
        prev_state_dict = self.q[hash(state)] #store reference, so after changing state to new we can still update value
        game_engine.make_move(state, best_action)
        self.update_q(prev_state_dict, state, best_action)
        super(QPlayer, self).make_move(state)

    def get_best_actoion(self, state):
        '''If q[state] is empty, then inserts set of avaliable actions, else returns current best action'''
        best_action, best_value = None, -1
        hs = hash(state)
        if hs in self.q:
            state_q = self.q[hs] 
            for action, value in state_q.items():
                if value > best_value:
                    best_action = action
                    best_value = value
        else:
            actions = game_engine.actions(state)
            if actions:
                self.q[hs] = dict.fromkeys(actions, 0)
                best_action = random.choice(actions)
            else:
                best_action = None
        return best_action

    def update_q(self, prev_state_dict, state, action):
        reward = game_engine.get_winner(state)
        if reward is None:
            reward = 0
        next_best_action = self.get_best_actoion(state)
        next_best_action_value = 0
        if next_best_action:
            next_best_action_value = self.q[hash(state)][next_best_action]
        prev_state_dict[action] = (1 - self.alpha) * prev_state_dict[action] + self.alpha * (reward + self.gamma * next_best_action_value)

         

