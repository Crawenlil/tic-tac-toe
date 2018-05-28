import numpy as np

class Board(object):
    def __init__(self, n):
        self.n = n
        self.board = np.zeros((n, n), dtype=int)
    
    def _symbol(self, x):
        symbol = ' '
        if x == 1:
            symbol = 'x'
        elif x == -1:
            symbol = 'o'
        return symbol

    def __str__(self):
        numbers = '    ' + ''.join(['{:^4}'.format(x) for x in range(self.n)]) + '\n'
        top = '   ┌' + '───┬' * (self.n - 1) + '───┐' + '\n'
        middle = ''
        for r in range(self.n):
            middle += '{:>3}│ '.format(r)+' │ '.join(map(self._symbol, self.board[r])) + ' │' + '\n'
            if r < self.n - 1:
                middle += '   ├' + '───┼' * (self.n - 1) + '───┤' + '\n'
        bot = '   └' + '───┴' * (self.n - 1) + '───┘'
        return numbers + top + middle + bot

    def __hash__(self):
        return hash(str(self))
