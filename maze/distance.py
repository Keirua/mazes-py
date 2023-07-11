class Distances:
    def __init__(self, root_node):
        self.root = root_node
        self.cells = {self.root: 0}

    def __getitem__(self, item):
        return self.cells[item]

    def __setitem__(self, key, value):
        self.cells[key] = value

    def path_to(self, goal):
        current = goal
        breadcrumbs = Distances(self.root)
        breadcrumbs[current] = self.cells[current]

        while current != self.root:
            for neighbor in current.links:
                if self.cells[neighbor] < self.cells[current]:
                    breadcrumbs[neighbor] = self.cells[neighbor]
                    current = neighbor

        breadcrumbs.compute_max()
        return breadcrumbs

    def compute_max(self):
        """returns the furthest and the longest distances found"""
        max_distance = 0
        max_cell = self.root
        for cell, distance in self.cells.items():
            if distance > max_distance:
                max_distance = distance
                max_cell = cell

        self.max_distance = max_distance
        self.max_cell = max_cell
