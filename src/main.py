#!/usr/bin/env python3
from game_executor import GameExecutor 
from player import HumanPlayer, QPlayer, RandomPlayer, SupervisedLearningPlayer
from utils import *

from sklearn.preprocessing import FunctionTransformer
from sklearn.pipeline import Pipeline
from sklearn.neural_network import MLPRegressor
from sklearn.tree import DecisionTreeRegressor
import numpy as np
import argparse
import py
import pickle

parser = argparse.ArgumentParser(description='Play some tic-tac-toe.')
parser.add_argument('--player-a', default="RandomPlayer", help="Player A, can be location of pickled player")
parser.add_argument('--player-b', default="RandomPlayer", help="Player B, can be location of pickled player")
parser.add_argument('--player-a-to', help="Save player A to location")
parser.add_argument('--player-b-to', help="Save player B to location")
parser.add_argument('--compare-players', action="store_true", help="Compare players and print stats")
parser.add_argument('--n-games', type=int, help="Number of games to play")
parser.add_argument('--with-ui', help="UI?", action="store_true")

def try_load_player(path):
    if path is None or not py.path.local(path).check(file=1):
        if path == "QPlayer":
            return train_q_player(3, 10000)
        elif path == "MLPPlayer":
            train = prepare_supervised_train_set(RandomPlayer("A"), RandomPlayer("B"), 3, n_games=1000)
            return train_mlp_super_player(train)
        elif path == "TreePlayer":
            train = prepare_supervised_train_set(RandomPlayer("A"), RandomPlayer("B"), 3, n_games=1000)
            return train_tree_super_player(train)
        elif path == "RandomPlayer":
            return RandomPlayer("RandomPlayer")
        elif path == "HumanPlayer":
            return HumanPlayer("HumanPlayer")
        else:
            raise Exception("Unknown player: {}".format(path))
    with open(path, 'rb') as f:
        return pickle.load(f)

def try_save_player(player, path):
    if path is not None:
        with open(path, 'wb') as f:
            pickle.dump(player, f)

def parse_args():
    args = parser.parse_args()
    args.player_a = try_load_player(args.player_a)
    args.player_b = try_load_player(args.player_b)
    return args

def game_state_to_array(game_states):
    transformed = np.array([gs.board.board.reshape(-1) for gs in game_states])
    return transformed

def train_super_player(clf, train):
    X, Y = train
    ft = FunctionTransformer(game_state_to_array, validate=False)
    the_classifier = Pipeline([('game_state_to_array', ft), ('game_state_classifier', clf)])
    the_classifier.fit(X, Y)
    the_player = SupervisedLearningPlayer("Super Player", the_classifier)
    return the_player

def prepare_supervised_train_set(player_a, player_b, board_size, n_games):
    game_executor = GameExecutor(player_a, player_b)
    X, Y = game_executor.prepare_train_set(board_size=board_size, n_games=n_games)
    return X, Y

def train_mlp_super_player(train):
    X, Y = train
    board_size = train[0][0].board.board.shape[0]
    clf = MLPRegressor(hidden_layer_sizes=(board_size*board_size, board_size*board_size, 1), batch_size=int(0.001*len(Y)), max_iter=1000)
    return train_super_player(clf, train)

def train_tree_super_player(train):
    X, Y = train
    board_size = train[0][0].board.board.shape[0]
    clf = DecisionTreeRegressor()
    return train_super_player(clf, train)

def train_q_player(board_size, train_set_size):
    random = RandomPlayer("Random")
    q_player = QPlayer("QPlayer", 0.5, 0.1) 
    game_executor = GameExecutor(q_player, random)
    game_executor.train_q_player(board_size=board_size, q_player=q_player, starting_player=PLAYER_X, n_games=train_set_size, with_ui=False)
    return q_player

def test(player1, player2, ui, n_games):
    print("Test begins...")
    n_games = int(n_games/2)
    game_executor = GameExecutor(player1, player2)
    winners1 = game_executor.play(board_size=3, starting_player=PLAYER_X, n_games=n_games, with_ui=ui)
    winners2 = game_executor.play(board_size=3, starting_player=PLAYER_O, n_games=n_games, with_ui=ui)
    print("Stats:")
    print("A - 1 - {}".format(player1))
    print("B - -1 - {}".format(player2))
    print("Number of wins for each player:")
    print("A begins:")
    for k in [1, 0, -1]:
        print("{}: {}".format(k, winners1[k]))
    print("B begins:")
    for k in [1, 0, -1]:
        print("{}: {}".format(k, winners2[k]))
    print("Totals:")
    for k in [1, 0, -1]:
        print("{}: {}".format(k, winners1[k] + winners2[k]))

def play_with_hooman(a, b, board_size, with_ui, n_games):
    game_executor = GameExecutor(a, b)
    winner = game_executor.play(board_size=board_size, starting_player=PLAYER_X, n_games=n_games, with_ui=with_ui)

def main():
    args = parse_args()
    if args.compare_players:
        test(args.player_a, args.player_b, args.with_ui, args.n_games)
    else:
        play_with_hooman(args.player_a, args.player_b, board_size=3, with_ui=args.with_ui, n_games=args.n_games)
    try_save_player(args.player_a, args.player_a_to)
    try_save_player(args.player_b, args.player_b_to)

if __name__ == '__main__':
    main()
