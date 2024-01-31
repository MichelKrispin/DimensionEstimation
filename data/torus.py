import numpy as np
from typing import Tuple, Optional


def get_data(n: int, noise: float, seed: int = 5) -> Tuple[np.array, Optional[list | None]]:
    """Create torus data.

    Args:
        n (int): Number of data points
        noise (float): Optional noise. If no noise this should be 0.0

    Returns:
        Tuple[np.array, Optional[List | None]]: data, layout
            If layout is none, there is no 'nice' graph arrangement
    """
    R = 1.0  # torus offset
    r = 0.5  # torus radius

    np.random.seed(seed)
    theta = 2 * np.pi * np.random.uniform(0, 1, size=(n))
    np.random.seed(seed + 34)
    phi = 2 * np.pi * np.random.uniform(0, 1, size=(n))
    x = np.cos(theta) * (R + r * np.cos(phi))
    y = np.sin(theta) * (R + r * np.cos(phi))
    z = r * np.sin(phi)

    if noise != 0.0:
        np.random.seed(seed + 7)
        vec = np.random.uniform(-noise, noise, size=(3, n))
        x += vec[0]
        y += vec[1]
        z += vec[2]

    # Arrange the graph in a circle layout, i.e., in the given x,y order
    # => Ignore the z axis for now (top-down projection)
    layout = [(i, j) for i, j in zip(x, y)]
    layout = {i: [x_i, y_i] for i, (x_i, y_i) in enumerate(layout)}

    return np.array([x, y, z]), layout


"""
# Code to plot the torus with cmd line args
# ptython a.py 500 0.3
import numpy as np
import matplotlib.pyplot as plt
import sys

n = int(sys.argv[1])
noise = float(sys.argv[2])

R = 1.0  # torus offset
r = 0.5  # torus radius

np.random.seed(5)
theta = 2 * np.pi * np.random.uniform(0, 1, size=(n))
np.random.seed(6)
phi = 2 * np.pi * np.random.uniform(0, 1, size=(n))
x = np.cos(theta) * (R + r * np.cos(phi))
y = np.sin(theta) * (R + r * np.cos(phi))
z = r * np.sin(phi)

if noise != 0.0:
    np.random.seed(7)
    vec = np.random.uniform(-noise, noise, size=(3, n))
    x += vec[0]
    y += vec[1]
    z += vec[2]

fig = plt.figure()
ax = plt.axes(projection='3d')

ax.scatter(x, y, z)
plt.show()
"""
