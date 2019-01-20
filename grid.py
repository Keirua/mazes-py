import random


class Distances:

    def __init__(self, root_node):
        self.root = root_node
        self.cells = {
            self.root: 0
        }

    def __getitem__(self, item):
        return self.cells[item]

    def __setitem__(self, key, value):
        self.cells[key] = value

    def path_to(self, goal):
        current = goal
        breadcrumbs = Distances(self.root)
        breadcrumbs[current] = self.cells[current]

        while current != self.root:
            for neighbor in current.links:
                if self.cells[neighbor] < self.cells[current]:
                    breadcrumbs[neighbor] = self.cells[neighbor]
                    current = neighbor

        return breadcrumbs


class Cell:
    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.north = None
        self.south = None
        self.west = None
        self.east = None
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

    def neighbors(self):
        neighbor_list = [self.north, self.south, self.west, self.east]
        return list(filter(lambda x: x is not None, neighbor_list))

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


class Grid:

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
                line.append(Cell(l, c))
            self.grid.append(line)

    def configure_cells(self):
        for r in range(self.rows):
            for c in range(self.columns):
                self.grid[r][c].north = self.get_cell(r - 1, c)
                self.grid[r][c].south = self.get_cell(r + 1, c)
                self.grid[r][c].west = self.get_cell(r, c - 1)
                self.grid[r][c].east = self.get_cell(r, c + 1)

    def get_cell(self, row, column):
        """Return the cell at the requested coordinate"""
        # could be replaced by array access, but looks less interesting since it's 2 dimensions
        if 0 <= row < self.rows and 0 <= column < self.columns:
            return self.grid[row][column]
        return None

    def content_of(self, cell):
        return " "

    def each_rows(self):
        """Yield all the rows of the grid"""
        for row in self.grid:
            yield row

    def each_cell(self):
        """Yield all the cells of the grid"""
        for row in self.grid:
            for cell in row:
                yield cell

    def random_cell(self):
        random_row = random.choice(self.grid)
        return random.choice(random_row)

    def size(self):
        """The size of the grid"""
        return self.rows * self.columns


class DistanceGrid(Grid):
    def __init__(self, rows=10, columns=10):
        super().__init__(rows, columns)
        self.distances = None

    def content_of(self, cell):
        if self.distances is not None and cell in self.distances.cells.keys():
            return self.distances[cell]

        return super().content_of(cell)
