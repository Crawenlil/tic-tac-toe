import re
import urwid
from collections import deque

from utils import *
from board import Board
from game_state import *
import game_engine


class GameExecutor(object):
    def __init__(self, player_x, player_o, move_delay=1, stop_at_end=True):
        self.player_x = player_x
        self.player_o = player_o
        self.move_delay = move_delay
        self.stop_at_end = stop_at_end

    def play(self, board_size, n_games=1, with_ui=True):
        if with_ui:
            self.play_game_with_ui(board_size)
        else:
            self.play_game_no_ui(n_games)

    def play_game_with_ui(self, board_size):
        self.gs = GameState(Board(board_size), self.player_x, self.player_o, PLAYER_X)
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





    


