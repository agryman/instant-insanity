"""Smoothly interpolate between values using cubic splines."""

import numpy as np

def interpolate(x0: float, x1: float, n: int) -> np.ndarray:
    """
    Generate a cubic spline that smoothly interpolates between two values.

    Let s(t) be the standard cubic spline function defined on the interval [0, 1].
    It is given by:

    s(t) = -2 t^3 + 3 t^2 = t^2 (3 - 2 t)

    It satisfies the boundary conditions:

    s(0) = 0
    s(1) = 1
    s'(0) = 0
    s'(1) = 0.

    It also satisfies:

    0 <= s(t) <= 1 for 0 <= t <= 1.

    The interpolated values of x as a function of t are given by:

    x(t) = x0 + (x1 - x0) s(t)
    x(0) = x0 + (x1 - x0) s(0) = x0 + (x1 - x0) 0 = x0
    x(1) = x0 + (x1 - x0) s(1) = x0 + (x1 - x0) 1 = x1

    x'(t) = (x1 - x0) s'(t)
    x'(0) = (x1 - x0) s'(0) = (x1 - x0) 0 = 0
    x'(1) = (x1 - x0) s'(1) = (x1 - x0) 0 = 0

    Args:
        x0: the initial value
        x1: the final value
        n: the number of points to generate, including the initial and final values

    Returns:
        an array x of length n containing the interpolated values.
        x[0] = x0, x[n-1] = x1, n >= 2
    """

    if n < 2:
        raise ValueError("n must be at least 2")

    # Generate n values of t evenly spaced in [0, 1]
    t = np.linspace(0, 1, n)

    # Compute s(t) = t^2 * (3 - 2t)
    s = t ** 2 * (3 - 2 * t)

    # Interpolated values: x(t) = x0 + (x1 - x0) * s(t)
    x = x0 + (x1 - x0) * s

    return x
