import numpy as np
import math
from PIL import Image, ImageDraw, ImageFilter
import colorsys
import random


def create_canvas(canvas_size, canvas_bg_color):
    canvas_element = Image.new("RGB", canvas_size, canvas_bg_color)
    return canvas_element


def hsv_to_rgb(h, s, v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h, s, v))


def draw_sinusoid(canvas, A, k, omega, phi, time):
    points = []
    draw = ImageDraw.Draw(canvas)
    for x in range(canvas.width):
        y = A * np.sin(k * x + omega * time + phi)
        points.append((x, y + canvas.height / 2))
    draw.line(points, fill=(45, 53, 47), width=5, joint="curve")


def draw_tangents(canvas, A, k, omega, phi, time):
    draw = ImageDraw.Draw(canvas)
    for x in range(canvas.width):
        tangent = A * np.cos(k * x + omega * time + phi) * k
        y = A * np.sin(k * x + omega * time + phi) + canvas.height / 2
        color = hsv_to_rgb(y / A, 1, y / A)
        x_2 = 0
        y_2 = tangent * (x_2 - x) + y
        draw.line([(x, y), (x_2, y_2)], fill=color, width = 1)
        x_3 = canvas.width
        y_3 = tangent * (x_3 - x) + y
        draw.line([(x, y), (x_3, y_3)], fill=color, width = 1)


images = []
dt = 5
for time in range(100):
    dt += 0.01
    image = create_canvas((2000, 2000), (0, 0, 0))
    draw_tangents(image, 200, 0.0005 * time, 2, math.radians(0), dt)
    blurImg = image.filter(ImageFilter.GaussianBlur(radius=10))
    images.append(blurImg)
images[0].save('vice.gif',
               save_all=True, append_images=images[1:], optimize=False, duration=167, loop=0)
