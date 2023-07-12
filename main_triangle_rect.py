from maze.formatter import TriangleGridImageFormatter
from maze.grid import TriangleWithRectangularShapeGrid
from maze.maze_generation import RecursiveBacktracker

if __name__ == "__main__":
    maze_generation_algorithm = RecursiveBacktracker()
    grid = TriangleWithRectangularShapeGrid(10, 17)
    maze_generation_algorithm.apply_to(grid)

    TriangleGridImageFormatter.save_image(grid, "out/maze_triangle_rect.png", 30)
