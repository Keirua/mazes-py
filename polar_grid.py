from maze.formatter import PolarGridImageFormatter
from maze.grid import PolarGrid
from maze.maze_generation import RecursiveBacktracker

if __name__ == '__main__':
    maze_generation_algorithm = RecursiveBacktracker()

    g = PolarGrid(8)

    maze_generation_algorithm.apply_to(g)

    PolarGridImageFormatter.save_image(g, "maze-polar.png", 30)


