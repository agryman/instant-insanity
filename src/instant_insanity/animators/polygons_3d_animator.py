from manim import Mobject
from manim.typing import Vector3D

from instant_insanity.animators.animorph import Animorph
from instant_insanity.core.geometry_types import PolygonKeyToVertexPathMapping, VertexPath
from instant_insanity.core.transformation import RigidMotion
from instant_insanity.mobjects.polygons_3d import Polygons3D


class Polygons3DAnimorph[KeyType](Animorph):
    """
    This is the abstract base class for Polygons3D animators.
    """
    def __init__(self, polygons: Polygons3D[KeyType]):
        if not isinstance(polygons, Polygons3D):
            raise TypeError(f'Expected a Polygons3D but got {type(polygons)}')
        super().__init__(polygons)

    def get_polygons(self) -> Polygons3D[KeyType]:
        mobject: Mobject = self.mobject
        assert isinstance(mobject, Polygons3D)
        polygons: Polygons3D[KeyType] = mobject
        return polygons


class RigidMotionPolygons3DAnimorph[KeyType](Polygons3DAnimorph[KeyType]):
    """
    This class animates a rigid motion of a moveable subset of polygons.

    Attributes:
        rigid_motion: a rigid motion of polygons
        moveable_polygon_keys: a subset of polygon keys
    """
    rigid_motion: RigidMotion
    moveable_polygon_keys: set[KeyType]

    def __init__(self,
                 polygons: Polygons3D[KeyType],
                 rotation: Vector3D,
                 translation: Vector3D,
                 movable_polygon_keys: set[KeyType]) -> None:
        super().__init__(polygons)
        self.rigid_motion = RigidMotion(rotation, translation)
        self.moveable_polygon_keys = movable_polygon_keys

    def morph_to(self, alpha: float) -> None:
        """
        Transforms the moveable polygons using the interpolated rigid motion.
        Leaves the invisible polygons unchanged.

        Args:
            alpha: the alpha parameter of the interpolated rigid motion.
        """
        super().morph_to(alpha)

        alpha_motion: RigidMotion = self.rigid_motion.mk_at(alpha)
        polygons: Polygons3D[KeyType] = self.get_polygons()
        key_to_model_path_0: PolygonKeyToVertexPathMapping[KeyType] = polygons.key_to_model_path_0

        key_to_model_path: PolygonKeyToVertexPathMapping[KeyType] = {}
        polygon_key: KeyType
        model_path_0: VertexPath
        for polygon_key, model_path_0 in key_to_model_path_0.items():
            model_path: VertexPath
            if polygon_key in self.moveable_polygon_keys:
                model_path = alpha_motion.transform_path(model_path_0)
            else:
                model_path = model_path_0
            key_to_model_path[polygon_key] = model_path

        polygons.set_key_to_model_path(key_to_model_path)
