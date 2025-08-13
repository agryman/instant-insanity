import numpy as np

from instant_insanity.core.depth_sort import DepthSort
from instant_insanity.core.projection import Projection, OrthographicProjection


def test_depth_sort():
    camera_z: float = 0.0
    u: np.ndarray = np.array([0, 0, 1], dtype=np.float64)
    projection: Projection = OrthographicProjection(u, camera_z=camera_z)
    depth_sorter: DepthSort = DepthSort(projection)
    triangle_A: np.ndarray = np.array([
        [0, 0, 0],
        [1, 0, 0],
        [1, 1, 0],
    ], dtype=np.float64)

    triangle_B: np.ndarray = triangle_A + np.array([0.5, 0, -1])
    polygons: dict[str, np.ndarray] = {
        'A': triangle_A,
        'B': triangle_B,
    }
    sorted_names: list[str]
    projected_polygons: dict[str, np.ndarray]
    sorted_names, projected_polygons = depth_sorter.depth_sort(polygons)
    assert sorted_names == ['B', 'A']
    assert len(projected_polygons) == len(polygons)
