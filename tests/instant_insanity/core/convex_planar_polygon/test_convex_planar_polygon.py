import pytest

import numpy as np
from instant_insanity.core.convex_planar_polygon import ConvexPlanarPolygon


@pytest.mark.parametrize(
    "vertices",
    [
        None,
        0,
        1.0,
        np.array([0, 0, 0], dtype=np.int16),
        np.array([0, 0, 0], dtype=np.float16),
        np.array([0, 0, 0], dtype=np.float32),
    ]
)
def test_type_error(vertices):
    with pytest.raises(TypeError):
        ConvexPlanarPolygon(vertices)

@pytest.mark.parametrize(
    "vertices",
    [
        np.array([0, 0, 0], dtype=np.float64),
        np.zeros((2, 3), dtype=np.float64),
        np.zeros((3, 2), dtype=np.float64),
    ]
)
def test_value_error(vertices):
    with pytest.raises(ValueError):
        ConvexPlanarPolygon(vertices)
