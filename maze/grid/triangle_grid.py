from typing import List, Optional

from maze.grid import Grid
from maze.grid.triangle_cell import TriangleCell


class TriangleWithRectangularShapeGrid(Grid):
    def __init__(self, rows: int = 10, columns: int = 10):
        self.rows = rows
        self.columns = columns
        self.grid: List[List[Optional[TriangleCell]]] = []
        for l in range(self.rows):
            line = []
            for c in range(self.columns):
                line.append(None)
            self.grid.append(line)
        self.prepare_grid()
        self.configure_cells()

    def prepare_grid(self):
        for r in range(self.rows):
            for c in range(self.columns):
                self.grid[r][c] = TriangleCell(r, c)

    def configure_cells(self):
        for r in range(self.rows):
            for c in range(self.columns):
                if self.grid[r][c] is not None:
                    if self.grid[r][c].is_upright:
                        self.grid[r][c].south = self.get_cell(r + 1, c)
                    else:
                        self.grid[r][c].north = self.get_cell(r - 1, c)
                    self.grid[r][c].west = self.get_cell(r, c - 1)
                    self.grid[r][c].east = self.get_cell(r, c + 1)


import math


class TriangleWithTriangularShapeGrid(TriangleWithRectangularShapeGrid):
    def __init__(self, size: int):
        self.size = size
        super().__init__(rows=size, columns=size)

    def prepare_grid(self):
        for l in range(math.ceil(self.size / 2)):
            line = []
            for c in range(l, self.size - l):
                line.append(TriangleCell(self.size - l - 1, c))
            self.grid.append(line)
