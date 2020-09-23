import numpy as np
from math import sqrt
from random import randint


def difference(red_band, green_band, blue_band, x1, y1, x2, y2):
    return sqrt(
        (red_band[y1, x1] - red_band[y2, x2]) ** 2 +\
            (green_band[y1, x1] - green_band[y2, x2]) ** 2 +\
                (blue_band[y1, x1] - blue_band[y2, x2]) ** 2
    )


def get_random_rgb_image():
    rgb = np.zeros(3, dtype=int)
    rgb[0] = randint(0, 255)
    rgb[1] = randint(0, 255)
    rgb[2] = randint(0, 255)
    return rgb


def get_random_gray_image():
    gray = np.zeros(1, dtype=int)
    gray[0] = randint(0, 255)
    return gray
