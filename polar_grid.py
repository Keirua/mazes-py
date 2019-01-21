from maze.formatter import ImageFormatter, StringFormatter, PolarGridImageFormatter
from maze.rectangulargrid import DistanceGrid, RectangularGrid
from maze.maze_generation import RecursiveBacktracker

if __name__ == '__main__':
    maze_generation_algorithm = RecursiveBacktracker()

    g = RectangularGrid(8, 8)

    maze_generation_algorithm.apply_to(g)

    PolarGridImageFormatter.save_image(g, "maze-polar.png", 30)


