import game_engine
from utils import *
import random
import copy

class Player(object):

    def __init__(self, name):
        self.name = name

    def make_move(self, state):
        pass

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

class RandomPlayer(Player):
    def make_move(self, state):
        actions = game_engine.actions(state)
        action = random.choice(actions)
        game_engine.make_move(state, action)

class SupervisedLearningPlayer(Player):
    def __init__(self, name, classifier):
        self.name = name
        self.classifier = classifier

    def make_move(self, state):
        actions = game_engine.actions(state)
        applied_actions = []
        for action in actions:
            tmp_state = copy.deepcopy(state)
            game_engine.make_move(tmp_state, action)
            applied_actions.append(tmp_state)
        action_scores = self.classifier.predict(applied_actions)
        return actions[0]


class QPlayer(Player):
    
    def __init__(self, name, alpha, gamma):
        super(Player, self).__init__(name)
        self.alpha = alpha
        self.gamma = gamma
        self.q = self.get_q()

    def get_Q(self):
        return {}

    def make_move(self, state):
        best_action, best_value = None, -1
        if state in self.q:
            state_q = self.q[state] 
            for action, value in state_q.items():
                if value > best_value:
                    best_action = action
                    best_value = value
        else:
            actions = game_engine.actions(state)
            self.q[state] = dict.fromkeys(actions, 0)
            best_action = random.choice(actions)

        prev_state_dict = self.q[state] #store reference, so after changing state to new we can still update value
        game_engine.make_move(state, best_action)
        update_q(prev_state_dict, state, best_action)

    def update_q(self, prev_state_dict, state, action):
        reward = game_engine.get_winner(state)
        if reward is None:
            reward = 0
        max_next_q = max(self.q[state], key=self.q[state].get)
        prev_state_dict[action] = (1 - self.alpha) * prev_state_dict[action] + self.alpha * (reward + self.gamma * self.q[state][max_next_q])

         

