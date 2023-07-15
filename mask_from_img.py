import sys

from maze.formatter import ImageFormatter, StringFormatter
from maze.mask import Mask, MaskedGrid
from maze.maze_generation import RecursiveBacktracker

if __name__ == "__main__":
    # img_id = "025.png"
    if len(sys.argv) > 1:
        img_id = sys.argv[1]  # "025.png"
    else:
        raise RuntimeError("No command line parameter provided.")
    maze_generation_algorithm = RecursiveBacktracker()
    mask = Mask.from_image(f"masks/{img_id}")

    g = MaskedGrid(mask)

    maze_generation_algorithm.apply_to(g)
    g.distances = g.random_cell().compute_distances()
    g.distances.compute_max()

    # print(StringFormatter.to_string(g))
    ImageFormatter.save_image(g, f"out/masked_maze_{img_id}")
