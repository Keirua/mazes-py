from formatter import ImageFormatter, StringFormatter
from grid import Grid
from maze_generation import SideWinder

if __name__ == '__main__':
    # maze_generation_algorithm = BinaryTree()
    maze_generation_algorithm = SideWinder()
    g = Grid(10, 10)

    maze_generation_algorithm.apply_to(g)

    print(StringFormatter.to_string(g))
    ImageFormatter.save_image(g, "maze.png", 30)
