import re
import urwid
from collections import deque

from utils import *
from board import Board
from game_state import *
import game_engine
import copy
import numpy as np
from collections import defaultdict


class GameExecutor(object):
    def __init__(self, player_x, player_o, move_delay=1, stop_at_end=True):
        self.player_x = player_x
        self.player_o = player_o
        self.move_delay = move_delay
        self.stop_at_end = stop_at_end

    def play(self, board_size, starting_player=PLAYER_X, n_games=1, with_ui=True):
        winners = defaultdict(int)
        for _ in range(n_games):
            if with_ui:
                winner = self.play_game_with_ui(board_size, starting_player)
            else:
                winner = self.play_game_no_ui(board_size, starting_player)
            winners[winner] = winners.get(winner, 0) + 1
        return winners

    def prepare_train_set(self, board_size, starting_player, n_games):
        train = [self.play_game_no_ui(board_size, starting_player, return_history=True) for _ in range(n_games)]
        X = []
        Y = []
        for winner, game_states in train:
            for gs in game_states:
                X.append(gs)
                Y.append(winner)
        return np.array(X), np.array(Y)

    def play_game_no_ui(self, board_size, starting_player, return_history=False):
        gs = GameState(Board(board_size), self.player_x, self.player_o, starting_player)

        if return_history:
            states_history = [copy.deepcopy(gs)]

        while game_engine.get_winner(gs) is None:
            if gs.turn == PLAYER_X:
                self.player_x.make_move(gs)
            else:
                self.player_o.make_move(gs)
            if return_history:
                states_history.append(copy.deepcopy(gs))

        winner = game_engine.get_winner(gs)

        if return_history:
            return winner, states_history
        else:
            return winner

    def play_game_with_ui(self, board_size, starting_player):
        self.gs = GameState(Board(board_size), self.player_x, self.player_o, starting_player)
        commands = deque()

        class QuestionBox(urwid.Filler):
            def keypress(self, size, key):
                if key != 'enter':
                    return super(QuestionBox, self).keypress(size, key)
                if edit.get_edit_text() == 'exit':
                    raise urwid.ExitMainLoop()
                m = re.match(r'(\d+)[\s|,|.]\s?(\d+)', edit.edit_text)
                if m:
                    commands.appendleft((int(m.group(1)), int(m.group(2))))
                edit.set_edit_text("")

        def commands_getter():
            if commands:
                return commands.pop()

        self.player_x.set_commands_getter(commands_getter)
        self.player_o.set_commands_getter(commands_getter)


        self.result_text = urwid.Text('', align='center')
        edit = urwid.Edit("{} ender move (row, column): ".format(str(self.gs.get_current_player())))
        self.edit = edit
        self.board_ui = urwid.Text(str(self.gs.board), align='center')
        pile = urwid.Pile([self.result_text, self.board_ui, edit])
        fill = QuestionBox(pile, 'middle')
        self.loop = urwid.MainLoop(fill)
        self.queue_delayed_move()
        self.loop.run()
        return game_engine.get_winner(self.gs)

    def queue_delayed_move(self):
        self.loop.set_alarm_in(self.move_delay, self.delayed_move)

    def delayed_move(self, loop, user_data):
        if self.gs.turn == PLAYER_X:
            self.player_x.make_move(self.gs)
        else:
            self.player_o.make_move(self.gs)
        self.update_ui()
        if game_engine.get_winner(self.gs) is None:
            self.queue_delayed_move();
        elif not self.stop_at_end:
            raise urwid.ExitMainLoop()

    def update_ui(self):
        self.edit.set_caption("{} ender move (row, column): ".format(str(self.gs.get_current_player())))
        self.board_ui.set_text(str(self.gs.board))
        winner = game_engine.get_winner(self.gs)
        if winner is not None:
            text = 'DRAW'
            if winner == PLAYER_X:
                text = 'WINNER: {}'.format(self.player_x)
            elif winner == PLAYER_O:
                text = 'WINNER: {}'.format(self.player_o)
            self.result_text.set_text(text)



