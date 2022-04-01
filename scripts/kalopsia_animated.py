from PIL import Image, ImageDraw
import math
import colorsys
import numpy as np


def clamp(x):
    return max(0, min(x, 255))


def combine_hex_values(d):
    d_items = sorted(d.items())
    tot_weight = sum(d.values())
    red = int(sum([int(k[:2], 16) * v for k, v in d_items]) / tot_weight)
    green = int(sum([int(k[2:4], 16) * v for k, v in d_items]) / tot_weight)
    blue = int(sum([int(k[4:6], 16) * v for k, v in d_items]) / tot_weight)
    zpad = lambda x: x if len(x) == 2 else '0' + x
    return zpad(hex(red)[2:]) + zpad(hex(green)[2:]) + zpad(hex(blue)[2:])


def hsv_to_rgb(h, s, v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h, s, v))


def create_canvas(canvas_size, canvas_bg_color):
    canvas_element = Image.new("RGBA", canvas_size, canvas_bg_color)
    return canvas_element


def apply_wave_function(width, height, wave_origins, amplitude, omega, rho, wavelength, time):
    k = 2 * np.pi / wavelength
    x = np.linspace(0, width, width)
    y = np.linspace(0, height, height)
    xx, yy = np.meshgrid(x, y)
    displacements = []
    for origin in wave_origins:
        distance = np.sqrt(np.square(xx - origin[0]) + np.square(yy - origin[1]))
        displacement = (amplitude * np.cos(k * distance - omega * time + rho)) / np.sqrt(distance)
        displacements.append(displacement)
    return displacements


def draw_waves(canvas_element, wave_origins, amplitude, frequency, rho, wavelength, time):
    size = canvas_element.size
    omega = math.radians(2 * np.pi * frequency)
    displacement_matrix = np.array(
        apply_wave_function(size[0], size[1], wave_origins, amplitude, omega, rho, wavelength, time))
    for y in range(0, len(displacement_matrix[0]), 1):
        for x in range(0, len(displacement_matrix[0][0]), 1):
            total_displacement = displacement_matrix[0][y][x] + displacement_matrix[1][y][x] + \
                                 displacement_matrix[2][y][x]
            total_displacement_abs = abs(displacement_matrix[0][y][x]) + abs(displacement_matrix[1][y][x]) + abs(
                displacement_matrix[2][y][x])
            color_1 = hsv_to_rgb(0.11, 1, total_displacement / 50)
            color_2 = hsv_to_rgb(0.61, 1, total_displacement / 50)
            color_3 = hsv_to_rgb(0.75, 1, total_displacement / 50)
            color_1_hex = "{0:02x}{1:02x}{2:02x}".format(clamp(color_1[0]), clamp(color_1[1]), clamp(color_1[2]))
            color_2_hex = "{0:02x}{1:02x}{2:02x}".format(clamp(color_2[0]), clamp(color_2[1]), clamp(color_2[2]))
            color_3_hex = "{0:02x}{1:02x}{2:02x}".format(clamp(color_3[0]), clamp(color_3[1]), clamp(color_3[2]))
            colors = {color_1_hex: abs(displacement_matrix[0][y][x]) / total_displacement_abs,
                      color_2_hex: abs(displacement_matrix[1][y][x]) / total_displacement_abs,
                      color_3_hex: abs(displacement_matrix[2][y][x]) / total_displacement_abs}
            color_hex = combine_hex_values(colors)
            color = tuple(int(color_hex[i:i + 2], 16) for i in (0, 2, 4))
            draw = ImageDraw.Draw(canvas_element)
            draw.point((x, y), fill=color)
    canvas.save("wave_{f}.png".format(f=time))


canvas = create_canvas((1280, 1080), (0, 0, 0))

wave_1 = [500, 500, 100, 500, 500]
wave_2 = [550, 550, 50, 550, 550]
wave_3 = [700, 300, 100, 700, 300]
space_transform = 2
time = 0
for angle in np.linspace(0, 360, 30):
    wave_1[0] = wave_1[3] + (wave_1[2]) * math.cos(math.radians(angle))
    wave_1[1] = wave_1[4] + (wave_1[2]) * math.sin(math.radians(angle))
    wave_2[0] = wave_2[3] + (wave_2[2]) * math.cos(math.radians(angle)) * -1
    wave_2[1] = wave_2[4] + (wave_2[2]) * math.sin(math.radians(angle)) * -1
    wave_3[0] = wave_3[3] + (wave_3[2]) * math.cos(math.radians(angle))
    wave_3[1] = wave_3[4] + (wave_3[2]) * math.sin(math.radians(angle))
    wave_origins = [[wave_1[0], wave_1[1]], [wave_2[0], wave_2[1]], [wave_3[0], wave_3[1]]]
    draw_waves(canvas, wave_origins, 1000, 1000, 0, 30, time)
    time += 10
