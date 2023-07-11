from typing import List

from maze.grid import Grid
from maze.grid.triangle_cell import TriangleCell


class TriangleGrid(Grid):
    def __init__(self, rows: int = 10, columns: int = 10):
        self.rows = rows
        self.columns = columns
        self.grid: List[List[TriangleCell]] = []
        self.prepare_grid()
        self.configure_cells()

    def prepare_grid(self):
        for l in range(self.rows):
            line = []
            for c in range(self.columns):
                line.append(TriangleCell(l, c))
            self.grid.append(line)

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
