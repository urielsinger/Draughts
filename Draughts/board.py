import socket

import Draughts.constants
from Draughts import Player, Cell
from Draughts.constants import cell_type, player_type, cell_size


class Board:
    def __init__(self, size, shape, canvas, controller, mode=None):
        self.size = (size, size)
        self.shape = (shape, shape)
        self.canvas = canvas
        self.controller = controller

        self.initialize()
        self.draw()

        self.host = '127.0.0.1'
        self.port = 65432
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.mode = mode
        if self.mode == "server":
            self.conn = []
            s.bind((self.host, self.port))
            s.listen()
            conn_client1, addr = s.accept()
            self.conn.append(conn_client1)

            s.listen()
            conn_client2, addr = s.accept()
            self.conn.append(conn_client2)

            self.conn[0].sendall(bytes('0', encoding='utf8'))
            self.conn[1].sendall(bytes('1', encoding='utf8'))
            self.game_type = "socket"

        elif self.mode == "client":
            s.connect((self.host, self.port))
            self.conn = s
            self.client_number = int(self.conn.recv(1024).decode("utf-8"))
            self.game_type = "socket"

        else:
            self.game_type = "normal"

        self.players = [Player(player_type.WHITE), Player(player_type.BLACK)]
        self.current_player = 0

        self.end_game = False

    def start(self):
        if self.mode == "client" and self.client_number == 1:
            self.canvas.update()
            start_i, start_j, end_i, end_j = self.receive_mode()
            self.do_turn(start_i, start_j, end_i, end_j, receive_mode=True)

        if self.mode == 'server':
            while not self.end_game:
                self.canvas.update()
                start_i, start_j, end_i, end_j = self.receive_mode()
                self.do_turn(start_i, start_j, end_i, end_j, receive_mode=True)

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

    def get_current_player(self, opponent=False):
        if not opponent:
            return self.players[self.current_player]
        return self.players[1 - self.current_player]

    def on_start(self, event):
        self.start_i, self.start_j = self.convert_grid_to_logical_position(event.x, event.y)

    def on_drop(self, event):
        end_i, end_j = self.convert_grid_to_logical_position(event.x, event.y)
        did_turn = self.do_turn(self.start_i, self.start_j, end_i, end_j)
        if did_turn and self.game_type == "socket" and not self.end_game:
            self.canvas.update()
            start_i, start_j, end_i, end_j = self.receive_mode()
            self.do_turn(start_i, start_j, end_i, end_j, receive_mode=True)

    def do_turn(self, start_i, start_j, end_i, end_j, receive_mode=False):
        if self.end_game:
            return False

        if self.is_move_legal(start_i, start_j, end_i, end_j):
            # update regular turn
            self.board[end_i][end_j].set_type(self.board[start_i][start_j].type)
            self.board[start_i][start_j].set_type(cell_type.EMPTY_BLACK)
            # update eat turn
            if abs(start_i - end_i) == 2:
                middle_i = int((start_i + end_i) / 2)
                middle_j = int((start_j + end_j) / 2)
                self.board[middle_i][middle_j].set_type(cell_type.EMPTY_BLACK)
                self.get_current_player(opponent=True).got_eaten()
            # update king
            if self.check_if_become_king(end_i, end_j):
                self.board[end_i][end_j].set_type(self.get_current_player().get_type(king=True))
            # draw
            self.draw()

            # check if game ended
            player_won = self.is_game_end()
            if player_won is not None:
                print(f'winner is {player_won}')
                # disable game
                self.end_game = True

            # send move
            if self.game_type == "socket" and not receive_mode:
                self.send_move(start_i, start_j, end_i, end_j)
            self.switch_turn()
            return True

        return False


    def is_game_end(self):
        for player in self.players:
            if player.total_pieces == 0:
                return player.get_type(opponent=True)
        return None

    def is_move_legal(self, start_i, start_j, end_i, end_j):
        is_my_piece = self.is_cell_type(start_i, start_j, type=self.get_current_player().get_type())
        is_destination_empty = self.is_cell_type(end_i, end_j, type=cell_type.EMPTY_BLACK)
        if is_my_piece and is_destination_empty:
            is_king = self.is_cell_type(start_i, start_j, type=self.get_current_player().get_type(king=True), normalize=False)
            if self.check_regular_turn(start_i, start_j, end_i, end_j, is_king):
                return True
            elif self.check_eating_turn(start_i, start_j, end_i, end_j, is_king):
                return True
        return False

    def is_cell_type(self, i, j, type, normalize=True):
        if normalize:
            cell_type = self.board[i][j].get_normalized_type()
        else:
            cell_type = self.board[i][j].type
        return cell_type == type

    def check_regular_turn(self, start_i, start_j, end_i, end_j, is_king=False, jump_size=1):
        direction = jump_size * self.get_current_player().get_direction()

        is_i_ok = abs(end_i - start_i) == jump_size  # moved one colum right or left
        is_j_ok = (end_j == start_j + direction) or (is_king and (end_j == start_j - direction))  # moved one line forward

        if is_i_ok and is_j_ok:
            return True
        return False

    def check_eating_turn(self, start_i, start_j, end_i, end_j, is_king):
        if not self.check_regular_turn(start_i, start_j, end_i, end_j, is_king, jump_size=2):
            return False

        middle_i = int((start_i + end_i)/2)
        middle_j = int((start_j + end_j)/2)

        if self.is_cell_type(middle_i, middle_j, type=self.get_current_player().get_type(opponent=True)):
            return True

        return False

    def switch_turn(self):
        self.current_player = 1 - self.current_player

    def check_if_become_king(self, end_i, end_j):
        return end_j == 0 or end_j == self.shape[1] - 1

    def convert_grid_to_logical_position(self, x, y):
        i = int(x // (self.size[0] / self.shape[0]))
        j = int(y // (self.size[1] / self.shape[1]))
        return i, j

    def convert_logical_to_grid_position(self, x, y):
        xp = (self.size[0] / self.shape[0]) * x + self.size[0] / self.shape[0] / 2
        yp = (self.size[1] / self.shape[1]) * y + self.size[1] / self.shape[1] / 2
        return xp, yp

    def send_move(self, start_i, start_j, end_i, end_j):
        move_str = f"{start_i}_{start_j}_{end_i}_{end_j}"
        if self.mode == 'client':
            self.conn.sendall(bytes(move_str, encoding='utf8'))
        else:
            self.conn[1-self.current_player].sendall(bytes(move_str, encoding='utf8'))

    def receive_mode(self):
        if self.mode == 'client':
            move_str = self.conn.recv(1024).decode("utf-8")
            start_i, start_j, end_i, end_j = list(map(int, move_str.split('_')))
        else:  # self.mode == 'server':
            move_str = self.conn[self.current_player].recv(1024).decode("utf-8")
            start_i, start_j, end_i, end_j = list(map(int, move_str.split('_')))
            self.send_move(start_i, start_j, end_i, end_j)
        return start_i, start_j, end_i, end_j