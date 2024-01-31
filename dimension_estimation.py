import numpy as np

# -------------------
#       Graph
# -------------------


# Construct the adjacency matrix
# Each point represents a node
# Two nodes are connected if the points are epsilon-close to each other
def construct_adjacency(data, eps, metric):
    n = data.shape[1]
    A = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            if metric(data[:, i], data[:, j]) < eps:
                A[i, j] = A[j, i] = 1
    return A


# Construct A_epsilon and A_2epsilon
def construct_adjacencies(data, eps, metric="euclidean"):
    if type(metric) == str:
        if metric == "euclidean":
            metric = euclidean_distance
        else:
            raise TypeError(f"{metric} is an unknown metric")
    elif not callable(metric):
        raise TypeError(f"{metric} must be a callable function")

    A_epsilon = construct_adjacency(data, eps, metric)
    A_2epsilon = construct_adjacency(data, 2 * eps, metric)
    return A_epsilon, A_2epsilon


# -------------------
#     Utilities
# -------------------


def euclidean_distance(l, r):
    return np.linalg.norm(l - r)


# -------------------
#     Estimators
# -------------------


# Compute the estimator p_hat
# -> The average over teh degrees of the first m_n vertices
def estimate_p_hat(A, m_n):
    n = A.shape[0]
    p_hat = 0.0
    for i in range(m_n):
        for j in range(i + 1, n):
            p_hat += A[i, j]
    p_hat *= 2.0 / (m_n * (2*n - m_n - 1))
    return p_hat


# Estimate the dimension estimator d_hat
def estimate_d_hat(p_2eps, p_eps):
    return (np.log(p_2eps) - np.log(p_eps)) / np.log(2)


# Compute the dimension estimator d_hat
def compute_d_hat(A_eps, A_2eps, m_n):
    p_hat_eps = estimate_p_hat(A_eps, m_n)
    p_hat_2eps = estimate_p_hat(A_2eps, m_n)
    if p_hat_eps < 1e-8:
        raise RuntimeError(f"p_hat_eps is too small: Probably eps has to be higher!")
    return estimate_d_hat(p_hat_2eps, p_hat_eps)
