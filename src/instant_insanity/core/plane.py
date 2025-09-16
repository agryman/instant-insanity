import numpy as np


def xy_polar(v0: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Project 3D vectors to the XY-plane and compute polar coordinates.

    Given an array of 3D vectors (x, y, z) shaped (n, 3), projects each
    vector to (x, y) and returns the polar angle and radius for each point.

    The radius is sqrt(x^2 + y^2). For (x, y) = (0, 0), angle is 0.0.
    Angles are in radians, computed with arctan2(y, x) and then normalized to the interval [0, 2*pi).

    Args:
        v0: Array of shape (n, 3) with dtype float64.

    Returns:
        A tuple (r, theta):
          - r: ndarray shape (n,), dtype float64, radii.
          - theta: ndarray shape (n,), dtype float64, angles in radians in the range [0, 2*pi).

    Raises:
        TypeError: If v0 is not a NumPy ndarray or dtype is not float64.
        ValueError: If v0 does not have shape (n, 3).
    """
    if not isinstance(v0, np.ndarray):
        raise TypeError('v0 must be a numpy.ndarray')

    if v0.dtype != np.float64:
        raise TypeError('v0 must have dtype=np.float64')

    if v0.ndim != 2 or v0.shape[1] != 3:
        raise ValueError('v0 must have shape (n, 3)')

    x = v0[:, 0]
    y = v0[:, 1]

    r = np.hypot(x, y)
    theta = np.arctan2(y, x)
    theta = np.mod(theta, 2 * np.pi)

    # Ensure exact zeros give angle 0 (np.arctan2(0, 0) already returns 0.0)
    # but we could explicitly normalize if desired:
    # theta = np.where(r == 0.0, 0.0, theta)

    return r, theta
