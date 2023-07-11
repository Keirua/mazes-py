import random
from abc import ABC, abstractmethod


class Grid(ABC):

    def __init__(self, rows=10, columns=10):
        self.rows = rows
        self.columns = columns
        self.grid = []
        self.prepare_grid()
        self.configure_cells()

    @abstractmethod
    def prepare_grid(self):
        pass

    @abstractmethod
    def configure_cells(self):
        pass

    def get_cell(self, row, column):
        """Return the cell at the requested coordinate"""
        # could be replaced by array access, but looks less interesting since it's 2 dimensions
        if 0 <= row < self.rows and 0 <= column < self.columns:
            return self.grid[row][column]
        return None

    def content_of(self, cell):
        return " "

    def background_color(self, cell):
        return None

    def each_rows(self):
        """Yield all the rows of the grid"""
        for row in self.grid:
            yield row

    def each_cell(self):
        """Yield all the cells of the grid"""
        for row in self.grid:
            for cell in row:
                if cell is not None:
                    yield cell

    def random_cell(self):
        cell = None
        while cell is None:
            random_row = random.choice(self.grid)
            cell = random.choice(random_row)
        return cell

    def size(self):
        """The size of the grid"""
        return self.rows * self.columns

    def deadends(self):
        deadend_list = []
        for cell in self.each_cell():
            if len(cell.links.keys()) == 1:
                deadend_list.append(cell)
        return deadend_list
