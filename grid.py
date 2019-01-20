import random
from PIL import Image, ImageDraw


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
        self.distances = distances


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

    def __str__(self):
        output = "+" + "---+" * self.rows + "\n"
        for row in self.each_rows():
            top = "|"
            bottom = "+"
            for cell in row:
                body = " " * 3
                east_boundary = " " if cell.has_link(cell.east) else "|"
                top += body + east_boundary
                south_boundary = " " * 3 if cell.has_link(cell.south) else "-" * 3
                bottom += south_boundary + "+"
            output += top + "\n"
            output += bottom + "\n"
        return output

    def save_image(self, filename, cell_size=10):
        wall_color = (0, 0, 0)
        background_color = (255, 255, 255)

        im = Image.new("RGB", (1 + self.rows * cell_size, 1 + self.columns * cell_size), background_color)
        draw = ImageDraw.Draw(im)
        for cell in self.each_cell():
            x1 = cell.column * cell_size
            y1 = cell.row * cell_size
            x2 = (cell.column + 1) * cell_size
            y2 = (cell.row + 1) * cell_size
            if not cell.north:
                draw.line((x1, y1, x2, y1), fill=wall_color)
            if not cell.west:
                draw.line((x1, y1, x1, y2), fill=wall_color)
            if not cell.has_link(cell.east):
                draw.line((x2, y1, x2, y2), fill=wall_color)
            if not cell.has_link(cell.south):
                draw.line((x1, y2, x2, y2), fill=wall_color)

        im.save(filename, "PNG")