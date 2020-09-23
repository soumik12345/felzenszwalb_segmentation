import numpy as np
from math import ceil, exp, pow


def convolve(src, mask):
    output = np.zeros(shape=src.shape, dtype=float)
    height, width = src.shape
    length = len(mask)
    for y in range(height):
        for x in range(width):
            sum = float(mask[0] * src[y, x])
            for i in range(1, length):
                sum += mask[i] * (
                    src[y, max(x - i, 0)] + src[y, min(x + i, width - 1)])
            output[y, x] = sum
    return output


def normalize(mask):
    sum = 2 * np.sum(np.absolute(mask)) + abs(mask[0])
    return np.divide(mask, sum)


def smoothen(src, sigma):
    mask = make_gaussian_filter(sigma)
    mask = normalize(mask)
    tmp = convolve(src, mask)
    dst = convolve(tmp, mask)
    return dst


def make_gaussian_filter(sigma):
    sigma = max(sigma, 0.01)
    length = int(ceil(sigma * 4.0)) + 1
    mask = np.zeros(shape=length, dtype=float)
    for i in range(length):
        mask[i] = exp(-0.5 * pow(i / sigma, i / sigma))
    return mask
