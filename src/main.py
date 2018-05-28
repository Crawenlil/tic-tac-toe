#!/usr/bin/env python3
from game_executor import GameExecutor 
from player import HumanPlayer, QPlayer, RandomPlayer, SupervisedLearningPlayer
from utils import *

from sklearn.preprocessing import FunctionTransformer
from sklearn.pipeline import Pipeline
from sklearn.neural_network import MLPRegressor
import numpy as np

def game_state_to_array(game_states):
    transformed = np.array([gs.board.board.reshape(-1) for gs in game_states])
    return transformed

def train_player(board_size, train_set_size):
    player = RandomPlayer("random")
    game_executor = GameExecutor(player, player)
    X, Y = game_executor.prepare_train_set(board_size=board_size, starting_player=PLAYER_X, n_games=train_set_size)
    ft = FunctionTransformer(game_state_to_array, validate=False)
    clf = MLPRegressor(hidden_layer_sizes=(board_size*board_size, board_size, 1), batch_size=len(Y), max_iter=1000)
    the_classifier = Pipeline([('game_state_to_array', ft), ('game_state_classifier', clf)])
    the_classifier.fit(X, Y)
    the_player = SupervisedLearningPlayer("Super Player", the_classifier)
    return the_player

def main():
    super_player = train_player(3, 1000)
    random = RandomPlayer("Random")
    game_executor = GameExecutor(super_player, random)
    winners1 = game_executor.play(board_size=3, starting_player=PLAYER_X, n_games=100, with_ui=False)
    print("Swap")
    game_executor = GameExecutor(random, super_player)
    winners2 = game_executor.play(board_size=3, starting_player=PLAYER_X, n_games=100, with_ui=False)
    print("Total stats:")
    print("1 - {}".format(super_player))
    print("-1 - {}".format(random))
    for k in set(list(winners1.keys()) + list(winners2.keys())):
        print("{}: {}".format(k, winners1.get(k, 0) + winners2.get(-1*k, 0)))


if __name__ == '__main__':
    main()

