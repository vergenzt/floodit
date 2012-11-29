#!/usr/bin/python
"""
floodit.py

This is an implementation of the game Flood-it, in which the player is presented
with a grid of colored squares, and they can change the color of the top-left
contiguous blob.  With each color change, the top-left blob "absorbs" adjacent
blobs of that color.  The objective is to fill the board with one color.
"""

from Tkinter import *
from grid import *

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.initialize_grid()
        self.pack()


    def initialize_grid(self):
        self.canvas = Canvas(self)
        self.canvas.pack()

        grid = FloodGrid()
        cellw = int(self.canvas['width']) / grid.width
        cellh = int(self.canvas['height']) / grid.height
        side = min(cellw, cellh)

        self.rects = [[None]*grid.width]*grid.height
        for i in xrange(grid.height):
            for j in xrange(grid.width):
                self.rects[i][j] = self.canvas.create_rectangle(
                    j*side, i*side, (j+1)*side, (i+1)*side,
                    fill=grid.by_position[i][j].color,
                    outline=''
                )

        self.grid = grid


if __name__=='__main__':
    root = Tk()
    app = Application(master=root)
    app.mainloop()

