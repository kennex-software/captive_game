#! python 3
# kennex
#

import random

def whitespace(surface, x, y, h, w):
    pixel_size = 2
    pixel_length = w / pixel_size
    pixel_height = h / pixel_size
    start = x

    pixel_grid = [[1]*int(pixel_height) for n in range(int(pixel_length))]


    colors = [(255, 255, 255), (205, 205, 205), (155, 155, 155), (100, 100, 100)]

    for row in pixel_grid:
        for col in row:
            color = random.randint(0, 3)
            surface.fill(colors[color], ((x, y), (pixel_size, pixel_size)))
            x += pixel_size
        y += pixel_size
        x = start





