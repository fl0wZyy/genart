from PIL import Image, ImageDraw
import math
import colorsys
import random



def hsv_to_rgb(h, s, v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h, s, v))


def create_canvas(canvas_size, canvas_bg_color):
    canvas_element = Image.new("RGB", canvas_size, canvas_bg_color)
    return canvas_element


def draw_tree(canvas_element, x1, y1, angle, depth, color):
    if depth:
        x2 = x1 + int(math.cos(math.radians(angle)) * depth * 3)
        y2 = y1 + int(math.sin(math.radians(angle)) * depth * 3)
        draw = ImageDraw.Draw(canvas_element)
        draw.line([(x1, y1), (x2, y2)], fill=color, width=2, joint="curve")
        diff_one = random.randint(-5, 5) * 5
        diff_two = random.randint(-5, 5) * 5
        draw_tree(canvas_element, x2, y2, angle - diff_one, depth - 1,
                  (int(color[0] * 0.955), int(color[1] * 0.955), int(color[2] * 0.955)))
        draw_tree(canvas_element, x2, y2, angle - diff_two, depth - 1,
                  (int(color[0] * 1.05), int(color[1] * 1.05), int(color[2] * 1.05)))




canvas = create_canvas((2000, 2000), (255, 255, 255))
draw_tree(canvas, 1000, 1000, 0, 15, (212, 175, 55))
draw_tree(canvas, 1000, 1000, 90, 15, (212, 175, 55))
draw_tree(canvas, 1000, 1000, 180, 15, (212, 175, 55))
draw_tree(canvas, 1000, 1000, 270, 15, (212, 175, 55))

canvas.save("test.png", "PNG")
