from formatter import ImageFormatter, StringFormatter
from grid import Grid, DistanceGrid
from maze_generation import SideWinder

if __name__ == '__main__':
    # maze_generation_algorithm = BinaryTree()
    maze_generation_algorithm = SideWinder()
    rows = 6
    columns = 6
    g = DistanceGrid(rows, columns)

    maze_generation_algorithm.apply_to(g)
    g.distances = g.grid[0][0].compute_distances()

    print(StringFormatter.to_string(g))
    ImageFormatter.save_image(g, "maze.png", 30)

    g.distances = g.distances.path_to(g.grid[rows-1][0])
    print(StringFormatter.to_string(g))

