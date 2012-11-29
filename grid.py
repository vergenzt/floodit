"""
grid.py

This file defines classes used for the Flood-it grid.
"""

import random

class FloodGrid(object):
    """A grid of colors."""

    COLORS = 'red green blue cyan yellow magenta'.split()

    def __init__(self, width=12, height=12, seed=None):
        """Initialize a random grid of colors."""
        self.width = width
        self.height = height
        random.seed(seed)

        grid = []
        for i in xrange(height):
            grid.append([])
            for j in xrange(width):
                color = random.choice(self.COLORS)
                left,up = None,None
                if j > 0: left = grid[i][j-1]
                if i > 0: up = grid[i-1][j]
                if (j>0 and i>0) and color == left.color == up.color:
                    left.positions.add((i,j))
                    left.merge(up)
                    grid[i-1][j] = left
                    grid[i].append(left)
                elif (j>0) and color == left.color:
                    left.positions.add((i,j))
                    grid[i].append(left)
                elif (i>0) and color == up.color:
                    up.positions.add((i,j))
                    grid[i].append(up)
                else:
                    blob = Blob(color, (i,j))
                    grid[i].append(blob)

        self.root = grid[0][0]


class Blob(object):
    """A contiguous blob of colors within a FloodGrid."""

    def __init__(self, color, pos):
        self.color = color
        self.neighbors = set()
        self.positions = set()
        self.positions.add(pos)

    def merge(self, other):
        """Merge Blob other into this Blob."""
        assert self.color == other.color
        self.positions |= other.positions
        self.neighbors |= other.neighbors

