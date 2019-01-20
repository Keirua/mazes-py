from formatter import ImageFormatter, StringFormatter
from grid import Grid, DistanceGrid
from maze_generation import SideWinder, AldousBroder, Wilson, HuntAndKill, RecursiveBacktracker

if __name__ == '__main__':
    # maze_generation_algorithm = BinaryTree()
    # maze_generation_algorithm = SideWinder()
    # maze_generation_algorithm = AldousBroder()
    # maze_generation_algorithm = Wilson()
    # maze_generation_algorithm = HuntAndKill()
    maze_generation_algorithm = RecursiveBacktracker()
    rows = 12
    columns = 12
    g = DistanceGrid(rows, columns)

    maze_generation_algorithm.apply_to(g)
    g.distances = g.random_cell().compute_distances()
    g.distances.compute_max()

    print(StringFormatter.to_string(g))
    ImageFormatter.save_image(g, "maze.png", 30)

    g.distances = g.distances.path_to(g.grid[rows-1][0])
    print(StringFormatter.to_string(g))

