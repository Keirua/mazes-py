import math

from PIL import Image, ImageDraw

from maze.grid import RectangularGrid, TriangleGrid

RGB_BLACK = (0, 0, 0)

RGB_WHITE = (255, 255, 255)


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

            # text_width, text_height = draw.textsize(str(grid.content_of(cell)))
            # text_coords = (x1 + cell_size / 2 - text_width / 2, y1 + cell_size / 2 - text_height / 2)
            # draw.text(text_coords, str(grid.content_of(cell)), fill=wall_color)

        im.save(filename, "PNG")


class PolarGridImageFormatter:
    @staticmethod
    def save_image(grid: RectangularGrid, filename, cell_size=10):
        wall_color = RGB_BLACK
        background_color = RGB_WHITE
        image_size = 2 * grid.rows * cell_size
        center = image_size / 2

        im = Image.new("RGB", (1 + image_size, 1 + image_size), background_color)
        draw = ImageDraw.Draw(im)

        for cell in grid.each_cell():
            if cell.row == 0:
                continue
            theta = 2 * math.pi / len(grid.grid[cell.row])
            inner_radius = cell.row * cell_size
            outer_radius = (1 + cell.row) * cell_size
            theta_ccw = cell.column * theta
            theta_cw = (cell.column + 1) * theta

            cx = center + int(inner_radius * math.cos(theta_cw))
            cy = center + int(inner_radius * math.sin(theta_cw))
            dx = center + int(outer_radius * math.cos(theta_cw))
            dy = center + int(outer_radius * math.sin(theta_cw))

            ax, ay = center - inner_radius, center - inner_radius
            bx, by = center + inner_radius, center + inner_radius
            if cell.has_link(cell.inward):
                draw.arc((ax, ay, bx, by), theta_ccw * 180 / math.pi, theta_cw * 180 / math.pi, fill=wall_color)

            if cell.has_link(cell.cw):
                draw.line((cx, cy, dx, dy), fill=wall_color)
            draw.arc((0, 0, image_size, image_size), 0, 360, fill=wall_color)

        im.save(filename, "PNG")


class TriangleGridImageFormatter:
    @staticmethod
    def save_image(grid: TriangleGrid, filename, cell_size=10):
        half_width = cell_size / 2.0
        height = cell_size * math.sqrt(3) / 2.0
        half_height = height / 2.0

        wall_color = RGB_BLACK
        background_color = RGB_WHITE
        image_width = int(cell_size * (grid.columns + 1) / 2.0)
        image_height = int(height * grid.rows)

        im = Image.new("RGB", (1 + image_width, 1 + image_height), background_color)
        draw = ImageDraw.Draw(im)

        for cell in grid.each_cell():
            cx = half_width + cell.column * half_width
            cy = half_height + cell.row * height
            west_x = int(cx - half_width)
            mid_x = int(cx)
            east_x = int(cx + half_width)

            apex_y = int(cy + half_height)
            base_y = int(cy - half_height)
            if cell.is_upright:
                apex_y = int(cy - half_height)
                base_y = int(cy + half_height)
            # points = [(west_x, base_y), (mid_x, apex_y), (east_x, base_y)]
            # draw.polygon(points)

            if not cell.west:
                draw.line((west_x, base_y, mid_x, apex_y), fill=wall_color)
            if not cell.has_link(cell.east):
                draw.line((east_x, base_y, mid_x, apex_y), fill=wall_color)
            no_south = cell.is_upright and cell.south is None
            not_linked = not cell.is_upright and not cell.has_link(cell.north)

            if no_south or not_linked:
                draw.line((east_x, base_y, west_x, base_y), fill=wall_color)

        im.save(filename, "PNG")
