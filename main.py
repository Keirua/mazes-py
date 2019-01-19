class Cell:
    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.links = {}

    def link(self, cell, bidir=True):
        self.links[cell] = True
        if bidir:
            cell.link(self, False)

    def unlink(self, cell, bidir=True):
        self.links[cell] = False
        if bidir:
            cell.unlink(self, False)

    def get_links(self):
        return self.links.keys()

    def has_link(self, cell):
        return self.get_links()


class Grid:
    rows = 10
    columns = 10

    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.grid = []
        self.prepare_grid()

    def prepare_grid(self):
        for l in range(self.rows):
            line = []
            for c in range(self.columns):
                line.append(Cell(l, c))
            self.grid.append(line)

    def configure_cells(self):
        for l in range(self.rows):
            for c in range(self.columns):
                if l-1 >= 0:
                    self.grid[l][c].north = self.grid[l-1][c]
                if l + 1 < self.rows:
                    self.grid[l][c].south = self.grid[l+1][c]
                if c-1 >= 0:
                    self.grid[l][c].west = self.grid[l][c-1]
                if c + 1 < self.columns:
                    self.grid[l][c].east = self.grid[l][c+1]

    def print(self):
        None


c1 = Cell(1, 2)
c2 = Cell(1, 3)
c1.link(c2, True)
g = Grid(4, 4)
g.print()

print(c1.row, c1.links)
