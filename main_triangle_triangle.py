from maze.formatter import TriangleGridImageFormatter
from maze.grid import TriangleWithTriangularShapeGrid
from maze.maze_generation import RecursiveBacktracker

if __name__ == "__main__":
    maze_generation_algorithm = RecursiveBacktracker()
    grid = TriangleWithTriangularShapeGrid(9)
    maze_generation_algorithm.apply_to(grid)

    TriangleGridImageFormatter.save_image(grid, "out/maze_triangle_triangle.png", 30)
