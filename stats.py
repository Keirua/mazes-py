from maze.rectangulargrid import RectangularGrid
from maze.maze_generation import SideWinder, AldousBroder, Wilson, HuntAndKill, BinaryTree
import math
from collections import OrderedDict

if __name__ == '__main__':
    algorithms = [
        BinaryTree(),
        SideWinder(),
        AldousBroder(),
        Wilson(),
        HuntAndKill()
    ]
    size = 20
    attempts = 100
    averages = OrderedDict()
    print("average deadends per {}x{} maze: ({} cells)".format(size, size, size * size))
    for algorithm in algorithms:
        deadends_count = []

        for i in range(attempts):
            g = RectangularGrid(size, size)
            algorithm.apply_to(g)

            deadends_count.append(len(g.deadends()))
        avg = math.fsum(deadends_count) / len(deadends_count)
        averages[algorithm.__class__.__name__] = int(avg)

    for k, v in averages.items():
        percentage = int((100. * v)/(size * size))
        print("{} : {}/{} ({}%)".format(k.ljust(12, ' '), str(v).rjust(3, ' '), size * size, str(percentage).rjust(2)))
