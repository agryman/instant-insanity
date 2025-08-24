from manim import Mobject
from manim.typing import Vector3D

from instant_insanity.animators.animorph import Animorph
from instant_insanity.core.geometry_types import PolygonId, PolygonIdToVertexPathMapping, VertexPath
from instant_insanity.core.transformation import RigidMotion
from instant_insanity.mobjects.polygons_3d import Polygons3D


class Polygons3DAnimorph(Animorph):
    """
    This is the abstract base class for Polygons3D animators.
    """
    def __init__(self, polygons: Polygons3D):
        if not isinstance(polygons, Polygons3D):
            raise TypeError(f'Expected a Polygons3D but got {type(polygons)}')
        super().__init__(polygons)

    def get_polygons(self) -> Polygons3D:
        mobject: Mobject = self.mobject
        assert isinstance(mobject, Polygons3D)
        polygons: Polygons3D = mobject
        return polygons


class RigidMotionPolygons3DAnimorph(Polygons3DAnimorph):
    """
    This class animates a rigid motion of a moveable subset of polygons.

    Attributes:
        rigid_motion: a rigid motion of polygons
        moveable_polygon_ids: a subset of PolygonId's
    """
    rigid_motion: RigidMotion
    moveable_polygon_ids: set[PolygonId]

    def __init__(self,
                 polygons: Polygons3D,
                 rotation: Vector3D,
                 translation: Vector3D,
                 movable_polygon_ids: set[PolygonId]) -> None:
        super().__init__(polygons)
        self.rigid_motion = RigidMotion(rotation, translation)
        self.moveable_polygon_ids = movable_polygon_ids

    def morph_to(self, alpha: float) -> None:
        """
        Transforms the moveable polygons using the interpolated rigid motion.
        Leaves the invisible polygons unchanged.

        Args:
            alpha: the alpha parameter of the interpolated rigid motion.
        """
        super().morph_to(alpha)

        alpha_motion: RigidMotion = self.rigid_motion.mk_at(alpha)
        polygons: Polygons3D = self.get_polygons()
        id_to_model_path_0: PolygonIdToVertexPathMapping = polygons.id_to_model_path_0

        id_to_model_path: PolygonIdToVertexPathMapping = {}
        polygon_id: PolygonId
        model_path_0: VertexPath
        for polygon_id, model_path_0 in id_to_model_path_0.items():
            model_path: VertexPath
            if polygon_id in self.moveable_polygon_ids:
                model_path = alpha_motion.transform_path(model_path_0)
            else:
                model_path = model_path_0
            id_to_model_path[polygon_id] = model_path

        polygons.set_id_to_model_path(id_to_model_path)

        # TODO test this as a replacement for CubeRigidMotionAnimorph
        # TODO we can use this in the construct graph scene where we move one cube from the puzzle
        # to the left side of the scene