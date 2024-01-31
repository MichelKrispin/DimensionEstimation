import numpy as np
from typing import Tuple, Optional


def get_data(n: int, noise: float) -> Tuple[np.array, Optional[list | None]]:
    """Embed a 3d sphere in 6d.

    Args:
        n (int): Number of data points
        noise (float): Optional noise. If no noise this should be 0.0

    Returns:
        Tuple[np.array, Optional[List | None]]: data, layout
            If layout is none, there is no 'nice' graph arrangement
    """
    dimensions = 6

    sphere = np.random.uniform(-1, 1, size=(3, n))
    sphere /= np.linalg.norm(sphere, axis=0)
    if noise != 0.0:
        np.random.seed(6)
        sphere += np.random.uniform(-noise, noise, size=sphere.shape)

    np.random.seed(12)
    transformation = np.random.uniform(1, 5, size=(dimensions, 3))
    data = transformation @ sphere

    # Arrange the graph in a circle layout, i.e., in the given x,y order
    # => Ignore the z axis for now (top-down projection)
    layout = [(i, j) for i, j in zip(data[0], data[3])]
    layout = {i: [x_i, y_i] for i, (x_i, y_i) in enumerate(layout)}

    return data, layout
