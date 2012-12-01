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
        parser = ArgumentParser(add_help=False)
        parser.add_argument('--help', action='help',
                            help='show this help message and exit')
        parser.add_argument('-w', '--width', type=int, default=12,
                            help='width of the grid')
        parser.add_argument('-h', '--height', type=int, default=12,
                            help='height of the grid')
        parser.add_argument('-s', '--seed', type=int,
                            help='specify random seed')
        parser.add_argument('--stdin', action='store_true',
                            help='take initial colors from stdin, 1 per line')
        parser.add_argument('-d', '--debug', action='store_true',
                            help='enable debug mode (display blob indices)')
        self.args = parser.parse_args()

        self.initialize()

    def initialize(self):
        self.grid()
        self.resizable(False, False)

        self.canvas = Canvas(self, width=300, height=300)
        self.canvas.grid(column=0, row=0, columnspan=8, padx=5, pady=5)

        self.grid = FloodGrid(
            width=self.args.width,
            height=self.args.height,
            seed=self.args.seed
        )
        cellw = int(self.canvas['width']) / self.grid.width
        cellh = int(self.canvas['height']) / self.grid.height
        side = min(cellw, cellh)

        # create the rectangles on the canvas
        self.rects = []
        if self.args.debug:
            self.indices = []
        for i in xrange(self.grid.height):
            self.rects.append([])
            if self.args.debug:
                self.indices.append([])
            for j in xrange(self.grid.width):
                r = self.canvas.create_rectangle(
                    j*side, i*side, (j+1)*side, (i+1)*side,
                    fill=self.grid.by_position[i][j].color
                )
                self.rects[-1].append(r)
                if self.args.debug:
                    t = self.canvas.create_text(
                        j*side, i*side,
                        anchor='nw',
                        text=str(self.grid.by_position[i][j].index)
                    )
                    self.indices[-1].append(t)
        Blob.position_changed = self.position_changed

        # create the turns label
        self.turns_taken = IntVar()
        label = Label(self,
            textvariable=self.turns_taken
        )
        label.grid(column=0, row=1)

        # create the control buttons
        self.buttons = []
        for i,color in enumerate(FloodGrid.COLORS):
            b = Button(self,
                bg = color, activebackground = color,
                borderwidth = 4,
                command = lambda c=color: self.press_button(c),
                state = DISABLED
            )
            self.bind(str(i+1), lambda e,b=b: b.invoke())
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
            self.read_from_stdin()
        for b in self.buttons:
            b.config(state = NORMAL)

    def read_from_stdin(self):
        """Read a color from stdin."""
        for line in sys.stdin:
            line = line.strip()
            if line in FloodGrid.COLORS:
                self.press_button(line)

    def press_button(self, color):
        """Callback for the UI color buttons."""
        try:
            self.grid.change_color(color)
            self.turns_taken.set(self.turns_taken.get() + 1)
            print "Turn %d: %s" % (self.turns_taken.get(), color)
        except AssertionError: pass

    def position_changed(self, (i,j), blob):
        """Callback for blob color changes."""
        self.canvas.itemconfig(self.rects[i][j], fill=blob.color)
        if self.args.debug:
            self.canvas.itemconfig(self.indices[i][j], text=blob.index)


if __name__=='__main__':
    app = Application(None)
    app.title('Flood-It!')
    app.mainloop()

