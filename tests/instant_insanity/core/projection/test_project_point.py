import math
import numpy as np
import pytest

from instant_insanity.core.projection import PerspectiveProjection, OrthographicProjection

@pytest.mark.parametrize(
    "camera_z, viewpoint, model_point, expected",
    [
        (0.0, [0, 0, 1], [0, 0, -1], [0, 0, -1]),
        (0.0, [0, 0, 1], [0, 0, -0.5], [0, 0, -0.5]),
        (0.0, [0, 0, 1], [0, 0, -0.25], [0, 0, -0.25]),
        (0.0, [0, 0, 1], [-1, 0, -1], [-0.5, 0, -1]),
    ]
)
def test_perspective_projection(camera_z, viewpoint, model_point, expected):
    viewpoint = np.array(viewpoint, dtype=np.float64)
    projection = PerspectiveProjection(viewpoint, camera_z=camera_z)
    model_point = np.array(model_point, dtype=np.float64)
    expected = np.array(expected, dtype=np.float64)
    actual = projection.project_point(model_point)
    assert np.allclose(expected, actual)

SQRT_2 = math.sqrt(2)
SQRT_5 = math.sqrt(5)
SQRT_10 = math.sqrt(10)

@pytest.mark.parametrize(
    "camera_z, u, model_point, expected",
    [
        (0.0, [0, 0, 1], [0, 0, -1], [0, 0, -1]),
        (0.0, [0, 0, 1], [0, 0, -0.5], [0, 0, -0.5]),
        (0.0, [0, 0, 1], [0, 0, -0.25], [0, 0, -0.25]),
        (0.0, [0, 0, 1], [-1, 0, -1], [-1, 0, -1]),
        (0.0, [1 / SQRT_2, 0, 1 / SQRT_2], [0, 0, -1], [1, 0, -1]),
        (0.0, [2 / SQRT_5, 0, 1 / SQRT_5], [0, 0, -1], [2, 0, -1]),
        (0.0, [3 / SQRT_10, 0, 1 / SQRT_10], [0, 0, -1], [3, 0, -1]),
    ]
)
def test_orthographic_projection(camera_z, u, model_point, expected):
    u = np.array(u, dtype=np.float64)
    projection = OrthographicProjection(u, camera_z=camera_z)
    model_point = np.array(model_point, dtype=np.float64)
    expected = np.array(expected, dtype=np.float64)
    actual = projection.project_point(model_point)
    assert np.allclose(expected, actual)
