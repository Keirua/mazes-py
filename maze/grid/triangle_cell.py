from maze.grid import Cell


class TriangleCell(Cell):
    def __init__(self, row, column):
        self.north = None
        self.south = None
        self.east = None
        self.west = None
        super().__init__(row, column)

    @property
    def is_upright(self):
        return (self.row + self.column) % 2 == 0

    def neighbors(self):
        neighbor_list = [self.west, self.east, self.south if self.is_upright else self.north]

        return list(filter(lambda x: x is not None, neighbor_list))
