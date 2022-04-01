import numpy as np
import matplotlib.pyplot as plt
import concurrent.futures
from PIL import Image
import colorsys


def mandelbrot(x, y, threshold):
    """Calculates whether the number c = x + i*y belongs to the
    Mandelbrot set. In order to belong, the sequence z[i + 1] = z[i]**2 + c
    must not diverge after 'threshold' number of steps. The sequence diverges
    if the absolute value of z[i+1] is greater than 4.

    :param float x: the x component of the initial complex number
    :param float y: the y component of the initial complex number
    :param int threshold: the number of iterations to considered it converged
    """
    # initial conditions
    c = complex(x, y)
    z = complex(0, 0)

    for i in range(threshold):
        z = z ** 2 + c
        if abs(z) > 4:  # it diverged
            return i

    return threshold - 1  # it didn't diverge


def hsv_to_rgb(h, s, v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h, s, v))


def draw_mandelbrot_animated(width, height, frames, beginning_frame, ending_frame, inc):
    images_output = []
    cm = plt.get_cmap('magma')
    re = np.linspace(-0.1, 0.1, width)
    im = np.linspace(-0.1, 0.1, height)
    for frame in range(beginning_frame, ending_frame):
        im_array_colored = np.zeros((len(re), len(im)) + (3,))
        current_threshold = round(1.1 ** (frame + 1))
        for i in range(len(re)):
            for j in range(len(im)):
                value = mandelbrot(re[i], im[j], current_threshold) / current_threshold
                im_array_colored[i, j] = (255*value, 255*value, 255*value)

        im_array_colored_int = im_array_colored.astype(np.uint8)
        images_output.append(Image.fromarray(im_array_colored_int))
    return images_output, inc


if __name__ == "__main__":
    results = []
    increment = int(50 / 10)
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for i in range(10):
            results.append(
                executor.submit(draw_mandelbrot_animated, 100, 100, 50, increment * i, increment * (i + 1), i))
    arrays = [[] for i in range(10)]
    for count, f in enumerate(concurrent.futures.as_completed(results)):
        array, rank = f.result()
        arrays[rank] = array
    final_images = ["" for i in range(50)]
    for array_index in range(len(arrays)):
        for image_index in range(len(arrays[array_index])):
            final_images[array_index * 5 + image_index] = arrays[array_index][image_index]

    final_images[0].save('boundless_mono.gif',
                         save_all=True, append_images=final_images[1:], optimize=False, duration=100, loop=0)
