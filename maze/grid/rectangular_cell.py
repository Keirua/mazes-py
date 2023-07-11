from maze.grid import Cell


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
