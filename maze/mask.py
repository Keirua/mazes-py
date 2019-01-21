import random

from maze.rectangulargrid import RectangularGrid, Cell, RectangularCell
from PIL import Image

class Mask:
    def __init__(self, rows=10, columns=10):
        self.rows = rows
        self.columns = columns
        self.bits = []
        for i in range(rows):
            cols = [True] * columns
            self.bits.append(cols)

    def __getitem__(self, item):
        if 0 <= item[0] < self.rows and 0 <= item[1] < self.columns:
            return self.bits[item[0]][item[1]]
        return None

    def __setitem__(self, key, value):
        if 0 <= key[0] < self.rows and 0 <= key[1] < self.columns:
            self.bits[key[0]][key[1]] = value

    def random_cell(self):
        while True:
            r, c = random.randint(0, self.rows), random.randint(0, self.columns)
            if self[(r,c)]:
                return r, c

    @staticmethod
    def from_textfile(filename):
        with open(filename) as f:
            lines = f.readlines()
            lines = [l.strip() for l in lines]

            rows = len(lines)
            cols = len(lines[0])
            mask = Mask(rows, cols)

            for r in range(rows):
                for c in range(cols):
                    if lines[r][c] == 'x':
                        mask[(r, c)] = False

            return mask

    @staticmethod
    def from_image(filename):
        img = Image.open(filename)
        print(img.getcolors())

        cols, rows = img.size
        mask = Mask(rows, cols)

        print(img.size)

        for r in range(rows):
            for c in range(cols):
                pixel = img.getpixel((c, r))
                if pixel == (0, 0, 0, 255):
                    mask[(r, c)] = False

        return mask


class MaskedGrid(RectangularGrid):
    def __init__(self, mask):
        self.mask = mask
        super().__init__(mask.rows, mask.columns)

    def prepare_grid(self):
        for r in range(self.rows):
            line = []
            for c in range(self.columns):
                if self.mask[(r, c)]:
                    line.append(RectangularCell(r, c))
                else:
                    line.append(None)
            self.grid.append(line)

    def random_cell(self):
        r, c = self.mask.random_cell()

        return self.grid[r][c]

