import random
from PIL import Image, ImageDraw
import numpy as np
import colorsys


def hsv_to_rgb(h, s, v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h, s, v))


def create_canvas(canvas_size, canvas_bg_color):
    canvas_element = Image.new("RGB", canvas_size, canvas_bg_color)
    return canvas_element


def rotate_vector(f, t):
    x = -2 * np.pi * f * t
    return complex(np.cos(x), np.sin(x))


def linear_interp(x1, x2, y1, y2, a):
    x = a * (x1 + x2)
    if x1 != x2:
        return tuple((x, (y1 * (x2 - x) + y2 * (x - x2)) / (x2 - x1)))
    else:
        return tuple((x, y1))


final = []
for frame in range(60):
    canvas = create_canvas((2000, 2000), (0, 0, 0))
    draw = ImageDraw.Draw(canvas)
    points_a = []
    for time in range(2000):
        base_trig = np.sin(2*time / 1000) + np.sin(4*time / 1000)
        c = base_trig * rotate_vector(frame / 60, time / 1000)
        points_a.append(tuple((585 + (250 * c.real), 585 + (250 * c.imag))))

    points_b = []
    for time in range(5000):
        base_trig = np.sin(2*time / 1000)+np.sin(6*time / 1000)
        c = base_trig * rotate_vector(frame / 60, time / 1000)
        points_b.append(tuple((1000 + (250 * c.real), 1250 + (250 * c.imag))))

    points_c = []
    for time in range(5000):
        base_trig = np.sin(2*time / 1000) + np.sin(8*time / 1000)
        c = base_trig * rotate_vector(frame / 60, time / 1000)
        points_c.append(tuple((1600 + (250 * c.real), 1700 + (250 * c.imag))))

    for i in range(len(points_a)):
        point_a = points_a[i]
        point_b = points_b[i]
        point_c = points_c[i]
        dist = np.sqrt(((point_a[0] - point_b[0]) ** 2 + (point_a[1] - point_b[1]) ** 2))
        dist_2 = np.sqrt(((point_b[0] - point_c[0]) ** 2 + (point_b[1] - point_c[1]) ** 2))
        between = [point_a]
        between_2 = [point_a]
        for j in range(5):
            x_c = point_a[0] + ((point_b[0] - point_a[0]) / 5) * j + random.randint(-20, 20)
            y_c = point_a[1] + ((point_b[1] - point_a[1]) / 5) * j + random.randint(-20, 20)
            x_d = point_b[0] + ((point_c[0] - point_b[0]) / 5) * j + random.randint(-20, 20)
            y_d = point_b[1] + ((point_c[1] - point_b[1]) / 5) * j + random.randint(-20, 20)

            point_c = tuple((x_c, y_c))
            point_d = tuple((x_d, y_d))
            between.append(point_c)
            between_2.append(point_d)
        between.append(point_b)
        between_2.append(point_b)
        dist_3 = np.sqrt(point_a[0]**2 + point_a[1]**2)
        dist_4 = np.sqrt(point_b[0] ** 2 + point_b[1] ** 2)
        draw.polygon(between, fill=hsv_to_rgb(dist / 2000, dist_3/2000, 1))
        draw.polygon(between, fill=hsv_to_rgb(dist_2 / 2000, dist_4/2000, 1))
    final.append(canvas)

final[0].save('fourier.gif', save_all=True, append_images=final[1:], optimize=False, duration=64, loop=0)
