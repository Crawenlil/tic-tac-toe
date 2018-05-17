import urwid
from board import Board
from collections import deque


b = Board(20)
b._board[1,1] = 1
b._board[1,4] = -1

def exit_on_q(key):
    if key in ('q', 'Q'):
        raise urwid.ExitMainLoop()

txt = urwid.Text(str(b), align='center')
fill = urwid.Filler(txt, 'middle')
edit = urwid.Edit("Enter move (row, column)")
loop = urwid.MainLoop(fill, unhandled_input=exit_on_q)
loop.run()

class QuestionBox(urwid.Filler):
    def keypress(self, size, key):
        if key != 'enter':
            return super(QuestionBox, self).keypress(size, key)
        m = re.match(r'(\d+)[\s|,|.]\s?(\d+)', edit.edit_text)
        if m:
            game_engine.make_move()
        self.original_widget = urwid.Text("Ender move (row, column)" % edit.edit_text)

class GameEngine(object):

    def play_game_ui(self):
        self.commands_q = deque()
        
        class QuestionBox(urwid.Filler):
            def keypress(qbox_self, size, key):
                if key != 'enter':
                    return super().keypress(size, key)
                if _edit.get_edit_text() == "exit":
                    raise urwid.ExitMainLoop()
                self.commands_q.append(_edit.get_edit_text())
                _edit.set_edit_text("")

        def commands_getter():
            if self.commands_q:
                command = self.commands_q[0]
                del self.commands_q[0]
                return command
    


