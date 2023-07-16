import math
from dataclasses import dataclass
from typing import List
import os
from PIL import Image, ImageDraw
import svgwrite
from maze.grid import RectangularGrid, TriangleWithRectangularShapeGrid

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


class Shape:
    pass


@dataclass
class BoundingBox(Shape):
    x_min: int
    y_min: int
    x_max: int
    y_max: int


@dataclass
class Line(Shape):
    x1: int
    y1: int
    x2: int
    y2: int


class ShapeFormatter:
    @staticmethod
    def save_image(grid: RectangularGrid, cell_size=10) -> (List[Shape], BoundingBox):
        walls: List[Shape] = []
        bbox = BoundingBox(x_min=0, y_min=0, x_max=1 + grid.columns * cell_size, y_max=1 + grid.rows * cell_size)

        # Then we draw the cell borders and content
        for cell in grid.each_cell():
            x1, y1, x2, y2 = cell.get_bounding_box(cell_size)

            if not cell.north:
                walls.append(Line(x1=x1, y1=y1, x2=x2, y2=y1))
            if not cell.west:
                walls.append(Line(x1=x1, y1=y1, x2=x1, y2=y2))
            if not cell.has_link(cell.east):
                walls.append(Line(x1=x2, y1=y1, x2=x2, y2=y2))
            if not cell.has_link(cell.south):
                walls.append(Line(x1=x1, y1=y2, x2=x2, y2=y2))

        return walls, bbox


class ImageSaver:
    def save_image(self, shapes: List[Shape], filename: str):
        """
        Save the actual image to a file
        """
        raise NotImplemented


class PNGImageSaver(ImageSaver):
    def save_image(self, shapes: List[Shape], bbox: BoundingBox, filename: str):
        wall_color = (0, 0, 0)
        background_color = (255, 255, 255)

        im = Image.new("RGB", (bbox.x_max, bbox.y_max), background_color)
        draw = ImageDraw.Draw(im)

        for shape in shapes:
            if type(shape) == Line:
                shape: Line = shape
                draw.line((shape.x1, shape.y1, shape.x2, shape.y2), fill=wall_color)

        im.save(filename, "PNG")


class SVGImageSaver(ImageSaver):
    def save_image(self, shapes: List[Shape], bbox: BoundingBox, filename: str):
        dwg = svgwrite.Drawing(filename, profile='tiny')

        wall_color = svgwrite.rgb(0, 0, 0, '%')
        for shape in shapes:
            if type(shape) == Line:
                shape: Line = shape
                dwg.add(dwg.line((shape.x1, shape.y1), (shape.x2, shape.y2), stroke=wall_color))

        dwg.save()


class ImageSaverFactory:
    @staticmethod
    def create(filename: str) -> ImageSaver:
        mapping = {
            ".svg": SVGImageSaver,
            ".png": PNGImageSaver
        }
        path, extension = os.path.splitext(filename)
        if extension.lower() in mapping.keys():
            return mapping[extension.lower()]()

        raise ValueError(f"output format for {extension} is not supported")



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
    def save_image(grid: TriangleWithRectangularShapeGrid, filename, cell_size=10):
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
