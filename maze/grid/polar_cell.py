from maze.grid.cell import Cell


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
