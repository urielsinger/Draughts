import os
import tkinter
from PIL import Image, ImageTk

from Draughts.constants import PROJECT_ROOT


class Cell:
    def __init__(self, type, x, y, size, canvas):
        self.type = type
        self.size = int(size)
        self.x = x
        self.y = y
        self.canvas = canvas
        self.change_picture()

    def set_type(self, type):
        self.type = type
        self.change_picture()

    def change_picture(self):
        image_path = os.path.join(PROJECT_ROOT, 'images', self.type.name + '.png')

        img = Image.open(image_path)
        img = img.resize((self.size, self.size), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(img)

    def draw(self):
        self.canvas_id = self.canvas.create_image(self.x, self.y, image=self.image)

    def change_location(self, x, y):
        self.canvas.move(self.canvas_id, x, y)
