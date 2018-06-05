#!/usr/bin/env python3
from game_executor import GameExecutor 
from player import HumanPlayer, QPlayer, RandomPlayer, SupervisedLearningPlayer
from utils import *

from sklearn.preprocessing import FunctionTransformer
from sklearn.pipeline import Pipeline
from sklearn.neural_network import MLPRegressor
import numpy as np
import argparse
import py
import pickle

parser = argparse.ArgumentParser(description='Play some tic-tac-toe.')
parser.add_argument('--player-a', default="RandomPlayer", help="Player A, can be location of pickled player")
parser.add_argument('--player-b', default="RandomPlayer", help="Player B, can be location of pickled player")
parser.add_argument('--player-a-to', help="Save player A to location")
parser.add_argument('--player-b-to', help="Save player B to location")
parser.add_argument('--with-ui', help="UI?", action="store_true")

def try_load_player(path):
    if path is None or not py.path.local(path).check(file=1):
        if path == "QPlayer":
            return train_q_player(3, 10000)
        elif path == "SuperPlayer":
            return train_player(3, 1000)
        elif path == "RandomPlayer":
            return RandomPlayer("RandomPlayer")
        elif path == "HumanPlayer":
            return RandomPlayer("HumanPlayer")
        else:
            raise Exception("Unknown player: {}".format(path))
    with open(path, 'rb') as f:
        return pickle.load(f)

def try_save_player(player, path):
    if path is not None:
        with open(path, 'wb') as f:
            pickle.dump(player, path)

def parse_args():
    args = parser.parse_args()
    args.player_a = try_load_player(args.player_a)
    args.player_b = try_load_player(args.player_b)
    return args

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

def test(player1, player2, ui):
    game_executor = GameExecutor(player1, player2)
    winners1 = game_executor.play(board_size=3, starting_player=PLAYER_X, n_games=100, with_ui=ui)
    game_executor = GameExecutor(player2, player1)
    winners2 = game_executor.play(board_size=3, starting_player=PLAYER_X, n_games=100, with_ui=ui)
    print("Total stats:")
    print("A - 1 - {}".format(player1))
    print("B - -1 - {}".format(player2))
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
    args = parse_args()
    test(args.player_a, args.player_b, args.with_ui)
    try_save_player(args.player_a, args.player_a_to)
    try_save_player(args.player_b, args.player_b_to)
    play_with_hooman(board_size=3)

if __name__ == '__main__':
    main()

