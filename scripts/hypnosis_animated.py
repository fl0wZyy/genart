from PIL import Image, ImageDraw, ImageColor
import math
import colorsys
import random
import numpy as np


def hsv_to_rgb(h, s, v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h, s, v))


def CreateCanvas(canvas_size, canvas_bg_color):
    canvas_element = Image.new("RGB", canvas_size, canvas_bg_color)
    return canvas_element


def ApplyWaveFunction(width, height, wave_origins, amplitude, omega, rho, wavelength, time):
    k = 2 * np.pi / wavelength
    x = np.linspace(0, width, width)
    y = np.linspace(0, height, height)
    xx, yy = np.meshgrid(x, y)
    total_displacement = 0
    for origin in wave_origins:
        distance = np.sqrt(np.square(xx - origin[0]) + np.square(yy - origin[1]))
        displacement = (amplitude * np.cos(k * distance - omega * time + rho)) / np.sqrt(distance) * 1000
        total_displacement += displacement
    return total_displacement


def DrawWaves(canvas_element, wave_origins, amplitude, frequency, rho, wavelength, time):
    size = canvas_element.size
    omega = math.radians(2 * np.pi * frequency)
    displacement_matrix = np.array(
        ApplyWaveFunction(size[0], size[1], wave_origins, amplitude, omega, rho, wavelength, time))
    image = Image.fromarray(displacement_matrix).convert('RGB')
    image.save('wave_2_{f}.png'.format(f=time))


canvas = CreateCanvas((5000, 4000), (0, 0, 0))

wave_1 = [2500, 2000, 500, 2500, 2000]
wave_2 = [1400, 1400, 300, 1400, 1400]
wave_3 = [3200, 2350, 100, 3200, 2350]
wave_4 = [3750, 1600, 700, 3750, 1600]
space_transform = 2
time = 0
for angle in np.linspace(0, 360, 30):
    wave_1[0] = wave_1[3] + (wave_1[2]) * math.cos(math.radians(angle))
    wave_1[1] = wave_1[4] + (wave_1[2]) * math.sin(math.radians(angle))
    wave_2[0] = wave_2[3] + (wave_2[2]) * math.cos(math.radians(angle))
    wave_2[1] = wave_2[4] + (wave_2[2]) * math.sin(math.radians(angle))
    wave_3[0] = wave_3[3] + (wave_3[2]) * math.cos(math.radians(angle))
    wave_3[1] = wave_3[4] + (wave_3[2]) * math.sin(math.radians(angle))
    wave_origins = [[wave_1[0], wave_1[1]], [wave_2[0], wave_2[1]], [wave_3[0], wave_3[1]]]
    DrawWaves(canvas, wave_origins, 1000, 60, 0, 150, time)
    print("Done with: " + str(time))
    time += 10
