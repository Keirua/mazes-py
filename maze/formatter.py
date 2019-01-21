import math

from maze.rectangulargrid import RectangularGrid
from PIL import Image, ImageDraw


# taken here
# http://code.activestate.com/recipes/65212/
def baseN(num, b, numerals="0123456789abcdefghijklmnopqrstuvwxyz"):
    if num == " ":
        return " "
    return ((num == 0) and "0") or (baseN(num // b, b).lstrip("0") + numerals[num % b])


class StringFormatter:
    @staticmethod
    def to_string(grid: RectangularGrid):
        output = "+" + "---+" * grid.columns + "\n"
        for row in grid.each_rows():
            top = "|"
            bottom = "+"
            for cell in row:
                v = grid.content_of(cell)
                body = " {} ".format(baseN(v, 36))

                east_boundary = " " if cell is not None and cell.has_link(cell.east) else "|"
                south_boundary = " " * 3 if cell is not None and cell.has_link(cell.south) else "-" * 3
                top += body + east_boundary
                bottom += south_boundary + "+"
            output += top + "\n"
            output += bottom + "\n"

        return output


class ImageFormatter:

    @staticmethod
    def save_image(grid: RectangularGrid, filename, cell_size=10):
        wall_color = (0, 0, 0)
        background_color = (255, 255, 255)

        im = Image.new("RGB", (1 + grid.columns * cell_size, 1 + grid.rows * cell_size), background_color)
        draw = ImageDraw.Draw(im)

        # First we draw the background
        for cell in grid.each_cell():
            x1, y1, x2, y2 = cell.get_bounding_box(cell_size)

            cell_bg = grid.background_color(cell)
            if cell_bg is not None:
                draw.rectangle((x1, y1, x2, y2), fill=tuple(cell_bg))

        # Then we draw the cell borders and content
        for cell in grid.each_cell():
            x1, y1, x2, y2 = cell.get_bounding_box(cell_size)

            if not cell.north:
                draw.line((x1, y1, x2, y1), fill=wall_color)
            if not cell.west:
                draw.line((x1, y1, x1, y2), fill=wall_color)
            if not cell.has_link(cell.east):
                draw.line((x2, y1, x2, y2), fill=wall_color)
            if not cell.has_link(cell.south):
                draw.line((x1, y2, x2, y2), fill=wall_color)

            text_width, text_height = draw.textsize(str(grid.content_of(cell)))
            text_coords = (x1 + cell_size / 2 - text_width / 2, y1 + cell_size / 2 - text_height / 2)
            draw.text(text_coords, str(grid.content_of(cell)), fill=wall_color)

        im.save(filename, "PNG")


class PolarGridImageFormatter:

    @staticmethod
    def save_image(grid: RectangularGrid, filename, cell_size=10):
        wall_color = (0, 0, 0)
        background_color = (255, 255, 255)
        image_size = 2 * grid.rows * cell_size
        center = image_size / 2

        im = Image.new("RGB", (1 + image_size, 1 + image_size), background_color)
        draw = ImageDraw.Draw(im)

        for cell in grid.each_cell():
            theta = 2 * math.pi / len(grid.grid[cell.row])
            inner_radius = cell.row * cell_size
            outer_radius = (1 + cell.row) * cell_size
            theta_ccw = cell.column * theta
            theta_cw = (cell.column + 1) * theta

            ax = center + int(inner_radius * math.cos(theta_ccw))
            ay = center + int(inner_radius * math.sin(theta_ccw))
            bx = center + int(outer_radius * math.cos(theta_ccw))
            by = center + int(outer_radius * math.sin(theta_ccw))
            cx = center + int(inner_radius * math.cos(theta_cw))
            cy = center + int(inner_radius * math.sin(theta_cw))
            dx = center + int(outer_radius * math.cos(theta_cw))
            dy = center + int(outer_radius * math.sin(theta_cw))

            if cell.has_link(cell.north):
                draw.line((ax, ay, cx, cy), fill=wall_color)
            if cell.has_link(cell.east):
                draw.line((cx, cy, dx, dy), fill=wall_color)
            draw.arc((0, 0, image_size, image_size), 0, 360, fill=wall_color)

        im.save(filename, "PNG")
