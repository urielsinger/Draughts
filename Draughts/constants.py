import os
from enum import Enum

PROJECT_DIR_PATH = os.path.dirname(__file__)
PROJECT_ROOT = os.path.dirname(PROJECT_DIR_PATH)

board_size = 600
board_shape = 8
cell_size = board_size / board_shape

class cell_type(Enum):
    BLACK = 1
    WHITE = 2
    EMPTY_BLACK = 3
    EMPTY_WHITE = 4

class player_type(Enum):
    BLACK = cell_type.BLACK
    WHITE = cell_type.WHITE
