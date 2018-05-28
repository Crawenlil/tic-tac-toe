from utils import *

class GameState():
    def __init__(self, board, player_x, player_o, turn):
        self.player_x = player_x
        self.player_o = player_o
        self.board = board
        self.turn = turn

    def get_current_player(self):
        return self.player_x if self.turn == PLAYER_X else self.player_o

    def __hash__(self):
        return hash((self.board, self.turn)) 
        



