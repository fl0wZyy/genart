import math
from PIL import Image
import numpy as np
import colorsys
import random


def hsv_to_rgb(h, s, v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h, s, v))


def newton_trig(step, guess):
    if step:
        poly_value = np.cosh(guess) - 1
        deriv_value = np.sinh(guess)
        new_guess = guess - poly_value / deriv_value
        guess = newton_trig(step - 1, new_guess)
    return guess


def create_canvas(canvas_size, canvas_bg_color):
    canvas_element = Image.new("RGB", canvas_size, canvas_bg_color)
    return canvas_element


def gravity(re_axis, im_axis, colors, threshold):
    im_array_colored = np.zeros((len(re_axis), len(im_axis)) + (3,))
    roots = [complex(0, np.pi / 2 + k * np.pi) for k in range(-5, 5)]
    for x in range(len(re_axis)):
        for y in range(len(im_axis)):
            pixel_complex = complex(re_axis[x], im_axis[y])
            guess = newton_trig(threshold, pixel_complex)
            distances = []
            for root in roots:
                c = guess - root
                distances.append(math.sqrt(c.real ** 2 + c.imag ** 2))
            color = colors[min(range(len(distances)), key=distances.__getitem__)]
            value = min(1, abs((10 - min(range(len(distances)), key=distances.__getitem__)) / 10))
            color = tuple([int(value * x) for x in color])
            im_array_colored[x, y] = color
    return im_array_colored


if __name__ == "__main__":
    images = []
    w = 2436
    h = 1125
    colors = [(248, 177, 149), (246, 114, 128), (192, 108, 132), (108, 91, 123), (53, 92, 125), (225, 245, 196),
              (237, 229, 116), (249, 212, 35), (252, 145, 58), (212, 145, 58), (252, 145, 112), (200, 200, 200)]

    re = np.linspace(-1.08, 1.08, w)
    im = np.linspace(-3.5, -2.75, h)
    array = gravity(re, im, colors, 100)
    array_int = array.astype(np.uint8)
    image = Image.fromarray(array_int)
    image.save("iPhone_11.png")
