#!/usr/bin/env python3
import json

from flask import Flask, render_template, request

from bokeh.embed import json_item
from bokeh.models import Range1d, Circle, MultiLine
from bokeh.plotting import figure, from_networkx

import igraph as ig
import networkx
import numpy as np

import dimension_estimation as dm
from data.fetch import fetch_data_functions

app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')

data_functions = {}


def make_plot(data_function, n, m_n, epsilon, noise):
    """Approximates the intrinsic dimension and makes a plot.

    Args:
        data_function (Callable[[int, float]], Tuple[np.array, Optional[list | None]]]): The get_data function that generates the data.
        n (int): Number of samples.
        m_n (int): Number of computed samples (m_n < n).
        epsilon (float): The size of the epsilon-ball.
        noise (float): Noise or 0.0, if there is none (noise >= 0.0).

    Raises:
        RuntimeError: If the intrinsic dimension computation wasn't successful.

    Returns:
        Tuple[str, float]: The plot html and the approximated intrinsic dimension.
    """
    # Fetch the data function
    get_data = globals()['data_functions'][data_function]['function']

    # Generate the 2d data
    data, layout = get_data(n, noise)
    if not layout:
        layout = networkx.spring_layout

    # Create the adjacency matrices
    A_eps, A_2eps = dm.construct_adjacencies(data, epsilon, 'euclidean')

    # Approximate the intrinsic dimension
    d_hat = dm.compute_d_hat(A_eps, A_2eps, m_n)
    if np.isnan(d_hat):
        raise RuntimeError('d_hat computation resulted in nan')

    # Create a graph from the adjacency matrix
    g = ig.Graph.Adjacency((A_eps > 0).tolist(), mode='undirected')

    # And then create the interactive plot
    plot = figure(
        min_height=200,
        min_width=200,
        tools="pan,wheel_zoom,save,reset",
        sizing_mode='stretch_both',
        active_scroll='wheel_zoom',
        x_range=Range1d(-1.1, 1.1),
        y_range=Range1d(-1.1, 1.1),
    )

    network_graph = from_networkx(g.to_networkx(),
                                  layout,
                                  scale=1,
                                  center=(0, 0))
    network_graph.node_renderer.glyph = Circle(size=5, fill_color='skyblue')
    network_graph.edge_renderer.glyph = MultiLine(line_alpha=0.5, line_width=1)
    plot.renderers.append(network_graph)

    return plot, d_hat


@app.route('/')
def index():
    globals()['data_functions'] = fetch_data_functions()
    return render_template('index.html', data_functions=data_functions.keys())


@app.route('/plot')
def plot():
    # Parse the parameters and pass them to the computation function
    data_function = request.args.get('data_function')
    n = int(request.args.get('n'))
    m_n = int(request.args.get('m_n'))
    epsilon = float(request.args.get('epsilon'))
    noise = float(request.args.get('noise'))

    try:
        p, d_hat = make_plot(data_function, n, m_n, epsilon, noise)
        return json.dumps({'plot': json_item(p), 'd_hat': d_hat})
    except Exception as e:
        return json.dumps({'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8000)
