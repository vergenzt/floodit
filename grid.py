"""
grid.py

This file defines classes used for the Flood-it grid.
"""

import random
import sys

class FloodGrid(object):
    """A grid of colors."""

    COLORS = 'red green blue cyan yellow magenta'.split()

    def __init__(self, width=12, height=12, seed=None):
        """Initialize a random grid of colors."""
        self.width = width
        self.height = height
        if not seed:
            seed = random.randint(0, sys.maxint)
        print "Using random seed %d" % seed
        random.seed(seed)

        grid = []
        for i in xrange(height):

            # create a random row
            row = []
            for j in xrange(width):
                color = random.choice(self.COLORS)
                if j == 0:
                    b = Blob(color, (i,j))
                    row.append(b)
                else:
                    left = row[j-1]
                    if color == left.color:
                        left.positions.add((i,j))
                        row.append(left)
                    else:
                        b = Blob(color, (i,j))
                        left.neighbors.add(b)
                        b.neighbors.add(left)
                        row.append(b)

            # fuse it to the previous rows
            grid.append(row)
            if i != 0:
                for j in xrange(width):
                    up   = grid[-2][j]
                    down = grid[-1][j]
                    if up.color == down.color:
                        if up.index != down.index:
                            up.merge(down)
                            for (i,j) in down.positions:
                                grid[i][j] = up
                    else:
                        up.neighbors.add(down)
                        down.neighbors.add(up)

        self.by_position = grid
        self.root = grid[0][0]


class Blob(object):
    """A contiguous blob of colors within a FloodGrid."""
    INDEX = 0

    def __init__(self, color, pos):
        self.index = Blob.INDEX
        Blob.INDEX += 1
        self.color = color
        self.neighbors = set()
        self.positions = set()
        self.positions.add(pos)

    def merge(self, other):
        """Merge Blob other into this Blob."""
        assert self.color == other.color
        self.positions |= other.positions
        self.neighbors |= other.neighbors

    def __str__(self):
        i = self.index
        c = self.color
        p = list(self.positions)
        n = [neighbor.index for neighbor in self.neighbors]
        s = '<grid.Blob%d (%s, p=%s, n=%s)>' % (i,c,p,n)
        return s

    def __hash__(self):
        h = 0
        h ^= hash(self.color)
        h ^= hash(frozenset(self.positions))
        h ^= hash(frozenset(self.neighbors))
        return h

