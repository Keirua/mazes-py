from maze.formatter import (
    ImageFormatter,
    PNGImageSaver,
    ShapeFormatter,
    StringFormatter,
)
from maze.grid import DistanceGrid
from maze.maze_generation import RecursiveBacktracker


def gen_maze_image(rows=4, columns=8, outfilename="out/maze_shapes.png"):
    maze_generation_algorithm = RecursiveBacktracker()
    g = DistanceGrid(rows, columns)

    maze_generation_algorithm.apply_to(g)
    g.distances = g.random_cell().compute_distances()
    g.distances.compute_max()

    print(StringFormatter.to_string(g))
    shapes, bbox = ShapeFormatter.save_image(grid=g, cell_size=30)
    image_saver = PNGImageSaver()
    image_saver.save_image(
        shapes,
        bbox,
    )


if __name__ == "__main__":
    rows = 4
    columns = 8
    gen_maze_image(rows, columns)
