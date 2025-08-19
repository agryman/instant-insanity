import numpy as np
import pytest

from instant_insanity.core.plane import xy_polar

def test_xy_polar_basic() -> None:
    v0 = np.array([
        [1.0, 0.0, 2.0],   # angle 0,   r=1
        [0.0, 1.0, -1.0],  # angle pi/2,r=1
        [-1.0, 0.0, 0.0],  # angle pi,  r=1
        [0.0, -1.0, 5.0],  # angle -pi/2,r=1
        [0.0, 0.0, 7.0],   # origin -> angle 0, r=0
    ], dtype=np.float64)

    theta, r = xy_polar(v0)

    assert theta.shape == (5,)
    assert r.shape == (5,)
    assert theta.dtype == np.float64
    assert r.dtype == np.float64

    # radii
    np.testing.assert_allclose(r, np.array([1.0, 1.0, 1.0, 1.0, 0.0], dtype=np.float64))

    # angles (check a few key values)
    np.testing.assert_allclose(theta[0], 0.0)
    np.testing.assert_allclose(theta[1], np.pi / 2)
    np.testing.assert_allclose(theta[2], np.pi)
    np.testing.assert_allclose(theta[3], -np.pi / 2)
    np.testing.assert_allclose(theta[4], 0.0)

def test_xy_polar_validation() -> None:
    with pytest.raises(TypeError):
        xy_polar([[1.0, 0.0, 0.0]])  # not an ndarray

    with pytest.raises(TypeError):
        xy_polar(np.array([[1.0, 0.0, 0.0]], dtype=np.float32))  # wrong dtype

    with pytest.raises(ValueError):
        xy_polar(np.array([1.0, 0.0, 0.0], dtype=np.float64))  # wrong shape

    with pytest.raises(ValueError):
        xy_polar(np.zeros((3, 2), dtype=np.float64))  # wrong second dimension