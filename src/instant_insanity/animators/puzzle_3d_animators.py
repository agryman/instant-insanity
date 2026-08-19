from types import MappingProxyType
from typing import Mapping, cast

from manim import Mobject, RIGHT
from manim.typing import Vector3D, Point3D

from instant_insanity.animators.animorph import Animorph
from instant_insanity.animators.cube_animators import CubeExplosionAnimorph
from instant_insanity.core.cube import FacePlane, FACE_PLANE_TO_VERTEX_PATH
from instant_insanity.core.geometry_types import PolygonKeyToVertexPathMapping, Point3D_Array
from instant_insanity.core.puzzle import PuzzleCubeNumber, FaceLabel, INITIAL_FACE_LABEL_TO_PLANE
from instant_insanity.core.transformation import transform_vertex_path
from instant_insanity.mobjects.puzzle_3d import Puzzle3D, Puzzle3DPolygonName

DEFAULT_MASK: Mapping[PuzzleCubeNumber, bool] = MappingProxyType(
    {cube_number: True for cube_number in PuzzleCubeNumber}
)


class Puzzle3DAnimorph(Animorph):
    """
    This is the abstract base class for Puzzle3D animorphs.
    """

    def __init__(self, puzzle3d: Puzzle3D) -> None:
        if not isinstance(puzzle3d, Puzzle3D):
            raise TypeError(f'Expected a Puzzle3D but got {type(puzzle3d)}')
        super().__init__(puzzle3d)

    def get_puzzle3d(self) -> Puzzle3D:
        mobject: Mobject = self.mobject
        assert isinstance(mobject, Puzzle3D)
        puzzle3d: Puzzle3D = mobject
        return puzzle3d

class Puzzle3DCubeExplosionAnimorph(Puzzle3DAnimorph):
    """
    This class animates the explosion of a cube within a Puzzle3D.

    Attributes:
        cube_number: the cube number.
        expansion_factor: the expansion factor.
    """
    cube_number: PuzzleCubeNumber
    expansion_factor: float

    def __init__(self, puzzle3d: Puzzle3D, expansion_factor: float, cube_number: PuzzleCubeNumber) -> None:
        super().__init__(puzzle3d)
        self.cube_number: PuzzleCubeNumber = cube_number
        self.expansion_factor: float = expansion_factor

    def morph_to(self, alpha: float) -> None:
        super().morph_to(alpha)
        puzzle3d: Puzzle3D = self.get_puzzle3d()
        cube_number: PuzzleCubeNumber = self.cube_number

        # copy the current model paths and then update the faces
        key_to_model_path: PolygonKeyToVertexPathMapping[Puzzle3DPolygonName] = puzzle3d.key_to_model_path.copy()
        face_label: FaceLabel
        for face_label in FaceLabel:
            polygon_name: Puzzle3DPolygonName = (cube_number, face_label)
            face_plane: FacePlane = INITIAL_FACE_LABEL_TO_PLANE[face_label]
            standard_model_path: Point3D_Array = CubeExplosionAnimorph.morph_standard_face_to(face_plane,
                                                                                              self.expansion_factor,
                                                                                              alpha)
            model_path_0: Point3D_Array = puzzle3d.key_to_model_path_0[polygon_name]
            translation: Vector3D = model_path_0[0] - FACE_PLANE_TO_VERTEX_PATH[face_plane][0]
            key_to_model_path[polygon_name] = standard_model_path + translation

        puzzle3d.set_key_to_model_path(key_to_model_path)


class Puzzle3DCubeRotationAnimorph(Puzzle3DAnimorph):
    """
    This class animates the rotation of each cube about its centre.

    Attributes:
        rotation: the rotation vector
        mask: dict of cube number to flag (True to rotate)
    """
    rotation: Vector3D
    mask: Mapping[PuzzleCubeNumber, bool]

    def __init__(self, puzzle3d: Puzzle3D,
                 rotation: Vector3D,
                 mask: Mapping[PuzzleCubeNumber, bool] = DEFAULT_MASK) -> None:
        super().__init__(puzzle3d)
        self.rotation = rotation
        self.mask = mask

    def morph_to(self, alpha: float) -> None:
        super().morph_to(alpha)
        puzzle3d: Puzzle3D = self.get_puzzle3d()
        rotation_alpha: Vector3D = self.rotation * alpha
        puzzle_centre: Point3D = puzzle3d.puzzle_centre
        cube_delta: Vector3D = puzzle3d.cube_delta

        # create a new vertex path dict by copying the unrotated vertex paths
        key_to_model_path: PolygonKeyToVertexPathMapping[Puzzle3DPolygonName] = puzzle3d.key_to_model_path_0.copy()

        # rotate each masked cube about its centre by rotation_alpha
        # each cube has a different centre so we need to rotate them individually
        cube_number: PuzzleCubeNumber
        for cube_number in PuzzleCubeNumber:
            if not self.mask[cube_number]:
                continue
            cube_centre: Point3D = puzzle3d.mk_cube_centre(cube_number, puzzle_centre, cube_delta)
            # rotate each face of the cube
            face_label: FaceLabel
            for face_label in FaceLabel:
                # get the initial vertex paths for the face
                polygon_name: Puzzle3DPolygonName = (cube_number, face_label)
                model_path: Point3D_Array = key_to_model_path[polygon_name]
                # translate the vertex paths back to the origin
                model_path = model_path - cube_centre
                # rotate the vertex paths and then translate back to cube centre
                model_path = transform_vertex_path(rotation_alpha, cube_centre, model_path)
                # save the rotated face
                key_to_model_path[polygon_name] = model_path

        # set the new vertex paths
        # this triggers an update to the polygon depth-sort order
        puzzle3d.set_key_to_model_path(key_to_model_path)


class Puzzle3DSetCubeGapAnimorph(Puzzle3DAnimorph):
    """
    This class animates the setting of the gap between regularly spaced cubes
    arranged in a row along the left-right axis. The centre of the puzzle
    remains fixed. Only the distance between the cubes changed.

    Let w be the width of each cube. The width is constant during the animation.
    Let g be a gap between cubes. The gap changes during the animation.
    Let the cubes be numbered from left to right as 1, 2, 3, 4.
    Let T1, T2, T3, T4 be the translation vectors for the cube centres relative to the centre of the row.
    Regard then as functions of g.
    T1(g) = -1.5 * (g + w) * RIGHT
    T2(g) = -0.5 * (g + w) * RIGHT
    T3(g) = 0.5 * (g + w) * RIGHT
    T4(g) = 1.5 * (g + w) * RIGHT

    Let n = 1, ..., 4 be a cube number.
    Define beta(n) to be the scaling coefficient for cube n.
    beta(1) = -1.5
    beta(2) = -0.5
    beta(3) = 0.5
    beta(4) = 1.5

    Let T(n, g) be the translation vector for cube n with gap g.
    T(n,g) = beta(n) * (g + w) * RIGHT

    Let g0 be the initial gap between cubes.
    Let g1 be the target gap between cubes.
    Let dg = g1 - g0 be the change in the gaps.

    Note that if g1 = g0 then dg = 0 so there should be no movement of the cubes.

    Smoothly interpolate from g0 to g1.
    Let g(alpha) be the gap between cubes at stage alpha of the animation.
    g(alpha) = (1-alpha) * g0 + alpha * g1

    This gives
    g(0) = g0
    g(1) = g1

    In terms of dg, we have
    g(alpha) = g0 + alpha * dg

    We need to compute how much to translate each cube from its initial position for each alpha.
    dT1(alpha) = T1(g(alpha)) - T1(g0)

    At stage alpha in the animation, each cube is translated from its initial position
    by the vectors dT1, dT2, dT3, dT4 given by the following expressions.
    dT1(alpha) = -1.5 * alpha * dg * RIGHT
    dT2(alpha) = -0.5 * alpha * dg * RIGHT
    dT3(alpha) = 0.5 * alpha * dg * RIGHT
    dT4(alpha) = 1.5 * alpha * dg * RIGHT

    dT(n, alpha) = beta(n) * alpha * dg * RIGHT

    We have
    T(n, g(alpha)) = T(n, g0) + dT(n, alpha)

    Attributes:
        target_gap: the target gap between cubes
    """
    target_gap: float

    def __init__(self, puzzle3d: Puzzle3D, target_gap: float) -> None:
        super().__init__(puzzle3d)
        self.target_gap = target_gap

    def morph_to(self, alpha: float) -> None:
        super().morph_to(alpha)
        puzzle3d: Puzzle3D = self.get_puzzle3d()

        initial_gap: float = puzzle3d.get_cube_gap()
        delta_gap: float = self.target_gap - initial_gap

        # create a new vertex path dict by copying the initial vertex paths
        key_to_model_path: PolygonKeyToVertexPathMapping[Puzzle3DPolygonName] = puzzle3d.key_to_model_path_0.copy()

        # translate each cube by delta_T(alpha)
        # each cube has a different translation vector so we need to translate them individually
        beta: list[float] = [-1.5, -0.5, 0.5, 1.5]
        beta_n: float
        cube_number: PuzzleCubeNumber
        for cube_number, beta_n in zip(PuzzleCubeNumber, beta):
            delta_t_n_alpha: Vector3D = beta_n * alpha * delta_gap * RIGHT
            # translate each face of the cube
            face_label: FaceLabel
            for face_label in FaceLabel:
                polygon_name: Puzzle3DPolygonName = (cube_number, face_label)
                model_path_0: Point3D_Array = key_to_model_path[polygon_name]
                model_path_alpha: Point3D_Array = model_path_0 + delta_t_n_alpha
                key_to_model_path[polygon_name] = model_path_alpha

        # set the new vertex paths
        # this triggers an update to the polygon depth-sort order
        puzzle3d.set_key_to_model_path(key_to_model_path)

class Puzzle3DTranslationAnimorph(Puzzle3DAnimorph):
    """
    This class animates the translation of a puzzle by a vector.
    """
    translation: Vector3D
    puzzle_centre_0: Point3D

    def __init__(self, puzzle3d: Puzzle3D, translation: Vector3D) -> None:
        super().__init__(puzzle3d)
        self.translation = translation
        self.puzzle_centre_0 = puzzle3d.puzzle_centre.copy()

    def morph_to(self, alpha: float) -> None:
        super().morph_to(alpha)
        puzzle3d: Puzzle3D = self.get_puzzle3d()

        # create a new vertex path dict by copying the initial vertex paths
        key_to_model_path: PolygonKeyToVertexPathMapping[Puzzle3DPolygonName] = puzzle3d.key_to_model_path_0.copy()

        alpha_translation: Vector3D = alpha * self.translation

        # translate the puzzle centre by alpha * translation
        puzzle3d.puzzle_centre = self.puzzle_centre_0 + alpha_translation

        # translate each cube by alpha * translation
        cube_number: PuzzleCubeNumber
        for cube_number in PuzzleCubeNumber:
            # translate each face of the cube
            face_label: FaceLabel
            for face_label in FaceLabel:
                polygon_name: Puzzle3DPolygonName = (cube_number, face_label)
                model_path_0: Point3D_Array = key_to_model_path[polygon_name]
                model_path_alpha: Point3D_Array = model_path_0 + alpha_translation
                key_to_model_path[polygon_name] = model_path_alpha

        # set the new vertex paths
        # this triggers an update to the polygon depth-sort order
        puzzle3d.set_key_to_model_path(key_to_model_path)
