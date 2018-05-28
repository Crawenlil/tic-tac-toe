#!/usr/bin/env python3
from game_executor import GameExecutor 
from player import HumanPlayer, QPlayer

players = {
    'Human' : HumanPlayer,
    'Q' : QPlayer
}

def main():
    player_x = HumanPlayer("Player X")
    player_o = HumanPlayer("Player O")
    game_executor = GameExecutor(player_x, player_o)
    game_executor.play(board_size=3, n_games=1, with_ui=True)


if __name__ == '__main__':
    main()

