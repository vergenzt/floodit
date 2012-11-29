"""
grid.py

This file defines classes used for the Flood-it grid.
"""

class FloodGrid(object):
    """A grid of colors."""
    pass


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

