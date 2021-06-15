import socket
from Draughts import Cell
from Draughts.constants import player_type, cell_type


class Player:
    def __init__(self, type, mode=None):
        self.type = type
        self.total_pieces = 12

        self.host = '127.0.0.1'
        self.port = 65432
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if mode == "server":
            s.bind((self.host, self.port))
            s.listen()
            self.conn, addr = s.accept()
            # while True:
            #     data = conn.recv(1024)
            #     if not data:
            #         break
            #     conn.sendall(data)
        elif mode == "client":
            s.connect((self.host, self.port))
            self.conn = s
            # s.sendall(b'Hello, world')
            # data = s.recv(1024)

    def is_white(self):
        return self.type == player_type.WHITE

    def is_black(self):
        return self.type == player_type.BLACK

    def get_type(self, opponent=False, king=False):
        king = 2 if king else 0

        if not opponent:
            return cell_type(self.type.value.value + king)
        return cell_type(3 - self.type.value.value + king)

    def get_direction(self):
        return -1 if self.is_white() else 1

    def got_eaten(self):
        self.total_pieces -= 1

    def send_move(self, start_i, start_j, end_i, end_j):
        move_str = f"{start_i}_{start_j}_{end_i}_{end_j}"
        self.conn.sendall(bytes(move_str, encoding='utf8'))

    def receive_mode(self):
        move_str = self.conn.recv(1024).decode("utf-8")
        start_i, start_j, end_i, end_j = list(map(int, move_str.split('_')))
        return start_i, start_j, end_i, end_j
