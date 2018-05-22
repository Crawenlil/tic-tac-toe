import game_engine

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

class QPlayer(Player):
    pass


