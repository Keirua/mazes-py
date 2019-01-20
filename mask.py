from maze.formatter import ImageFormatter, StringFormatter
from maze.mask import MaskedGrid, Mask
from maze.maze_generation import RecursiveBacktracker

if __name__ == '__main__':
    maze_generation_algorithm = RecursiveBacktracker()

    mask = Mask(5,5)
    mask[(0, 0)] = False
    mask[(2, 2)] = False
    mask[(4, 4)] = False
    print(mask.bits)
    g = MaskedGrid(mask)

    maze_generation_algorithm.apply_to(g)
    g.distances = g.random_cell().compute_distances()
    g.distances.compute_max()

    print(StringFormatter.to_string(g))
    ImageFormatter.save_image(g, "masked_maze.png", 30)
