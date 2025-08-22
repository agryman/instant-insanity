from typing import Any, OrderedDict

from manim import Polygon, VGroup

from instant_insanity.core.depth_sort import DepthSort
from instant_insanity.core.geometry_types import PolygonIdToVertexPathMapping, SortedPolygonIdToVertexPathMapping, \
    SortedPolygonIdToPolygonMapping, PolygonId, VertexPath
from instant_insanity.core.projection import Projection

class ThreeDPolygons(VGroup):
    """
    This class manages a set of 3D polygons in model space and their depth-sorted projections onto scene space.

    We use the term *vertex* to refer to a point in 3D space.
    We use the term *vertex path* to refer to the sequence of vertices that define the corners of the polygon.
    We use the term *polygon* to refer to a Manim `Polygon` which is defined by a vertex path and other style attributes.

    These polygons are assumed to be planar, convex, and to not intersect each other,
    except possibly along vertices or edges. That is, there are allowed to intersect
    in a set of points whose area is zero. Furthermore, we assume that they have a valid
    depth sort. This means that the binary relation *polygon X is strictly behind polygon Y*
    in the given projection defines a directed acyclic graph.

    Each polygon is uniquely identified by a `PolygonId` which is simply a type alias for `str`.
    This id is used as the key in several `dict`s.
    We use the term *name* to refer to an application-specific polygon identifier.
    It is up to users of this class to encode and decode meaningful names to and from their corresponding  `PolygonId`s.

    This class supports animations of the set of polygons.

    It is the responsibility of an animator to compute the interpolated model vertex paths
    for all values of the interpolation parameter `alpha` between 0 and 1.

    The animator MUST interpolate model vertex paths continuously and satisfy the boundary condition that
    the interpolated model vertex paths computed for `alpha` = 0 MUST equal the initial model vertex paths.

    A typical renderer loop is as follows:
    1. the renderer updates the animation parameter alpha and calls the animator
    2. the animator computes the interpolated model paths corresponding to alpha
    3. the depth sorter projects the interpolated model paths to the corresponding interpolated scene paths
    4. the depth sorter sorts the interpolated scene paths and returns them in an `OrderedDict`
    4. the scene constructs new `Polygon` objects from the interpolated scene paths and stores them in name_to_scene_polygon
    5. the scene removes all submobjects from this vgroup
    6. the scene adds the new scene polygons to this vgroup in the depth-sorted order

    Attributes:
        projection: the `Projection` from model space onto scene space.
        depth_sorter: the depth sorter used to depth-sort polygons.
        id_to_model_path_0: the initial model paths of each polygon.
        id_to_model_path: the interpolated model paths of each polygon.
        id_to_scene_path: the `OrderedDict` of scene paths of each scene polygon.
        id_to_scene_polygon: the `OrderedDict` of depth-sorted scene polygons.
    """
    projection: Projection
    depth_sorter: DepthSort
    id_to_model_path_0: PolygonIdToVertexPathMapping
    id_to_model_path: PolygonIdToVertexPathMapping
    id_to_scene_path: SortedPolygonIdToVertexPathMapping
    id_to_scene_polygon: SortedPolygonIdToPolygonMapping

    @staticmethod
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

    def __init__(self,
                 projection: Projection,
                 id_to_initial_model_path: PolygonIdToVertexPathMapping,
                 **kwargs: Any) -> None:
        """

        Args:
            projection: the projection from model space onto scene space.
            id_to_initial_model_path: the dict of initial model paths.
            **kwargs: additional arguments passed to `Polygon`.
        """
        super().__init__(**kwargs)

        depth_sorter: DepthSort = DepthSort(projection)
        id_to_scene_path: SortedPolygonIdToVertexPathMapping = depth_sorter.depth_sort(id_to_initial_model_path)
        id_to_scene_polygon: SortedPolygonIdToPolygonMapping = ThreeDPolygons.mk_id_to_scene_polygon(id_to_scene_path, **kwargs)

        self.projection = projection
        self.depth_sorter = depth_sorter
        self.id_to_model_path_0 = id_to_initial_model_path
        self.id_to_model_path = id_to_initial_model_path
        self.id_to_scene_path = id_to_scene_path
        self.id_to_scene_polygon = id_to_scene_polygon

    def update_polygons(self, id_to_model_path: PolygonIdToVertexPathMapping, **kwargs) -> None:
        """
        Updates the polygons from the given interpolated model paths.

        Args:
            id_to_model_path: the interpolated model vertex paths for each polygon
                corresponding the current tracker alpha value.
            **kwargs: additional keyword arguments passed to mk_polygon.
        """

        self.id_to_model_path = id_to_model_path
        self.id_to_scene_path = self.depth_sorter.depth_sort(id_to_model_path)
        self.id_to_scene_polygon = ThreeDPolygons.mk_id_to_scene_polygon(self.id_to_scene_path, **kwargs)
