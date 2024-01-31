import numpy as np
from typing import Tuple, Optional


def get_data(n: int, noise: float) -> Tuple[np.array, Optional[list | None]]:
    """Create one-dimensional circle data

    Args:
        n (int): Number of data points
        noise (float): Optional noise. If no noise this should be 0.0

    Returns:
        Tuple[np.array, Optional[list | None]]: data, layout
            If layout is none, there is no 'nice' graph arrangement
    """
    np.random.seed(5)
    random_angles = 2 * np.pi * np.random.uniform(0, 1, size=(n))
    x = np.cos(random_angles)
    y = np.sin(random_angles)

    # Add noise if needed
    if noise != 0.0:
        np.random.seed(6)
        random_offsets = np.random.uniform(1 - noise, 1 + noise, size=(n))
        x *= random_offsets
        y *= random_offsets

    # Arrange the graph in a circle layout, i.e., in the given order
    layout = [(i, j) for i, j in zip(x, y)]
    layout = {i: [x_i, y_i] for i, (x_i, y_i) in enumerate(layout)}

    return np.array([x, y]), layout
