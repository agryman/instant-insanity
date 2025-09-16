from manim import ManimColor, ORIGIN
from manim.typing import Point3D

from instant_insanity.core.cube import FacePlane, FACE_PLANE_TO_VERTEX_PATH
from instant_insanity.core.geometry_types import PolygonKeyToVertexPathMapping, Point3D_Array
from instant_insanity.core.projection import Projection
from instant_insanity.core.puzzle import PuzzleCubeSpec, PuzzleCube, FaceColour, FaceLabel, INITIAL_FACE_LABEL_TO_PLANE
from instant_insanity.mobjects.coloured_cube import MANIM_COLOUR_MAP
from instant_insanity.mobjects.polygons_3d import Polygons3D, DEFAULT_POLYGON_SETTINGS


class PuzzleCube3D(Polygons3D[FaceLabel]):
    """
    This class draws a puzzle cube in 3D space.

    Attributes:
        cube_spec: the puzzle cube specification which gives the colours of all faces.
        puzzle_cube: the PuzzleCube object which provides the colours of all faces.
        cube_centre: the center of the cube in model space?
    """
    cube_spec: PuzzleCubeSpec
    puzzle_cube: PuzzleCube
    cube_centre: Point3D

    def __init__(self,
                 projection: Projection,
                 cube_spec: PuzzleCubeSpec,
                 cube_centre: Point3D = ORIGIN) -> None:
        """
        Args:
            projection: the projection.
            cube_spec: the puzzle cube specification.
            cube_centre: the centre of the cube in model space.
        """
        self.cube_spec = cube_spec
        self.puzzle_cube = PuzzleCube(cube_spec)
        self.cube_centre = cube_centre
        key_to_model_path_0: PolygonKeyToVertexPathMapping[FaceLabel] = PuzzleCube3D.mk_face_to_model_path_0(cube_centre)

        super().__init__(projection, key_to_model_path_0)


    @staticmethod
    def mk_face_to_model_path_0(cube_centre: Point3D = ORIGIN) -> PolygonKeyToVertexPathMapping[FaceLabel]:
        """
        Makes the initial model space vertex paths.

        Args:
            cube_centre: the center of the cube in model space.

        Returns:
            the initial model space vertex paths.
        """
        face_to_model_path_0: PolygonKeyToVertexPathMapping[FaceLabel] = {}
        face_label: FaceLabel
        for face_label in FaceLabel:
            face_plane: FacePlane = INITIAL_FACE_LABEL_TO_PLANE[face_label]
            vertex_path: Point3D_Array = FACE_PLANE_TO_VERTEX_PATH[face_plane]
            face_to_model_path_0[face_label] = vertex_path + cube_centre
        return face_to_model_path_0

    def get_colour_name(self, face_name: FaceLabel) -> FaceColour:
        """
        Returns the colour name for the given face colour.
        Args:
            face_name: the face name.

        Returns:
            the colour name for the given face name.
        """
        colour_name: FaceColour = self.puzzle_cube.face_label_to_colour[face_name]
        return colour_name

    def get_manim_colour(self, face_name: FaceLabel) -> ManimColor:
        """
        Returns the colour of the given face.
        Args:
            face_name: The name of the face.

        Returns:
            The Manim colour of the given face.
        """
        colour_name: FaceColour = self.get_colour_name(face_name)
        colour: ManimColor = MANIM_COLOUR_MAP[colour_name]
        return colour

    def get_polygon_settings(self, face_label: FaceLabel) -> dict:
        polygon_settings: dict = DEFAULT_POLYGON_SETTINGS.copy()
        colour: ManimColor = self.get_manim_colour(face_label)
        polygon_settings['fill_color'] = colour
        return polygon_settings

