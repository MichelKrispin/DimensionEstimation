import numpy as np
from typing import Tuple, Optional


def get_data(n: int, noise: float, seed: int = 12) -> Tuple[np.array, Optional[list | None]]:
    """Embed a 3d sphere in 6d.

    Args:
        n (int): Number of data points
        noise (float): Optional noise. If no noise this should be 0.0

    Returns:
        Tuple[np.array, Optional[List | None]]: data, layout
            If layout is none, there is no 'nice' graph arrangement
    """
    dimensions = 7

    plane = np.random.uniform(-1, 1, size=(2, n))
    if noise != 0.0:
        np.random.seed(seed + 6)
        plane += np.random.uniform(-noise, noise, size=plane.shape)

    np.random.seed(seed)
    transformation = np.random.uniform(1, 5, size=(dimensions, 2))
    data = transformation @ plane

    # Arrange the graph in a circle layout, i.e., in the given x,y order
    # => Ignore the z axis for now (top-down projection)
    layout = [(i, j) for i, j in zip(data[0], data[1])]
    layout = {i: [x_i, y_i] for i, (x_i, y_i) in enumerate(layout)}

    return data, layout
