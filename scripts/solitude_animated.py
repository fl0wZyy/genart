import math
import concurrent.futures
import random

from numpy.polynomial import Polynomial, polynomial
from PIL import Image, ImageDraw
import numpy as np


def newton(coefficients, step, guess, a):
    poly = Polynomial(coefficients)
    deriv = Polynomial.deriv(poly)
    deriv_coeff = []
    for coeff in deriv:
        deriv_coeff.append(coeff)
    if step:
        poly_value = polynomial.polyval(guess, coefficients)
        deriv_value = polynomial.polyval(guess, deriv_coeff)
        new_guess = guess - a * (poly_value / deriv_value)
        guess = newton(coefficients, step - 1, new_guess, a)
    return guess


def create_canvas(canvas_size, canvas_bg_color):
    canvas_element = Image.new("RGB", canvas_size, canvas_bg_color)
    return canvas_element


def gravity(re_axis, im_axis, iteration, colors, detail_level, a):
    roots = Polynomial([1, 0, 0, -1]).roots()
    im_array_colored = np.zeros((len(re_axis), len(im_axis)) + (3,))
    for x in range(len(re_axis)):
        for y in range(len(im_axis)):
            pixel_complex = complex(re_axis[x], im_axis[y])
            guess = newton([1, 0, 0, -1], detail_level, pixel_complex, a)
            distances = []
            for root in roots:
                c = guess - root
                distances.append(math.sqrt(c.real ** 2 + c.imag ** 2))

            min_distance_index = min(range(len(distances)), key=distances.__getitem__)
            min_distance = distances[min_distance_index]
            base_color = colors[min_distance_index]
            red = max(int(base_color[0] * (max(distances) - min_distance)), 0)
            blue = max(int(base_color[1] * (max(distances) - min_distance)), 0)
            green = max(int(base_color[2] * (max(distances) - min_distance)), 0)
            color = (red, blue, green)
            im_array_colored[x, y] = color
    return im_array_colored, iteration


if __name__ == "__main__":
    w = 200
    h = 200
    scope = np.linspace(1, 0, 1)
    colors = [(random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)) for _ in range(3)]
    images = []
    for a in range(-10, 10, 1):
        detail = 5
        a_level = a/100
        results = []
        re = np.linspace(-1, 1, w)
        im = np.linspace(-1, 1, h)
        increment = int(len(re) / 20)
        with concurrent.futures.ProcessPoolExecutor() as executor:
            for i in range(20):
                results.append(executor.submit(gravity, re[i * increment:increment * (i + 1)], im, i, colors, detail, a_level))

        arrays = [0 for i in range(20)]
        for count, f in enumerate(concurrent.futures.as_completed(results)):
            array, rank = f.result()
            array_int = array.astype(np.uint8)
            arrays[rank] = array_int
        stacked = np.concatenate(arrays)
        image = Image.fromarray(stacked)
        images.append(image)

    final = images
    for k in reversed(images):
        final.append(k)

    final[0].save('solitude.gif', save_all=True, append_images=final[1:], optimize=False, duration=100, loop=0)
