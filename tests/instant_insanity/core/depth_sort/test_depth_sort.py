import numpy as np

from instant_insanity.core.depth_sort import DepthSort
from instant_insanity.core.projection import Projection, OrthographicProjection
from instant_insanity.core.geometry_types import Point3D_Array, PolygonKeyToVertexPathMapping, SortedPolygonKeyToVertexPathMapping


def test_depth_sort():
    camera_z: float = 0.0
    u: np.ndarray = np.array([0, 0, 1], dtype=np.float64)
    projection: Projection = OrthographicProjection(u, camera_z=camera_z)
    depth_sorter: DepthSort = DepthSort(projection)

    triangle_a: Point3D_Array = np.array([
        [0, 0, 0],
        [1, 0, 0],
        [1, 1, 0],
    ], dtype=np.float64)

    triangle_b: Point3D_Array = triangle_a + np.array([0.5, 0, -1])

    key_a: str = 'a'
    key_b: str = 'b'
    polygons: PolygonKeyToVertexPathMapping[str] = {
        key_a: triangle_a,
        key_b: triangle_b,
    }

    sorted_paths: SortedPolygonKeyToVertexPathMapping = depth_sorter.depth_sort(polygons)
    sorted_keys: list[str] = list(sorted_paths.keys())
    assert sorted_keys == [key_b, key_a]
    assert len(sorted_paths) == len(polygons)
