from abc import ABC, abstractmethod
from typing import Any, OrderedDict
import numpy as np

from manim import (VGroup, ValueTracker, Polygon, Scene, tempconfig, ORIGIN, RIGHT, LEFT, UP, OUT,
                   RED, GREEN, BLUE, YELLOW, BLACK, PI, ManimColor)

from instant_insanity.core.config import LINEN_CONFIG
from instant_insanity.core.geometry_types import (Vertex, VertexPath, PolygonId, PolygonIdToVertexPathMapping,
                                                  SortedPolygonIdToPolygonMapping, SortedPolygonIdToVertexPathMapping,
                                                  as_vertex, as_vertex_path)
from instant_insanity.core.projection import Projection, PerspectiveProjection
from instant_insanity.core.depth_sort import DepthSort
from instant_insanity.core.transformation import transform_vertices
from instant_insanity.manim_scenes.coordinate_grid import GridMixin


class TrackedVGroup(VGroup):
    """
    This class is a VGroup with a ValueTracker.

    Attributes:
        tracker: the ValueTracker
    """
    tracker: ValueTracker

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.tracker = ValueTracker(0.0)

def mk_id_to_scene_polygon(id_to_scene_path: SortedPolygonIdToVertexPathMapping,
                           **kwargs) -> SortedPolygonIdToPolygonMapping:
    """
    Makes an `OrderedDict` that maps `PolygonId` to `Polygon` from their vertex paths in scene space.

    Args:
        id_to_scene_path: the `OrderedDict` of vertex paths in scene space.
        **kwargs: optional arguments passed to `Polygon`.

    Returns:
        the `OrderedDict` of `Polygon` instances.
    """
    id_to_scene_polygon: SortedPolygonIdToPolygonMapping = OrderedDict()
    polygon_id: PolygonId
    scene_path: VertexPath
    for polygon_id, scene_path in id_to_scene_path.items():
        scene_polygon: Polygon = Polygon(*scene_path, **kwargs)
        id_to_scene_polygon[polygon_id] = scene_polygon

    return id_to_scene_polygon

class ThreeDPolygons(TrackedVGroup, ABC):
    """
    This class animates a collection of 3D polygons.

    We use the term *vertex* to refer to a point in 3D space.
    We use the term *vertex path* to refer to the sequence of vertices that define the corners of the polygon.
    We use the term *polygon* to refer to a Manim `Polygon` which is defined by a vertex path and other style attributes.

    These polygons are assumed to be planar, convex, and to not intersect each other
    accept possibly along vertices or edges. That is, there are allowed to intersect
    in a set of points that has area zero. Furthermore, we assume that they have a valid
    depth sort. The directed graph on the set of polygons defined by relation *X is strictly behind Y*
    in the given projection is assumed to be acyclic.

    Each polygon is uniquely identified by a `PolygonId` which is used as a dict key.
    We use the term *name* to refer to an application-specific polygon identifier.
    It is up to users of this class to encode and decode meaningful names into `PolygonId`s.

    This class supports animations of the set of polygons.
    It contains a `ValueTracker` that animates an interpolation parameter `alpha` which ranges
    from 0 to 1.

    It is the responsibility of an animator to compute the interpolated model vertex paths
    for all values `alpha` of the interpolation parameter between 0 and 1.

    The animator MUST interpolate continuously in the sense that the interpolated model vertex paths
    computed for `alpha` = 0 should equal the initial model vertex paths.

    The renderer loop is as follows:
    1. the renderer updates the animation parameter alpha and calls the animator
    2. the animator computes the interpolated model paths corresponding to alpha
    3. if alpha = 0 then the interpolated model paths are copied to the initial model paths
    3. the depth-sorter projects the interpolated model paths to the interpolated scene paths
    4. the depth-sorted sorts the interpolated scene paths and returns them in an ordered dict
    4. the scene constructs new Polygon objects from the interpolated scene paths and stores them in name_to_scene_polygon
    5. the scene removes all submobjects from this vgroup
    6. the scene adds the new scene polygons to this vgroup in the depth-sorted order

    Attributes:
        projection: the `Projection` from model space onto scene space.
        depth_sorter: the depth sorter used to depth-sort polygons.
        id_to_initial_model_path: the initial model paths of each polygon.
        id_to_interpolated_model_path: the interpolated model paths of each polygon.
        id_to_scene_path: the `OrderedDict` of scene paths of each scene polygon.
        id_to_scene_polygon: the `OrderedDict` of depth-sorted scene polygons.
    """
    projection: Projection
    depth_sorter: DepthSort
    id_to_initial_model_path: PolygonIdToVertexPathMapping
    id_to_interpolated_model_path: PolygonIdToVertexPathMapping
    id_to_scene_path: SortedPolygonIdToVertexPathMapping
    id_to_scene_polygon: SortedPolygonIdToPolygonMapping

    def __init__(self,
                 projection: Projection,
                 id_to_initial_model_path: PolygonIdToVertexPathMapping,
                 **kwargs: Any) -> None:
        super().__init__(**kwargs)

        depth_sorter: DepthSort = DepthSort(projection)
        id_to_scene_path: SortedPolygonIdToVertexPathMapping = depth_sorter.depth_sort(id_to_initial_model_path)
        id_to_scene_polygon: SortedPolygonIdToPolygonMapping = mk_id_to_scene_polygon(id_to_scene_path, **kwargs)

        self.projection = projection
        self.depth_sorter = depth_sorter
        self.id_to_initial_model_path = id_to_initial_model_path
        self.id_to_interpolated_model_path = id_to_initial_model_path
        self.id_to_scene_path = id_to_scene_path
        self.id_to_scene_polygon = id_to_scene_polygon

    def update_polygons(self, id_to_interpolated_model_path: PolygonIdToVertexPathMapping, **kwargs) -> None:
        """
        Updates the polygons from the given interpolated model paths.

        Args:
            id_to_interpolated_model_path: the interpolated model vertex paths for each polygon
                corresponding the current tracker alpha value.
            **kwargs: additional keyword arguments passed to mk_polygon.
        """

        self.id_to_interpolated_model_path = id_to_interpolated_model_path
        self.id_to_scene_path = self.depth_sorter.depth_sort(id_to_interpolated_model_path)
        self.id_to_scene_polygon = mk_id_to_scene_polygon(self.id_to_scene_path, **kwargs)

    #TODO: rebase ThreeDPuzzleCube on it

class TestThreeDPolygons(GridMixin, Scene):
    def construct(self):
        self.add_grid(True)

        # create a projection
        camera_z: float = 2.0
        viewpoint: np.ndarray = np.array([2, 2, 6], dtype=np.float64)
        projection: Projection = PerspectiveProjection(viewpoint, camera_z=camera_z)

        # create the vertex paths for a tetrahedron
        o: Vertex = as_vertex(ORIGIN)
        x: Vertex = as_vertex(RIGHT)
        y: Vertex = as_vertex(UP)
        z: Vertex = as_vertex(OUT)

        oxy: VertexPath = as_vertex_path([o, x, y])
        oxz: VertexPath = as_vertex_path([o, x, z])
        oyz: VertexPath = as_vertex_path([o, y, z])
        xyz: VertexPath = as_vertex_path([x, y, z])

        oxy_id: PolygonId = PolygonId('oxy')
        oxz_id: PolygonId = PolygonId('oxz')
        oyz_id: PolygonId = PolygonId('oyz')
        xyz_id: PolygonId = PolygonId('xyz')

        id_to_initial_model_path: PolygonIdToVertexPathMapping = {
            oxy_id: oxy,
            oxz_id: oxz,
            oyz_id: oyz,
            xyz_id: xyz,
        }

        polygon_to_colour: dict[PolygonId, ManimColor] = {
            oxy_id: RED,
            oxz_id: GREEN,
            oyz_id: BLUE
        }

        polygon_defaults: dict = {
            'fill_opacity': 1.0,
            'fill_color': YELLOW,
            'stroke_width': 1.0,
            'stroke_color': BLACK
        }
        polygons: ThreeDPolygons = ThreeDPolygons(projection,
                                                  id_to_initial_model_path,
                                                  **polygon_defaults)

        self.add(*polygons.id_to_scene_polygon.values())
        self.wait()

        self.remove(*polygons.id_to_scene_polygon.values())
        self.wait()

        # transform the model paths and update the polygons object
        rotation: np.ndarray = np.array(RIGHT * PI / 2.0, dtype=np.float64)
        translation: np.ndarray = np.array(LEFT * 4, dtype=np.float64)
        id_to_interpolated_model_path: PolygonIdToVertexPathMapping = {
            polygon_id : transform_vertices(rotation, translation, id_to_initial_model_path[polygon_id])
            for polygon_id in id_to_initial_model_path.keys()
        }
        polygons.update_polygons(id_to_interpolated_model_path, **polygon_defaults)

        for polygon_id in polygon_to_colour.keys():
            polygons.id_to_scene_polygon[polygon_id].set_fill(polygon_to_colour[polygon_id])

        self.add(*polygons.id_to_scene_polygon.values())
        self.wait()

        self.wait()

if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = TestThreeDPolygons()
        scene.render()
