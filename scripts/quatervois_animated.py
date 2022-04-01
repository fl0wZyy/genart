from PIL import Image, ImageDraw
import math
import colorsys
import random
import datetime


def hsv_to_rgb(h, s, v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h, s, v))


def create_canvas(canvas_size, canvas_bg_color):
    canvas_element = Image.new("RGB", canvas_size, canvas_bg_color)
    return canvas_element


def draw_tree(canvas_element, x1, y1, angle, depth, x_cords, y_cords):
    if depth:
        x2 = x1 + int(math.cos(math.radians(angle)) * depth * 7)
        y2 = y1 + int(math.sin(math.radians(angle)) * depth * 7)
        x_cords[depth].append(x2)
        y_cords[depth].append(y2)
        diff_one = random.randint(-5, 5) * 5
        diff_two = random.randint(-5, 5) * 5
        draw_tree(canvas_element, x2, y2, angle - diff_one, depth - 1, x_cords, y_cords)
        draw_tree(canvas_element, x2, y2, angle - diff_two, depth - 1, x_cords, y_cords)


x_coords = [[] for _ in range(16)]
y_coords = [[] for _ in range(16)]
x_coords_1 = [[] for _ in range(16)]
y_coords_1 = [[] for _ in range(16)]
x_coords_2 = [[] for _ in range(16)]
y_coords_2 = [[] for _ in range(16)]
x_coords_3 = [[] for _ in range(16)]
y_coords_3 = [[] for _ in range(16)]

canvas = create_canvas((2000, 2000), (0, 0, 0))
draw_tree(canvas, 1000, 1000, 0, 15, x_coords, y_coords)
draw_tree(canvas, 1000, 1000, 90, 15, x_coords_1, y_coords_1)
draw_tree(canvas, 1000, 1000, 180, 15, x_coords_2, y_coords_2)
draw_tree(canvas, 1000, 1000, 270, 15, x_coords_3, y_coords_3)
draw = ImageDraw.Draw(canvas)
x_coords.reverse()
y_coords.reverse()
x_coords_1.reverse()
y_coords_1.reverse()
x_coords_2.reverse()
y_coords_2.reverse()
x_coords_3.reverse()
y_coords_3.reverse()
images = [canvas.copy()]

color = (int(45), int(53), int(47))
draw.line([(1000, 1000), (x_coords[0][0], (y_coords[0][0]))], fill=color,
          width=5, joint="curve")
draw.line([(1000, 1000), (x_coords_1[0][0], (y_coords_1[0][0]))], fill=color,
          width=5, joint="curve")
draw.line([(1000, 1000), (x_coords_2[0][0], (y_coords_2[0][0]))], fill=color,
          width=5, joint="curve")
draw.line([(1000, 1000), (x_coords_3[0][0], (y_coords_3[0][0]))], fill=color,
          width=5, joint="curve")

images.append(canvas.copy())
for i in range(len(x_coords) - 2):
    color = (int(45*1.5**i), int(53*1.5**i), int(47*1.5**i))
    counter = 0
    for j in range(len(x_coords[i])):
        for k in range(2):
            draw.line([(x_coords[i][j], (y_coords[i][j])), (x_coords[i + 1][counter], y_coords[i + 1][counter])],
                      fill=color, width=int(5*0.9**i), joint="curve")
            draw.line([(x_coords_1[i][j], (y_coords_1[i][j])), (x_coords_1[i + 1][counter], y_coords_1[i + 1][counter])],
                      fill=color, width=int(5 * 0.9 ** i), joint="curve")
            draw.line([(x_coords_2[i][j], (y_coords_2[i][j])), (x_coords_2[i + 1][counter], y_coords_2[i + 1][counter])],
                      fill=color, width=int(5 * 0.9 ** i), joint="curve")
            draw.line([(x_coords_3[i][j], (y_coords_3[i][j])), (x_coords_3[i + 1][counter], y_coords_3[i + 1][counter])],
                      fill=color, width=int(5 * 0.9 ** i), joint="curve")
            counter += 1

    images.append(canvas.copy())

for _ in range(15):
    images.append(images[-1])
final = images
for k in reversed(images):
    final.append(k)

final[0].save('chaos.gif', save_all=True, append_images=final[1:], optimize=False, duration=60, loop=0)
