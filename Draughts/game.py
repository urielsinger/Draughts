import tkinter

from Draughts import Board
from Draughts.constants import board_size, board_shape

class Game:
    def __init__(self):
        self.window = tkinter.Tk()
        self.window.title('Draughts')
        self.canvas = tkinter.Canvas(self.window, width=board_size, height=board_size)
        self.canvas.pack()

        self.board = Board(board_size, board_shape, canvas=self.canvas)
        self.window.bind("<ButtonPress-1>", self.board.on_start)
        self.window.bind("<B1-Motion>", self.board.on_drag)
        self.window.bind("<ButtonRelease-1>", self.board.on_drop)



    def play(self):
        self.window.mainloop()