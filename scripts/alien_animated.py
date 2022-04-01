import math
import concurrent.futures
from PIL import Image
import numpy as np
import colorsys


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


def gravity(re_axis, im_axis, iteration, colors, threshold):
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
    return im_array_colored, iteration


if __name__ == "__main__":
    images = []
    w = 200
    h = 200
    colors = [(248, 177, 149), (246, 114, 128), (192, 108, 132), (108, 91, 123), (53, 92, 125), (225, 245, 196),
              (237, 229, 116), (249, 212, 35), (252, 145, 58), (212, 145, 58), (252, 145, 112), (200, 200, 200)]

    re = np.linspace(-0.375, 0.375, w)
    im = np.linspace(-3.5, -2.75, h)
    increment = int(len(re) / 15)

    for frame in range(49, 50):
        results = []
        with concurrent.futures.ProcessPoolExecutor() as executor:
            for i in range(15):
                results.append(executor.submit(gravity, re[i * increment:increment * (i + 1)], im, i, colors, frame))

        arrays = [0 for i in range(15)]
        for count, f in enumerate(concurrent.futures.as_completed(results)):
            array, rank = f.result()
            array_int = array.astype(np.uint8)
            arrays[rank] = array_int
        stacked = np.concatenate(arrays)
        rotated = np.rot90(stacked)
        image = Image.fromarray(rotated)
        images.append(image)

    images[0].save('dawn.gif', save_all=True, append_images=images[1:], optimize=False, duration=80, loop=0)
