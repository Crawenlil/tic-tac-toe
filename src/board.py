import numpy as np

class Board(object):
    def __init__(self, n):
        self._n = n
        self._board = np.zeros((n, n), dtype=int)
    
    def _symbol(self, x):
        symbol = ' '
        if x == 1:
            symbol = 'x'
        elif x == -1:
            symbol = 'o'
        return symbol

    def __str__(self):
        #' ─ │ ┌ ┐ └ ┘ ├ ┤ ┬ ┴ ┼ ' 
        top = '┌' + '───┬' * (self._n - 1) + '───┐' + '\n'
        middle = ''
        for r in range(self._n):
            middle += '│ '+' │ '.join(map(self._symbol, self._board[r])) + ' │' + '\n'
            if r < self._n - 1:
                middle += '├' + '───┼' * (self._n - 1) + '───┤' + '\n'
        bot = '└' + '───┴' * (self._n - 1) + '───┘'
        return top + middle + bot

    

