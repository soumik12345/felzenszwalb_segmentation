import numpy as np
from .disjoint_set import DisjointSet
from .utils import smoothen, difference, get_random_rgb_image


def segment_graph(num_vertices, num_edges, edges, c):
    edges[0 : num_edges, :] = edges[edges[0 : num_edges, 2].argsort()]
    u = DisjointSet(num_vertices)
    threshold = np.zeros(shape=num_vertices, dtype=float)
    for i in range(num_vertices):
        threshold[i] = c
    for i in range(num_edges):
        pedge = edges[i, :]
        a = u.find(pedge[0])
        b = u.find(pedge[1])
        if a != b:
            if (pedge[2] <= threshold[a]) and (pedge[2] <= threshold[b]):
                u.join(a, b)
                a = u.find(a)
                threshold[a] = pedge[2] + (c / u.size(a))
    return u


def segment(in_image, sigma, k, min_size):
    height, width, band = in_image.shape
    smooth_red_band = smoothen(in_image[:, :, 0], sigma)
    smooth_green_band = smoothen(in_image[:, :, 1], sigma)
    smooth_blue_band = smoothen(in_image[:, :, 2], sigma)
    # build graph
    edges_size = width * height * 4
    edges = np.zeros(shape=(edges_size, 3), dtype=object)
    num = 0
    for y in range(height):
        for x in range(width):
            if x < width - 1:
                edges[num, 0] = int(y * width + x)
                edges[num, 1] = int(y * width + (x + 1))
                edges[num, 2] = difference(
                    smooth_red_band, smooth_green_band,
                    smooth_blue_band, x, y, x + 1, y
                )
                num += 1
            if y < height - 1:
                edges[num, 0] = int(y * width + x)
                edges[num, 1] = int((y + 1) * width + x)
                edges[num, 2] = difference(
                    smooth_red_band, smooth_green_band,
                    smooth_blue_band, x, y, x, y + 1
                )
                num += 1
            if (x < width - 1) and (y < height - 2):
                edges[num, 0] = int(y * width + x)
                edges[num, 1] = int((y + 1) * width + (x + 1))
                edges[num, 2] = difference(
                    smooth_red_band, smooth_green_band,
                    smooth_blue_band, x, y, x + 1, y + 1
                )
                num += 1
            if (x < width - 1) and (y > 0):
                edges[num, 0] = int(y * width + x)
                edges[num, 1] = int((y - 1) * width + (x + 1))
                edges[num, 2] = difference(
                    smooth_red_band, smooth_green_band,
                    smooth_blue_band, x, y, x + 1, y - 1
                )
                num += 1
    u = segment_graph(width * height, num, edges, k)
    for i in range(num):
        a = u.find(edges[i, 0])
        b = u.find(edges[i, 1])
        if (a != b) and ((u.size(a) < min_size) or (u.size(b) < min_size)):
            u.join(a, b)
    num_cc = u.num_sets()
    output = np.zeros(shape=(height, width, 3))

    colors = np.zeros(shape=(height * width, 3))
    for i in range(height * width):
        colors[i, :] = get_random_rgb_image()
    for y in range(height):
        for x in range(width):
            comp = u.find(y * width + x)
            output[y, x, :] = colors[comp, :]
    return output
