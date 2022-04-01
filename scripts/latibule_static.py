import noise
import numpy as np
import random
from PIL import Image

blue = [65, 105, 225]
green = [34, 139, 34]
beach = [238, 214, 175]
snow = [255, 250, 250]
mountain = [139, 137, 137]


def BlankWorld(shape, scale, octaves, persistence, lacunarity):
    blank_world = np.zeros(shape)
    for i in range(shape[0]):
        for j in range(shape[1]):
            blank_world[i][j] = noise.pnoise2(i / scale,
                                              j / scale,
                                              octaves=octaves,
                                              persistence=persistence,
                                              lacunarity=lacunarity,
                                              repeatx=1024,
                                              repeaty=1024,
                                              base=0)
    return blank_world


def Colorize(world, shape, sea_level):
    color_world = np.zeros(world.shape + (3,))
    for i in range(shape[0]):
        for j in range(shape[1]):
            if world[i][j] < sea_level:
                color_world[i][j] = blue
            elif world[i][j] < sea_level + 0.05:
                color_world[i][j] = beach
            elif world[i][j] < sea_level + 0.3:
                color_world[i][j] = green
            elif world[i][j] < sea_level + 0.4:
                color_world[i][j] = mountain
            elif world[i][j] < sea_level + 1.05:
                color_world[i][j] = snow

    return color_world


images = []
sea = 0.5
for _ in range(50):
    sea -= 0.011
    base = BlankWorld((1024, 1024), 100, 6, 0.5, 2.0)
    colored_world = Colorize(base, (1024, 1024), sea)
    colored_world_int = colored_world.astype(np.uint8)
    images.append(Image.fromarray(colored_world_int))

for index in range(len(images)-1, 0, -1):
    images.append(images[index])

images[0].save('world.gif', save_all=True, append_images=images[1:], optimize=False, duration=100, loop=0)
