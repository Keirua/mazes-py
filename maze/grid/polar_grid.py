import math

from maze.grid.grid import Grid
from maze.grid.polar_cell import PolarCell


class PolarGrid(Grid):
    def __init__(self, rows):
        super().__init__(rows, 1)
        print(len(self.grid))
        self.prepare_grid()
        self.configure_cells()

    def get_cell(self, row, column):
        """Return the cell at the requested coordinate"""
        if 0 <= row < self.rows and 0 <= column: #< len(self.grid[row]):
            return self.grid[row][column % len(self.grid[row])]
        return None

    def prepare_grid(self):
        row_height = 1.0 / float(self.rows)
        print(row_height)
        rows = [[PolarCell(0, 0)]]

        for row in range(1, self.rows):
            radius = float(row) / self.rows
            circumference = 2 * math.pi * radius
            previous_count = len(rows[row - 1])
            print(previous_count)
            approximate_cell_width = circumference / previous_count
            ratio = int(approximate_cell_width / row_height)
            cells = previous_count * ratio
            rows.append([PolarCell(row, col) for col in range(cells)])

        self.grid = rows

    def configure_cells(self):
        for cell in self.each_cell():
            row, col = cell.row, cell.column

            if row > 0:
                cell.cw = self.get_cell(row, col + 1)
                cell.ccw = self.get_cell(row, col - 1)
                ratio = len(self.grid[row]) / len(self.grid[row - 1])
                parent = self.grid[row - 1][col // int(ratio)]
                parent.outwards.append(cell)
                cell.inward = parent
