from maze.grid import RectangularCell
from maze.grid.grid import Grid


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
    """
    Subclass of the Rectangular grid that displays the distance from the origin using a color coding
    """

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
