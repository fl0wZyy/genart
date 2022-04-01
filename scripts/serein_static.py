import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from PIL import Image, ImageDraw, ImageColor
import colorsys


def julia_quadratic(zx, zy, cx, cy, threshold):
    z = complex(zx, zy)
    c = complex(cx, cy)

    for i in range(threshold):
        z = z ** 2 + c
        if abs(z) > 4.:  # it diverged
            return i

    return threshold - 1


def hsv_to_rgb(h, s, v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h, s, v))


def draw_julia(width, height, frames, threshold, r, frame):
    images_output = []
    re = np.linspace(-2, 2, width)
    im = np.linspace(-2, 2, height)
    a = np.linspace(0, 2 * np.pi, frames)
    im_array_colored = np.zeros((len(re), len(im)) + (3,))
    cx, cy = r * np.cos(a[frame]), r * np.sin(a[frame])
    for i in range(len(re)):
        for j in range(len(im)):
            value = julia_quadratic(re[i], im[j], cx, cy, threshold) / threshold
            im_array_colored[i, j] = (int(255*value), int(255*value), int(255*value))

    im_array_colored_int = im_array_colored.astype(np.uint8)
    image = Image.fromarray(im_array_colored_int)
    image.save(f"julia_frame_{frame}.png")
    return images_output


draw_julia(2000, 2000, 100, 20, 0.7885, 90)
