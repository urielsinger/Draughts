from Draughts import Player, Cell
from Draughts.constants import cell_type, player_type, cell_size


class Board:
    def __init__(self, size, shape, canvas):
        self.size = (size, size)
        self.shape = (shape, shape)
        self.canvas = canvas

        self.initialize()
        self.draw()

        self.players = [Player(player_type.WHITE), Player(player_type.BLACK)]
        self.current_player = 0

    def initialize(self):
        self.board = []

        # empty board
        for i in range(self.shape[0]):
            row = []
            for j in range(self.shape[1]):
                x, y = self.convert_logical_to_grid_position(i, j)

                type = cell_type.EMPTY_WHITE if i % 2 == j % 2 else cell_type.EMPTY_BLACK
                if type == cell_type.EMPTY_BLACK:
                    if j <= 2:
                        type = cell_type.BLACK
                    elif j >= 5:
                        type = cell_type.WHITE

                cell = Cell(type, x, y, cell_size, self.canvas)
                row.append(cell)
            self.board.append(row)

    def draw(self):
        for row in self.board:
            for cell in row:
                cell.draw()

    def get_current_player(self):
        return self.players[self.current_player]

    def on_start(self, event):
        self.start_i, self.start_j = self.convert_grid_to_logical_position(event.x, event.y)

    def on_drag(self, event):
        x, y = event.x, event.y
        pass

    def on_drop(self, event):
        end_i, end_j = self.convert_grid_to_logical_position(event.x, event.y)

        if self.is_move_legal(self.start_i, self.start_j, end_i, end_j):
            self.board[self.start_i][self.start_j].set_type(cell_type.EMPTY_BLACK)
            self.board[end_i][end_j].set_type(self.get_current_player().type.value)
            self.draw()
            self.switch_turn()

    def is_move_legal(self, start_i, start_j, end_i, end_j):
        if self.board[start_i][start_j].type == self.get_current_player().type.value and \
                self.board[end_i][end_j].type == cell_type.EMPTY_BLACK:
            return True
        else:
            return False


    def convert_grid_to_logical_position(self, x, y):
        i = int(x // (self.size[0] / self.shape[0]))
        j = int(y // (self.size[1] / self.shape[1]))
        return i, j

    def convert_logical_to_grid_position(self, x, y):
        xp = (self.size[0] / self.shape[0]) * x + self.size[0] / self.shape[0] / 2
        yp = (self.size[1] / self.shape[1]) * y + self.size[1] / self.shape[1] / 2
        return xp, yp

    def switch_turn(self):
        self.current_player = 1 - self.current_player
