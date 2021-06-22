from Draughts.constants import player_type, cell_type


class Player:
    def __init__(self, type):
        self.type = type
        self.total_pieces = 12

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
