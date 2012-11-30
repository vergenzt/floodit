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

import sys
from argparse import ArgumentParser

class Application(Tk):
    def __init__(self, parent):
        Tk.__init__(self, parent)

        # parse command line arguments
        parser = ArgumentParser()
        parser.add_argument('-s', '--seed', type=int,
                            help='specify random seed')
        parser.add_argument('--stdin', action='store_true',
                            help='take initial colors from stdin, 1 per line')
        self.args = parser.parse_args()

        self.initialize()

    def initialize(self):
        self.grid()
        self.resizable(False, False)

        self.canvas = Canvas(self, width=300, height=300)
        self.canvas.grid(column=0, row=0, columnspan=8, padx=5, pady=5)

        self.grid = FloodGrid(seed=self.args.seed)
        cellw = int(self.canvas['width']) / self.grid.width
        cellh = int(self.canvas['height']) / self.grid.height
        side = min(cellw, cellh)

        # create the rectangles on the canvas
        self.rects = []
        for i in xrange(self.grid.height):
            self.rects.append([])
            for j in xrange(self.grid.width):
                r = self.canvas.create_rectangle(
                    j*side, i*side, (j+1)*side, (i+1)*side,
                    fill=self.grid.by_position[i][j].color
                )
                self.rects[-1].append(r)

        # create the control buttons
        self.buttons = []
        for i,color in enumerate(FloodGrid.COLORS):
            b = Button(self,
                bg = color, activebackground = color,
                borderwidth = 4,
                command = lambda c=color: self.set_color(c),
                state = DISABLED
            )
            b.grid(column=i+1, row=1, pady=5, sticky='S')
            self.buttons.append(b)

        # align the grid columns and rows
        self.grid_columnconfigure(0, weight=1)
        for i in range(1,8):
            self.grid_columnconfigure(i+1, weight=0)
        self.grid_columnconfigure(7, weight=1)
        self.grid_rowconfigure(1, pad=10)

        # run initial colorations
        if self.args.stdin:
            for line in sys.stdin:
                if line in FloodGrid.COLORS:
                    self.set_color(line)
        for b in self.buttons:
            b.config(state = NORMAL)

    def set_color(self, color):
        """
        Set the color for the top-left blob.  Called by the UI buttons.
        """
        root = self.grid.root
        root.color = color
        # set the canvas rectangle colors
        for (i,j) in root.positions:
            self.canvas.itemconfig(self.rects[i][j], fill=color)
        # merge same-color neighbors into the root
        for blob in root.neighbors.copy():
            if blob.color == color:
                root.merge(blob)


if __name__=='__main__':
    app = Application(None)
    app.title('Flood-It!')
    app.mainloop()

