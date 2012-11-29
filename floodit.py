#!/usr/bin/python
"""
floodit.py

This is an implementation of the game Flood-it, in which the player is presented
with a grid of colored squares, and they can change the color of the top-left
contiguous blob.  With each color change, the top-left blob "absorbs" adjacent
blobs of that color.  The objective is to fill the board with one color.
"""

from Tkinter import *

class Application(Frame):
    pass

if __name__=='__main__':
    root = Tk()
    app = Application(master=root)
    app.mainloop()

