import numpy as np

import board
from action import Action

def make_move(state, action):
    action(state)
    change_turn(state)

def change_turn(state):
    state.turn *= -1


def get_winner(state):
    b = state.board.board
    n = state.board.n
    horizontal = np.sum(b, axis=1)
    vertical = np.sum(b, axis=0)
    diagonal1 = b.trace()
    diagonal2 = np.fliplr(b).trace()
    if n in vertical or n in horizontal or n == diagonal1 or n == diagonal2:
        return 1
    if -n in vertical or -n in horizontal or -n == diagonal1 or -n == diagonal2:
        return -1
    if not actions(state):
        return 0
    return None

def actions(state):
    symbol = state.turn
    return [Action(coords, symbol) for coords in np.argwhere(state.board.board == 0)]
    
