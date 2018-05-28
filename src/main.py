#!/usr/bin/env python3
from game_executor import GameExecutor 
from player import HumanPlayer, QPlayer, RandomPlayer

players = {
    'Human' : HumanPlayer,
    'Q' : QPlayer
}

def train_player(board_size, train_set_size):
    player = RandomPlayer("random")
    game_executor = GameExecutor(player, player)
    train = game_executor.prepare_train_set(board_size=board_size, n_games=train_set_size)
    import pdb; pdb.set_trace()

def main():
    # train_player(3, 10)
    player_x = RandomPlayer("Player X")
    player_o = RandomPlayer("Player O")
    game_executor = GameExecutor(player_x, player_o)
    game_executor.play(board_size=3, n_games=1, with_ui=False)


if __name__ == '__main__':
    main()

