#!/usr/bin/env python3
from game_executor import GameExecutor 
from player import HumanPlayer, QPlayer, RandomPlayer
from utils import *

def train_player(board_size, train_set_size):
    player = RandomPlayer("random")
    game_executor = GameExecutor(player, player)
    train = game_executor.prepare_train_set(board_size=board_size, n_games=train_set_size)
    import pdb; pdb.set_trace()

def main():
    # train_player(3, 10)
    player_x = QPlayer("Player X", PLAYER_X, 0.5, 0.1)
    player_o = RandomPlayer("Player O", PLAYER_O)
    game_executor = GameExecutor(player_x, player_o)
    game_executor.play(board_size=3, starting_player=PLAYER_X, n_games=1, with_ui=False)


if __name__ == '__main__':
    main()

