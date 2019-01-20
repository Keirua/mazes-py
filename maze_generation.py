import random

from grid import Grid
from abc import ABC, abstractmethod


class MazeGenerationAlgorithm(ABC):
    @abstractmethod
    def apply_to(self, grid: Grid):
        pass


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
                    cell.link(cell.east)


class AldousBroder(MazeGenerationAlgorithm):

    def apply_to(self, grid: Grid):
        cell = grid.random_cell()
        unvisited_count = grid.size() - 1
        while unvisited_count > 0:
            neighbor = random.choice(cell.neighbors())
            if len(neighbor.links.keys()) == 0:
                cell.link(neighbor)
                unvisited_count -= 1
            cell = neighbor


class Wilson(MazeGenerationAlgorithm):
    def apply_to(self, grid: Grid):
        unvisited = [cell for cell in grid.each_cell()]
        first_cell = random.choice(unvisited)
        unvisited.remove(first_cell)

        while len(unvisited) > 0:
            cell = random.choice(unvisited)
            path = [cell]
            while cell in unvisited:
                cell = random.choice(cell.neighbors())
                if cell in path:
                    path = path[0:path.index(cell) + 1]
                else:
                    path.append(cell)

            for i in range(0, len(path) - 1):
                path[i].link(path[i + 1])
                unvisited.remove(path[i])


class HuntAndKill(MazeGenerationAlgorithm):
    def apply_to(self, grid: Grid):
        current = grid.random_cell()
        while current is not None:
            unvisited_neighbors = list(filter(lambda x: len(x.links.keys()) == 0, current.neighbors()))

            if len(unvisited_neighbors) > 0:
                neighbor = random.choice(unvisited_neighbors)
                current.link(neighbor)
                current = neighbor
            else:
                current = None
                for cell in grid.each_cell():
                    visited_neighbors = list(filter(lambda x: len(x.links.keys()) != 0, cell.neighbors()))
                    if len(cell.links) == 0 and len(visited_neighbors) > 0:
                        current = cell
                        neighbor = random.choice(visited_neighbors)
                        current.link(neighbor)
                        break
