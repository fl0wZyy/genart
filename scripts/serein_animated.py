import numpy as np
from PIL import Image
import concurrent.futures
import colorsys
import matplotlib.pyplot as plt


def julia_quadratic(zx, zy, cx, cy, threshold):
    z = complex(zx, zy)
    c = complex(cx, cy)

    for i in range(threshold):
        z = z ** 2 + z ** 3 + c
        if abs(z) > 2.:  # it diverged
            return i

    return threshold - 1


def hsv_to_rgb(h, s, v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h, s, v))


def draw_julia_animated(width, height, frames, beginning_frame, ending_frame, threshold, r, increment):
    cm = plt.get_cmap('cubehelix')
    images_output = []
    re = np.linspace(-1.75, 0.75, width)
    im = np.linspace(-1.25, 1.25, height)
    a = np.linspace(0, 2 * np.pi, frames)
    for frame in range(beginning_frame, ending_frame):
        im_array_colored = np.zeros((len(re), len(im)))
        # im_array_colored = np.zeros((len(re), len(im)) + (3,))
        cx, cy = 0.285, frame * (0.01 / frames)
        for i in range(len(re)):
            for j in range(len(im)):
                value = julia_quadratic(re[i], im[j], cx, cy, threshold) / threshold
                im_array_colored[i, j] = value

        """im_array_colored_int = im_array_colored.astype(np.uint8)
        print(im_array_colored_int)
        images_output.append(Image.fromarray(im_array_colored_int))"""
        im_array_colored[im_array_colored < np.percentile(im_array_colored, 75)] = 0
        im_array_magma = cm(im_array_colored)
        images_output.append(Image.fromarray((im_array_magma[:, :, :3] * 255).astype(np.uint8)))

    return images_output, increment


if __name__ == "__main__":
    results = []
    increment = int(100 / 10)
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for i in range(10):
            results.append(
                executor.submit(draw_julia_animated, 2000, 2000, 5, increment * i, increment * (i + 1), 100, 0.7885, i))
    arrays = [[] for i in range(10)]
    for count, f in enumerate(concurrent.futures.as_completed(results)):
        array, rank = f.result()
        arrays[rank] = array
    final_images = ["" for i in range(100)]
    for array_index in range(len(arrays)):
        for image_index in range(len(arrays[array_index])):
            final_images[array_index * 10 + image_index] = arrays[array_index][image_index]

    final = final_images

    for i in range(len(final_images) - 1, 0, -1):
        final.append(final_images[i])

    final[0].save('serein.gif', save_all=True, append_images=final[1:], optimize=False, duration=100, loop=0)
