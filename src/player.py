import game_engine
import random
import copy

class Player(object):

    def __init__(self, name):
        self.name = name

    def make_move(self, state):
        actions = game_engine.actions(state)
        command = self.get_command()
        if command:
            for action in actions:
                if action.coords[0] == command[0] and action.coords[1] == command[1]:
                    game_engine.make_move(state, action)

    def set_commands_getter(self, commands_getter):
        self.get_command = commands_getter

    def __str__(self):
        return self.name

class HumanPlayer(Player):
    pass

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
    pass


