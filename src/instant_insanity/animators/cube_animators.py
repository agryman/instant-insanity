from abc import ABC

import numpy as np
from manim import Mobject

from instant_insanity.animators.animorph import Animorph
from instant_insanity.core.cube import FaceName, FACE_NAME_TO_UNIT_NORMAL, RBF, LBF, LTF, FACE_NAME_TO_VERTEX_PATH
from instant_insanity.core.geometry_types import PolygonIdToVertexPathMapping, PolygonId, VertexPath, Vertex, Vector
from instant_insanity.core.transformation import transform_vertex_path, rotation_matrix_about_line, \
    apply_linear_transform

from instant_insanity.mobjects.three_d_puzzle_cube import ThreeDPuzzleCube


class CubeAnimorph(Animorph):
    """
    This is the abstract base class for `ThreeDPuzzleCube` animorphs.
    """

    def __init__(self, cube: ThreeDPuzzleCube):
        if not isinstance(cube, ThreeDPuzzleCube):
            raise TypeError(f'cube must be of type ThreeDPuzzleCube but got {type(cube)}')
        super().__init__(cube)

    def get_cube(self) -> ThreeDPuzzleCube:
        mobject: Mobject = self.mobject
        assert isinstance(mobject, ThreeDPuzzleCube)
        cube: ThreeDPuzzleCube = mobject
        return cube



class CubeRigidMotionAnimorph(CubeAnimorph):
    """
    The class animates a rigid motion of a cube.
    The rigid motion is defined by a rotation followed by a translation.

    Attributes:
        rotation: the rotation vector.
        translation: the translation vector.
    """

    rotation: np.ndarray
    translation: np.ndarray

    def __init__(self,
                 cube: ThreeDPuzzleCube,
                 rotation: np.ndarray,
                 translation: np.ndarray,
                 ) -> None:
        super().__init__(cube)
        self.rotation = rotation
        self.translation = translation

    def morph_to(self, alpha: float) -> None:
        super().morph_to(alpha)
        cube: ThreeDPuzzleCube = self.get_cube()

        # does this fix the ghost problem?
        cube.remove(*cube.submobjects)

        alpha_rotation: np.ndarray = alpha * self.rotation
        alpha_translation: np.ndarray = alpha * self.translation
        id_to_initial_model_path: PolygonIdToVertexPathMapping = cube.id_to_initial_model_path
        polygon_id: PolygonId
        model_path: VertexPath
        id_to_transformed_model_path: PolygonIdToVertexPathMapping = {
            polygon_id: transform_vertex_path(alpha_rotation, alpha_translation, model_path)
            for polygon_id, model_path in id_to_initial_model_path.items()
        }
        cube.mk_polygons(id_to_transformed_model_path)


class CubeExplosionAnimorph(CubeAnimorph):
    """
    This animorph explodes the cube by an expansion factor.

    Attributes:
        expansion_factor: the expansion factor.
    """
    expansion_factor: float

    def __init__(self, cube: ThreeDPuzzleCube, expansion_factor: float) -> None:
        super().__init__(cube)
        self.expansion_factor = expansion_factor

    def morph_face_to(self, name: FaceName, alpha: float = 0.0) -> np.ndarray:
        """
        Makes the NumPy array of face vertices corresponding to the animation parameter alpha.

        The faces rotate to become perpendicular to the z-axis.
        Front/Back faces are already perpendicular to the z-axis so no rotation.
        Right/Left faces rotate about the y-axis by plus/minus 90 degrees.
        Top/Bottom faces rotate about the x-axis by plus/minus 90 degrees.

        The faces move outward in the direction of their normals.

        Args:
            name: the face name
            alpha: the animation parameter

        Returns:
            the NumPy array of face vertices
        """

        origin: Vertex = np.zeros(3, dtype=np.float64)
        unit_i: Vector = np.array([1, 0, 0], dtype=np.float64)
        unit_j: Vector = np.array([0, 1, 0], dtype=np.float64)
        unit_k: Vector = np.array([0, 0, 1], dtype=np.float64)
        quarter_turn: float = np.pi / 2.0

        # compute the point p, unit vector u, and angle theta that define a rotation about a line
        p: Vertex = origin
        u: Vector = unit_k
        theta_max: float = 0.0
        z_max: float = -(3.0 + self.expansion_factor) / 2.0
        face_normal: Vector = FACE_NAME_TO_UNIT_NORMAL[name]
        translation_max: Vector = z_max * unit_k + (self.expansion_factor - 1.0) * face_normal

        match name:
            case FaceName.RIGHT:
                p = RBF
                u = unit_j
                theta_max = -quarter_turn
            case FaceName.LEFT:
                p = LBF
                u = unit_j
                theta_max = quarter_turn
            case FaceName.TOP:
                p = LTF
                u = unit_i
                theta_max = quarter_turn
            case FaceName.BOTTOM:
                p = LBF
                u = unit_i
                theta_max = -quarter_turn
            case FaceName.FRONT:
                translation_max = origin
            case FaceName.BACK:
                translation_max = -(self.expansion_factor - 1.0) * unit_k

        theta: float = alpha * theta_max
        rot_mat: np.ndarray = rotation_matrix_about_line(p, u, theta)
        model_vertex_path: VertexPath = FACE_NAME_TO_VERTEX_PATH[name]
        rotated_vertex_path: VertexPath = apply_linear_transform(rot_mat, model_vertex_path)

        translation: Vector = alpha * translation_max
        transformed_vertex_path: np.ndarray = rotated_vertex_path + translation

        return transformed_vertex_path

    def morph_to(self, alpha: float) -> None:
        super().morph_to(alpha)
        cube: ThreeDPuzzleCube = self.get_cube()

        id_to_transformed_model_path: PolygonIdToVertexPathMapping = {
            ThreeDPuzzleCube.name_to_id(name): self.morph_face_to(name, alpha)
            for name in FaceName
        }
        cube.mk_polygons(id_to_transformed_model_path)
