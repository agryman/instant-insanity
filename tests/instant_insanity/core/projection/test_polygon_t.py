import numpy as np
import pytest
from instant_insanity.core.convex_planar_polygon import ConvexPlanarPolygon
from instant_insanity.core.projection import PerspectiveProjection, OrthographicProjection

SQRT_2 = np.sqrt(2)
SQRT_3 = np.sqrt(3)
SQRT_5 = np.sqrt(5)
SQRT_6 = np.sqrt(6)

@pytest.mark.parametrize(
    "projection, expected_t",
    [
        (PerspectiveProjection(np.array([0, 0, 1], dtype=np.float64), camera_z=0.0), -10.0),
        (PerspectiveProjection(np.array([0, 0, 10], dtype=np.float64), camera_z=0.0), -10.0),
        (PerspectiveProjection(np.array([0, 10, 10], dtype=np.float64), camera_z=0.0), -5.0 * SQRT_5),
        (PerspectiveProjection(np.array([10, 10, 10], dtype=np.float64), camera_z=0.0), -5.0 * SQRT_6),
        (OrthographicProjection(np.array([0, 0, 1], dtype=np.float64), camera_z=0.0), -10.0),
        (OrthographicProjection(np.array([0, 1, 1], dtype=np.float64) / SQRT_2, camera_z=0.0), -10.0 * SQRT_2),
        (OrthographicProjection(np.array([1, 1, 1], dtype=np.float64) / SQRT_3, camera_z=0.0), -10.0 * SQRT_3),
    ]
)
def test_perspective_projection(projection, expected_t):
    vertices = np.array([
        [0, 0, -10],
        [10, 0, -10],
        [10, 10, -10],
        [0, 10, -10]
    ], dtype=np.float64)
    polygon = ConvexPlanarPolygon(vertices)
    model_point = np.array([0,0,-10], dtype=np.float64)
    p = projection.project_point(model_point)
    x, y, _ = p
    actual_t = projection.polygon_t(polygon, x, y)
    assert np.isclose(actual_t, expected_t)
