from typing import OrderedDict

from manim import Polygon, VGroup, WHITE, BLACK, LineJointType

from instant_insanity.core.depth_sort import DepthSort
from instant_insanity.core.geometry_types import (
    PolygonKeyToVertexPathMapping, SortedPolygonKeyToVertexPathMapping,
    SortedPolygonKeyToPolygonMapping, VertexPath,
)
from instant_insanity.core.projection import Projection

DEFAULT_POLYGON_SETTINGS: dict = {
    'fill_color': WHITE,
    'fill_opacity': 1.0,
    'stroke_color': BLACK,
    'stroke_opacity': 1.0,
    'stroke_width': 2.0,
    'joint_type': LineJointType.ROUND,
}


class Polygons3D[KeyType](VGroup):
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

    Each polygon is uniquely identified by a key of type `KeyType`.
    This key is used as the key in several `dict`s.
    The `KeyType` can be any immutable type such as strings, enums, tuples, etc.

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
        visible_polygon_keys: the subset of visible polygons
        key_to_model_path_0: the initial model paths of each polygon.
        key_to_model_path: the interpolated model paths of each polygon.
        key_to_scene_path: the `OrderedDict` of scene paths of each scene polygon.
        key_to_scene_polygon: the `OrderedDict` of depth-sorted scene polygons.
    """
    projection: Projection
    depth_sorter: DepthSort[KeyType]
    visible_polygon_keys: set[KeyType]
    key_to_model_path_0: PolygonKeyToVertexPathMapping[KeyType]
    key_to_model_path: PolygonKeyToVertexPathMapping[KeyType]
    key_to_scene_path: SortedPolygonKeyToVertexPathMapping[KeyType]
    key_to_scene_polygon: SortedPolygonKeyToPolygonMapping[KeyType]

    def __init__(self,
                 projection: Projection,
                 key_to_model_path_0: PolygonKeyToVertexPathMapping[KeyType]) -> None:
        """

        Args:
            projection: the projection from model space onto scene space.
            key_to_model_path_0: the dict of initial model paths.
        """
        super().__init__()

        self.projection = projection
        self.depth_sorter: DepthSort[KeyType] = DepthSort[KeyType](projection)

        self.key_to_model_path_0 = key_to_model_path_0
        self.key_to_model_path = key_to_model_path_0.copy()
        self.visible_polygon_keys = set(key_to_model_path_0.keys())

        self.update_scene_polygons()

    def update_scene_polygons(self) -> None:
        """
        Updates the scene polygons by projecting and depth-sorting the visible model paths.
        This method should be called whenever either the model paths or the visible polygon ids are changed.
        """

        # depth sort only the visible polygons
        polygon_key: KeyType
        visible_key_to_model_path: PolygonKeyToVertexPathMapping[KeyType] = {
            polygon_key: self.key_to_model_path[polygon_key] for polygon_key in self.visible_polygon_keys
        }
        self.key_to_scene_path = self.depth_sorter.depth_sort(visible_key_to_model_path)

        # make the Polygon mobjects
        polygon: Polygon
        scene_path: VertexPath
        self.key_to_scene_polygon: SortedPolygonKeyToPolygonMapping[KeyType] = OrderedDict()
        for polygon_key, scene_path in self.key_to_scene_path.items():
            polygon_settings: dict = self.get_polygon_settings(polygon_key)
            polygon = Polygon(*scene_path, **polygon_settings)
            self.key_to_scene_polygon[polygon_key] = polygon

        # remove the submobjects of this group and add the updated polygons in depth-sorted order
        self.remove_polygons()
        for polygon in self.key_to_scene_polygon.values():
            self.add(polygon)

    def set_visible_polygon_keys(self, visible_polygon_keys: set[KeyType]) -> None:
        assert visible_polygon_keys <= set(self.key_to_model_path_0.keys())

        self.visible_polygon_keys = visible_polygon_keys.copy()
        self.update_scene_polygons()

    def set_key_to_model_path(self, key_to_model_path: PolygonKeyToVertexPathMapping[KeyType]) -> None:
        """
        Updates the polygons from the given model paths.

        Args:
            key_to_model_path: the updated model vertex paths for each polygon
                corresponding the current tracker alpha value.
        """
        assert set(key_to_model_path.keys()) == set(self.key_to_model_path_0.keys())

        self.key_to_model_path = key_to_model_path
        self.update_scene_polygons()

    def get_polygon_settings(self, polygon_key: KeyType) -> dict:
        return DEFAULT_POLYGON_SETTINGS

    def conceal_polygons(self) -> None:
        """
        Conceals all the polygons.
        Call this before running an animation to avoid ghosts.
        Apparently, Manim takes a snapshot image of all the nonmoving mobjects before running an animation.
        It then uses the snapshot as a fixed background over which it animates the scene.
        For some reason, Manim may fail to mark a mobject as moving even though it has an updater attached to it.
        Concealing the polygons works around this quirk (bug?).

        """
        self.remove_polygons()

    def remove_polygons(self) -> None:
        """
        Removes all the polygons from the group.
        Do this whenever the z-order changes.
        Then add the polygons back in the correct z-order.
        """
        self.remove(*self.submobjects)

    def checkpoint(self) -> None:
        """
        Sets the initial model paths to be the current model paths.
        """
        self.key_to_model_path_0 = self.key_to_model_path.copy()

    def detach_polygon(self, polygon_key: KeyType) -> Polygon:
        """
        Detaches a polygon from the group so that it can be separately animated.

        Args:
            polygon_key: the polygon key.

        Returns:
            the polygon that was detached.
        """
        polygon: Polygon = self.key_to_scene_polygon[polygon_key]
        visible_polygon_keys: set[KeyType] = self.visible_polygon_keys - {polygon_key}
        self.set_visible_polygon_keys(visible_polygon_keys)
        return polygon
