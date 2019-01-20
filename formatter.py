from grid import Grid
from PIL import Image, ImageDraw


class StringFormatter:
    @staticmethod
    def to_string(grid: Grid):
        output = "+" + "---+" * grid.rows + "\n"
        for row in grid.each_rows():
            top = "|"
            bottom = "+"
            for cell in row:
                body = " {} ".format(grid.content_of(cell))
                east_boundary = " " if cell.has_link(cell.east) else "|"
                top += body + east_boundary
                south_boundary = " " * 3 if cell.has_link(cell.south) else "-" * 3
                bottom += south_boundary + "+"
            output += top + "\n"
            output += bottom + "\n"

        return output


class ImageFormatter:

    @staticmethod
    def save_image(grid:Grid, filename, cell_size=10):
        wall_color = (0, 0, 0)
        background_color = (255, 255, 255)

        im = Image.new("RGB", (1 + grid.rows * cell_size, 1 + grid.columns * cell_size), background_color)
        draw = ImageDraw.Draw(im)
        for cell in grid.each_cell():
            x1 = cell.column * cell_size
            y1 = cell.row * cell_size
            x2 = (cell.column + 1) * cell_size
            y2 = (cell.row + 1) * cell_size
            if not cell.north:
                draw.line((x1, y1, x2, y1), fill=wall_color)
            if not cell.west:
                draw.line((x1, y1, x1, y2), fill=wall_color)
            if not cell.has_link(cell.east):
                draw.line((x2, y1, x2, y2), fill=wall_color)
            if not cell.has_link(cell.south):
                draw.line((x1, y2, x2, y2), fill=wall_color)
            draw.text((x1 + cell_size/2, y1+ cell_size/2), grid.content_of(cell), fill=wall_color)

        im.save(filename, "PNG")
