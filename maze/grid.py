import math
import random
from abc import ABC, abstractmethod

from maze.distance import Distances


class Cell(ABC):
    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.links = {}

    def link(self, cell, bidirectional=True):
        self.links[cell] = True
        if bidirectional:
            cell.link(self, False)

    def unlink(self, cell, bidirectional=True):
        self.links[cell] = False
        if bidirectional:
            cell.unlink(self, False)

    def has_link(self, cell):
        return cell in self.links and self.links[cell]

    @abstractmethod
    def neighbors(self):
        pass

    @abstractmethod
    def get_bounding_box(self, cell_size):
        pass

    def compute_distances(self):
        distances = Distances(self)
        frontier = [self]

        while len(frontier) > 0:
            new_frontier = []
            for cell in frontier:
                for linked in cell.links.keys():
                    if linked in distances.cells:
                        continue
                    distances[linked] = distances[cell] + 1
                    new_frontier.append(linked)

            frontier = new_frontier
        return distances


class RectangularCell(Cell):

    def __init__(self, row, column):
        self.north = None
        self.south = None
        self.east = None
        self.west = None
        super().__init__(row, column)

    def neighbors(self):
        neighbor_list = [self.north, self.south, self.west, self.east]
        return list(filter(lambda x: x is not None, neighbor_list))

    def get_bounding_box(self, cell_size):
        x1 = self.column * cell_size
        y1 = self.row * cell_size
        x2 = (self.column + 1) * cell_size
        y2 = (self.row + 1) * cell_size

        return x1, y1, x2, y2


class PolarCell(Cell):

    def __init__(self, row, column):
        super().__init__(row, column)
        self.outwards = []
        self.cw = None
        self.ccw = None
        self.inward = None

    def neighbors(self):
        neighbor_list = [self.inward, self.ccw, self.cw] + self.outwards
        return list(filter(lambda x: x is not None, neighbor_list))

    # todo: refactor
    def get_bounding_box(self, cell_size):
        x1 = self.column * cell_size
        y1 = self.row * cell_size
        x2 = (self.column + 1) * cell_size
        y2 = (self.row + 1) * cell_size

        return x1, y1, x2, y2


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


class RectangularGrid(Grid):

    def __init__(self, rows=10, columns=10):
        self.rows = rows
        self.columns = columns
        self.grid = []
        self.prepare_grid()
        self.configure_cells()

    def prepare_grid(self):
        for l in range(self.rows):
            line = []
            for c in range(self.columns):
                line.append(RectangularCell(l, c))
            self.grid.append(line)

    def configure_cells(self):
        for r in range(self.rows):
            for c in range(self.columns):
                if self.grid[r][c] is not None:
                    self.grid[r][c].north = self.get_cell(r - 1, c)
                    self.grid[r][c].south = self.get_cell(r + 1, c)
                    self.grid[r][c].west = self.get_cell(r, c - 1)
                    self.grid[r][c].east = self.get_cell(r, c + 1)


class DistanceGrid(RectangularGrid):
    def __init__(self, rows=10, columns=10):
        super().__init__(rows, columns)
        self.distances = None

    def content_of(self, cell):
        if self.distances is not None and cell in self.distances.cells.keys():
            return self.distances[cell]

        return super().content_of(cell)

    def background_color(self, cell):
        if cell not in self.distances.cells.keys():
            return None
        distance = self.distances[cell]
        intensity = (self.distances.max_distance - distance) / float(self.distances.max_distance)
        dark = int(255 * intensity)
        bright = int(128 + 127 * intensity)
        return [dark, bright, dark]


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
