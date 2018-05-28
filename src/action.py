class Action(object):
    def __init__(self, coords, symbol):
        self.coords = coords
        self.symbol = symbol

    def __call__(self, state):
        state.board.board[self.coords[0], self.coords[1]] = self.symbol

    def __str__(self):
        return "{}, {} -> {}".format(self.coords[0], self.coords[1], self.symbol)
    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash((self.coords[0], self.coords[1]))


