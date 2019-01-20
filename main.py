from formatter import ImageFormatter, StringFormatter
from grid import Grid, DistanceGrid
from maze_generation import SideWinder, AldousBroder, Wilson

if __name__ == '__main__':
    # maze_generation_algorithm = BinaryTree()
    # maze_generation_algorithm = SideWinder()
    # maze_generation_algorithm = AldousBroder()
    maze_generation_algorithm = Wilson()
    rows = 30
    columns = 30
    g = DistanceGrid(rows, columns)

    maze_generation_algorithm.apply_to(g)
    g.distances = g.grid[rows//2][columns//2].compute_distances()
    g.distances.compute_max()

    print(StringFormatter.to_string(g))
    ImageFormatter.save_image(g, "maze.png", 30)

    g.distances = g.distances.path_to(g.grid[rows-1][0])
    print(StringFormatter.to_string(g))

