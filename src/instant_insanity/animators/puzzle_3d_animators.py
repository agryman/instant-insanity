from manim import Mobject
from manim.typing import Vector3D, Point3D
from numpy.random import standard_t

from instant_insanity.animators.animorph import Animorph
from instant_insanity.animators.cube_animators import CubeExplosionAnimorph
from instant_insanity.core.cube import FacePlane, FACE_PLANE_TO_VERTEX_PATH
from instant_insanity.core.geometry_types import PolygonKeyToVertexPathMapping, Point3D_Array
from instant_insanity.core.puzzle import PuzzleCubeNumber, FaceLabel, INITIAL_FACE_LABEL_TO_PLANE
from instant_insanity.core.transformation import transform_vertex_path
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
    """
    rotation: Vector3D

    def __init__(self, puzzle3d: Puzzle3D, rotation: Vector3D) -> None:
        super().__init__(puzzle3d)
        self.rotation = rotation

    def morph_to(self, alpha: float) -> None:
        super().morph_to(alpha)
        puzzle3d: Puzzle3D = self.get_puzzle3d()
        rotation_alpha: Vector3D = self.rotation * alpha
        puzzle_centre: Point3D = puzzle3d.puzzle_centre
        cube_delta: Vector3D = puzzle3d.cube_delta

        # create a new vertex path dict by copying the unrotated vertex paths
        key_to_model_path: PolygonKeyToVertexPathMapping[Puzzle3DPolygonName] = puzzle3d.key_to_model_path_0.copy()

        # rotate each cube about its centre by rotation_alpha
        # each cube has a different centre so we need to rotate them individually
        cube_number: PuzzleCubeNumber
        for cube_number in PuzzleCubeNumber:
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
