from typing import Any

from manim import ManimColor, WHITE, BLACK, Polygon, LineJointType

from instant_insanity.core.cube import FaceName, FACE_NAME_TO_VERTEX_PATH
from instant_insanity.core.geometry_types import PolygonIdToVertexPathMapping, PolygonId, VertexPath
from instant_insanity.core.projection import Projection
from instant_insanity.core.puzzle import PuzzleCubeSpec, PuzzleCube, FaceColour
from instant_insanity.scenes.coloured_cube import MANIM_COLOUR_MAP
from instant_insanity.mobjects.polygons_3d import Polygons3D, DEFAULT_POLYGON_SETTINGS


class PuzzleCube3D(Polygons3D):
    """
    This class draws a puzzle cube in 3D space.

    Attributes:
        cube_spec: the puzzle cube specification which gives the colours of all faces.
        puzzle_cube: the PuzzleCube object which provides the colours of all faces.
    """
    cube_spec: PuzzleCubeSpec
    puzzle_cube: PuzzleCube

    def __init__(self,
                 projection: Projection,
                 cube_spec: PuzzleCubeSpec,
                 **polygon_settings: Any) -> None:
        """
        Args:
            projection: the projection.
            cube_spec: the puzzle cube specification.
        """
        self.cube_spec = cube_spec
        self.puzzle_cube = PuzzleCube(cube_spec)
        id_to_model_path_0: PolygonIdToVertexPathMapping = PuzzleCube3D.mk_id_to_model_path_0()

        super().__init__(projection, id_to_model_path_0, **polygon_settings)

    @staticmethod
    def name_to_id(face_name: FaceName) -> PolygonId:
        """
        Converts a face name to a polygon id.
        Args:
            face_name: the face name.

        Returns:
            the polygon id.
        """
        face_name_str: str = str(face_name.value)
        return PolygonId(face_name_str)

    @staticmethod
    def id_to_name(polygon_id: PolygonId) -> FaceName:
        """
        Converts a polygon id to a face name.

        Args:
            polygon_id: the polygon id.

        Returns:
            the face name.
        """
        return FaceName(polygon_id)

    @staticmethod
    def mk_id_to_model_path_0() -> PolygonIdToVertexPathMapping:
        """
        Makes the initial model space vertex paths.
        Returns:
            the initial model space vertex paths.
        """
        face_name: FaceName
        vertex_path: VertexPath
        id_to_model_path_0: PolygonIdToVertexPathMapping = {
            PuzzleCube3D.name_to_id(face_name): vertex_path
            for face_name, vertex_path in FACE_NAME_TO_VERTEX_PATH.items()
        }
        return id_to_model_path_0

    def get_colour_name(self, face_name: FaceName) -> FaceColour:
        """
        Returns the colour name for the given face colour.
        Args:
            face_name: the face name.

        Returns:
            the colour name for the given face name.
        """
        colour_name: FaceColour = self.puzzle_cube.name_to_colour[face_name]
        return colour_name

    def get_manim_colour(self, face_name: FaceName) -> ManimColor:
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

    def get_polygon_settings(self, polygon_id: PolygonId) -> dict:
        polygon_settings: dict = DEFAULT_POLYGON_SETTINGS.copy()
        face_name: FaceName = self.id_to_name(polygon_id)
        colour: ManimColor = self.get_manim_colour(face_name)
        polygon_settings['fill_color'] = colour
        return polygon_settings

