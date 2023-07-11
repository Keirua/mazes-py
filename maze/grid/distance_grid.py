from maze.grid.rectangular_grid import RectangularGrid


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


