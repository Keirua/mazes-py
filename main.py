import unittest


class Cell:
    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.north = None
        self.south = None
        self.west = None
        self.east = None
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

    # todo: implement
    def has_link(self, cell):
        None

    # todo: implement
    def neighbors(self):
        None


class Grid:
    rows = 10
    columns = 10

    def __init__(self, rows, columns):
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
        for l in range(self.rows):
            for c in range(self.columns):
                if l - 1 >= 0:
                    self.grid[l][c].north = self.grid[l - 1][c]
                if l + 1 < self.rows:
                    self.grid[l][c].south = self.grid[l + 1][c]
                if c - 1 >= 0:
                    self.grid[l][c].west = self.grid[l][c - 1]
                if c + 1 < self.columns:
                    self.grid[l][c].east = self.grid[l][c + 1]

    # todo: can it be replaced by array access?
    def get_cell(self, l, c):
        if 0 <= l < self.rows and 0 <= c < self.columns:
            return self.grid[l][c]
        return None

    def print(self):
        None


c1 = Cell(1, 2)
c2 = Cell(1, 3)
c1.link(c2, True)

class TestGridMethods(unittest.TestCase):

    def test_init(self):
        g = Grid(4, 4)
        self.assertEqual(g.get_cell(3, 2), g.grid[3][2])

        self.assertTrue(g.grid[2][2].north == g.grid[1][2])
        self.assertTrue(g.grid[2][2].south == g.grid[3][2])
        self.assertTrue(g.grid[2][2].east == g.grid[2][3])
        self.assertTrue(g.grid[2][2].west == g.grid[2][1])

        self.assertIsNone(g.grid[0][2].north)
        self.assertIsNone(g.grid[3][2].south)
        self.assertIsNone(g.grid[2][3].east)
        self.assertIsNone(g.grid[2][0].west)


if __name__ == '__main__':
    unittest.main()
