from maze.formatter import TriangleGridImageFormatter
from maze.grid import TriangleGrid
from maze.maze_generation import RecursiveBacktracker

if __name__ == "__main__":
    maze_generation_algorithm = RecursiveBacktracker()
    grid = TriangleGrid(10, 17)
    maze_generation_algorithm.apply_to(grid)

    TriangleGridImageFormatter.save_image(grid, "out/maze_triangle.png", 30)
