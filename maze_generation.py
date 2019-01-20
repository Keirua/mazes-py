import random

class MazeGenerationAlgorithm:
    def apply_to(self):
        None


class BinaryTree(MazeGenerationAlgorithm):

    def apply_to(self, grid: Grid):
        """The binary tree algorithm applied to our grid"""
        for cell in grid.each_cell():
            neighbors = list(filter(lambda x: x is not None, [cell.north, cell.east]))
            if len(neighbors) > 0:
                n = random.choice(neighbors)
                cell.link(n)


class SideWinder(MazeGenerationAlgorithm):

    def apply_to(self, grid: Grid):
        for row in grid.grid:
            run = []
            for cell in row:
                run.append(cell)

                at_eastern_boundary = cell.east is None
                at_northern_boundary = cell.north is None
                should_close_out = at_eastern_boundary or (not at_northern_boundary and random.randint(0, 2) == 0)
                if should_close_out:
                    member = random.choice(run)

                    if member.north is not None:
                        member.link(member.north)
                        run.clear()
                else:
                    cell.link(cell.east, False)