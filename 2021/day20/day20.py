import numpy as np
from functools import partial

VICINITY = [(y, x) for y in range(-2, 1) for x in range(-2, 1)]  # [(y, x), ...] in order of magnitude


def get_or_background(y, x, image, background):
    if 0 <= y < image.shape[0] and 0 <= x < image.shape[1]:
        return image[y, x]
    else:
        return background


def enhance(image, background, enhancement):
    """
    :param image: A two-dimensional numpy array containing the non-background pixels, with 1 for lit and 0 for dark
    :param background: A boolean representing the colour of the infinitely many background pixels
    :param enhancement: A list representing the enhancement algorithm
    :return: A tuple of an image of length and width two more than the original image, and a background
    """

    new_image = np.empty((image.shape[0]+2,)*2, dtype=np.int8)
    # We work with coords in the new image, and correct by treating the vicinity as -2..+0 rather than -1..+1
    for y, x in np.ndindex(*new_image.shape):
        enhancement_index = 0
        for dy, dx in VICINITY:
            enhancement_index <<= 1
            enhancement_index |= get_or_background(y + dy, x + dx, image, background)
        new_image[y][x] = enhancement[enhancement_index]

    background = enhancement[-background]  # Gets 0th rule if background is 0, and last rule if background is 1
    return new_image, background


def parse_inp(inp):
    enhancement = [+(i == "#") for i in inp[0]]  # Unary + converts bool to int
    image = np.array([[+(i == "#") for i in line] for line in inp[2:]])
    return enhancement, image


def do_it(inp, steps):
    enhancement, image = parse_inp(inp)
    background = 0
    for _ in range(steps):
        image, background = enhance(image, background, enhancement)
    assert background == 0
    return image.sum()


part_a = partial(do_it, steps=2)
part_b = partial(do_it, steps=50)
