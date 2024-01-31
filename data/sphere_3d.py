import numpy as np
from typing import Tuple, Optional


def get_data(n: int, noise: float, seed: int = 12) -> Tuple[np.array, Optional[list | None]]:
    """Create 3-dimensional sphere data

    Args:
        n (int): Number of data points
        noise (float): Optional noise. If no noise this should be 0.0

    Returns:
        Tuple[np.array, Optional[List | None]]: data, layout
            If layout is none, there is no 'nice' graph arrangement
    """
    np.random.seed(seed)
    vec = np.random.uniform(-1, 1, size=(3, n))
    vec /= np.linalg.norm(vec, axis=0)
    if noise != 0.0:
        np.random.seed(seed + 6)
        vec += np.random.uniform(-noise, noise, size=vec.shape)

    # Arrange the graph in a circle layout, i.e., in the given x,y order
    # => Ignore the z axis for now (top-down projection)
    layout = [(i, j) for i, j in zip(vec[0], vec[1])]
    layout = {i: [x_i, y_i] for i, (x_i, y_i) in enumerate(layout)}

    return vec, layout
