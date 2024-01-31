import numpy as np
from typing import Tuple, Optional
from sklearn.datasets import make_s_curve


def get_data(
    n: int, noise: float, seed: int = 12
) -> Tuple[np.ndarray, Optional[list | None]]:
    """S Curve with only one intrinsic dimension in 3D.

    Args:
        n (int): Number of data points
        noise (float): Optional noise. If no noise this should be 0.0

    Returns:
        Tuple[np.array, Optional[List | None]]: data, layout
            If layout is none, there is no 'nice' graph arrangement
    """
    # data = make_s_curve(n, noise=noise)[0].T
    data = np.empty(shape=(3, n))
    np.random.seed(seed)
    t = np.random.uniform(-3 / 2 * np.pi, 3 / 2 * np.pi, size=(n))
    # t = np.linspace(-3 / 2 * np.pi, 3 / 2 * np.pi, n)
    data[0, :] = np.sin(t)
    data[1, :] = np.linspace(0, 2, n)
    data[2, :] = np.sign(t) * (np.cos(t) - 1)

    if noise != 0.0:
        np.random.seed(seed + 6)
        data += np.random.uniform(-noise, noise, size=data.shape)

    # Arrange the graph in a circle layout, i.e., in the given x,y order
    # => Ignore the z axis for now (top-down projection)
    layout = [(i, j) for i, j in zip(data[0], data[2])]
    layout = {i: [x_i, y_i] for i, (x_i, y_i) in enumerate(layout)}

    return data, layout


"""
import matplotlib.pyplot as plt
from matplotlib import ticker
from sklearn import datasets

n_samples = 1000
S_points, S_color = datasets.make_s_curve(n_samples, random_state=0)


def plot_3d(points, points_color, title):
    x, y, z = points.T
    fig, ax = plt.subplots(
        figsize=(6, 6),
        facecolor="white",
        tight_layout=True,
        subplot_kw={"projection": "3d"},
    )
    fig.suptitle(title, size=16)
    col = ax.scatter(x, y, z, c=points_color, s=50, alpha=0.8)
    ax.view_init(azim=-60, elev=9)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
    ax.zaxis.set_major_locator(ticker.MultipleLocator(1))
    fig.colorbar(col, ax=ax, orientation="horizontal", shrink=0.6, aspect=60, pad=0.01)
    plt.show()


plot_3d(S_points, S_color, "Original S-curve samples")
"""
