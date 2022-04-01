import numpy as np
import math
from PIL import Image, ImageDraw
import colorsys
import random

N = 500
time_step = 0.2
iterations = 20
scale = 4


def hsv_to_rgb(h, s, v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h, s, v))


def linear_sol(b, x, x0, a, c):
    c_recip = 1.0 / c
    for k in range(iterations):
        for j in range(1, N - 1):
            for i in range(1, N - 1):
                x[i, j] = (x0[i, j] + a * (x[i + 1, j] + x[i - 1, j] + x[i, j + 1] + x[i, j - 1])) * c_recip
        set_bnd(b, x)


def diffuse(b, x, x0, diff, dt):
    a = dt * diff * (N - 2) * (N - 2)
    linear_sol(b, x, x0, a, 1 + 6 * a)


def project(velocX, velocY, p, div):
    for j in range(1, N - 1):
        for i in range(1, N - 1):
            div[i, j] = -0.5 * (velocX[i + 1, j] - velocX[i - 1, j] + velocY[i, j + 1] - velocY[i, j - 1]) / N
            p[i, j] = 0

    set_bnd(0, div)
    set_bnd(0, p)
    linear_sol(0, p, div, 1, 6)

    for j in range(1, N - 1):
        for i in range(1, N - 1):
            velocX[i, j] -= 0.5 * (p[i + 1, j] - p[i - 1, j])
            velocY[i, j] -= 0.5 * (p[i, j + 1] - p[i, j - 1])

    set_bnd(1, velocX)
    set_bnd(2, velocY)


def advect(b, d, d0, velocX, velocY, dt):
    dtx = dt * (N - 2)
    dty = dt * (N - 2)

    for j in range(1, N - 1):
        for i in range(1, N - 1):
            tmp1 = dtx * velocX[i, j]
            tmp2 = dty * velocY[i, j]
            x = float(i) - tmp1
            y = float(j) - tmp2

            if x < 0.5:
                x = 0.5
            if x > (N + 0.5):
                x = N + 0.5
            i0 = math.floor(x)
            i1 = i0 + 1.0

            if y < 0.5:
                y = 0.5
            if y > (N + 0.5):
                y = N + 0.5

            j0 = min(math.floor(y), N - 1)
            j1 = min(j0 + 1.0, N - 1)

            s1 = x - i0
            s0 = 1.0 - s1
            t1 = y - j0
            t0 = 1.0 - t1

            i0i = min(int(i0), N - 1)
            i1i = min(int(i1), N - 1)

            j0i = min(int(j0), N - 1)
            j1i = min(int(j1), N - 1)

            d[i, j] = s0 * (t0 * d0[i0i, j0i] + t1 * d0[i0i, j1i]) + s1 * (t0 * d0[i1i, j0i] + t1 * d0[i1i, j1i])

    set_bnd(b, d)


def set_bnd(b, x):
    for i in range(1, N - 1):
        if b == 2:
            x[i, 0] = -x[i, 1]
            x[i, N - 1] = -x[i, N - 2]
        else:
            x[i, 0] = x[i, 1]
            x[i, N - 1] = x[i, N - 2]

    for j in range(1, N - 1):
        if b == 1:
            x[0, j] = -x[1, j]
            x[N - 1, j] = -x[N - 2, j]
        else:
            x[0, j] = x[1, j]
            x[N - 1, j] = x[N - 2, j]

    x[0, 0] = 0.5 * (x[1, 0] + x[0, 1])
    x[0, N - 1] = 0.5 * (x[1, N - 1] + x[0, N - 2])
    x[N - 1, 0] = 0.5 * (x[N - 2, 0] + x[N - 1, 1])
    x[N - 1, N - 1] = 0.5 * (x[N - 2, N - 1] + x[N - 1, N - 2])


class Fluid:

    def __init__(self, diffusion, viscosity):
        self.size = N
        self.dt = time_step
        self.diff = diffusion
        self.visc = viscosity

        self.s = np.zeros((N, N), dtype=float)
        self.density = np.zeros((N, N), dtype=float)

        self.vx = np.zeros((N, N), dtype=float)
        self.vy = np.zeros((N, N), dtype=float)

        self.vx0 = np.zeros((N, N), dtype=float)
        self.vy0 = np.zeros((N, N), dtype=float)

    def add_density(self, x: int, y: int, amount: float):
        self.density[x, y] += amount

    def add_velocity(self, x: int, y: int, amountX: float, amountY: float):
        self.vx[x, y] += amountX
        self.vy[x, y] += amountY

    def step(self):
        diffuse(1, self.vx0, self.vx, self.visc, self.dt)
        diffuse(2, self.vy0, self.vy, self.visc, self.dt)

        project(self.vx0, self.vy0, self.vx, self.vy)

        advect(1, self.vx, self.vx0, self.vx0, self.vy0, self.dt)
        advect(2, self.vy, self.vy0, self.vx0, self.vy0, self.dt)

        project(self.vx, self.vy, self.vx0, self.vy0)

        diffuse(0, self.s, self.density, self.diff, self.dt)
        advect(0, self.density, self.s, self.vx, self.vy, self.dt)

    def render(self, frame):
        canvas = Image.new("RGB", (self.size * scale, self.size * scale), (0, 0, 0))
        draw = ImageDraw.Draw(canvas)
        for i in range(self.size):
            for j in range(self.size):
                x = i * scale
                y = j * scale
                color = hsv_to_rgb(0.95, 1, self.density[i, j] / 150
                                   )
                draw.ellipse((x - int(scale / 2), y - int(scale / 2), x + int(scale / 2), y + int(scale / 2)),
                             fill=color)
        canvas.save(f"test_{frame}.png")
        images.append(canvas)


images = []

fluid = Fluid(0, 0)
radius = random.randint(int(N / 8), int(N / 4))
center_x = int(N / 2)
center_y = int(N / 2)

for x in range(-radius, radius + 1):
    Y = int((radius * radius - x * x) ** 0.5)  # bound for y given x
    for y in range(-Y, Y + 1):
        if y % 2 == 0:
            fluid.add_density(x + center_x, y + center_y, random.uniform(50, 155))

fluid.add_velocity(center_x + 1, center_y, random.uniform(int(N / 3), int(N / 2)), 0)
fluid.add_velocity(center_x + 1, center_y + 1, random.uniform(int(N / 3), int(N / 2)),
                   random.uniform(int(N / 3), int(N / 2)))
fluid.add_velocity(center_x + 1, center_y - 1, random.uniform(int(N / 3), int(N / 2)),
                   -random.uniform(int(N / 3), int(N / 2)))
fluid.add_velocity(center_x - 1, center_y, -random.uniform(int(N / 3), int(N / 2)), 0)
fluid.add_velocity(center_x - 1, center_y + 1, -random.uniform(int(N / 3), int(N / 2)),
                   random.uniform(int(N / 3), int(N / 2)))
fluid.add_velocity(center_x - 1, center_y - 1, -random.uniform(int(N / 3), int(N / 2)),
                   -random.uniform(int(N / 3), int(N / 2)))

for i in range(100):
    fluid.render(i)
    fluid.step()

    if i % 10 == 0 and i != 0:
        fluid.add_velocity(center_x + 1, center_y, random.uniform(int(N / 3), int(N / 2)), 0)
        fluid.add_velocity(center_x + 1, center_y + 1, random.uniform(int(N / 3), int(N / 2)),
                           random.uniform(int(N / 3), int(N / 2)))
        fluid.add_velocity(center_x + 1, center_y - 1, random.uniform(int(N / 3), int(N / 2)),
                           -random.uniform(int(N / 3), int(N / 2)))
        fluid.add_velocity(center_x - 1, center_y, -random.uniform(int(N / 3), int(N / 2)), 0)
        fluid.add_velocity(center_x - 1, center_y + 1, -random.uniform(int(N / 3), int(N / 2)),
                           random.uniform(int(N / 3), int(N / 2)))
        fluid.add_velocity(center_x - 1, center_y - 1, -random.uniform(int(N / 3), int(N / 2)),
                           -random.uniform(int(N / 3), int(N / 2)))

images[0].save('boundless.gif',
               save_all=True, append_images=images[1:], optimize=False, duration=80, loop=0)
