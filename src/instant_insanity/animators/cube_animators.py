from abc import ABC

import numpy as np
from manim import Mobject
from manim.typing import Vector3D

from instant_insanity.animators.animorph import Animorph
from instant_insanity.core.cube import FacePlane, FACE_PLANE_TO_UNIT_NORMAL, RBF, LBF, LTF, FACE_PLANE_TO_VERTEX_PATH
from instant_insanity.core.geometry_types import PolygonKeyToVertexPathMapping, VertexPath, Vertex, Vector
from instant_insanity.core.puzzle import FaceLabel, INITIAL_FACE_LABEL_TO_PLANE
from instant_insanity.core.transformation import transform_vertex_path, rotation_matrix_about_line, \
    apply_linear_transform

from instant_insanity.mobjects.puzzle_cube_3d import PuzzleCube3D


class CubeAnimorph(Animorph, ABC):
    """
    This is the abstract base class for `ThreeDPuzzleCube` animorphs.
    """

    def __init__(self, cube: PuzzleCube3D):
        assert isinstance(cube, PuzzleCube3D)
        super().__init__(cube)

    def get_cube3d(self) -> PuzzleCube3D:
        mobject: Mobject = self.mobject
        assert isinstance(mobject, PuzzleCube3D)
        cube3d: PuzzleCube3D = mobject
        return cube3d



class CubeRigidMotionAnimorph(CubeAnimorph):
    """
    The class animates a rigid motion of a cube.
    The rigid motion is defined by a rotation followed by a translation.

    Attributes:
        rotation: the rotation vector.
        translation: the translation vector.
    """

    rotation: Vector3D
    translation: Vector3D

    def __init__(self,
                 cube: PuzzleCube3D,
                 rotation: Vector3D,
                 translation: Vector3D,
                 ) -> None:
        super().__init__(cube)
        self.rotation = rotation
        self.translation = translation

    def morph_to(self, alpha: float) -> None:
        super().morph_to(alpha)
        cube: PuzzleCube3D = self.get_cube3d()

        alpha_rotation: np.ndarray = alpha * self.rotation
        alpha_translation: np.ndarray = alpha * self.translation
        key_to_model_path_0: PolygonKeyToVertexPathMapping[FaceLabel] = cube.key_to_model_path_0
        face_label: FaceLabel
        model_path_0: VertexPath
        key_to_model_path: PolygonKeyToVertexPathMapping[FaceLabel] = {
            face_label: transform_vertex_path(alpha_rotation, alpha_translation, model_path_0)
            for face_label, model_path_0 in key_to_model_path_0.items()
        }
        cube.set_key_to_model_path(key_to_model_path)


class CubeExplosionAnimorph(CubeAnimorph):
    """
    This animorph explodes the cube by an expansion factor.

    Attributes:
        expansion_factor: the expansion factor.
    """
    expansion_factor: float

    def __init__(self, cube: PuzzleCube3D, expansion_factor: float) -> None:
        super().__init__(cube)
        self.expansion_factor = expansion_factor

    def morph_to(self, alpha: float) -> None:
        super().morph_to(alpha)
        cube3d: PuzzleCube3D = self.get_cube3d()

        key_to_model_path: PolygonKeyToVertexPathMapping[FaceLabel] = {}
        face_label: FaceLabel
        for face_label in FaceLabel:
            face_plane: FacePlane = INITIAL_FACE_LABEL_TO_PLANE[face_label]
            standard_model_path: VertexPath = CubeExplosionAnimorph.morph_standard_face_to(face_plane,
                                                                                  self.expansion_factor,
                                                                                  alpha)
            model_path_0: VertexPath = cube3d.key_to_model_path_0[face_label]
            translation: Vector3D = model_path_0[0] - FACE_PLANE_TO_VERTEX_PATH[face_plane][0]
            key_to_model_path[face_label] = standard_model_path + translation

        cube3d.set_key_to_model_path(key_to_model_path)

    @staticmethod
    def morph_standard_face_to(name: FacePlane,
                               expansion_factor: float,
                               alpha: float) -> np.ndarray:
        """
        Makes the NumPy array of face vertices corresponding to the animation parameter alpha
        applied to the standard cube, namely the unrotated cube centered at the origin.

        The faces rotate to become perpendicular to the z-axis.
        Front/Back faces are already perpendicular to the z-axis so no rotation.
        Right/Left faces rotate about the y-axis by plus/minus 90 degrees.
        Top/Bottom faces rotate about the x-axis by plus/minus 90 degrees.

        The faces move outward in the direction of their normals.

        Args:
            name: the face name.
            expansion_factor: the expansion factor.
            alpha: the animation parameter

        Returns:
            the model path corresponding to alpha.
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
        z_max: float = -(3.0 + expansion_factor) / 2.0
        face_normal: Vector = FACE_PLANE_TO_UNIT_NORMAL[name]
        translation_max: Vector = z_max * unit_k + (expansion_factor - 1.0) * face_normal

        match name:
            case FacePlane.RIGHT:
                p = RBF
                u = unit_j
                theta_max = -quarter_turn
            case FacePlane.LEFT:
                p = LBF
                u = unit_j
                theta_max = quarter_turn
            case FacePlane.TOP:
                p = LTF
                u = unit_i
                theta_max = quarter_turn
            case FacePlane.BOTTOM:
                p = LBF
                u = unit_i
                theta_max = -quarter_turn
            case FacePlane.FRONT:
                translation_max = origin
            case FacePlane.BACK:
                translation_max = -(expansion_factor - 1.0) * unit_k

        theta: float = alpha * theta_max
        rot_mat: np.ndarray = rotation_matrix_about_line(p, u, theta)
        standard_model_path_0: VertexPath = FACE_PLANE_TO_VERTEX_PATH[name]
        rotated_model_path: VertexPath = apply_linear_transform(rot_mat, standard_model_path_0)

        translation: Vector = alpha * translation_max
        model_path: np.ndarray = rotated_model_path + translation

        return model_path
