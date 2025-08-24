"""
This module implements the Puzzle3D class which is a Polygon3D that consists
of all 24 faces of the 4 puzzle cubes.
"""
from manim.typing import Point3D, Vector3D
from manim import LEFT, RIGHT, ManimColor

from instant_insanity.core.geometry_types import PolygonIdToVertexPathMapping, PolygonId, VertexPath
from instant_insanity.core.cube import FaceName, FACE_NAME_TO_VERTEX_PATH
from instant_insanity.core.projection import Projection
from instant_insanity.core.puzzle import Puzzle, PuzzleSpec, PuzzleCubeNumber, PuzzleCube, FaceColour
from instant_insanity.mobjects.polygons_3d import Polygons3D, DEFAULT_POLYGON_SETTINGS
from instant_insanity.mobjects.puzzle_cube_3d import PuzzleCube3D
from instant_insanity.scenes.coloured_cube import MANIM_COLOUR_MAP

type CubeNumberToCubeMapping = dict[PuzzleCubeNumber, PuzzleCube3D]

# A polygon in this group is uniquely identified by the pair (cube_number, face_name).
type Puzzle3DPolygonName = tuple[PuzzleCubeNumber, FaceName]

class Puzzle3D(Polygons3D):
    """
    This class implements a 3D puzzle.
    The puzzle consists of four 3D puzzle cubes.
    The puzzle contains the flattened list of all the faces of the cubes.
    Since each cube has six faces, there are a total of 24 polygons in the puzzle.
    A face from one cube may obscure a face from another cube so the set of all faces
    must be depth-sorted as a whole.

    Attributes:
        puzzle_spec: the puzzle specification which gives the colours of all faces.
        puzzle: the Puzzle object defined by the puzzle specification.
    """
    puzzle_spec: PuzzleSpec
    puzzle: Puzzle

    def __init__(self, projection: Projection, puzzle_spec: PuzzleSpec) -> None:
        self.puzzle_spec = puzzle_spec
        self.puzzle = Puzzle(puzzle_spec)
        id_to_model_path_0: PolygonIdToVertexPathMapping = Puzzle3D.mk_id_to_model_path_0()

        super().__init__(projection, id_to_model_path_0)

    @staticmethod
    def name_to_id(name: Puzzle3DPolygonName) -> PolygonId:
        """
        Converts a puzzle polygon name to its polygon id.

        Args:
            name: a polygon name, e.g. (PuzzleCubeNumber.TWO, FaceName.RIGHT).

        Returns:
            the polygon id, e.g. PolygonID('2/right').
        """
        cube_number: PuzzleCubeNumber
        face_name: FaceName
        cube_number, face_name = name

        id_str: str = f'{cube_number.value}/{face_name.value}'

        return PolygonId(id_str)

    @staticmethod
    def id_to_name(polygon_id: PolygonId) -> Puzzle3DPolygonName:
        """
        Converts a polygon id to its polygon name.
        Args:
            polygon_id: a polygon id, e.g. PolygonId('2/right').

        Returns:
            its polygon name, e.g. (PuzzleCubeNumber.TWO, FaceName.RIGHT).
        """
        id_str: str = str(polygon_id)

        cube_number_str: str
        face_name_value: str
        cube_number_str, face_name_value = id_str.split('/')

        cube_number_value: int = int(cube_number_str)
        cube_number = PuzzleCubeNumber(cube_number_value)

        face_name: FaceName = FaceName(face_name_value)

        return cube_number, face_name

    @staticmethod
    def mk_id_to_model_path_0() -> PolygonIdToVertexPathMapping:
        """
        Makes the initial model space vertex paths.
        Returns:
            the initial model space vertex paths.
        """
        # arrange the cubes horizontally from left to right with centres laying on the x-axis
        cube_side_length: float = 2.0 # the side length of the standard cube
        buff: float = 0.1 # the horizontal space between cubes, MUST be positive to avoid collisions
        cube_1_origin: Point3D = 1.5 * cube_side_length * LEFT
        delta_origin: Vector3D = (cube_side_length + buff) * RIGHT

        id_to_model_path_0: PolygonIdToVertexPathMapping = dict()
        i: int
        cube_number: PuzzleCubeNumber
        for i, cube_number in enumerate(PuzzleCubeNumber):
            cube_origin_i: Point3D = cube_1_origin + delta_origin * i
            face_name: FaceName
            vertex_path: VertexPath
            for face_name, vertex_path in FACE_NAME_TO_VERTEX_PATH.items():
                polygon_id = Puzzle3D.name_to_id((cube_number, face_name))
                id_to_model_path_0[polygon_id] = vertex_path + cube_origin_i

        return id_to_model_path_0

    def get_polygon_settings(self, polygon_id: PolygonId) -> dict:
        """
        Gets a dict of settings the polygon.

        Args:
            polygon_id: a polygon id.

        Returns:
            a dict of settings the polygon.
        """
        cube_number: PuzzleCubeNumber
        face_name: FaceName
        cube_number, face_name = Puzzle3D.id_to_name(polygon_id)
        puzzle_cube: PuzzleCube = self.puzzle.number_to_cube[cube_number]
        colour_name: FaceColour = puzzle_cube.name_to_colour[face_name]
        colour: ManimColor = MANIM_COLOUR_MAP[colour_name]
        polygon_settings: dict = DEFAULT_POLYGON_SETTINGS.copy()
        polygon_settings['fill_color'] = colour

        return polygon_settings
