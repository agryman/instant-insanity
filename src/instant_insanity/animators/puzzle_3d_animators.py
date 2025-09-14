from manim import Mobject
from manim.typing import Vector3D
from numpy.random import standard_t

from instant_insanity.animators.animorph import Animorph
from instant_insanity.animators.cube_animators import CubeExplosionAnimorph
from instant_insanity.core.cube import FacePlane, FACE_PLANE_TO_VERTEX_PATH
from instant_insanity.core.geometry_types import PolygonKeyToVertexPathMapping, VertexPath
from instant_insanity.core.puzzle import PuzzleCubeNumber, FaceLabel, INITIAL_FACE_LABEL_TO_PLANE
from instant_insanity.mobjects.puzzle_3d import Puzzle3D, Puzzle3DPolygonName


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
            standard_model_path: VertexPath = CubeExplosionAnimorph.morph_standard_face_to(face_plane,
                                                                                  self.expansion_factor,
                                                                                  alpha)
            model_path_0: VertexPath = puzzle3d.key_to_model_path_0[polygon_name]
            translation: Vector3D = model_path_0[0] - FACE_PLANE_TO_VERTEX_PATH[face_plane][0]
            key_to_model_path[polygon_name] = standard_model_path + translation

        puzzle3d.set_key_to_model_path(key_to_model_path)
