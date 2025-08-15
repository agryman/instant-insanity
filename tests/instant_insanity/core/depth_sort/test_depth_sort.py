import numpy as np

from instant_insanity.core.depth_sort import DepthSort
from instant_insanity.core.projection import Projection, OrthographicProjection
from instant_insanity.core.geometry_types import *


def test_depth_sort():
    camera_z: float = 0.0
    u: np.ndarray = np.array([0, 0, 1], dtype=np.float64)
    projection: Projection = OrthographicProjection(u, camera_z=camera_z)
    depth_sorter: DepthSort = DepthSort(projection)

    triangle_a: VertexPath = np.array([
        [0, 0, 0],
        [1, 0, 0],
        [1, 1, 0],
    ], dtype=np.float64)

    triangle_b: VertexPath = triangle_a + np.array([0.5, 0, -1])

    id_a: PolygonId = PolygonId('a')
    id_b: PolygonId = PolygonId('b')
    polygons: PolygonIdToVertexPathMapping = {
        id_a: triangle_a,
        id_b: triangle_b,
    }

    sorted_paths: SortedPolygonIdToVertexPathMapping = depth_sorter.depth_sort(polygons)
    sorted_ids: list[PolygonId] = list(sorted_paths.keys())
    assert sorted_ids == [id_b, id_a]
    assert len(sorted_paths) == len(polygons)
