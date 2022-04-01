import random

import numpy as np
from scipy import integrate
import matplotlib
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import cnames
from matplotlib import animation
import seaborn as sns
from IPython.display import HTML


def lorentz_deriv(l_coor, t0, sigma=5., beta=2. / 3, rho=28.0):
    """Compute the time-derivative of a Lorentz system."""
    [x, y, z] = l_coor
    return [sigma * (y - x), x * (rho - z) - y, x * y - beta * z]


# parameters
N_trajectories = 20
size_queue = 500
T = 8
N = 1000

# initial condition
x0 = np.array([[random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)] for i in range(N_trajectories)])
print(x0)
x0[:, 2] = np.linspace(0, 30, N_trajectories)

# Solve for the trajectories
t = np.linspace(0, T, N)
x_t = np.asarray([integrate.odeint(lorentz_deriv, x0i, t)
                  for x0i in x0])

print('Trajectories simulated.')

array_colors = [sns.hls_palette(N, l=.75, s=x) for x in np.linspace(0.75, 0.9, N_trajectories)]

# Set up figure & 3D axis for animation
fig = plt.figure(facecolor='black')
ax = fig.add_axes([0, 0, 1, 1], projection='3d')
ax.axis('off')

# set up lines and points
lines = [ax.plot([], [], [], '-', c=c[0], alpha=0.7)[0] for c in array_colors]
pts = [ax.plot([], [], [], 'o', c=c[0])[0] for c in array_colors]

# prepare the axes limits
ax.set_xlim((-25, 25))
ax.set_ylim((-35, 35))
ax.set_zlim((-10, 40))

# set point-of-view: specified by (altitude degrees, azimuth degrees)
ax.view_init(30, 0)


def animate(i):
    t = int(i / N * T)
    for idx, (line, pt, xi) in enumerate(zip(lines, pts, x_t)):
        x, y, z = xi[:i].T

        line.set_data(x[-size_queue:], y[-size_queue:])
        line.set_3d_properties(z[-size_queue:])
        line.set_color(array_colors[idx][i])

        pt.set_data(x[-1:], y[-1:])
        pt.set_3d_properties(z[-1:])
        pt.set_color(array_colors[idx][i])

    ax.view_init(30, 0.3 * i)
    fig.canvas.draw()
    return lines + pts


# instantiate the animator.
anim = animation.FuncAnimation(fig, animate, frames=N, interval=30, blit=True)
anim.save('lorenz_2.gif', writer='imagemagick', fps=60, savefig_kwargs={'transparent': True, 'facecolor': 'black'})
