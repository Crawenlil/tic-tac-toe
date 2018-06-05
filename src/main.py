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
    player = RandomPlayer("Random")
    game_executor = GameExecutor(player, player)
    X, Y = game_executor.prepare_train_set(board_size=board_size, starting_player=PLAYER_X, n_games=train_set_size)
    ft = FunctionTransformer(game_state_to_array, validate=False)
    clf = MLPRegressor(hidden_layer_sizes=(board_size*board_size, board_size, 1), batch_size=len(Y), max_iter=1000)
    the_classifier = Pipeline([('game_state_to_array', ft), ('game_state_classifier', clf)])
    the_classifier.fit(X, Y)
    the_player = SupervisedLearningPlayer("Super Player", the_classifier)
    return the_player

def train_q_player(board_size, train_set_size):
    random = RandomPlayer("Random")
    q_player = QPlayer("QPlayer", 0.5, 0.1) 
    game_executor = GameExecutor(q_player, random)
    game_executor.play(board_size=board_size, starting_player=PLAYER_X, n_games=train_set_size, with_ui=False)
    return q_player

def test(player1, player2):
    game_executor = GameExecutor(player1, player2)
    winners1 = game_executor.play(board_size=3, starting_player=PLAYER_X, n_games=100, with_ui=False)
    game_executor = GameExecutor(player2, player1)
    winners2 = game_executor.play(board_size=3, starting_player=PLAYER_X, n_games=100, with_ui=False)
    print("Total stats:")
    print("1 - {}".format(player1))
    print("-1 - {}".format(player2))
    winners2[1], winners2[-1] = winners2[-1], winners2[1] 
    for k in set(list(winners1.keys()) + list(winners2.keys())):
        print("{}: {}".format(k, winners1[k] + winners2[k]))

def play_with_hooman(board_size):
    super_player = train_player(board_size=board_size, train_set_size=10000)
    #super_player = RandomPlayer("Random")
    hooman_player = HumanPlayer("Human")
    game_executor = GameExecutor(super_player, hooman_player)
    winner = game_executor.play(board_size=board_size, starting_player=PLAYER_X, n_games=1, with_ui=True)


def main():
    #q_player = train_q_player(board_size=3, train_set_size=10000)
    #super_player = train_player(board_size=3, train_set_size=1000)
    #random = RandomPlayer("Random")
    #test(super_player, q_player)
    play_with_hooman(board_size=3)

if __name__ == '__main__':
    main()

