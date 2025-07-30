import math
import numpy as np
import pytest
from instant_insanity.core.convex_planar_polygon import ConvexPlanarPolygon
from instant_insanity.core.projection import PerspectiveProjection, OrthographicProjection

SQRT_2 = np.sqrt(2)
SQRT_3 = np.sqrt(3)

@pytest.mark.parametrize(
    "projection",
    [
        PerspectiveProjection(0.0, np.array([0, 0, 1], dtype=np.float64)),
        PerspectiveProjection(0.0, np.array([0, 0, 10], dtype=np.float64)),
        PerspectiveProjection(0.0, np.array([0, 10, 10], dtype=np.float64)),
        PerspectiveProjection(0.0, np.array([10, 10, 10], dtype=np.float64)),
        OrthographicProjection(0.0, np.array([0, 0, 1], dtype=np.float64)),
        OrthographicProjection(0.0, np.array([0, 1, 1], dtype=np.float64) / SQRT_2),
        OrthographicProjection(0.0, np.array([1, 1, 1], dtype=np.float64) / SQRT_3),
    ]
)
def test_perspective_projection(projection):
    vertices = np.array([
        [0, 0, -10],
        [10, 0, -10],
        [10, 10, -10],
        [0, 10, -10]
    ], dtype=np.float64)
    polygon = ConvexPlanarPolygon(vertices)
    for vertex in polygon.vertices:
        p = projection.project_point(vertex)
        x, y, expected_t = p
        actual_t = projection.polygon_t(polygon, x, y)
        assert np.isclose(actual_t, expected_t)
