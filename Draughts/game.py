import tkinter
from tkinter import font as tkfont

from Draughts import Board
from Draughts.constants import board_size, board_shape

class Game(tkinter.Tk):
    def __init__(self, *args, **kwargs):
        tkinter.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.title('Draughts')
        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tkinter.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.option_frame = OptionPage(parent=container, controller=self)
        self.option_frame.grid(row=0, column=0, sticky="nsew")

        self.board_frame = BoardPage(parent=container, controller=self)
        self.board_frame.grid(row=0, column=0, sticky="nsew")

        self.option_frame.tkraise()

    def start_game(self, mode):
        self.board_frame.tkraise()
        self.board_frame.start_mode(mode)

    def play(self):
        self.mainloop()


class BoardPage(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)
        self.controller = controller

        self.canvas = tkinter.Canvas(self, width=board_size, height=board_size)
        self.canvas.pack()

    def start_mode(self, mode):
        self.board = Board(board_size, board_shape, canvas=self.canvas, controller=self.controller, mode=mode)
        self.controller.bind("<ButtonPress-1>", self.board.on_start)
        # self.controller.bind("<B1-Motion>", self.board.on_drag)
        self.controller.bind("<ButtonRelease-1>", self.board.on_drop)
        self.board.start()

class OptionPage(tkinter.Frame):

    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)
        self.controller = controller
        label = tkinter.Label(self, text="Choose Game Mode", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button_server = tkinter.Button(self, text="Server", command=lambda: controller.start_game(mode="server"))
        button_client = tkinter.Button(self, text="Client", command=lambda: controller.start_game(mode="client"))
        button_normal = tkinter.Button(self, text="Normal", command=lambda: controller.start_game(mode="normal"))
        button_server.pack()
        button_client.pack()
        button_normal.pack()
