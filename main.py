from formatter import ImageFormatter, StringFormatter
from grid import Grid, DistanceGrid
from maze_generation import SideWinder

if __name__ == '__main__':
    # maze_generation_algorithm = BinaryTree()
    maze_generation_algorithm = SideWinder()
    g = DistanceGrid(4, 4)

    maze_generation_algorithm.apply_to(g)
    g.grid[0][0].compute_distances()
    g.distances = g.grid[0][0].distances

    print(StringFormatter.to_string(g))
    ImageFormatter.save_image(g, "maze.png", 30)
