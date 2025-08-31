"""
This module implements the Puzzle3D class which is a Polygon3D that consists
of all 24 faces of the 4 puzzle cubes.
"""
from manim.typing import Point3D, Vector3D
from manim import LEFT, RIGHT, ManimColor

from instant_insanity.core.geometry_types import PolygonIdToVertexPathMapping, PolygonId, VertexPath
from instant_insanity.core.cube import FacePlane, FACE_PLANE_TO_VERTEX_PATH
from instant_insanity.core.projection import Projection
from instant_insanity.core.puzzle import Puzzle, PuzzleSpec, PuzzleCubeNumber, PuzzleCube, FaceColour
from instant_insanity.mobjects.polygons_3d import Polygons3D, DEFAULT_POLYGON_SETTINGS
from instant_insanity.mobjects.puzzle_cube_3d import PuzzleCube3D
from instant_insanity.scenes.coloured_cube import MANIM_COLOUR_MAP

type CubeNumberToCubeMapping = dict[PuzzleCubeNumber, PuzzleCube3D]

# A polygon in this group is uniquely identified by the pair (cube_number, face_name).
type Puzzle3DPolygonName = tuple[PuzzleCubeNumber, FacePlane]

DEFAULT_CUBE_SIDE_LENGTH: float = 2.0  # the side length of the standard cube
DEFAULT_BUFF: float = 0.1  # the horizontal space between cubes, MUST be positive to avoid collisions
DEFAULT_CUBE_ONE_CENTRE: Point3D = 1.5 * DEFAULT_CUBE_SIDE_LENGTH * LEFT
DEFAULT_CUBE_CENTRE_DELTA: Vector3D = (DEFAULT_CUBE_SIDE_LENGTH + DEFAULT_BUFF) * RIGHT


class Puzzle3D(Polygons3D):
    """
    This class implements a 3D puzzle.
    The puzzle consists of four 3D puzzle cubes.
    The puzzle contains the flattened list of all the faces of the cubes.
    Since each cube has six faces, there are a total of 24 polygons in the puzzle.
    A face from one cube may obscure a face from another cube so the set of all faces
    must be depth-sorted as a whole.

    Attributes:
        puzzle: the Puzzle object.
        cube_one_centre: the centre of cube one.
        cube_centre_delta: the change in centres between cubes.
    """
    puzzle: Puzzle
    cube_one_centre: Point3D
    cube_one_centre_delta: Vector3D

    def __init__(self, projection: Projection,
                 puzzle: Puzzle,
                 cube_one_centre: Point3D = DEFAULT_CUBE_ONE_CENTRE,
                 cube_centre_delta: Vector3D = DEFAULT_CUBE_CENTRE_DELTA) -> None:
        self.puzzle = puzzle
        self.cube_one_centre = cube_one_centre
        self.cube_centre_delta = cube_centre_delta
        id_to_model_path_0: PolygonIdToVertexPathMapping = Puzzle3D.mk_id_to_model_path_0(cube_one_centre,
                                                                                          cube_centre_delta)

        super().__init__(projection, id_to_model_path_0)

    @staticmethod
    def name_to_id(name: Puzzle3DPolygonName) -> PolygonId:
        """
        Converts a puzzle polygon name to its polygon id.

        Args:
            name: a polygon name, e.g. (PuzzleCubeNumber.TWO, FacePlane.RIGHT).

        Returns:
            the polygon id, e.g. PolygonID('2/right').
        """
        cube_number: PuzzleCubeNumber
        face_plane: FacePlane
        cube_number, face_plane = name

        id_str: str = f'{cube_number.value}/{face_plane.value}'

        return PolygonId(id_str)

    @staticmethod
    def id_to_name(polygon_id: PolygonId) -> Puzzle3DPolygonName:
        """
        Converts a polygon id to its polygon name.
        Args:
            polygon_id: a polygon id, e.g. PolygonId('2/right').

        Returns:
            its polygon name, e.g. (PuzzleCubeNumber.TWO, FacePlane.RIGHT).
        """
        id_str: str = str(polygon_id)

        cube_number_str: str
        face_plane_value: str
        cube_number_str, face_plane_value = id_str.split('/')

        cube_number_value: int = int(cube_number_str)
        cube_number = PuzzleCubeNumber(cube_number_value)

        face_plane: FacePlane = FacePlane(face_plane_value)

        return cube_number, face_plane

    @staticmethod
    def mk_id_to_model_path_0(cube_one_centre: Point3D,
                              cube_centre_delta: Vector3D) -> PolygonIdToVertexPathMapping:
        """
        Makes the initial model space vertex paths.
        Returns:
            the initial model space vertex paths.
        """
        # arrange the cubes horizontally from left to right with centres laying on the x-axis

        id_to_model_path_0: PolygonIdToVertexPathMapping = dict()
        i: int
        cube_number: PuzzleCubeNumber
        for i, cube_number in enumerate(PuzzleCubeNumber):
            cube_origin_i: Point3D = cube_one_centre + cube_centre_delta * i
            face_name: FacePlane
            vertex_path: VertexPath
            for face_name, vertex_path in FACE_PLANE_TO_VERTEX_PATH.items():
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
        face_name: FacePlane
        cube_number, face_name = Puzzle3D.id_to_name(polygon_id)
        puzzle_cube: PuzzleCube = self.puzzle.number_to_cube[cube_number]
        colour_name: FaceColour = puzzle_cube.name_to_colour[face_name]
        colour: ManimColor = MANIM_COLOUR_MAP[colour_name]
        polygon_settings: dict = DEFAULT_POLYGON_SETTINGS.copy()
        polygon_settings['fill_color'] = colour

        return polygon_settings

    def get_colour_name(self, cube_number: PuzzleCubeNumber, face_name: FacePlane) -> FaceColour:
        puzzle: Puzzle = self.puzzle
        cube: PuzzleCube = puzzle.number_to_cube[cube_number]
        colour_name: FaceColour = cube.name_to_colour[face_name]
        return colour_name

    def hide_cube(self, cube_number: PuzzleCubeNumber) -> None:
        cube_ids: set[PolygonId] = {Puzzle3D.name_to_id((cube_number, face_name))
                                    for face_name in FacePlane}
        visible_polygon_ids: set[PolygonId] = self.visible_polygon_ids - cube_ids
        self.set_visible_polygon_ids(visible_polygon_ids)
