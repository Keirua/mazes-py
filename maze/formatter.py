from maze.grid import Grid
from PIL import Image, ImageDraw


# taken here
# http://code.activestate.com/recipes/65212/
def baseN(num, b, numerals="0123456789abcdefghijklmnopqrstuvwxyz"):
    if num == " ":
        return " "
    return ((num == 0) and "0") or (baseN(num // b, b).lstrip("0") + numerals[num % b])


class StringFormatter:
    @staticmethod
    def to_string(grid: Grid):
        output = "+" + "---+" * grid.rows + "\n"
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
    def save_image(grid: Grid, filename, cell_size=10):
        wall_color = (0, 0, 0)
        background_color = (255, 255, 255)

        im = Image.new("RGB", (1 + grid.rows * cell_size, 1 + grid.columns * cell_size), background_color)
        draw = ImageDraw.Draw(im)
        # font = ImageFont.load_default()

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
