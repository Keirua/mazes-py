import sys

from maze.formatter import ImageFormatter, StringFormatter
from maze.mask import Mask, MaskedGrid
from maze.maze_generation import RecursiveBacktracker


import cv2


def write_img_b_in_a_and_scale_it_down(image_a, image_b, scale_factor=0.5):
    # Resize image b to 50% of its original size
    scaled_image_b = cv2.resize(image_b, None, fx=scale_factor, fy=scale_factor)

    # Get the dimensions of image a and scaled image b
    height_a, width_a, _ = image_a.shape
    height_b, width_b, _ = scaled_image_b.shape

    # Calculate the coordinates for placing scaled image b in the upper right corner of image a
    x_offset = width_a - width_b
    y_offset = 0

    # Place the scaled image b on image a
    image_a[y_offset:y_offset+height_b, x_offset:x_offset+width_b] = scaled_image_b

    return image_a


if __name__ == "__main__":
    # img_id = "025.png"
    if len(sys.argv) > 1:
        img_id = sys.argv[1]  # "025.png"
    else:
        raise RuntimeError("No command line parameter provided.")
    maze_generation_algorithm = RecursiveBacktracker()
    mask = Mask.from_image(f"masks/{img_id}")

    g = MaskedGrid(mask)

    maze_generation_algorithm.apply_to(g)
    g.distances = g.random_cell().compute_distances()
    g.distances.compute_max()


    # print(StringFormatter.to_string(g))
    maze_filename = f"out/masked_maze_{img_id}"
    ImageFormatter.save_image(g, maze_filename)

    maze_image = cv2.imread(maze_filename)
    initial_image = cv2.imread(f"pokemon/{img_id}")
    out = write_img_b_in_a_and_scale_it_down(maze_image, initial_image, 0.5)
    cv2.imwrite(maze_filename, out)
